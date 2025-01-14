"""
CLI for rdown
"""

import sys
import ReceiptLineRenderer
import rdown
from argparse import ArgumentParser

version_str = 'rdown [version {}]'.format(rdown.__version__)

def main(args):
  namespace = parse(args)
  if namespace.filenames:
    for filename in filenames:
      try:
        with open(filename, 'r', encoding='utf-8') as fin:
          rendered = rdown.markdown(fin)
          sys.stdout.buffer.write(rendered.encode())
      except OSError:
        sys.exit('Cannot open file "{}".'.format(filename))
  else:
    interactive()

def interactive():
  """
  Parse user input, dump to stdout, rinse and repeat.
  Python REPL style.
  """
  _import_readline()
  _print_heading()
  contents = []
  more = False
  while True:
    try:
      prompt, more = ('... ', True) if more else ('>>> ', True)
      contents.append(input(prompt) + '\n')
    except EOFError:
      print('\n' + rdown.markdown(contents), end='')
      more = False
      contents = []
    except KeyboardInterrupt:
      print('\nExiting.')
      break

def parse(args):
  parser = ArgumentParser()
  parser.add_argument('-v', '--version', action='version', version=version_str)
  parser.add_argument('filenames', nargs='*',
                      help='specify an optional list of files to convert')
  return parser.parse_args(args)

def _import_readline():
  try:
    import readline  # noqa: F401
  except ImportError:
    print('[warning] readline library not available.')


def _print_heading():
  print('{} (interactive)'.format(version_str))
  print('Type Ctrl-D to complete input, or Ctrl-C to exit.')


if __name__ == "__main__":
    main(sys.argv[1:])