
class PrettyError(Exception):
  """We catch this error so we print it out prettily."""
  pass


class InvalidInputError(PrettyError):
  pass
