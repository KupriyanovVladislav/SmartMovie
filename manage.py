#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
from os import environ, path
import sys


def main():
    environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartMovie.settings')
    try:
        from django.core.management import execute_from_command_line
        from dotenv import load_dotenv
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    load_dotenv(path.join(path.dirname(__file__), '.env'))
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
