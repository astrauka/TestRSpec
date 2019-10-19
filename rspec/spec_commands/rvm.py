import os
from plugin_helpers.utils import memoize


class Rvm(object):
    def __init__(self, context):
        self.context = context

    def result(self):
        if not self.context.from_settings("check_for_rvm"):
            return
        if self._from_settings():
            return "{0} -S".format(self._from_settings())

    @memoize
    def _from_settings(self):
        file = os.path.expanduser(self.context.from_settings("paths_rvm"))
        if file and os.path.isfile(file):
            return file
