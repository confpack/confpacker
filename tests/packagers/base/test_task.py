from __future__ import absolute_import

from libconfpacker.packagers.base.task import Task, MultipleActionsError

from ... import helpers


class TestTask(helpers.ConfpackerTestCase):
  def setUp(self):
    helpers.ConfpackerTestCase.setUp(self)
    self.raw_task = {
      "name": "test task",
      "file": "src=/etc/nginx/sites-available/serverid dest=/etc/nginx/sites-enabled/serverid state=link",
      "notify": "restart nginx"
    }

  def test_task_will_initialize_correctly_and_generate_correct_postinst_cmd(self):
    task = Task(self.raw_task)
    self.assertEqual(self.raw_task["name"], task.name)

    self.assertEqual("file", task.action)
    self.assertEqual(self.raw_task["file"], task.action_args)

    self.assertEqual(self.raw_task["notify"], task.directives["notify"])

    self.assertEqual("confpack-runtime file 'src=/etc/nginx/sites-available/serverid dest=/etc/nginx/sites-enabled/serverid state=link'", task.postinst_cmd())

  def test_task_will_fail_if_multiple_actions_found(self):
    self.raw_task["service"] = "name=nginx state=restarted"
    with self.assertRaises(MultipleActionsError):
      Task(self.raw_task)
