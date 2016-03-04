from plugin_helpers.decorators import memoize
from rspec.project_root import ProjectRoot
from rspec.output import Output

class TaskContext(object):
  SPEC_FILE_POSTFIX = "_spec.rb"

  def __init__(self, sublime, edit):
    self.sublime = sublime
    self.edit = edit

  @memoize
  def view(self):
    return self.sublime.view

  @memoize
  def file_name(self):
    return self.view().file_name()

  # from https://github.com/theskyliner/CopyFilepathWithLineNumbers/blob/master/CopyFilepathWithLineNumbers.py
  @memoize
  def line_number(self):
    (rowStart, colStart) = self.view().rowcol(self.view().sel()[0].begin())
    (rowEnd, colEnd)     = self.view().rowcol(self.view().sel()[0].end())
    lines = (str) (rowStart + 1)

    if rowStart != rowEnd:
        #multiple selection
        lines += "-" + (str) (rowEnd + 1)

    return lines

  @memoize
  def spec_target(self):
    return "{0}:{1}".format(self.file_name(), self.line_number())

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
    return self.file_name().endswith(TaskContext.SPEC_FILE_POSTFIX)
