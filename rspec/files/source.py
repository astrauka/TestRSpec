import os

from plugin_helpers.utils import memoize
from rspec.files.opposite import OppositeFile


class SourceFile(object):
    def __init__(self, context, append_directory):
        self.context = context
        self.append_directory = append_directory

    def result(self):
        source_name = self._source_name()
        if os.path.isfile(source_name):
            return source_name

    def _source_name(self):
        return os.path.join(
            self.context.project_root(),
            self.append_directory,
            self._name_without_spec_directory(),
        )

    def _name_without_spec_directory(self):
        return self._relative_name().replace(
            self.context.from_settings("spec_folder") + os.sep, "", 1
        )

    @memoize
    def _relative_name(self):
        return OppositeFile(self.context).relative_name()
