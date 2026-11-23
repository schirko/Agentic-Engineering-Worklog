# Presentation plan: Agentic Engineering Worklog

**Status:** approved by Scott on November 20, 2026 (10 to 15 slides; open with the question; nothing to add). Built as a 15-slide Claude slide deck: https://claude.ai/artifact/95VpP2jvpWi8REGDvNsqHP. The final slide list is in "As built" below; the draft list is kept for the record.

## Purpose

Tell the whole project as one short story an employer can follow in about 12 minutes, with or without me in the room: what I set out to do, what I built in five steps, what I found when I measured it, and what comes next.

It follows the pattern of the meat-prices and Life Expectancy Predictor presentations: one deck, with speaker notes, shown on the project page with a cover picture and four downloads.

## Audience

A hiring manager or a data team lead. They may know data science well but have never built an AI agent. Every term is explained the first time it appears, the way the lessons do it.

## The story in one sentence

I built an AI agent from scratch on a free model on my own PC, and measured it at every step, which showed what each piece really does, including that a perfect test score can prove less than it seems.

## Story arc

1. **The question** (slides 1 to 3): can I build an agent from scratch and prove it works? What agentic engineering means.
2. **Building it, one piece at a time** (slides 4 to 9): the setup, then lessons 1 to 4, each with the one thing it showed.
3. **The twist** (slides 10 and 11): lesson 4 scored 6 of 6, but a control test in lesson 5 showed much of that score didn't depend on memory at all.
4. **The result** (slides 12 and 13): a tested program I use every day.
5. **What I learned and what's next** (slides 14 and 15).

## Slides

Every number below comes from a saved notebook run. The lesson each one comes from is given in brackets.

| # | Headline | Visual | What I say (summary of the speaker notes) |
|---|---|---|---|
| 1 | Can I build an AI agent from scratch, and prove it works? | Title, with a real exchange from the terminal program underneath | A work log agent: you tell it what you worked on in plain English and it saves records and answers questions. No framework, a free model, my own PC, and a test at every step. |
| 2 | From a sentence to a saved record | "Fixed the alert email bug in Cornerpost Watch, about 2 hours" → arrow → the saved record (project, description, hours) | The goal, and why it's harder than it looks: the model has to decide which project, how many hours, and whether to save anything at all. It's the base for a productivity app I want to build. |
| 3 | What is agentic engineering? | Two columns, vibe coding vs. agentic engineering, with the loop Specify, Plan, Implement, Verify | Vibe coding trusts what looks right; agentic engineering asks what proves it's right. This project does both senses: engineering *with* an agent, and engineering *an* agent. |
| 4 | A free model on a home PC | Four number tiles: qwen3:8b · 5.2 GB download, 5.9 GB loaded · 100% on two GTX 1060 6 GB cards · 17.5 tokens per second · $0 per call [lesson 1] | Running locally means no API bill and no data leaving the PC, at the cost of speed and capability. |
| 5 | A model only knows what you send it | Two exchanges: "What project did I work on this morning?" answered with "I don't have access…", then answered correctly once the earlier message was sent along [lesson 1] | The model keeps nothing between calls. Memory is a list of messages, and my code controls it. |
| 6 | Looking like a record isn't a record | The model's reply "LOGGED: Meat Price Data \| Cleaned the meat price data." beside the note: no such project, and nothing was saved [lesson 1] | It invented a project name, and its reply only looked like a saved entry. This is why the agent needs real tools and a list of real project names. |
| 7 | One tool: the model asks, my code runs | Flow diagram: message → model → tool request → my code runs `add_entry` → log file → result back to the model. Score: 6 of 6 [lesson 2] | The log held 9 entries before and after the model's request; it changed only when my code ran the tool. The model never touches the file. |
| 8 | The loop: where it becomes an agent | Loop diagram (ask the model → run the tools → send results back → repeat until it answers, at most 6 steps) and the real exchange where it saved first and searched second. Score: 6 of 6 [lesson 3] | Hand it exact work: totals are added up in code, so the model reported 2.5 and 3 hours correctly and saved 30 minutes as 0.5. |
| 9 | Do you even need an agent? | The ladder: plain code → one model call → an agent | Most tasks don't need an agent. I move up the ladder only when the next step depends on what the last one found. |
| 10 | Memory works, and it has a cost | Line chart: tokens the model read on each turn, 573 → 652 → 741 → 772 → 931 [lesson 4] | Every earlier turn is re-read on every call: about 60% more after five turns. And a surprise: the correction "make that two hours" worked with no memory at all, because the correction tool reads the last entry from the file. |
| 11 | A perfect score can prove less than it seems | Bar chart: tests passed with memory on (6 of 6) and off (2 of 6), with the 4-test gap marked [lesson 5] | Lesson 4 scored 6 of 6, but its tests mostly didn't need memory. A control (the same tests with memory switched off) separates "it works" from "memory is why it works". |
| 12 | Without memory, it guesses instead of asking | Two real failures: "my main project" saved to Cornerpost Watch (the first name on its list); "the company site" saved to Agentic Engineering Worklog, with no warning [lesson 5] | This also explains lesson 4: its test used Cornerpost Watch, the model's default guess, so it passed for the wrong reason. A guess gets saved as if it were fact. |
| 13 | A real job: a program I use every day | The package as five boxes (config, tools, agent, the program, about 389 lines in all) beside a real session of `python -m worklog` [lesson 5] | Two separate runs shared the log: the second, with no memory of the first, still reported the right total of 4 hours. |
| 14 | What I learned | Five short statements | 1. The model only knows what you send it. 2. Give it real tools and exact work. 3. Saved data is more reliable than memory. 4. A test needs a control to prove what it measures. 5. When it lacks information, it guesses. |
| 15 | What's next | Three cards | Make it ask when the project isn't clear; build the productivity desktop app on it; add agent features to Cornerpost Logic and Cornerpost Watch. Links to the project page and the code. |

