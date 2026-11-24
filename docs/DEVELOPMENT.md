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

### Fix: lesson 1's speed figure

While gathering numbers for the presentation, lesson 1's saved output (17.5 tokens per second, 17.5 seconds, 28 tokens out) didn't match its explanation (20.0, 25.7, 25) or the project page (21). Those came from earlier runs. The explanation, the lesson 1 page, the project page tile and the README were corrected to the saved run, with a note that speed varies a little between runs. Lesson 4's mention of "20 tokens per second" was corrected too. Code cells and outputs were not changed.

### The presentation

1. **Planned** in `docs/PRESENTATION_PLAN.md`. Scott approved it: 10 to 15 slides, opening with the question.
2. **Template:** copied from the meat-prices deck's exported file so all three portfolio decks match: Space Grotesk and Inter, dark `#1F1B18`, light `#FAF8F5` and `#F1ECE6`, small uppercase labels, 72 px headings, 100 px big numbers, cards, footer with source and slide number. Only the primary colour changes: green `#2E6A4C` (meat-prices is maroon).
3. **Pictures:** `presentation/charts.py` draws the token chart and the cover's glowing line from lesson 4's saved numbers (573, 652, 741, 772, 931).
4. **Built** as a Claude slide deck (Slides type), 15 slides with speaker notes: https://claude.ai/artifact/95VpP2jvpWi8REGDvNsqHP.
5. **Checked:** every number against the saved runs, and every slide rendered and looked at. Two layout fixes came out of it (slide 12's table was too narrow and pushed text into the footer; slide 11's quotes were in all capitals).
6. **Exported:** Scott reviewed it ("I love it!") and saved the PDF, PowerPoint and web page from the deck's Share › Export menu into `presentation/`, named to match the other projects. The image export saves only the slide that's open, so the 15 slide images were made from the PDF export instead (`pdftoppm`, 1920 × 1080, the same size as the Life Expectancy images) and zipped. The cover thumbnail is slide 1 at 800 × 450. A `noindex` tag was added to the web page's head, following the portfolio rule.
7. **Checked the exports:** the PDF has 15 pages, the PowerPoint 15 slides with 15 sets of speaker notes, the web page 15 slides; all 15 slide images were looked at.
8. **Published:** the files went to `scott/agentic-engineering-worklog/presentation/`, and the project page got a "The story, as a presentation" section copied from the meat-prices page (cover, "View the presentation", four download tiles with sizes), placed after "What I found", plus a "The presentation" button at the top. In dark mode the green turns light, so its buttons and badges use dark text there.

### Mapping the whole field (November 22, 2026)

Scott asked for everything involved in agentic engineering to be outlined in the project, since it's the project's name.

1. **Researched** the term's origin (Karpathy, February 2025 and 2026), the main definitions (Karpathy, Simon Willison, IBM, Google Research, Addy Osmani), the five stages (writing code → prompting → agents → harness → loops, with "loops" named in June 2026), the practices (context, tools, memory, guardrails, human in the loop, evals, observability, cost, security) and the working patterns for building with coding agents.
2. **Wrote `docs/AGENTIC_ENGINEERING_MAP.md`:** every part explained in plain words, where the project covers it, the gaps, and sources.
3. **Wrote `docs/ROADMAP.md`** for Scott's review: Parts 2 to 4 (lessons 6 to 10, and two real-life scenarios) to cover the gaps.
4. **Added the five stages** to the project page (a "From writing code to loops" section with a table, and a button at the top), the README, and the presentation (slide 4, replacing the ladder slide, so the deck stays at 15 slides).
5. **To do:** re-export the presentation, because the files on the portfolio still have the ladder slide.

### Lesson 6: Ask, don't guess

1. **Decided with Scott:** lessons 6 to 10 in order; a second model as grader in lesson 8; Scenario B on Herd Planner.
2. **Changed the package:**
   - `config.ASK_WHEN_UNCLEAR = True`
   - an `ASK_RULE` instruction in `agent.py`, added by `build_system_prompt(ask_when_unclear=...)`
   - a matching `Conversation(ask_when_unclear=...)` option, so a test can switch the rule off as a control
   - the terminal program uses the rule from now on
   - lesson 5's saved run was made before the rule existed, so rerunning lesson 5 now would use it
3. **Wrote the notebook:**
   - the exact context the model is sent
   - the rule and its size
   - a worked example
   - nine test conversations run three ways: the rule off (control 1), the rule on, and the rule on without memory (control 2), counting passes, wrong saves and needless questions
   - the token cost of the rule
