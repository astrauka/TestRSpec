from plugin_helpers.decorators import memoize
from plugin_helpers.project_files import ProjectFiles
from rspec.project_root import ProjectRoot
from rspec.output import Output
import sublime, os

class TaskContext(object):
  PACKAGE_NAME = "SublimeRSpec"
  GEMFILE_NAME = "Gemfile"
  SPEC_FILE_POSTFIX = "_spec.rb"

  def __init__(self, sublime_command, edit, spec_target_is_file=False):
    self.sublime_command = sublime_command
    self.edit = edit
    self.spec_target_is_file = spec_target_is_file

  @memoize
  def view(self):
    return self.sublime_command.view

  @memoize
  def file_name(self):
    return self.view().file_name()

  @memoize
  def file_base_name(self):
    return os.path.basename(self.file_name())

  @memoize
  def file_relative_name(self):
    return os.path.relpath(self.file_name(), self.project_root())

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
    file_relative_name = self.file_relative_name()
    if self.spec_target_is_file:
      return file_relative_name
    else:
      return ":".join([file_relative_name, self.line_number()])

  @memoize
  def project_root(self):
    return ProjectRoot(self.file_name(), self.from_settings("spec_folder")).result()

  def window(self):
    return self.view().window()

  @memoize
  def output_buffer(self):
    return Output(
      self.view().window(),
      self.edit,
      self.from_settings("panel_settings")
    )

  def output_panel(self):
    return self.output_buffer().panel()

  def log(self, message, level=Output.Levels.INFO):
    self.output_buffer().log("{0}: {1}".format(level, message))

  def display_output_panel(self):
    self.output_buffer().show_panel()

  @memoize
  def settings(self):
    return sublime.load_settings("{0}.sublime-settings".format(TaskContext.PACKAGE_NAME))

  def from_settings(self, key, default_value = None):
    return self.settings().get(key, default_value)

  def is_test_file(self):
    return self.file_name().endswith(TaskContext.SPEC_FILE_POSTFIX)

  @memoize
  def which_rspec(self):
    return os.popen("which rspec").read().split('\n')[0]

  @memoize
  def gemfile_path(self):
    path = os.path.join(self.project_root(), TaskContext.GEMFILE_NAME)
    if not os.path.isfile(path): return

    return path

  def project_files(self, file_matcher):
    return ProjectFiles(
      self.project_root(),
      file_matcher,
      self.from_settings("ignored_directories")
    ).filter()
