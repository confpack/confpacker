from __future__ import absolute_import

import os.path

from libconfpacker.packagers.base import Package

from ... import helpers


class TestPackage(helpers.ConfpackerTestCase):
  def test_package_should_load_data_if_correct(self):
    package = Package(
      "nginx-conf",
      os.path.join(helpers.CORRECT1_PATH, "packages", "nginx-conf"),
      "201501010101-abcdef"
    )

    self.assertEquals(1, len(package.meta["system_pkg_dependency"]))
    self.assertEquals({"name": "nginx"}, package.meta["system_pkg_dependency"][0])

    self.assertEqual({"server_name": "{{ confpacker_fqdn }}"}, package.vars)

    self.assertEqual(2, len(package.main_tasks))
    self.assertEqual("file", package.main_tasks[0].action)
    self.assertEqual("path=/etc/nginx/sites-available/default state=absent", package.main_tasks[0].action_args)
    self.assertEqual("file", package.main_tasks[1].action)
    self.assertEqual("src=/etc/nginx/sites-available/serverid dest=/etc/nginx/sites-enabled/serverid state=link", package.main_tasks[1].action_args)
    self.assertEqual("linking serverid", package.main_tasks[1].name)

    self.assertEqual({"name": "restart nginx", "service": "name=nginx state=restarted"}, package.main_handlers[0])
    self.assertEqual(2, len(package.files))

    files = {target_path: real_path for real_path, target_path in package.files}

    serverid_path = "/etc/nginx/sites-available/serverid"
    sslconf_path = "/etc/nginx/ssl.conf"
    self.assertEqual(package.src_directory + "/files" + serverid_path, files[serverid_path])
    self.assertEqual(package.src_directory + "/files" + sslconf_path, files[sslconf_path])

    self.assertEqual(1, len(package.templates))
    self.assertEqual([(package.src_directory + "/templates/etc/nginx/nginx.conf", "/etc/nginx/nginx.conf")], package.templates)

    self.assertEqual(os.path.join(helpers.CORRECT1_PATH, "packages", "nginx-conf"), package.src_directory)

  def test_package_should_raise_if_handlers_is_wrong_type(self):
    with self.assertRaises(TypeError):
      Package(
        "incorrect-handlers-type",
        os.path.join(helpers.INCORRECT_HANDLERS_TYPE, "packages", "incorrect-handlers-type"),
        "201501010101-abcdef"
      )
