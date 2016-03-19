from plugin_helpers.utils import memoize, unique
from plugin_helpers.open_file import OpenFile
from rspec.output import Output
from rspec.files.opposite import OppositeFile
from rspec.files.spec import SpecFile
from rspec.files.source import SourceFile
from rspec.rspec_print import rspec_print
import os

class SwitchBetweenCodeAndTest(object):
  def __init__(self, context):
    self.context = context

  def run(self):
    # prioritize matches by path
    files = unique(self._files_by_path() + self._files_by_name())
    if files:
      OpenFile(self.context.window(), files).run()
    else:
      rspec_print("No files found, searched for {0}".format(self._file_base_name()))

  def _files_by_path(self):
    if self._searching_for_spec_file():
      return self._ignoring_spec_path_building_directories()
    else:
      return self._appending_spec_path_building_directories()

  def _ignoring_spec_path_building_directories(self):
    # by spec/rel_path
    # by spec/rel_path-ignored_dir
    ignored_directories = OppositeFile(self.context).ignored_directories()
    files = [SpecFile(self.context, directory).result() for directory in ignored_directories]
    return list(filter(None, files))

  def _appending_spec_path_building_directories(self):
    # by rel_path-spec
    # by rel_path-spec+ignored_dir
    appended_directories = OppositeFile(self.context).ignored_directories()
    files = [SourceFile(self.context, directory).result() for directory in appended_directories]
    return list(filter(None, files))

  def _files_by_name(self):
    file_matcher = lambda file: file == self._file_base_name()
    return self.context.project_files(file_matcher)

  @memoize
  def _file_base_name(self):
    return OppositeFile(self.context).base_name()

  def _searching_for_spec_file(self):
    return not self.context.is_test_file()
