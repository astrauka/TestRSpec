import sublime

from rspec.last_run import LastRun
from rspec.rspec_print import rspec_print


class LastCopy(object):
    @classmethod
    def run(klass):
        command = LastRun.command_hash().get("shell_cmd")
        sublime.set_clipboard(command)
        rspec_print("Copied to clipboard: {0}".format(command))
        sublime.active_window().status_message(
            "TestRspec: Copied last spec command to clipboard"
        )
