#!./.venv/bin/python3
import sys
from app.core import TextApp


if __name__ == '__main__':
    if '-t' in sys.argv:
        app: TextApp = TextApp()
        app.start_app()
