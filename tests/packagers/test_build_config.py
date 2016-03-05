from __future__ import absolute_import

import os.path

from libconfpacker.packagers.build_config import BuildConfig

from cpcommon.exceptions import NoBacktraceError

from .. import helpers


class TestBuildConfig(helpers.ConfpackerTestCase):
  def test_initializing_build_config(self):
    bc = BuildConfig(helpers.CORRECT1_PATH)
    self.assertEqual(2, len(bc.package_paths))

    self.assertEqual(os.path.join(helpers.CORRECT1_PATH, "packages", "nginx-conf"), bc.package_paths["nginx-conf"])
    self.assertEqual(os.path.join(helpers.CORRECT1_PATH, "packages", "example-com-conf"), bc.package_paths["example-com-conf"])

    self.assertEqual({"packages_prefix": "test1-", "types": ["deb"], "maintainer": "John Doe <john.doe@example.com>"}, bc.config)

  def test_fail_build_config_with_incorrect_config_yml(self):
    with self.assertRaises(NoBacktraceError):
      BuildConfig(helpers.INCORRECT_CONFIG_YML_PATH)
