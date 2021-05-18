import os
from ...plugin_helpers.utils import memoize


class BinRspec:
    def __init__(self, context):
        self.context = context

    def result(self):
        if not self._file_exists():
            return

        return self._bin_path()

    def _file_exists(self):
        if not self._bin_url():
            return

        return os.path.exists(self._bin_url())

    @memoize
    def _bin_path(self):
        return self.context.from_settings("paths_bin_rspec")

    @memoize
    def _bin_url(self):
        if not self._bin_path():
            return
        if self._is_full_path():
            return self._bin_path()

        return os.path.join(self.context.project_root(), self._bin_path())

    def _is_full_path(self):
        return not self._bin_path().startswith("./")
