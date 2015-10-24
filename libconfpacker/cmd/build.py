from __future__ import print_function, absolute_import

import argparse
import os.path
import logging
import sys

from cpcommon import verify_directory_exists_or_sysexit, Command

from .. import packager


class BuildMain(Command):
  def __init__(self):
    self.argparser = argparse.ArgumentParser(description="Builds packages from a provisioning directory")
    self.argparser.add_argument("-d", "--directory", nargs="?", default=".", help="the path to the directory with all provisioning files. Default: current working directory")
    self.argparser.add_argument("-o", "--output", nargs="?", default="out/", help="the package output directory. Default: `pwd`/out")
    self.argparser.add_argument("-t", "--type", nargs="?", default="deb", choices=packager.types.keys(), help="the type of package to output")
    self.argparser.add_argument("packages", nargs="*", default=[], help="the list of packages to build. Default: builds all packages")
    self.argparser.prog = self.argparser.prog + " setup_environment"

    self.logger = logging.getLogger()

  def get_help(self):
    return self.argparser.format_help()

  def get_description(self):
    return self.argparser.description

  def __call__(self, argv):
    args = self.argparser.parse_args(argv)

    verify_directory_exists_or_sysexit(args.directory)

    package_paths = {}
    if len(args.packages) > 0:
      for package in args.packages:
        package_path = os.path.join(args.directory, "packages", package)
        if not os.path.isdir(package_path):
          print("error: package {} does not exist in {}".format(package, args.directory))
          sys.exit(1)
        package_paths[package] = package_path
    else:
      for dirname in os.listdir(os.path.join(args.directory, "packages")):
        package_path = os.path.join(args.directory, "packages", dirname)
        if dirname.startswith("_") or not os.path.isdir(package_path):
          continue

        package_paths[dirname] = package_path

    packer = packager.types[args.type](args.directory, args.output)
    build_id, outdir = packer.build(package_paths)

    return 0
