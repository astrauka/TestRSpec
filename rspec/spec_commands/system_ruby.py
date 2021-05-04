import os
from ...plugin_helpers.utils import memoize


class SystemRuby(object):
    def __init__(self, context):
        self.context = context

    def result(self):
        if not self.context.from_settings("check_for_system_ruby"):
            return
        if self._from_settings():
            return "{0} -S".format(self._from_settings())

    @memoize
    def _from_settings(self):
        command = os.path.expanduser(self.context.from_settings("paths_system_ruby"))
        if not command:
            return

        file = command.split()[0]
        if os.path.isfile(file):
            return command
