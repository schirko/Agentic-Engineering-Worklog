"""The agent: the loop (lesson 3) and the conversation memory (lesson 4)."""

from datetime import date

import ollama

from . import config
from .tools import TOOLS, run_tool


def build_system_prompt(today=None):
    """The standing instructions, with today's date filled in.

    The date is worked out each time a conversation starts, so a program left running
    past midnight still knows what "today" means.
    """
    today = today or date.today()
    return (
        "You are a work log assistant. "
        f"Today is {today.isoformat()} ({today.strftime('%A')}). "
        "When the user describes work they did, call add_entry. "
        "When the user asks about past work, call search_entries and answer from its result. "
        "If a request needs both, save first and search after. "
        "If the user corrects something they just logged, call update_last_entry instead of add_entry. "
        "Known projects: " + ", ".join(config.KNOWN_PROJECTS) + ". "
        "Use one of those names when the work matches one. "
        "Only include hours if the user stated them. Convert minutes to hours. "
        "If the message is not about work, answer normally without calling a tool."
    )


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

    def __init__(self, max_turns=None, verbose=False):
        self.max_turns = config.MAX_TURNS if max_turns is None else max_turns
        self.verbose = verbose
        self.system_prompt = build_system_prompt()
        self.turns = []
        self.prompt_tokens = []  # tokens the model read on each turn's first call

    def recent_messages(self):
        """The messages from the last max_turns turns, as one flat list."""
        kept = self.turns[-self.max_turns:] if self.max_turns > 0 else []
        return [message for turn in kept for message in turn]

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
                result = run_tool(name, arguments)
                calls_made.append((name, arguments))
                if self.verbose:
                    print(f"  [step {step}] {name}({arguments}) -> {result.splitlines()[0]}")
                turn.append({"role": "tool", "tool_name": name, "content": result})

        turn.append({"role": "assistant", "content": reply})
        self.turns.append(turn)
        return reply, calls_made
