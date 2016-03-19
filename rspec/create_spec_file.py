from plugin_helpers.utils import memoize
from plugin_helpers.open_file import OpenFile
from rspec.files.opposite import OppositeFile
from rspec.files.spec import SpecFile
import os, re, sublime

class CreateSpecFile(object):
  CLASS_DESCRIPTOR = "class"

  def __init__(self, context):
    self.context = context

  def run(self):
    # create file
    #   determine spec file name
    # fill with snippet data
    #   determine class name
    self._create_directories()
    self._write_template()
    self._open()

  def _create_directories(self):
    os.makedirs(os.path.dirname(self._file_name()), exist_ok = True)

  def _write_template(self):
    # if os.path.isfile(self._file_name()): return

    handler = open(self._file_name(), "w+")
    handler.write(self._spec_template())
    handler.close()

  def _open(self):
    OpenFile(self.context.window(), self._file_name()).run()
    self.context.window().active_view().run_command(
      "goto_line",
      { "line": self.context.from_settings("create_spec_cursor_line") }
    )

  @memoize
  def _file_name(self):
    ignored_directory = OppositeFile(self.context).ignored_directories()[1] or ""
    return SpecFile(self.context, ignored_directory).result()

  @memoize
  def _spec_template(self):
    return sublime.expand_variables(
      "\n".join(self.context.from_settings("create_spec_snippet", [""])),
      { "class_name": self._class_name() }
    )

  def _class_name(self):
    body = self.context.view().substr(sublime.Region(0, self.context.view().size()))
    matches = re.findall(self.context.from_settings("create_file_class_name_regexp"), body)
    names = []
    for descriptor, name in matches:
      names.append(name)
      if descriptor == self.CLASS_DESCRIPTOR: break

    return "::".join(names)
