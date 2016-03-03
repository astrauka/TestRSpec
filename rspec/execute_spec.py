from decorators import memoize

class ExecuteSpec(object):
  def __init__(self, context):
    self.context = context
    self.run()

  def run(self):
    if not self.context.project_root(): return self.notify_missing_project_root()
    if not self.context.is_test_file(): return self.notify_not_test_file()

    self.context.log("Project root: {0}".format(self.context.project_root()))
    self.context.display_output_panel()

  def notify_missing_project_root(self):
    self.context.log(
      "Could not find 'spec/' folder traversing back from {0}".format(self.file_name()),
      level=Output.Levels.ERROR
    )
    self.context.display_output_panel()

  def notify_not_test_file(self):
    self.context.log(
      "Trying to test not a test file: {0}".format(self.file_name()),
      level=Output.Levels.ERROR
    )
    self.context.display_output_panel()

