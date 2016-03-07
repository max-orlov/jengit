import sys
from StringIO import StringIO

import argh

import jengit


def main():
    parser = argh.ArghParser()
    subparsers_action = argh.utils.get_subparsers(parser, create=True)
    subparsers_action.metavar = ''
    parser.add_commands(jengit.app.commands)
    errors = StringIO()
    parser.dispatch(errors_file=errors)
    errors_value = errors.getvalue()
    if errors_value:
        errors_value = errors_value.replace('CommandError', 'error').strip()
        sys.exit(errors_value)
