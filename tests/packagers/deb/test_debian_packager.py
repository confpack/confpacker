from __future__ import absolute_import

from libconfpacker.packagers.deb import DebianPackager
from libconfpacker.packagers.build_config import BuildConfig

from ... import helpers


class TestDebianPackager(helpers.ConfpackerTestCase):
  def setUp(self):
    helpers.ConfpackerTestCase.setUp(self)
    self.bc = BuildConfig(helpers.CORRECT1_PATH)
    self.packager = DebianPackager(self.bc, helpers.DEFAULT_OUTDIR)

  def _setup_single_build(self, package, build_version):
    this_build_outdir = os.path.join(self.packager.output_dir, build_version)
    os.mkdir(this_build_outdir)
    this_package_outdir = os.path.join(this_build_outdir, package.name)
    os.mkdir(this_package_outdir)
    return this_package_outdir

  def _get_package(self, pkg_name):
    build_version = self.packager.get_build_version()
    for name, pkg_src_path in self.build_config.package_paths.items():
      if name == pkg_name:
        return Package(package_name, pkg_src_path, build_dir), build_version

    raise LookupError("package {} cannot be found".format(pkg_name))

  def test_copy_files_to_build_dir(self):
    package, build_version = self._get_package("nginx-conf")
    this_package_outdir = self._setup_single_build(package, build_version)

    self.packager.copy_files_to_build_dir(package, this_package_outdir)
    import pdb; pdb.set_trace()

