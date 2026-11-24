# The map of agentic engineering

Everything involved in agentic engineering, explained in plain words, with where this project covers each part and where it doesn't yet. The roadmap for covering the gaps is in `docs/ROADMAP.md`.

Researched November 22, 2026. The field moves fast: the "loops" stage only got its name in June 2026. Sources are at the end.

## What agentic engineering is

**Agentic engineering** is building software with AI agents doing much of the hands-on work, while a person stays in charge of what gets built and proves it's right. IBM defines it as "the practice of using engineering expertise to orchestrate and oversee AI agents through the software development process." It's the disciplined counterpart to *vibe coding* (prompting an AI and accepting whatever looks right).

### Where the term came from

- **February 2025:** Andrej Karpathy (an OpenAI cofounder and former head of AI at Tesla) coined **"vibe coding"**: prompting an AI, accepting what it writes without reading it closely, and pasting errors back in until it works. Good for throwaway prototypes.
- **January 2026:** Karpathy wrote that he'd gone from about 80% hand-written code to about 80% agent-written code in a couple of months, as coding agents improved.
- **February 4 and 5, 2026:** on vibe coding's first anniversary, Karpathy called it passé for professional work and named its successor **"agentic engineering"**: agents write most of the code, and the engineer directs and oversees them.
- **February 2026:** Addy Osmani (Google) wrote that the two aren't a binary but a **spectrum**, with "AI-assisted engineering" in the middle. What moves you along it is how much structure, verification and human judgment surrounds the AI's output. Simon Willison began *Agentic Engineering Patterns*, a living guide for professionals using coding agents, and IBM and Google Research published definitions.
- **June 2026:** the newest layer, **loop engineering**, got its name (see stage 5 below).

### The definitions side by side

| Source | Definition, in short |
|---|---|
| Karpathy (Feb 2026) | Agents write the code; the engineer orchestrates and oversees them |
| Simon Willison | Developing software with the help of coding agents. Running code is what makes it possible: without it, a model's output has limited value |
| IBM | Using engineering expertise to orchestrate and oversee AI agents through the software development process |
| Google Research | Treating models as semi-autonomous systems that carry out multi-step work (*trajectories*) against checkable specifications, inside a harness of tools, prompts and guardrails |
| Addy Osmani | Agents do the work under your direction (*agentic*), with engineering discipline throughout (*engineering*); the person focuses on architecture, correctness, edge cases and maintainability |

All five agree on the core: the AI does more of the typing, the person owns the goal and the proof that it's met.

The phrase has two meanings, and this project does both:

1. **Engineering *with* agents:** using a coding agent (such as Claude Code) to help build software, with the person specifying, reviewing and verifying.
2. **Engineering *an* agent:** building an agent yourself, which is what lessons 1 to 5 did.

## The five stages: from writing code to loops

Each stage moves the developer's effort one level further from typing code. Each one contains the one before it: a loop runs a harness, a harness runs an agent, an agent is driven by prompts, and the tools are ordinary code.

| Stage | What the developer does | The skill | In this project |
|---|---|---|---|
| **1. Writing code** | Types every line | Programming | The tools themselves: `add_entry`, `search_entries`, `update_last_entry`, totals added up in code |
| **2. Prompting** | Asks a model for an answer, one request at a time | Writing clear instructions | Lesson 1: one model call, the system prompt |
| **3. Agents** | Gives the model tools and lets it take several steps toward a goal | Designing tools and the step loop | Lesson 2 (one tool) and lesson 3 (the loop, `MAX_STEPS = 6`) |
| **4. Harness** | Builds everything around the model: instructions, tools, the loop, memory, limits | Designing the environment the agent works in | Lessons 4 and 5: the `worklog` package is a harness around qwen3:8b |
| **5. Loops** | Designs a system that prompts, checks and reruns the agent toward a goal, without a person writing each prompt | Designing a cycle you trust enough to walk away from | **Not yet built** (planned: lessons 9 and 10) |

Some writers split stage 2 in two: **prompt engineering** ("how should I phrase this?") and **context engineering** ("what does the model need to know right now?"). The progression is then written *prompt → context → harness → loop*.

### Two kinds of loop

The word "loop" means two different things, and it's easy to mix them up:

- **The inner loop** is the agent's own cycle: ask the model, run the tools it asks for, send the results back, repeat until it answers. Lesson 3 built this. It's part of the harness.
- **The outer loop** is what "loop engineering" means: a system around the agent that gives it a goal, checks its work, and runs it again until the goal is met or it hands back to a person. This project hasn't built one yet.

