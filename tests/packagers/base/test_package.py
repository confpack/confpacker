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
    self.assertEqual({"file": "path=/etc/nginx/sites-available/default state=absent"}, package.main_tasks[0])
    self.assertEqual({"file": "src=/etc/nginx/sites-available/serverid dest=/etc/nginx/sites-enabled/serverid state=link", "name": "linking serverid"}, package.main_tasks[1])

    self.assertEqual({"name": "restart nginx", "service": "name=nginx state=restarted"}, package.main_handlers[0])
    self.assertEqual(2, len(package.files))
    files = set(package.files)
    self.assertTrue("/etc/nginx/sites-available/serverid" in files)
    self.assertTrue("/etc/nginx/ssl.conf" in files)

    self.assertEqual(1, len(package.templates))
    self.assertEqual(["/etc/nginx/nginx.conf"], package.templates)

  def test_package_should_raise_if_handlers_is_wrong_type(self):
    with self.assertRaises(TypeError):
      Package(
        "incorrect-handlers-type",
        os.path.join(helpers.INCORRECT_HANDLERS_TYPE, "packages", "incorrect-handlers-type"),
        "201501010101-abcdef"
      )
