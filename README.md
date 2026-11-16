# Agentic Engineering Worklog

A lesson-by-lesson record of learning to build an AI agent from scratch in Python, with no framework, using a free model that runs on my own PC.

The agent turns plain-English notes such as "fixed the alert email bug in Cornerpost Watch, about 2 hours" into saved records, and will answer questions about them. Every lesson is scored on a small test set, so progress is measured rather than assumed.

**Project page:** https://schirko.com/scott/agentic-engineering-worklog/

## Status: in progress

| Lesson | What it adds | Status |
|---|---|---|
| 1. One model call | Send a message from Python and get text back | Done |
| 2. One tool | The model asks for a Python function; my code runs it | Done: 6 of 6 on the test set |
| 3. The loop | The model keeps calling tools until the job is done (the point it becomes an agent) | Next |
| 4. Memory | The agent picks up where it left off | Planned |
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
