from rspec.files.opposite import OppositeFile
from plugin_helpers.utils import memoize
import os

class SpecFile(object):
  def __init__(self, context, ignored_directory):
    self.context = context
    self.ignored_directory = ignored_directory

  def result(self):
    if not self._relative_name().startswith(self.ignored_directory): return

    spec_name = self._spec_name()
    if os.path.isfile(spec_name): return spec_name

  def _spec_name(self):
    return os.path.join(
      self.context.project_root(),
      self.context.from_settings("spec_folder"),
      self._name_wihtout_ignored_directory()
    )

  def _name_wihtout_ignored_directory(self):
    return self._relative_name().replace(self.ignored_directory, "", 1)

  @memoize
  def _relative_name(self):
    return OppositeFile(self.context).relative_name()
