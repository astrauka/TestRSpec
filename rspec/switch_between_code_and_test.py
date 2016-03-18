from plugin_helpers.decorators import memoize
from rspec.output import Output
from plugin_helpers.open_file import OpenFile
import os

class SwitchBetweenCodeAndTest(object):
  SPEC_EXTENSION = "_spec.rb"
  SOURCE_EXTENSION = ".rb"

  def __init__(self, context):
    self.context = context

  def run(self):
    files = self._files_by_path() or self._files_by_name()
    if files:
      OpenFile(self.context.window(), files).run()
    else:
      print("SublimeRSpec: No files found, searched for {0}".format(self._file_base_name()))

  def _files_by_path(self):
    if self._searching_for_spec_file():
      return self._ignoring_spec_path_building_directories()
    else:
      return self._appending_spec_path_building_directories()

  def _ignoring_spec_path_building_directories(self):
    # by spec/rel_path
    # by spec/rel_path-ignored_dir
    relative_name = self._file_relative_name()
    ignored_directories = self._ignored_directories() or []
    ignored_directories.insert(0, '') # no ignores

    for ignored_directory in ignored_directories:
      if not relative_name.startswith(ignored_directory): next
      name = relative_name.replace(ignored_directory + os.sep, '', 1)
      file = os.path.join(
        self.context.project_root(),
        self.context.from_settings("spec_folder"),
        name
      )
      if os.path.isfile(file): return file

  def _appending_spec_path_building_directories(self):
    return

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
    return self.context.from_settings("ignored_spec_path_building_directories")
