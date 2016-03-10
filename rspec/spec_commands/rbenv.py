import os
from plugin_helpers.decorators import memoize

class Rbenv(object):
  def __init__(self, context):
    self.context = context

  def result(self):
    if not self.context.from_settings("check_for", {}).get("rbenv_rspec"): return None

    return(
      self._from_which() or
      self._from_settings()
    )

  def _from_which(self):
    file = self.context.which_rspec()
    if ".rbenv" in file: return file

  def _from_settings(self):
    file = os.path.expanduser(self.context.from_settings("paths", {}).get("rbenv_rspec"))
    if file and os.path.isfile(file): return file
