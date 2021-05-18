import sublime

from ..plugin_helpers.utils import memoize


class Output:
    class Levels:
        ERROR = "ERROR"
        WARNING = "WARNING"
        INFO = "INFO"

    PANEL_NAME = "exec"  # must be same as sublime command exec output panel name

    DEFAULT_SYNTAX = "Packages/TestRSpec/themes/RSpecConsole.sublime-syntax"
    PLAIN_TEXT_SYNTAX = "Packages/Text/Plain text.tmLanguage"

    @classmethod
    def destroy(cls):
        for window in sublime.windows():
            cls.destroy_window_panels(window)

    @classmethod
    def destroy_window_panels(cls, window):
        panel = window.find_output_panel(cls.PANEL_NAME)
        if not panel:
            return
        if panel.settings().get("syntax") != cls.DEFAULT_SYNTAX:
            return

        panel.settings().set("syntax", cls.PLAIN_TEXT_SYNTAX)
        window.destroy_output_panel(cls.PANEL_NAME)

    def __init__(self, window, edit, panel_settings={}):
        self.window = window
        self.edit = edit
        self.panel_settings = panel_settings

    def log(self, message):
        self.panel().insert(self.edit, self.panel().size(), "{0}\n".format(message))

    @memoize
    def panel(self):
        panel = self.window.get_output_panel(Output.PANEL_NAME)
        for key, value in self.panel_settings.items():
            panel.settings().set(key, value)

        return panel

    @memoize
    def panel_name(self):
        return "output.{0}".format(Output.PANEL_NAME)

    def show_panel(self):
        self.window.run_command("show_panel", {"panel": self.panel_name()})
