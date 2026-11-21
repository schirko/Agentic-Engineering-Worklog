"""The agent's tools: plain Python functions, plus the descriptions the model reads.

The model never runs these functions. It asks for one by name, and agent.py runs it and
sends the result back (lesson 2).
"""

import json
from datetime import datetime
from pathlib import Path

from . import config

# The file the tools read and write. It starts as your real work log; tests and demos
# point it somewhere else with set_log_file(), so they never touch your real entries.
_log_file = config.WORK_LOG


def set_log_file(path):
    """Point every tool at a different log file, such as a demo or test log."""
    global _log_file
    _log_file = Path(path)
    _log_file.parent.mkdir(parents=True, exist_ok=True)


def get_log_file():
    """The log file the tools are currently using."""
    return _log_file


def read_entries():
    """Every entry in the log, oldest first. An empty list if the file doesn't exist yet."""
    if not _log_file.exists():
        return []
    lines = _log_file.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def write_entries(entries):
    """Replace the whole log with these entries."""
    _log_file.parent.mkdir(parents=True, exist_ok=True)
    _log_file.write_text("".join(json.dumps(e) + "\n" for e in entries), encoding="utf-8")


def add_entry(project, description, hours=None):
    """Save one new entry at the end of the log and return a short confirmation."""
    entry = {
        "logged_at": datetime.now().isoformat(timespec="seconds"),
        "project": project,
        "description": description,
        "hours": hours,
    }
    _log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(_log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    return f"Saved entry for {project}."


def search_entries(project=None, date_from=None, date_to=None):
    """Find entries by project and date range (YYYY-MM-DD, both ends included).

    Returns one line per entry and a total, worked out here in code so the model never
    has to do the arithmetic (lesson 3).
    """
    matches = []
    for entry in read_entries():
        day = entry["logged_at"][:10]
        if project and entry["project"].lower() != project.lower():
            continue
        if date_from and day < date_from:
            continue
        if date_to and day > date_to:
            continue
        matches.append(entry)

    if not matches:
        return "No matching entries."

    lines = []
    total = 0.0
    for entry in matches:
        hours = entry["hours"]
        if hours is not None:
            total += float(hours)
        shown = f"{hours} h" if hours is not None else "hours not given"
        lines.append(f"{entry['logged_at'][:10]} | {entry['project']} | {entry['description']} | {shown}")
    lines.append(f"{len(matches)} entries. Total hours where given: {total:g}")
    return "\n".join(lines)


def update_last_entry(project=None, description=None, hours=None):
    """Correct the most recent entry, changing only the parts given (lesson 4)."""
    entries = read_entries()
    if not entries:
        return "Error: the log is empty, so there is nothing to update."
    last = entries[-1]
    if project is not None:
        last["project"] = project
    if description is not None:
        last["description"] = description
    if hours is not None:
        last["hours"] = hours
    write_entries(entries)
    return f"Updated the last entry: {last['project']} | {last['description']} | {last['hours']} h"


# The descriptions the model reads. It never sees the code above, only these.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_entry",
            "description": "Save one new work log entry. Use this when the user describes work they did.",
            "parameters": {
                "type": "object",
                "properties": {
                    "project": {"type": "string", "description": "Name of the project the work was for."},
                    "description": {"type": "string", "description": "Short description of what was done."},
                    "hours": {"type": "number", "description": "Hours spent. Leave this out if the user did not say."},
                },
                "required": ["project", "description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_entries",
            "description": (
                "Look up saved work log entries. Use this to answer questions about past work. "
                "Returns the matching entries and the total hours."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "project": {"type": "string", "description": "Only entries for this project. Leave out for all projects."},
                    "date_from": {"type": "string", "description": "First day to include, as YYYY-MM-DD."},
                    "date_to": {"type": "string", "description": "Last day to include, as YYYY-MM-DD."},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_last_entry",
            "description": (
                "Correct the most recently saved entry. Use this when the user changes something they just "
                "logged, for example 'make that two hours' or 'that was for Herd Planner'. "
                "Only pass the fields that change."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "project": {"type": "string", "description": "The corrected project name."},
                    "description": {"type": "string", "description": "The corrected description."},
                    "hours": {"type": "number", "description": "The corrected number of hours."},
                },
                "required": [],
            },
        },
    },
]

# The lookup table: the only functions the model can cause to run (lesson 2).
AVAILABLE_TOOLS = {
    "add_entry": add_entry,
    "search_entries": search_entries,
    "update_last_entry": update_last_entry,
}


def run_tool(name, arguments):
    """Run one requested tool and return its text result. Mistakes become error text, not crashes."""
    if name not in AVAILABLE_TOOLS:
        return f"Error: there is no tool named {name}."
    try:
        return AVAILABLE_TOOLS[name](**arguments)
    except TypeError as error:
        return f"Error: {error}"
