"""Settings for the work log agent.

Everything you might want to change lives here, so you never have to dig through the
other files to adjust how the agent behaves.
"""

from pathlib import Path

# The local model Ollama runs. Must be downloaded first: `ollama pull qwen3:8b`.
MODEL = "qwen3:8b"

# Where files live. PROJECT_ROOT is the folder that holds this package, worked out from
# this file's own location, so the paths stay right wherever the project folder is moved.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
WORK_LOG = DATA_DIR / "work_log.jsonl"  # your real work log (kept out of Git)

# Project names the model should use. Giving it this list stops it inventing names
# (lesson 1's "Meat Price Data"). Add your own projects here.
KNOWN_PROJECTS = [
    "Cornerpost Watch",
    "Cornerpost Logic",
    "Herd Planner",
    "Agentic Engineering Worklog",
]

# The most rounds of tool use the agent may take for one message (lesson 3).
MAX_STEPS = 6

# How many earlier turns of the conversation the agent remembers (lesson 4).
MAX_TURNS = 5
