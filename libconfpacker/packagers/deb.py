from __future__ import absolute_import

from .packager_base import PackagerBase


class DebianPackager(PackagerBase):
  def build_one(self, package, source_path, timestamp, git_sha, this_out_dir):
    pass