### Appendix (after the closing slide)

| # | Headline | Content |
|---|---|---|
| A1 | The test sets | One row per lesson: what was tested, how many cases, the score |
| A2 | Limits | Six tests per lesson is small; an 8B model is slower and less capable than hosted models; results are from my PC, not a live demo |

## As built (15 slides; slide 4 changed November 22, 2026)

To fit Scott's 10 to 15 slides, lesson 1's two findings share one slide, and the two appendix slides became one. On November 22 the ladder slide (plain code → one model call → an agent) was replaced by the five-stage slide (writing code → prompting → agents → harness → loops), because the ladder is the first three of those stages.

| # | Slide id | Headline | Type and background |
|---|---|---|---|
| 1 | cover | Can I build an AI agent from scratch, and prove it works? | Cover, dark, glowing line of lesson 4's token counts |
| 2 | goal | Turn one plain-English sentence into a saved record. | Content, light |
| 3 | agentic | AI does much of the work. A person decides what's built and proves it's right. | Cards and the four-step loop, light alternate |
| 4 | stages | Five stages of AI-assisted software. This project climbs four, then the fifth. | Five cards as a staircase, light (added November 22; replaces the ladder slide) |
| 5 | setup | A free model on a home PC: no API bill, and nothing leaves the machine. | Big numbers (8B, 100%, 17.5, $0), light |
| 6 | lesson1 | The model keeps nothing between calls, and invents what it doesn't know. | Two transcripts, dark |
| 7 | tool | The model asks for a tool. My code runs it. | Flow diagram and big numbers (6 of 6, 9 → 9), light |
| 8 | loop | Let it keep using tools until the job is done. That's an agent. | Steps and transcript, light alternate |
| 9 | memory | Memory works, and every turn costs more to read. | Token chart and +62%, light alternate |
| 10 | control | Same six tests, run twice: with memory, and with it switched off. | **Statement: 6 of 6, 2 of 6, 4**, green |
| 11 | guesses | Without the information it needs, it guesses instead of asking. | Two cards, dark |
| 12 | program | A program I run every day: python -m worklog | Package table and transcript, light |
| 13 | learned | Five things I'd tell anyone building their first agent. | Numbered rows, light alternate |
| 14 | next | From a learning project to tools I'll use every day. | Three cards, dark |
| 15 | appendix | Measured at every step, with known right answers. | Table of test sets and limits, light alternate |

Every slide has speaker notes. Number checks against the saved runs: 17.5 tokens per second and 5.9 GB at 100% on the GPUs (lesson 1); 6 of 6 and 9 → 9 (lesson 2); 6 of 6 and "2 hours" (lesson 3); 573 → 931 tokens, +62% (lesson 4: 931 ÷ 573 = 1.625); 6 of 6 with memory, 2 of 6 without, 4 hours total, 389 lines (lesson 5).

## Look: the same template as the other two decks

All three presentations share one template, so they look like a set. Only the primary colour changes: meat-prices is maroon, and this one is **green**, the project page's own accent.

Taken from the meat-prices deck's exported file:

| Part | Template (same in all three) | This deck |
|---|---|---|
| Fonts | Space Grotesk for headings and big numbers, Inter for text | same |
| Dark background | `#1F1B18` | same |
| Light backgrounds, alternating | `#FAF8F5` and `#F1ECE6` | same |
| Heading text | `#1F1B18`; footer text `#5F5852` | same |
| Primary colour (small labels, big numbers, chart highlights, one full-colour statement slide) | maroon `#9A3B2E` | green `#2E6A4C` |
| Glow on dark slides | a soft maroon line | a soft lighter green, `#6FBF94` |

Slide types, used exactly as the template uses them:

