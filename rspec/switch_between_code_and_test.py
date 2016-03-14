from plugin_helpers.decorators import memoize
from rspec.output import Output

class SwitchBetweenCodeAndTest(object):
  SPEC_EXTENSION = "_spec.rb"
  SOURCE_EXTENSION = ".rb"

  def __init__(self, context):
    self.context = context

  def run(self):
    files = self._files()

  def _files(self):
    file_matcher = lambda file: file.endswith(self._target_file_name())
    return self.context.project_files(file_matcher)

  def _target_file_name(self):
    if self.context.is_test_file():
      return self.context.file_name().replace(self.SPEC_EXTENSION, self.SOURCE_EXTENSION)
    else:
      return self.context.file_name().replace(self.SOURCE_EXTENSION, self.SPEC_EXTENSION)
