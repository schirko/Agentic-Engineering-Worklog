# Agentic Engineering Worklog

A lesson-by-lesson record of learning to build an AI agent from scratch in Python, with no framework, using a free model that runs on my own PC.

The agent turns plain-English notes such as "fixed the alert email bug in Cornerpost Watch, about 2 hours" into saved records, and will answer questions about them. Every lesson is scored on a small test set, so progress is measured rather than assumed.

**Project page:** https://schirko.com/scott/agentic-engineering-worklog/

## What is agentic engineering?

Agentic engineering is building software with AI agents doing much of the hands-on work, while a person stays in charge of what gets built and whether it's right. The agent writes code, runs it, and fixes its own errors in a loop. The person decides what to build, sets the limits, checks the results, and decides what ships.

It is the disciplined version of **vibe coding**. In vibe coding you describe what you want, the AI writes it, and if it seems to work you move on without reading the code closely: fast, and fine for quick experiments. Agentic engineering keeps the AI help but adds checks: write down what the code should do first, review the plan, build in small steps, and prove it works with tests. The question is "what proves it's right?", not "does it look right?"

The work runs in a four-step loop: **Specify, Plan, Implement, Verify**. The person owns the first and last steps; the agent does most of the middle.

The phrase covers two things, and this project does both:

1. **Engineering with agents:** using an AI coding agent to build software under that discipline.
2. **Engineering agents:** building an agent itself (the model, its tools and its loop) and measuring whether it behaves. The lesson notebooks do this, scoring the agent on a test set at every step.

## Status: in progress

| Lesson | What it adds | Status |
|---|---|---|
| 1. One model call | Send a message from Python and get text back | Done |
| 2. One tool | The model asks for a Python function; my code runs it | Done: 6 of 6 on the test set |
| 3. The loop | The model keeps calling tools until the job is done (the point it becomes an agent) | Done: 6 of 6 on tools, answers and saves |
| 4. Memory | The agent picks up where it left off | Next |
| 5. A real job | The full work log agent | Planned |

## Setup

- Model: `qwen3:8b` through [Ollama](https://ollama.com), on two NVIDIA GTX 1060 6 GB cards (about 21 tokens per second)
- Python package: `ollama`
- Notebooks run in PyCharm: open one and run each cell in order with Shift + Enter

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install ollama jupyter
ollama pull qwen3:8b
```

## Layout

- `notebooks/`: one notebook per lesson, saved with its real output
- `docs/Plain-Code-Model-Call-or-Agent.md`: how I decide whether a task needs plain code, one model call, or an agent
- `data/`: the work log the agent writes (`work_log.jsonl`); kept out of Git because it is personal
