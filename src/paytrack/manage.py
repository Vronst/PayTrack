#!./.venv/bin/python3
import sys
from .app.core import TextApp


def main():
    if '-t' in sys.argv:
        app: TextApp = TextApp()
        if '-d' in sys.argv:
            try:
                app.start_app(debug=True)
            except ValueError as e:
                print(e)
        else:
            app.start_app()
    elif '-p' in sys.argv:
        # TODO: change password without limitation to minimum of...
        ...
    elif '-w' in sys.argv:
        # TODO: Web app start
        ...
    else:
        print("Possible commands:"
              "\n-t     starts text app"
              "\n-w     starts web app")


if __name__ == '__main__':
    main()
