"""The work log agent.

A small AI agent that saves plain-English notes about your work to a log file and answers
questions about them. It runs on a local model through Ollama.

The package is split into four files, each with one job:

- config.py: the settings you might want to change (model, project names, limits).
- tools.py: the actions the agent can take (save, search, correct) and their descriptions.
- agent.py: the loop and the conversation memory that make it an agent.
- __main__.py: the terminal program you run with `python -m worklog`.

Lessons 1 to 4 built each of these pieces in a notebook. Lesson 5 moved them here.
"""
