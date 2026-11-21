"""The terminal program. Run it from the project folder with:

    python -m worklog

Type what you worked on, or ask about past work. Type "quit" (or press Ctrl+C) to stop.

Options:
    --once "message"   handle one message and exit, instead of chatting
    --log PATH         use a different log file, such as a demo log
    --quiet            hide the tool steps and show only the replies
"""

import argparse
import sys

import ollama

from . import config, tools
from .agent import Conversation


def model_is_ready():
    """Check that Ollama is running and the model is downloaded, with a clear message if not."""
    try:
        names = [m.model for m in ollama.list().models]
    except Exception:
        print("Can't reach Ollama. Start it from the Windows Start menu, then try again.")
        return False
    if not any(name.startswith(config.MODEL) for name in names):
        print(f"The model {config.MODEL} isn't downloaded. Run: ollama pull {config.MODEL}")
        return False
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m worklog", description="Chat with your work log agent.")
    parser.add_argument("--once", metavar="MESSAGE", help="handle one message and exit")
    parser.add_argument("--log", metavar="PATH", help="use this log file instead of the real work log")
    parser.add_argument("--quiet", action="store_true", help="hide the tool steps")
    args = parser.parse_args(argv)

    if args.log:
        tools.set_log_file(args.log)

    if not model_is_ready():
        return 1

    chat = Conversation(verbose=not args.quiet)

    if args.once:
        reply, _ = chat.send(args.once)
        print(f"Agent: {reply}")
        return 0

    print(f"Work log agent ({config.MODEL}). Log: {tools.get_log_file()}")
    print('Tell me what you worked on, or ask about past work. Type "quit" to stop.')
    while True:
        try:
            text = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if text.lower() in {"quit", "exit", "q"}:
            break
        if not text:
            continue
        reply, _ = chat.send(text)
        print(f"Agent: {reply}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
