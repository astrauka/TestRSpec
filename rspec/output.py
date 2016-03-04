from plugin_helpers.decorators import memoize

class Output(object):
  class Levels:
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"

  PANEL_NAME = "rspec"

  def __init__(self, window, edit):
    self.window = window
    self.edit = edit

  def log(self, message):
    self.panel().insert(self.edit, self.panel().size(), "{0}\n".format(message))

  @memoize
  def panel(self):
    panel = self.window.get_output_panel(Output.PANEL_NAME)
    panel.settings().set("color_scheme", self.color_scheme())
    return panel

  def show_panel(self):
    self.window.run_command("show_panel", {"panel": "output.{0}".format(Output.PANEL_NAME)})

  def color_scheme(self):
    return "Packages/RubyTest/TestConsole.hidden-tmTheme"