### Not every task needs to climb

The stages describe where the field has gone, not a rule that every task should go to the top. Plain code is still the right answer when the rules can be written down, and an agent is only worth its cost when the next step depends on what the last one found (`docs/Plain-Code-Model-Call-or-Agent.md`).

## The model, the tools and the harness

Every agent, small or large, is made of the same parts. Claude Code's own documentation describes it this way: the agentic loop is powered by **models that reason** and **tools that act**, and Claude Code is the layer around the model that provides the tools and manages what the model sees. That surrounding layer is the **agentic harness**.

### What a model is

A **model** (a large language model) is the AI itself: a very large neural network trained on huge amounts of text and code. It reads the messages it's sent and writes a reply one token at a time. It keeps nothing between calls (lesson 1), so the harness decides what it sees each time. A **Claude model** is a model trained by Anthropic; qwen3:8b, used in this project, is a much smaller open model from Alibaba that runs on a home PC.

Models come in sizes, with a trade-off between speed and cost on one side and capability on the other. Claude's family runs from Haiku (smallest and fastest) through Sonnet (the everyday workhorse) to Opus (the strongest reasoning). This project measured the same trade-off from the other end: a small local model is free and private, but slower and easier to fool.

### This project's agent beside Claude Code

| Part | The work log agent (this project) | Claude Code |
|---|---|---|
| **The model** (thinks and decides) | qwen3:8b, running on this PC | A Claude model, hosted by Anthropic |
| **The tools** (act) | `add_entry`, `search_entries`, `update_last_entry` | Read and edit files, run commands, search the web, and more |
| **The harness** (everything around the model) | The `worklog` package: instructions, tool list, the loop, memory, limits | Claude Code itself |
| **The loop** | Ask the model, run its tools, send results back, at most 6 steps | Gather context → take action → verify results, repeated until done |
| **Standing instructions** | The system prompt in `agent.py` | The system prompt plus the project's `CLAUDE.md` file |
| **Memory** | The last 5 turns, plus the log file | The context window (summarised when it fills), plus saved memory files |
| **Safety** | `MAX_STEPS`, a tool lookup table (more in lesson 7) | Permission modes, checkpoints that undo file edits |

The shapes match because the design is the same; the difference is scale. That's the point of building a small one by hand: the professional tools stop being a black box.

One difference worth noticing: Claude Code's safety features are enforced **in code**, not requested in the instructions. Lesson 6 shows why that matters.

## The practices

These run through every stage. Each one says what it is, why it matters, and where this project stands.

### 1. Specification: say what "done" means

Write down what the software should do before an agent builds it, so the result can be checked against something. The work runs in a loop: **Specify → Plan → Implement → Verify**, with the person owning the first and last steps.

**In this project:** each lesson starts with "What we are looking for" and ends with a test set whose right answers are known in advance. **Gap:** no lesson yet uses a coding agent to build a feature from a written spec (planned: the real-life scenario).

### 2. Prompt engineering: the instructions

The system prompt: the agent's role, rules and decision rules (for example, "if the user corrects something they just logged, call update_last_entry").

**In this project:** lessons 1 to 4 built the system prompt step by step, including the list of known projects that stopped the model inventing names. ✓

### 3. Context engineering: what the model sees

Choosing what information goes into the model's limited working memory on each call: instructions, tool descriptions, conversation history, retrieved records. Too little and it guesses; too much and it's slow, costly and distracted.

**In this project:** lesson 4 measured the cost (573 → 931 tokens over five turns) and limited memory to five turns. Lesson 5 showed the agent guesses when the context lacks what it needs. Lesson 6 showed exactly what the model is sent, then tested an instruction to ask instead of guessing: the model ignored it (0 questions in 27 runs). A check in code that refuses an unnamed project, and tells the model to ask, was added instead. **Gap:** search results aren't yet limited to the relevant records.

### 4. Tool design

Tools are the agent's hands. Good tools have clear names and descriptions, do one job, check their inputs, return only what's needed, and turn errors into messages instead of crashes.

**In this project:** lessons 2 to 4, including the `AVAILABLE_TOOLS` lookup table (the model can only cause listed functions to run) and `run_tool` returning error text. ✓ **Gap:** tools don't yet check that a project name is a real one (planned: lesson 7).

### 5. Memory and state

Short-term memory is the recent conversation, sent again with each call. Long-term state is saved data that outlasts a session.

