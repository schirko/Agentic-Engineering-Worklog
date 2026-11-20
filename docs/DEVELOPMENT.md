# Development guide

How this project is built and published. Read this before changing anything that goes to the portfolio.

## What this project owns on the portfolio

The portfolio lives in the Schirko repo at `B:\Development\Python\Schirko\scott\` and is served at https://schirko.com/scott/.

This project writes **only** these paths:

- `scott/agentic-engineering-worklog/` (the project page and the exported lessons)
- `scott/images/screenshots/agentic-engineering-worklog.png` (the card picture)

**Never write `scott/index.html` or `scott/styles.css`.** The portfolio project ("Resume Review") owns them. If the card needs changing, write the new card text and give it to Scott to pass on to that session.

No step in this project's publishing process writes `scott/index.html`. None ever has, so there was nothing to remove. If a future script is added, it must not write it either.

## Publishing a lesson

1. Run the lesson notebook in PyCharm from top to bottom and save it, so its real output is stored in the `.ipynb`.
2. Export it to `scott/agentic-engineering-worklog/lessons/lesson-NN.html` with nbconvert's `basic` template, wrapped in a page that has:
   - `<meta name="robots" content="noindex, nofollow">`
   - the shared back bar stylesheet `/scott/backbar.css` and the favicon links from the portfolio guide
   - the `sx-backbar` markup as the first element in `<body>`, with `sx-crumb` set to "Agentic Engineering Worklog"
   - only absolute `/scott/...` links
3. Update `scott/agentic-engineering-worklog/index.html`: the lesson list, the stats, and any new findings. Every number must come from the saved notebook output.
4. Commit the notebook in this repo, and the `scott/agentic-engineering-worklog` folder in the Schirko repo. Then redeploy in Coolify.
5. If the card text should change, give Scott the new text for the portfolio session.

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
- When a test is meant to show that a feature matters, also run it with the feature switched off (a control). A test that still passes isn't measuring that feature.

## Rules for results

- Numbers on the page come from a notebook run that is saved in the repo. Nothing is estimated or typed from memory.
- If a run contradicts a notebook's explanation, correct the explanation and say what happened ("In my run…").
- `data/` holds the personal work log and is in `.gitignore`. Tests write to their own file in `data/` and never touch `work_log.jsonl`.
