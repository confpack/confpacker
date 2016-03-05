
import copy

SUPPORTED_DIRECTIVES = {
  "notify"
}


class MultipleActionsError(StandardError):
  pass


class Task(object):
  def __init__(self, raw_task):
    raw_task = copy.copy(raw_task)
    self.directives = {}

    for directive in SUPPORTED_DIRECTIVES:
      self.directives[directive] = raw_task.get(directive)
      raw_task.pop(directive, None)

    self.name = raw_task.get("name")
    raw_task.pop("name", None)

    if len(raw_task) > 1:
      raise MultipleActionsError("multiple actions detected: {}".format(raw_task.keys()))

    self.action = raw_task.keys()[0]
    self.action_args = raw_task[self.action]

  def postinst_cmd(self):
    return "confpack-runtime {} '{}'".format(self.action, self.action_args)
