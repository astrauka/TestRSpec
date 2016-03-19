from plugin_helpers.utils import memoize

class Output(object):
  class Levels:
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"

  PANEL_NAME = "exec" # must be same as sublime command exec output panel name

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
