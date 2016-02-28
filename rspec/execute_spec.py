from decorators import memoize
from output import Output
from project_root import ProjectRoot

class ExecuteSpec(object):
  def __init__(self, sublime, edit):
    self.sublime = sublime
    self.edit = edit
    self.view = sublime.view
    self.run()

  def run(self):
    if not self.project_root(): return self.notify_missing_project_root()

    self.log(
      Output.Levels.INFO,
      "Project root: {0}".format(self.project_root())
    )
    self.display_output_panel()

  @memoize
  def project_root(self):
    return ProjectRoot(self.file_name()).result()

  def notify_missing_project_root(self):
    self.log(
      Output.Levels.ERROR,
      "Could not find 'spec/' folder traversing back from {0}".format(self.file_name())
    )
    self.display_output_panel()

  def notify_not_test_file(self):
    self.log(
      Output.Levels.ERROR,
      "Trying to test not a test file: {0}".format(self.file_name())
    )
    self.display_output_panel()

  @memoize
  def file_name(self):
    return self.view.file_name()

  def log(self, level, message):
    self.output_buffer().log("{0}: {1}".format(level, message))

  def display_output_panel(self):
    self.output_buffer().show_panel()

  @memoize
  def output_buffer(self):
    return Output(self.view.window(), self.edit)
