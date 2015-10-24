#!/usr/bin/env python
from __future__ import print_function

import sys

import libconfpacker
from cpcommon.cmdline import Cmdline

SCRIPT_NAMES = {"confpacker", "confpacker.py"}


def main(argv):
  cmdline = Cmdline(SCRIPT_NAMES)
  cmdline.register_command(confpacker.BuildMain)
  return cmdline.main(argv)


if __name__ == "__main__":
  sys.exit(main(sys.argv[:]))
