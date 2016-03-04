from __future__ import absolute_import

import logging

from .deb import DebianPackager
from .build_config import BuildConfig


SUPPORT_PACKAGERS = {
  "deb": DebianPackager
}

logger = logging.getLogger("confpacker")


def build(src_directory, out_directory, packages=[]):
  bc = BuildConfig(src_directory, packcages=packages)
  for packager_names in bc.config["types"]:
    for packager_name in packager_names:
      if packager_name not in SUPPORT_PACKAGERS:
        logger.warn("{} is not a valid packager. supported are: {}".format(packager_name, SUPPORT_PACKAGERS))
        continue

    packager = SUPPORT_PACKAGERS[packager_name](bc, out_directory)
    packager.build()