**In this project:** lesson 4 (conversation memory) and lessons 4 and 5 (the log file did memory's job, and two separate program runs shared it). ✓

### 6. Guardrails and permissions

Limits enforced **in code**, not just asked for in the prompt: which tools the agent may use, checks on arguments, a cap on steps, and a person's approval before anything risky or hard to undo.

**In this project:** `MAX_STEPS`, the tool lookup table, demo logs for tests, lesson 6's named-project check (the first rule moved from the instructions into code after the instruction failed), and lesson 7's guardrails: a project must be on the known list, and hours must be more than 0 and at most 24. Lesson 7 also tests the checks on their own, with no model (a unit test).

### 7. Human in the loop

Deciding which actions the agent may take alone and which need a person: approval before changes, a person reviewing results, and the agent handing back when it's unsure.

**In this project:** Scott reviews every lesson's results. Since lesson 6, a refused save makes the agent ask which project. Since lesson 7, changing a saved entry needs the person's "yes".

### 8. Evals: measuring whether it works

**Evals** (evaluations) are test sets for AI behaviour. They come in several kinds:

- **Known-answer tests**: fixed inputs with right answers worked out in advance.
- **Controls**: the same tests with a feature switched off, to see what the feature really does.
- **Trajectory evals**: checking not just the final answer but the steps taken (the right tools, in the right order).
- **LLM-as-judge**: a second model grades answers where there's no single right one, checked against human grades.
- **Regression tests**: rerunning everything after each change, so a fix doesn't break something else.

**In this project:** known-answer tests in every lesson (6 of 6 in lessons 2 to 5), and a control in lesson 5 (6 of 6 with memory, 2 of 6 without). ✓ **Gap:** six tests per lesson is small; no trajectory checks, no judge, and no single test suite that reruns everything (planned: lesson 8).

### 9. Observability: seeing what it did

A **trace** is a record of every step an agent took: what it was sent, which tools it called, what came back, how long it took and how many tokens it used. Without traces, a wrong answer can't be explained.

**In this project:** the `[step N]` lines and token counts. **Gap:** nothing is saved, so a past run can't be reviewed (planned: lesson 8).

### 10. Cost and speed

Every call costs time, and with hosted models, money. Memory, retries and long loops all multiply it.

**In this project:** measured in lessons 1 and 4 (17.5 tokens per second; +62% tokens by turn 5). Running locally costs $0 per call. ✓

### 11. Security

An agent that reads text from outside (emails, web pages, files) can be tricked by instructions hidden in that text (**prompt injection**). Defences are least privilege (only the tools it needs), treating outside text as data, and approval for risky actions.

**In this project:** the agent only reads what Scott types and its own log, and its tools can only touch the log file. Lesson 7 shows prompt injection with a poisoned log entry, and defends in depth: tool results are marked as data, actions are checked in code, and changes need approval.

### 12. Loop engineering: the building blocks

The outer loop is built from six parts, as named by Addy Osmani in June 2026:

| Part | Its job | Planned in this project |
|---|---|---|
| **Automations** | Start the work on a schedule, without a person | Lesson 10: a scheduled daily or weekly run |
| **Worktrees** | Give parallel agents separate copies of the code so they don't collide | Explained in lesson 9; one agent at a time on this PC |
| **Skills** | Written-down project knowledge every run reads | Lesson 10: a skill file for the work log rules |
| **Connectors** | Let the agent act in real tools (through MCP, the Model Context Protocol) | Explained in lesson 10 |
| **Sub-agents** | Separate the *maker* from the *checker*, so an agent doesn't grade its own work | Lesson 9: a maker proposes a change, a checker runs the evals |
| **State** | A file outside the conversation that records what's done and what's next | Lesson 9: a loop state file |

Loops have well-known risks: they can burn tokens, they make mistakes unattended, and the faster they ship code, the wider the gap between the code and what the person understands. So the person still reads every change.

## Engineering *with* coding agents: the working patterns

The practices above are about building an agent. These are about using a coding agent (such as Claude Code) to build software, collected mainly from Simon Willison's *Agentic Engineering Patterns* and Google's *Industrial Agentic Engineering*.

| Pattern | What it means |
|---|---|
| **Writing code is cheap now** | Trying an idea costs minutes, so try several and keep the best. But code that's cheap to write is still expensive to review and maintain. |
| **Hoard things you know how to do** | Keep working examples, checklists and instructions (skills, `AGENTS.md` / `CLAUDE.md` files) that agents can reuse. |
| **Use Git with the agent** | Small commits, one per step, so any change can be reviewed or undone. |
| **First run the tests** | Start each session by having the agent run the existing tests, so it learns the project and you know the starting state. |
| **Red/green testing** | Write a test that fails (red) for the new behaviour, then have the agent make it pass (green). The test is the spec. |
| **Agentic manual testing** | Have the agent use the real program (or a browser, taking screenshots) to check behaviour that tests don't cover. |
| **Sub-agents** | Give a separate agent a narrow job, such as research or review, so the main one keeps a clean context. |
| **Linear walkthroughs** | Ask an agent to explain a change step by step, so you can review it faster and really understand it. |
| **Verification by checks** | Accept work when it passes the tests and checks, not because it looks right. |
| **Fix the harness, not the code** | When an agent gets something wrong, change its instructions, tools or checks so the mistake doesn't repeat (Google calls this *meta-debugging*). |
| **Don't ship what you haven't reviewed** | The person reads every change before it's merged. Osmani warns of developers "who can prompt but can't debug". |

**In this project:** lessons 1 to 5 were built with an AI coding assistant under these rules (a plan first, small steps, every result checked against a saved run, nothing published that wasn't reviewed). That process is recorded in `docs/DEVELOPMENT.md`, but it isn't yet shown as a case study (planned: Scenario B, which uses every pattern above on a real feature). Lesson 9's outer loop is *fix the harness* automated: it changes the agent's instructions, not its code.

## Coverage at a glance

| Part | Covered now | Planned |
|---|---|---|
| Writing code, prompting, agents, harness | Lessons 1 to 5 | |
| Loops | | Lessons 9 and 10 |
| Specification | Partly | Real-life scenario |
| Prompt engineering | ✓ | |
| Context engineering | Lesson 6 | |
| Tool design | ✓ | Lesson 7 (validation) |
| Memory and state | ✓ | |
| Guardrails and permissions | Lessons 6 and 7 | |
| Human in the loop | Lessons 6 and 7 | |
| Evals | Partly | Lesson 8 |
| Observability | Partly | Lesson 8 |
| Cost and speed | ✓ | |
| Security | Lesson 7 | |
| Engineering *with* a coding agent | In `DEVELOPMENT.md` | Scenario B (case study) |

## Sources

- Claude Code documentation, "How Claude Code works": https://code.claude.com/docs/en/how-claude-code-works

- The New Stack, "Vibe coding is passé. Karpathy has a new name for the future of software" (February 10, 2026): https://thenewstack.io/vibe-coding-is-passe-karpathy-has-a-new-name-for-the-future-of-software/
- Addy Osmani, "Agentic Engineering" (February 4, 2026): https://addyosmani.com/blog/agentic-engineering/
- Simon Willison, "What is agentic engineering?": https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering
- Simon Willison, *Agentic Engineering Patterns* (chapter list): https://simonwillison.net/guides/agentic-engineering-patterns/
- Google Research, "Industrial Agentic Engineering": https://research.google/pubs/industrial-agentic-engineering/

- IBM, "What is agentic engineering?" (February 2026): https://www.ibm.com/think/topics/agentic-engineering
- Simon Willison, "Writing code is cheap now": https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/
- Elastic, "Context engineering vs. prompt engineering": https://www.elastic.co/search-labs/blog/context-engineering-vs-prompt-engineering
- Addy Osmani, "Loop Engineering" (June 2026): https://addyosmani.com/blog/loop-engineering/
- Machine Learning Mastery, "An introduction to loop engineering": https://machinelearningmastery.com/an-introduction-to-loop-engineering/
- "Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents" (arXiv 2609.00006): https://arxiv.org/pdf/2609.00006
- "Don't Blame the Large Language Model: How Agent Harness Evolution Shapes Coding Agent Quality" (arXiv 2607.03691): https://arxiv.org/pdf/2607.03691
- "Stop Hand-Holding Your Coding Agent" (arXiv 2607.00038): https://arxiv.org/abs/2607.00038
- Arize, "AI agent guardrails vs. evals": https://arize.com/blog/ai-agent-guardrails-vs-evals/
- LangChain, "How to Evaluate LLMs and Agents": https://www.langchain.com/resources/how-to-evaluate-llms
- DigitalOcean, "A Simple Guide to Building AI Agents Correctly": https://www.digitalocean.com/community/tutorials/build-ai-agents-the-right-way
