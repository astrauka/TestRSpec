import os
import re
import sublime

from ..plugin_helpers.utils import memoize
from ..plugin_helpers.open_file import OpenFile
from .files.opposite import OppositeFile


class CreateSpecFile:
    CLASS_DESCRIPTOR = "class"

    def __init__(self, context):
        self.context = context

    def run(self):
        if self.context.is_test_file():
            return

        self._create_directories()
        self._write_template()
        self._open()

    def _create_directories(self):
        os.makedirs(os.path.dirname(self._file_name()), exist_ok=True)

    def _write_template(self):
        if os.path.isfile(self._file_name()):
            return

        handler = open(self._file_name(), "w+")
        handler.write(self._spec_template())
        handler.close()

    def _open(self):
        OpenFile(
            self.context.window(),
            "{}:{}".format(self._file_name(), self._create_spec_cursor_line()),
        ).run()

    @memoize
    def _file_name(self):
        relative_name = os.path.join(
            self._spec_folder(), OppositeFile(self.context).relative_name()
        )
        for ignored_directory in OppositeFile(self.context).ignored_directories():
            relative_name = self._spec_name_with_ignore(
                ignored_directory, relative_name
            )

        return os.path.join(self.context.project_root(), relative_name)

    def _spec_name_with_ignore(self, ignored_directory, relative_name):
        ignore = os.path.join(self._spec_folder(), ignored_directory)
        if ignore in relative_name:
            return os.path.join(
                self._spec_folder(), relative_name.replace(ignore, "", 1)
            )
        else:
            return relative_name

    @memoize
    def _spec_folder(self):
        return self.context.from_settings("spec_folder")

    @memoize
    def _create_spec_cursor_line(self):
        return self.context.from_settings("create_spec_cursor_line")

    @memoize
    def _spec_template(self):
        return sublime.expand_variables(
            "\n".join(self.context.from_settings("create_spec_snippet", [""])),
            {"class_name": self._class_name()},
        )

    def _class_name(self):
        body = self.context.view().substr(sublime.Region(0, self.context.view().size()))
        matches = re.findall(
            self.context.from_settings("create_spec_class_name_regexp"), body
        )
        names = []
        for descriptor, name in matches:
            names.append(name)
            if self._ignore_nested_classes() and descriptor == self.CLASS_DESCRIPTOR:
                break

        return "::".join(names)
    
    @memoize
    def _ignore_nested_classes(self):
        return self.context.from_settings("ignore_nested_classes")
