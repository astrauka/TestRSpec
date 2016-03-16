from plugin_helpers.decorators import memoize
from rspec.output import Output
from plugin_helpers.open_file import OpenFile

class SwitchBetweenCodeAndTest(object):
  SPEC_EXTENSION = "_spec.rb"
  SOURCE_EXTENSION = ".rb"

  def __init__(self, context):
    self.context = context

  def run(self):
    files = self._files_by_path() or self._files_by_name()
    if files:
      OpenFile(self.context.window(), files).run()
    else:
      print("SublimeRSpec: No files found, searched for {0}".format(self._file_base_name()))

  def _files_by_path(self):
    return

  @memoize
  def _file_base_name(self):
    name = self.context.file_base_name()

    if self.context.is_test_file():
      return name.replace(self.SPEC_EXTENSION, self.SOURCE_EXTENSION)
    else:
      return name.replace(self.SOURCE_EXTENSION, self.SPEC_EXTENSION)

  def _files_by_name(self):
    file_matcher = lambda file: file.endswith(self._file_base_name())
    return self.context.project_files(file_matcher)

