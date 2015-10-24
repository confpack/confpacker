from __future__ import absolute_import

import os.path

import yaml

from cpcommon.ansible_compatibility import parse_ansible_yaml


class Package(object):
  def __init__(self, pkg_src_dir):
    self.pkg_src_dir = pkg_src_dir

    meta_path = os.path.join(self.pkg_src_dir, "meta.yml")
    tasks_path = os.path.join(self.pkg_src_dir, "tasks.yml")
    triggers_path = os.path.join(self.pkg_src_dir, "triggers.yml")

    self.meta = {}
    self.tasks = {}
    self.triggers = {}

    if os.path.isfile(meta_path):
      with open(meta_path) as f:
        self.meta = parse_ansible_yaml(yaml.load(f.read()))

    if os.path.isfile(tasks_path):
      with open(tasks_path) as f:
        self.tasks = parse_ansible_yaml(yaml.load(f.read()))

    if os.path.isfile(triggers_path):
      with open(triggers_path) as f:
        self.triggers = parse_ansible_yaml(yaml.load(f.read()))

    self.files = self._scan_files()
    self.templates = self._scan_templates()

  def _scan_files(self):
    pass

  def _scan_templates(self):
    pass
