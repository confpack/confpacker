from __future__ import absolute_import

from datetime import datetime
import logging
import os
import os.path
import subprocess

import yaml

from cpcommon import cd


class Package(object):
  def src_path(self, *path):
    return os.path.join(self.src_directory, *path)

  def __init__(self, name, src_directory, build_version):
    self.logger = logging.getLogger("confpacker")
    self.name = name
    self.src_directory = src_directory
    self.build_version = build_version

    self.meta = self.load_meta()
    self.main_tasks = self.load_tasks()
    self.main_handlers = self.load_handlers(ignore_error=True)
    self.vars = self.load_vars(ignore_error=True)
    self.secrets = self.load_secrets(ignore_error=True)
    self.files = self.scan_files()
    self.templates = self.scan_templates()

  def _load_yml_file(self, filepath, expected_type, ignore_error=False):
    if not os.path.exists(filepath):
      if ignore_error:
        return expected_type()

      raise LookupError("cannot find {}".format(filepath))

    with open(filepath) as f:
      thing = yaml.load(f.read())

    if thing is None and ignore_error:
      return expected_type()

    if not isinstance(thing, expected_type):
      raise TypeError("expected a {} but got a {} in {}".format(expected_type, type(thing), filepath))

    return thing

  def load_meta(self):
    meta_path = self.src_path("meta.yml")
    return self._load_yml_file(meta_path, dict, ignore_error=True)

  def load_tasks(self, filename="main.yml", ignore_error=False):
    tasks_path = self.src_path("tasks", filename)
    return self._load_yml_file(tasks_path, list, ignore_error=ignore_error)

  def load_handlers(self, filename="main.yml", ignore_error=False):
    handlers_path = self.src_path("handlers", filename)
    return self._load_yml_file(handlers_path, list, ignore_error=ignore_error)

  def load_vars(self, filename="main.yml", directory="vars", ignore_error=False):
    vars_path = self.src_path(directory, filename)
    return self._load_yml_file(vars_path, dict, ignore_error=ignore_error)

  def load_secrets(self, filename="main.yml", ignore_error=False):
    # TODO: this is not yet implemented
    return {}

  def scan_directory_for_files(self, directory):
    base_path = self.src_path(directory)
    if not os.path.isdir(base_path):
      return []

    files = []
    for root, dirs, files_in_dir in os.walk(base_path):
      for filename in files_in_dir:
        path = os.path.join(root, filename)
        if path.startswith(base_path):
          path = path[len(base_path):]
        else:
          # TODO: This may happen for a symlink. Need to be investigated
          raise RuntimeError("file path {} does not start with src directory path {}?".format(path, self.src_directory))

        files.append(path)

    return files

  def scan_files(self):
    return self.scan_directory_for_files("files")

  def scan_templates(self):
    return self.scan_directory_for_files("templates")


class BasePackager(object):
  def __init__(self, build_config, output_dir):
    self.logger = logging.getLogger("confpacker")
    self.build_config = build_config
    self.output_dir = output_dir

    if not os.path.exists(self.output_dir):
      os.mkdir(self.output_dir)

  def get_source_git_sha(self):
    with cd(self.build_config.src_directory):
      if os.path.isdir(".git"):
        sha = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).strip()
      else:
        sha = ""

    return sha

  def get_timestamp(self):
    return datetime.now().strftime("%Y%m%d%H%M%S")

  def get_build_version(self):
    timestamp = self.get_timestamp()
    git_sha = self.get_source_git_sha()

    build_version = timestamp
    if git_sha:
      build_version = build_version + "-" + git_sha

    return build_version

  def build(self):
    build_version = self.get_build_version()
    this_out_dir = os.path.join(self.output_dir, build_version)
    if os.path.exists(this_out_dir):
      raise RuntimeError("{} already exists? this should not happen".format(this_out_dir))

    os.mkdir(this_out_dir)
    for pkg_name, pkg_src_path in self.build_config.package_paths.items():
      package = Package(pkg_name, pkg_src_path, build_version)
      self.build_one(package, build_version, this_out_dir)

  def build_one(self, package, build_version, out_dir):
    raise NotImplementedError
