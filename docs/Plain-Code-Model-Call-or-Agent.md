# Plain Code, a Model Call, or an Agent?

Notes for the agent lessons: how to decide how much AI a task needs. The core advice comes from the lesson material; the parts marked **Added** came from a discussion in the Cornerpost Watch project on 2026-11-10. The same notes live in `B:\Development\Python\Cornerpost-Watch\docs\Detection-and-AI-Approach.md`, where they sit next to how that site's detector works.

**The short version:** start with plain code and move up only when the problem forces you to. Most good products are mostly plain code, with a model call or a small agent in the places that need flexibility. Lesson 2 is level 2 (one model call inside plain code); lesson 3 turns the same task into level 3 (the loop).

## The ladder and the questions

**The ladder (start at the bottom; move up only when the problem forces you to)**

1. **Plain code.** The rules can be written down. Example: "flag animals whose withdrawal date is after today" is a date comparison.
2. **One model call inside plain code.** The steps are fixed, but one step involves messy language or judgment. Example: turning "gave tag 214 her booster today" into a record is one call; code does the rest.
3. **An agent.** The steps can't be known in advance, because the next step depends on what the last one found.

**Questions to ask**

- Can I write the steps as a flowchart? If yes, it's not an agent.
- Is the input messy (free text, photos, vague questions)? If yes, a model belongs somewhere.
- Does the path change based on what's found along the way? If yes, an agent is worth considering.
- **Added: can I write the rule down, or must it be learned from examples?** If it must be learned, the tool is statistics or machine learning — a different kind of AI from chat models and agents. For data-science work this is usually the most important question.

**What an agent costs**

- Slower, and paid models charge per step.
- Less predictable: the same question can take a different path each time.
- Harder to test: there's no single right sequence to check.
- **Added:** mistakes build on each other, since a wrong early step sends every later one the wrong way.
- **Added:** it needs guardrails — limits on what it may do, and a set of test questions with known answers so you can tell whether a change made it better or worse.

**Two kinds of "AI" (the gap in the original ladder)**

| Kind | What it does | Example in this project |
|---|---|---|
| Chat models and agents | Work with language: read, write, decide the next step | Writing an alert email in plain English |
| Statistics and machine learning | Learn patterns from data that can't be written as rules | Learning what's normal for each spot; classifying a change as road, pad or pond |

**A note on the example in the original advice:** "What changed on the north parcel since spring?" is usually level 2, not 3. The steps are fixed (find the parcel, run the change check for those dates, describe the result) with one model call to write the answer. It only becomes an agent if questions vary a lot ("compare with last year", "is the neighbour's road on my side?").

## Worked example: Cornerpost Watch

| Part | Level |
|---|---|
| Detector rules (today) | Plain code |
| Learning each spot's normal (notebook 02) | Statistics, learned from data |
| Change classifier with confidence scores (M5) | Machine learning, learned from data |
| Writing the alert email in plain English | One model call, optional |
| "Ask about my land" chat for clients | Possibly an agent, much later, and only if the questions really vary |

## A checklist to use on any new idea

1. Write the steps as a flowchart. Could you? → plain code, or plain code plus a model call.
2. Mark each step whose input is messy (free text, photos, vague questions). → that step gets one model call.
3. Mark each rule you can't write down but could learn from examples. → statistics or machine learning, not a chat model.
4. Only if the order of steps depends on what earlier steps found → consider an agent, and plan its guardrails and test questions before building it.
