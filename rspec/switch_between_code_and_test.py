from plugin_helpers.utils import memoize, unique
from rspec.output import Output
from plugin_helpers.open_file import OpenFile
from rspec.rspec_print import rspec_print
import os

class SwitchBetweenCodeAndTest(object):
  SPEC_EXTENSION = "_spec.rb"
  SOURCE_EXTENSION = ".rb"

  def __init__(self, context):
    self.context = context

  def run(self):
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
    ignored_directories = self._ignored_directories() + self._direct_match()
    files = [self._file_ignoring_directory(directory) for directory in ignored_directories]
    return list(filter(None, files))

  def _file_ignoring_directory(self, directory):
    if not self._file_relative_name().startswith(directory): return

    spec_file = self._spec_file(directory)
    if os.path.isfile(spec_file): return spec_file

  def _spec_file(self, ignored_directory):
    return os.path.join(
      self.context.project_root(),
      self.context.from_settings("spec_folder"),
      self._file_relative_name().replace(ignored_directory, '', 1)
    )

  def _appending_spec_path_building_directories(self):
    # by rel_path-spec
    # by rel_path-spec+ignored_dir
    appended_directories = self._ignored_directories() + self._direct_match()
    files = [self._file_appending_directory(directory) for directory in appended_directories]
    return list(filter(None, files))

  def _file_appending_directory(self, directory):
    source_file = self._source_file(directory)
    if os.path.isfile(source_file): return source_file

  def _source_file(self, append_directory):
    return os.path.join(
      self.context.project_root(),
      append_directory,
      self._file_relative_name().replace(self.context.from_settings("spec_folder") + os.sep, '', 1),
    )

  @memoize
  def _file_relative_name(self):
    return self.context.file_relative_name().replace(
      self.context.file_base_name(), self._file_base_name()
    )

  @memoize
  def _file_base_name(self):
    name = self.context.file_base_name()

    if self._searching_for_spec_file():
      return name.replace(self.SOURCE_EXTENSION, self.SPEC_EXTENSION, 1)
    else:
      return name.replace(self.SPEC_EXTENSION, self.SOURCE_EXTENSION, 1)

  def _files_by_name(self):
    file_matcher = lambda file: file.endswith(self._file_base_name())
    return self.context.project_files(file_matcher)

  def _searching_for_spec_file(self):
    return not self.context.is_test_file()

  @memoize
  def _ignored_directories(self):
    directories = self.context.from_settings("ignored_spec_path_building_directories") or []
    return [directory + os.sep for directory in directories]

  def _direct_match(self):
    return ['']
