"""The agent: the loop (lesson 3) and the conversation memory (lesson 4)."""

from datetime import date

import ollama

from . import config
from .tools import TOOLS, run_tool


ASK_RULE = (
    "If it isn't clear which known project the work was for, from the message or the conversation so far, "
    "do not guess and do not call add_entry: ask the user which project it was, then wait for the answer. "
    "If the project is clear, don't ask. "
)


def build_system_prompt(today=None, ask_when_unclear=None):
    """The standing instructions, with today's date filled in.

    The date is worked out each time a conversation starts, so a program left running
    past midnight still knows what "today" means. The ask rule (lesson 6) is added
    when ask_when_unclear is on, which it is by default (config.ASK_WHEN_UNCLEAR).
    """
    today = today or date.today()
    if ask_when_unclear is None:
        ask_when_unclear = config.ASK_WHEN_UNCLEAR
    return (
        "You are a work log assistant. "
        f"Today is {today.isoformat()} ({today.strftime('%A')}). "
        "When the user describes work they did, call add_entry. "
        "When the user asks about past work, call search_entries and answer from its result. "
        "If a request needs both, save first and search after. "
        "If the user corrects something they just logged, call update_last_entry instead of add_entry. "
        "Known projects: " + ", ".join(config.KNOWN_PROJECTS) + ". "
        "Use one of those names when the work matches one. "
        + (ASK_RULE if ask_when_unclear else "")
        + "Only include hours if the user stated them. Convert minutes to hours. "
        "If the message is not about work, answer normally without calling a tool."
    )


NOT_NAMED = (
    "Not saved: the user hasn't said which project this work was for. "
    "Ask the user which project it was, then wait for the answer."
)


def project_was_named(project, user_texts):
    """True if the project's name appears in anything the user said (lesson 6).

    This is a check in code, not an instruction: the model can't talk its way past it.
    It only checks that the name was said, not that it was said about this work.
    """
    said = " ".join(user_texts).lower()
    return bool(project) and project.lower() in said


def call_model(messages):
    """One call to the local model, with every tool on offer."""
    return ollama.chat(
        model=config.MODEL,
        messages=messages,
        tools=TOOLS,
        think=False,
        options={"temperature": 0},
    )


class Conversation:
    """An agent that remembers recent turns.

    A turn is one user message and everything that followed it: tool requests, tool
    results and the reply. Only the last `max_turns` turns are sent again, so the
    agent doesn't slow down as the conversation grows.
    """

    def __init__(self, max_turns=None, verbose=False, ask_when_unclear=None, require_named_project=None):
        self.max_turns = config.MAX_TURNS if max_turns is None else max_turns
        self.require_named_project = (
            config.REQUIRE_NAMED_PROJECT if require_named_project is None else require_named_project
        )
        self.blocked_calls = 0  # saves refused by the named-project check
        self.verbose = verbose
        self.system_prompt = build_system_prompt(ask_when_unclear=ask_when_unclear)
        self.turns = []
        self.prompt_tokens = []  # tokens the model read on each turn's first call

    def recent_messages(self):
        """The messages from the last max_turns turns, as one flat list."""
        kept = self.turns[-self.max_turns:] if self.max_turns > 0 else []
        return [message for turn in kept for message in turn]

    def check_call(self, name, arguments, turn):
        """Checks in code before a tool runs. Returns a refusal message, or None to go ahead."""
        if self.require_named_project and name == "add_entry":
            said = [m["content"] for m in self.recent_messages() + turn
                    if isinstance(m, dict) and m.get("role") == "user"]
            if not project_was_named(arguments.get("project"), said):
                return NOT_NAMED
        return None

    def send(self, user_text):
        """Handle one message. Returns the reply and a list of (tool name, arguments) used."""
        turn = [{"role": "user", "content": user_text}]
        calls_made = []
        reply = f"Stopped after {config.MAX_STEPS} steps without a final answer."

        for step in range(1, config.MAX_STEPS + 1):
            messages = [{"role": "system", "content": self.system_prompt}] + self.recent_messages() + turn
            response = call_model(messages)
            if step == 1:
                self.prompt_tokens.append(response.prompt_eval_count)
            tool_calls = response.message.tool_calls or []

            if not tool_calls:
                reply = response.message.content
                break

            turn.append(response.message)
            for call in tool_calls:
                name, arguments = call.function.name, dict(call.function.arguments)
                refusal = self.check_call(name, arguments, turn)
                if refusal:
                    self.blocked_calls += 1
                result = refusal or run_tool(name, arguments)
                calls_made.append((name, arguments))
                if self.verbose:
                    print(f"  [step {step}] {name}({arguments}) -> {result.splitlines()[0]}")
                turn.append({"role": "tool", "tool_name": name, "content": result})

        turn.append({"role": "assistant", "content": reply})
        self.turns.append(turn)
        return reply, calls_made
