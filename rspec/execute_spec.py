from plugin_helpers.decorators import memoize
from rspec.output import Output

class ExecuteSpec(object):
  def __init__(self, context):
    self.context = context
    self.run()

  def run(self):
    if not self.context.project_root(): return self.notify_missing_project_root()
    if not self.context.is_test_file(): return self.notify_not_test_file()

    self.context.log("Project root {0}".format(self.context.project_root()))
    self.context.log("Spec target {0}".format(self.context.spec_target()))
    self.context.display_output_panel()

  def notify_missing_project_root(self):
    self.context.log(
      "Could not find 'spec/' folder traversing back from {0}".format(self.context.file_name()),
      level=Output.Levels.ERROR
    )
    self.context.display_output_panel()

  def notify_not_test_file(self):
    self.context.log(
      "Trying to test not a test file: {0}".format(self.context.file_name()),
      level=Output.Levels.ERROR
    )
    self.context.display_output_panel()
