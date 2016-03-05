from __future__ import absolute_import

import re

from libconfpacker.packagers.base import BasePackager
from libconfpacker.packagers.build_config import BuildConfig

from ... import helpers


class BasePackagerTest(BasePackager):
  def __init__(self, *args, **kwargs):
    BasePackager.__init__(self, *args, **kwargs)
    self.build_logs = {}

  def build_one(self, package, build_version, out_dir):
    self.build_logs[package.name] = {
      "package": package,
      "build_version": build_version,
      "out_dir": out_dir,
    }


class TestBasePackager(helpers.ConfpackerTestCase):
  def setUp(self):
    helpers.ConfpackerTestCase.setUp(self)
    self.bc = BuildConfig(helpers.CORRECT1_PATH)
    self.packager = BasePackagerTest(self.bc, helpers.DEFAULT_OUTDIR)

  # TODO: fill out this test
  def test_get_build_version_with_git(self):
    pass

  def test_build_will_call_build_one(self):
    self.packager.build()
    self.assertEqual(2, len(self.packager.build_logs))

    # no git here so format should be YYYYMMDDHHMMSS, 14 characters
    self.assertTrue(re.match("^\d{14}$", self.packager.build_logs["nginx-conf"]["build_version"]))
    self.assertTrue(re.match("^\d{14}$", self.packager.build_logs["example-com-conf"]["build_version"]))
