from decorators import memoize
from project_root import ProjectRoot
from output import Output

class Context(object):
  SPEC_FILE_POSTFIX = "_spec.rb"

  def __init__(self, sublime, edit):
    self.sublime = sublime
    self.edit = edit

  @memoize
  def view(self):
    return sublime.view

  @memoize
  def file_name(self):
    return self.view().file_name()

  @memoize
  def project_root(self):
    return ProjectRoot(self.file_name()).result()

  @memoize
  def output_buffer(self):
    return Output(self.view().window(), self.edit)

  def log(self, message, level=Output.Levels.INFO):
    self.output_buffer().log("{0}: {1}".format(level, message))

  def display_output_panel(self):
    self.output_buffer().show_panel()

  def is_test_file(self):
    return self.file_name().endswith(SPEC_FILE_POSTFIX)
