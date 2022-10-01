import os

from .opposite import OppositeFile
from ...plugin_helpers.utils import memoize


class SpecFile:
    def __init__(self, context, ignored_directory):
        self.context = context
        self.ignored_directory = ignored_directory

    def result(self):
        if not self._relative_name().startswith(self.ignored_directory):
            return

        spec_name = self.spec_name()
        if os.path.isfile(spec_name):
            return spec_name

    def spec_name(self):
        return os.path.join(
            self.context.package_root(),
            self.context.from_settings("spec_folder"),
            self._name_without_ignored_directory(),
        )

    def _name_without_ignored_directory(self):
        return self._relative_name().replace(self.ignored_directory, "", 1)

    @memoize
    def _relative_name(self):
        return OppositeFile(self.context).relative_name()
