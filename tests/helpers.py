import logging
import os.path
import unittest
import shutil

# Don't be verbose in tests..
logging.getLogger().setLevel(logging.WARN)

TEST_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_DATADIR_PATH = os.path.join(TEST_DIR_PATH, "testdata")

CORRECT1_PATH = os.path.join(TEST_DATADIR_PATH, "correct1")
INCORRECT_CONFIG_YML_PATH = os.path.join(TEST_DATADIR_PATH, "incorrect-config-yml")
INCORRECT_HANDLERS_TYPE = os.path.join(TEST_DATADIR_PATH, "incorrect-handlers-type")

DEFAULT_OUTDIR = os.path.join(TEST_DATADIR_PATH, "out")


class ConfpackerTestCase(unittest.TestCase):
  def tearDown(self):
    if os.path.exists(DEFAULT_OUTDIR):
      shutil.rmtree(DEFAULT_OUTDIR, ignore_errors=True)
