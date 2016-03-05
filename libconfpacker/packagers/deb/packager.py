from __future__ import absolute_import

import os
import shutil

from ..base import BasePackager

from cpcommon import mkdir_p


class DebianPackager(BasePackager):
  def build_one(self, package, build_version, out_dir):
    # Things we need to do:
    #
    # 1. Copy all files into the correct directory
    # 2. Copy all templates into a /etc/confpack/<pkg_name>/templates/...
    # 3. Make an empty file for the correct location for the templates
    # 4. Generate postinst script:
    #   1. Template the things
    #   2. Perform the tasks
    #   3. Notify the triggers
    self.copy_files_to_build_dir(package.files, out_dir)

    self.copy_templates_to_build_dir(package, build_version, out_dir)
    self.generate_control_files(package, build_version, out_dir)
    self.package_deb(package, build_version, out_dir)

  def copy_files_to_build_dir(self, package, out_dir):
    data_dir = os.path.join(out_dir, "data")
    for local_path, target_path in package.files:
      path_in_data_dir = os.path.join(data_dir, target_path)
      parent_directory = os.path.dirname(path_in_data_dir)
      mkdir_p(parent_directory)

      shutil.copy2(local_path, path_in_data_dir)

  def copy_templates_to_build_dir(self, package, out_dir):
    data_dir = os.path.join(out_dir, "data")
    for local_path, target_path in package.templates:
      path_in_data_dir = os.path.join(data_dir, target_path)
      open(path_in_data_dir, "w").close()  # create empty file

      path_in_data_dir = os.path.join(data_dir, "etc", "confpack", "templates", package.name, target_path)
      parent_directory = os.path.dirname(path_in_data_dir)
      mkdir_p(parent_directory)

      shutil.copy2(local_path, path_in_data_dir)

  def generate_control_files(self, package, build_version, out_dir):
    pass

  def package_deb(self, package, build_version, out_dir):
    pass