- **Cover:** dark background, a faint glowing picture from the project's own data behind the text, a small uppercase label ("An agent story · …"), a 120 px title, a one-line subtitle, and a byline with the project's web address.
- **Content slide:** a small uppercase label in the primary colour (24 px, spaced letters), a 72 px heading that states the point, then one chart, picture or set of cards, with a source line and slide number at the bottom.
- **Big numbers:** two or three numbers at 100 px in the primary colour, each with a one-line explanation.
- **Cards:** two or three boxes, each with a 40 px title and a 28 px explanation.
- **Statement slide:** the whole slide in the primary colour with white text, used once, for the key result.
- **Dark slide:** used for the turning points of the story.

Which type each slide uses:

| # | Type | Background |
|---|---|---|
| 1 | Cover (glow: the 5 turns of token growth from lesson 4, or the agent loop as a faint line drawing) | dark |
| 2 | Content: sentence → saved record | light |
| 3 | Cards: vibe coding vs. agentic engineering, with the four-step loop | light, alternate |
| 4 | Big numbers: 5.9 GB · 100% on the GPUs · 17.5 tokens/s · $0 | light |
| 5 | Content: the two exchanges | light, alternate |
| 6 | Content: "LOGGED: Meat Price Data" | dark |
| 7 | Content: tool flow diagram, score 6 of 6 | light |
| 8 | Content: loop diagram and exchange, score 6 of 6 | light, alternate |
| 9 | Cards: the ladder | light |
| 10 | Content: token chart | light, alternate |
| 11 | **Statement: 6 vs 2** | green |
| 12 | Cards: the two wrong guesses | dark |
| 13 | Content: the package and a real session | light |
| 14 | Cards: what I learned | light, alternate |
| 15 | Cards: what's next | dark |
| A1, A2 | Appendix: test sets, limits | light |

Terminal exchanges are shown as real text in a monospace font, copied from the saved notebook output, never retyped. The two charts (slides 10 and 11 on paper; the statement slide may use big numbers instead of a chart) are made in Python from the saved numbers, in the template's colours.

## Format and files

Built as a Claude slide deck (the same tool as the other two presentations). From the deck's **Export** menu it downloads as PDF, PowerPoint (with speaker notes), a one-file web page, and slide images.

Published to the portfolio in `scott/agentic-engineering-worklog/presentation/`:

| File | What it is |
|---|---|
| `agentic-engineering-worklog-story.html` | The deck as one web page that works offline (the "View the presentation" button opens this) |
| `agentic-engineering-worklog-story.pdf` | For reading or printing |
| `agentic-engineering-worklog-story.pptx` | Editable PowerPoint, with speaker notes |
| `agentic-engineering-worklog-story-slides.zip` | Every slide as a PNG |
| `cover.png` | The cover slide at 800 × 450, used as the thumbnail |

## The section on the project page

The same layout as meat-prices and Life Expectancy Predictor:

- A heading, **"The story, as a presentation"**, with the id `presentation`.
- On the left, the cover picture with a "15 slides" label; it opens the presentation.
- On the right, a one-paragraph description, a **"View the presentation"** button, and four download tiles: PDF, PowerPoint, Web page and Slide images, each with its file size.
- A **"The presentation"** button in the row of buttons at the top of the page.
- The same CSS as the meat-prices page (`.deck`, `.deck-thumb`, `.dls`, `.dl`), with the page's green in place of maroon.
- Placed after "What I found", before "The lessons".

## Fix before building: lesson 1's speed figure

Lesson 1's saved output shows **17.5 tokens per second** and **17.5 seconds** in total. Its explanation says 20.0 tokens per second and 25.7 seconds, and the project page says 21 tokens per second. Those figures came from earlier runs, not the saved one. Before the deck is built:

- Rewrite lesson 1's explanation to use the saved run's numbers (17.5 tokens per second, 17.5 seconds), and add a line saying speed varies a little from run to run.
- Change the project page's "21" tile, the README and the lesson 1 page to 17.5.

## How it will be built (steps)

1. Scott reviews and approves this plan.
2. Fix lesson 1's speed figure (above), in the notebook, its page, the project page and the README.
3. Make the two charts in Python from the saved numbers.
4. Build the deck: outline and look first, then the slides three at a time, with speaker notes on each. Check every number against this plan's sources.
5. Scott reviews the deck and asks for changes.
6. Scott downloads the PDF, PowerPoint, web page and slide images from the deck's Export menu into a folder I can reach.
7. I make the cover picture, zip the slide images, add the presentation section to the project page, and write everything to the portfolio folder.
8. Scott commits and pushes; I give new card text if needed.
9. The steps actually taken are added to the build record in `docs/DEVELOPMENT.md`.

## Questions for Scott (answered)

1. Is 15 slides (plus 2 appendix slides) and about 12 minutes the right length?
2. Should slide 1 open with the question, as written, or with the result ("6 vs 2")?
3. Anything you want added or left out?
