import os
import sublime

from ..plugin_helpers.utils import memoize
from ..plugin_helpers.project_files import ProjectFiles
from .project_root import ProjectRoot
from .output import Output
from .rspec_print import rspec_print


class TaskContext:
    GEMFILE_NAME = "Gemfile"
    LOG_LEVELS = [Output.Levels.ERROR, Output.Levels.WARNING, Output.Levels.INFO]

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

    @memoize
    def spec_file_extension(self):
        return self.from_settings("spec_file_extension")

    # from https://github.com/theskyliner/CopyFilepathWithLineNumbers/blob/master/CopyFilepathWithLineNumbers.py
    @memoize
    def line_number(self):
        (rowStart, colStart) = self.view().rowcol(self.view().sel()[0].begin())
        (rowEnd, colEnd) = self.view().rowcol(self.view().sel()[0].end())
        lines = (str)(rowStart + 1)

        if rowStart != rowEnd:
            # multiple selection
            lines += "-" + (str)(rowEnd + 1)

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
            self.view().window(), self.edit, self.from_settings("panel_settings")
        )

    def output_panel(self):
        return self.output_buffer().panel()

    def log(self, message, level=Output.Levels.INFO):
        if not self._can_log(level):
            return

        formatted_message = "{0}: {1}".format(level, message)
        if self.from_settings("log_to_console"):
            rspec_print(formatted_message)
        else:
            self.output_buffer().log(formatted_message)

    def display_output_panel(self):
        self.output_buffer().show_panel()

    @memoize
    def _settings(self):
        return sublime.load_settings("TestRSpec.sublime-settings")

    def from_settings(self, key, default_value=None):
        return self._settings().get(key, default_value)

    def is_test_file(self):
        return self.file_name().endswith(self.spec_file_extension())

    @memoize
    def gemfile_path(self):
        path = os.path.join(self.project_root(), TaskContext.GEMFILE_NAME)
        if not os.path.isfile(path):
            return

        return path

    def project_files(self, file_matcher):
        return ProjectFiles(
            self.project_root(), file_matcher, self.from_settings("ignored_directories")
        ).filter()

    def _get_log_level(self, log_level, default=0):
        try:
            return self.LOG_LEVELS.index(str(log_level).upper())
        except ValueError:
            rspec_print("Invalid log level: {0}".format(log_level))
            return default

    def _can_log(self, log_level):
        return self._get_log_level(log_level, 0) <= self._get_log_level(self.from_settings("log_level", 2))
