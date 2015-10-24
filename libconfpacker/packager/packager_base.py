from datetime import datetime
import os
import os.path
import subprocess

from cpcommon import cd


class PackagerBase(object):
  def __init__(self, source_directory, output_dir):
    self.source_directory = source_directory
    self.output_dir = output_dir
    if not os.path.exists(self.output_dir):
      os.mkdir(self.output_dir)

  def get_source_git_sha(self):
    with cd(self.source_directory):
      if os.path.isdir(".git"):
        sha = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).strip()
      else:
        sha = ""

    return sha

  def get_timestamp(self):
    return datetime.now().strftime("%Y%m%d%H%M%S")

  def build(self, packages):
    timestamp = self.get_timestamp()
    git_sha = self.get_source_git_sha()

    build_id = timestamp
    if git_sha:
      build_id = timestamp + "-" + git_sha

    this_out_dir = os.path.join(self.output_dir, build_id)
    if os.path.exists(this_out_dir):
      raise RuntimeError("{} already exists? rebuild should be fine?".format(this_out_dir))

    os.mkdir(this_out_dir)

    for package, source_path in packages.iteritems():
      self.build_one(package, source_path, timestamp, git_sha, this_out_dir)

    return build_id, this_out_dir

  def build_one(self, package, timestamp, git_sha, this_out_dir):
    raise NotImplementedError
