# Development guide

How this project is built, tested and published. Read this before changing anything that goes to the portfolio.

## What this project owns on the portfolio

The portfolio lives in the Schirko repo at `B:\Development\Python\Schirko\scott\` and is served at https://schirko.com/scott/.

This project writes **only** these paths:

- `scott/agentic-engineering-worklog/` (the project page and the exported lessons)
- `scott/images/screenshots/agentic-engineering-worklog.png` (the card picture)

**Never write `scott/index.html` or `scott/styles.css`.** The portfolio project ("Resume Review") owns them. If the card needs changing, write the new card text and give it to Scott to pass on to that session.

No step in this project's publishing process writes `scott/index.html`. None ever has, so there was nothing to remove. If a future script is added, it must not write it either.

## The code: the `worklog` package

Lessons 1 to 4 built the agent inside notebooks. Lesson 5 moved it into a package so the notebooks and the terminal program share one copy of the code.

| File | Its one job | First built in |
|---|---|---|
| `worklog/config.py` | Settings: model name, file paths, `KNOWN_PROJECTS`, `MAX_STEPS`, `MAX_TURNS` | lessons 1 to 4 |
| `worklog/tools.py` | The tools (`add_entry`, `search_entries`, `update_last_entry`), their descriptions for the model, the `AVAILABLE_TOOLS` lookup table and `run_tool` | lessons 2 to 4 |
| `worklog/agent.py` | `build_system_prompt`, `call_model`, and the `Conversation` class (the loop plus memory) | lessons 3 and 4 |
| `worklog/__main__.py` | The terminal program: `python -m worklog` | lesson 5 |
| `worklog/__init__.py` | Marks the folder as a package and describes it | lesson 5 |

Design decisions, and why:

- **Paths come from the package's own location** (`Path(__file__).resolve().parent.parent`), so moving the project folder doesn't break anything. This mattered when the folder moved from `B:\_Dev` to `B:\Development`.
- **The log file can be switched** with `tools.set_log_file(path)` (in code) or `--log PATH` (in the program). Notebooks and tests always use a demo log, never `data/work_log.jsonl`.
- **Today's date is worked out when a conversation starts**, not when the package is imported, so a program left running past midnight still knows what "today" means.
- **Totals are added up in code** in `search_entries`, so the model only repeats a finished number (lesson 3's finding).
- **Tool errors become text**, not crashes: `run_tool` returns "Error: …" for an unknown tool or wrong arguments, and the model sees it.
- **The program checks Ollama first** (`model_is_ready`): if Ollama isn't running or the model isn't downloaded, it prints what to do instead of a traceback.

After editing any file in `worklog/`, restart the notebook kernel before rerunning: Python keeps the first copy it imported.

## Testing before Scott runs it

The real model runs only on Scott's PC. Before a lesson is handed over, its code is checked against a **stand-in model** in the build sandbox:

- A small file replaces `ollama.chat` (and, from lesson 5, `ollama.list`) with a function that returns fixed answers for each test message. It answers differently when the earlier messages are missing, so the memory-on and memory-off paths are both exercised.
- For the terminal program, which runs as a separate process, the stand-in is loaded through a `sitecustomize.py` file on `PYTHONPATH`. Python loads that file automatically at start-up, so the child process gets the stand-in too.
- The whole notebook is then run from top to bottom with `jupyter nbconvert --execute`.

The stand-in checks that **the code runs** and the test logic is right. It says nothing about how the real model behaves, so **no number from a stand-in run is ever published.** All published numbers come from Scott's saved run.

## Running a lesson notebook (Scott's step)

1. Start Ollama.
2. Open the notebook in PyCharm and use **Run All** (the double-arrow button), so every cell runs and stores its output.
3. **Wait for the last cell to finish.** In lesson 5, Step 5 makes 24 or more model calls and takes a few minutes; its last line is "Really need memory: …".
4. Save with **Ctrl + S**, then commit and push the notebook.

Before writing explanations, the saved notebook is checked: every code cell must have output. Lesson 5 needed three commits because of this: the first was made before the notebook ran (no outputs), and the second while Step 5 was still running (Steps 1, 2 and 5 had no output). The third had everything.

## Publishing a lesson

1. Check the saved run (above).
2. Rewrite the explanations from the saved output. The code cells and outputs must stay exactly as they ran: the rewrite script compares them before and after and stops if anything changed.
3. Export the notebook to `scott/agentic-engineering-worklog/lessons/lesson-NN.html` with nbconvert's `basic` template, wrapped in a page that has:
   - `<meta name="robots" content="noindex, nofollow">`
   - the shared back bar stylesheet `/scott/backbar.css` and the favicon links from the portfolio guide
   - the `sx-backbar` markup as the first element in `<body>`, with `sx-crumb` set to "Agentic Engineering Worklog"
   - only absolute `/scott/...` links
4. Update `scott/agentic-engineering-worklog/index.html`: the lesson list, the stats, the findings, the Limits note, "What's next" and the "Page updated" date. Every number must come from the saved notebook output.
5. Render the pages in a browser and look at them. Fix anything that displays wrongly (lesson 5's Project and Model lines ran together until a blank line was added between them).
6. Refresh the card picture: screenshot the top of the project page at a 1440 × 810 browser size (16:9), and resize it to **1200 × 675** pixels, the size of the existing file.
7. Commit the notebook and README in this repo, and the `scott/agentic-engineering-worklog` folder and the screenshot in the Schirko repo. Then redeploy in Coolify.
8. If the card text should change, give Scott the new text for the portfolio session.

## How each lesson is explained

Documentation is the most important part of this project: it is what shows the work. Every lesson notebook follows the same pattern, written for a reader who is new to the subject:

- **An opening** that says what the lesson adds, where the last one left off, and the big idea in plain words.
- **For each step:**
    - *What we are looking for*: the question this step answers.
    - *The code, line by line*: every new term is defined the first time it appears.
    - *How to read it*: the actual output from the saved run, quoted or put in a table, with the right answers worked out by hand where possible.
    - *What it means*: the lesson to take away, including anything surprising.
    - *What's next and why*: how this step leads to the next.
- **At the end:** exercises, a summary, a list of the terms the lesson uses, and what comes next.

The explanations are written after the notebook has run, from its saved output. If a run contradicts what a step expected, the explanation says so plainly and explains why, rather than describing the result that was predicted. Lesson 3's "watch it fail" step and lesson 4's memory tests are examples.

## Tests

- Every lesson ends with a small test set and a known starting state, so the right answers are known in advance.
- Tests write to their own file in `data/`, never to `work_log.jsonl`.
- When a test is meant to show that a feature matters, also run it with the feature switched off (a control). A test that still passes isn't measuring that feature. Lesson 5 does this for memory.
- Design tests so the model can't pass by guessing. Lesson 4's "main project" test used Cornerpost Watch, which the model picks anyway when it has no information (it's first in `KNOWN_PROJECTS`), so the test passed without memory. Lesson 5 uses Herd Planner instead.

## Rules for results

- Numbers on the page come from a notebook run that is saved in the repo. Nothing is estimated or typed from memory.
- If a run contradicts a notebook's explanation, correct the explanation and say what happened ("In my run…").
- `data/` holds the personal work log and is in `.gitignore`. Tests write to their own file in `data/` and never touch `work_log.jsonl`.

## Build record

What was done in each lesson, in order.

### Lesson 1: One model call

- Installed Ollama and downloaded `qwen3:8b`; created `.venv` and installed `ollama` and `jupyter`.
- Wrote the notebook: one call, timing and memory use, a second call showing the model keeps nothing between calls, and a first try at logging work as text.
- Findings: about 21 tokens per second; the model invented a project name ("Meat Price Data") and replied "LOGGED: …" without saving anything.

### Lesson 2: One tool

- Wrote `add_entry` and its description, and the `AVAILABLE_TOOLS` lookup table.
- Gave the model the list of real project names.
- Test set: 6 of 6. The log only changed when the code ran the tool.

### Lesson 3: The loop

- Added `search_entries`, with totals worked out in code, and the loop with `MAX_STEPS = 6`.
- Test set: 6 of 6 on tools, answers and saves. The model requested both tools in one round when asked to log and then total.

### Lesson 4: Memory

- Added the `Conversation` class (keeping whole turns, up to `max_turns`) and `update_last_entry`.
- Test set: 6 of 6, but a stateless agent also handled "make that two hours" and `max_turns = 0` still chose Cornerpost Watch. Prompt size grew from 573 to 931 tokens over five turns.
- Explanations rewritten honestly from the run, and the need for a control noted.

### Lesson 5: A real job

1. **Built the package** from the lesson 4 code: `config.py`, `tools.py`, `agent.py`, `__main__.py`, `__init__.py` (design decisions above).
2. **Wrote the notebook**: setup and demo log, a tour of the package, using it from Python, running it as a program with `subprocess`, a test set run with `max_turns = 5` and `max_turns = 0`, and daily-use instructions.
3. **Designed three new tests that need memory**: a main project that isn't first in the list (Herd Planner), a project named only in an earlier message ("the company site"), and a question about what was just said ("30 minutes").
4. **Tested against the stand-in model**, for both the notebook and the program. One fix came out of it: the program is started with `PYTHONIOENCODING=utf-8`, so a reply containing a special character can't crash it on Windows when its output is collected.
5. **Wrote the files to the PC** and updated the README (status table and a "Using the agent" section).
6. **Scott ran the notebook.** It took three commits to get a complete saved run (see "Running a lesson notebook").
7. **Wrote the explanations from the real run.** Results: 6 of 6 with memory, 2 of 6 without, 4 tests really need memory. Without memory, the model guessed Cornerpost Watch (first in the list) and filed "the company site" under Agentic Engineering Worklog, with no warning.
8. **Published**: lesson 5 page, project page (stats, two new findings, lesson list, Limits, "What's next"), and a new card screenshot. New card text given to Scott.

### Next: the presentation

Planned in `docs/PRESENTATION_PLAN.md` for Scott to review before it's built, following the meat-prices project's presentation.
