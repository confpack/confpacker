from __future__ import absolute_import

import logging
import os.path

import yaml

from cpcommon.exceptions import NoBacktraceError


REQUIRED_CONFIG_KEYS = {
  "packages_prefix": str,
  "types":           list,
  "maintainer":      str,
}


class BuildConfig(object):
  def __init__(self, src_directory, packages=[]):
    self.logger = logging.getLogger("confpacker")
    self.src_directory = src_directory
    self.packages = packages[:]

    self.load_build_config()
    self.discover_packages()

  def discover_packages(self):
    self.package_paths = {}
    if len(self.packages) > 0:
      for package in self.packages:
        package_path = os.path.join(self.src_directory, "packages", package)
        if not os.path.isdir(package_path):
          raise NoBacktraceError("package {} does not exist at {}".format(package, package_path))

        self.logger.debug("discovered {} at {}".format(package, package_path))
        self.package_paths[package] = package_path
    else:
      for dirname in os.listdir(os.path.join(self.src_directory, "packages")):
        package_path = os.path.join(self.src_directory, "packages", dirname)
        if dirname.startswith("_") or not os.path.isdir(package_path):
          continue

        self.logger.debug("discovered {} at {}".format(dirname, package_path))
        self.package_paths[dirname] = package_path

  def load_build_config(self):
    config_path = os.path.join(self.src_directory, "config.yml")
    if not os.path.exists(config_path):
      raise NoBacktraceError("config file does not exist at {}. please create one before proceeding.".format(config_path))

    with open(config_path) as f:
      self.config = yaml.load(f.read())

    self.logger.debug("loaded build config at {}".format(config_path))

    for key, ttype in REQUIRED_CONFIG_KEYS.items():
      if key not in self.config:
        raise NoBacktraceError("config requires key {}".format(key))

      if ttype is not None and not isinstance(self.config[key], ttype):
        raise NoBacktraceError("config must be an instance of {}".format(ttype))
