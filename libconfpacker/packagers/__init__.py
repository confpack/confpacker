from __future__ import absolute_import

import os.path

import yaml

from .deb import DebianPackager
from .exceptions import InvalidInputError

packagers = {
  "deb": DebianPackager
}


class BuildConfig(object):
  def __init__(self, filename):
    with open(filename) as f:
      self.options = yaml.load(f.read())


def build(src_dir, out_dir):
  build_config = BuildConfig(os.path.join(src_dir, "config.yml"))
  build_packagers = []
  for pt in build_config.get("types", ["deb"]):
    if pt not in packagers:
      raise InvalidInputError("{} is not a valid type. valid ones are: {}".format(pt, packagers.keys()))

    build_packagers.append(packagers[pt])