4. **Tested against the stand-in model.** It ran end to end, and the terminal program asked "Which project was that for?" for an unclear message. Three expected figures were corrected before handing over: the instructions are about 900 characters, the rule adds about 240, and setting A should score about 6 of 9.

### Model, tools, harness: the comparison with Claude Code (November 22, 2026)

Scott asked what a "Claude model" is while reading Claude Code's documentation ("How Claude Code works"). The answer turned out to describe this project too, so it was documented:

1. **Map:** a new section, "The model, the tools and the harness": what a model is, how model sizes trade speed for capability, and a part-by-part table of this agent beside Claude Code, with the documentation page as the source.
2. **Lesson 5 notebook and page:** a new section naming the `worklog` package as a harness, with the comparison table and two new glossary rows (Model, Harness). Code cells and saved outputs unchanged; the section is dated.
3. **Project page:** the comparison table, under "From writing code to loops".
4. **Presentation:** slide 12's table of file sizes was replaced by the comparison table (the deck stays at 15 slides).
5. **README:** one paragraph naming the package as a harness.

### Lesson 6, first run: the instruction failed (November 22, 2026)

Scott ran lesson 6 as first built (ask rule only). Results, from the saved notebook:

| Setting | Passed | Wrong saves | Questions asked |
|---|---|---|---|
| A. Rule off, memory on | 4 of 9 | 5 | 0 |
| B. Rule on, memory on | 5 of 9 | 4 | 0 |
| C. Rule on, memory off | 3 of 9 | 6 | 0 |

- The model **never asked a question** in 27 runs. Step 4's example saved "the company site" under Agentic Engineering Worklog with the rule on.
- The rule added 56 tokens per call (576 → 632, +10%).
- The stand-in model used for testing had followed the rule, because it was written to. This is why numbers from a stand-in run are never published: it tests that the code runs, not how the real model behaves.
- This first run is kept in Git history (the commit "Document model, tools and harness; compare with Claude Code; lesson 6 run").

### Lesson 6, revised: the check in code (November 23, 2026)

1. **Package:**
   - `config.REQUIRE_NAMED_PROJECT = True`
   - in `agent.py`, `project_was_named()` and `Conversation.check_call()`, which run before every tool and refuse `add_entry` unless the user named the project in the remembered conversation
   - the refusal (`NOT_NAMED`) is sent back to the model as the tool's result and tells it to ask
   - `Conversation(require_named_project=...)` switches the check off for controls, and `blocked_calls` counts refusals
   - the terminal program uses the check from now on
2. **Notebook:**
   - Steps 4 to 6 were rewritten from the first run's real results (the rule failed)
   - new Step 7 shows the check's code and repeats the example with the check on
   - new Step 8 reruns the nine conversations with the check on, with and without memory (settings D and E), beside setting B
   - the closing sections were rewritten: "an instruction is a request, not a guarantee; put the rules that matter in code"
3. **Stand-in model** changed to ignore the rule, like the real one, and to ask when a save is refused. Against it, D and E scored 9 of 9 with 0 wrong saves. These numbers are not published; Scott's rerun decides.
4. **Next:** Scott reruns the whole notebook (Run All). Then Steps 7 and 8 are explained from the saved output, and Steps 4 to 6 are checked against it (temperature 0 should repeat the first run closely, but not necessarily exactly).

### Lesson 6, rerun and published (November 23, 2026)

1. **Scott reran the whole notebook.** Steps 1 to 6 repeated the first run exactly (same table, same 56 tokens), which shows the model is deterministic at temperature 0.
2. **Results with the check:**

| Setting | Passed | Wrong saves | Asked | Saves refused |
|---|---|---|---|---|
| B. Rule only | 5 of 9 | 4 | 0 | 0 |
| D. Rule and check | 9 of 9 | 0 | 3 | 4 |
| E. Rule and check, no memory | 9 of 9 | 0 | 6 | 6 |

   In Step 7 the model guessed, was refused, then asked "Which project was the work on the company site for?", and saved to Cornerpost Logic once told.
3. **Explanations rewritten from the saved run;** code cells and outputs unchanged.
4. **Published:** lesson 6 page; the project page got lesson 6 (Done) and lesson 7 (Next) in the lesson list, a new first finding ("An instruction is a request, not a guarantee"), the lessons stat changed to "6 of 10", and an updated "What's next".
5. **The presentation is not updated yet:** lesson 6's finding will be added with the Part 2 and 3 slides, then re-exported once.
