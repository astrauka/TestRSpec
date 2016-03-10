from plugin_helpers.decorators import memoize
from rspec.output import Output
from rspec.spec_command import SpecCommand

class ExecuteSpec(object):
  def __init__(self, context):
    self.context = context
    self.run()

  def run(self):
    if not self.context.project_root(): return self.notify_missing_project_root()
    if not self.context.is_test_file(): return self.notify_not_test_file()

    self.context.log("Error occurred, see more in 'View -> Show Console")
    self.context.log("Project root {0}".format(self.context.project_root()))
    self.context.log("Spec target {0}".format(self.context.spec_target()))
    self.context.display_output_panel()
    self.execute_spec()

  def notify_missing_project_root(self):
    self.context.log(
      "Could not find 'spec/' folder traversing back from {0}".format(self.context.file_name()),
      level=Output.Levels.ERROR
    )
    self.context.display_output_panel()

  def notify_not_test_file(self):
    self.context.log(
      "Trying to test not a test file: {0}".format(self.context.file_name()),
      level=Output.Levels.ERROR
    )
    self.context.display_output_panel()

  def execute_spec(self):
    command = ' '.join([SpecCommand(self.context).result(), self.context.spec_target()])
    pannel_settings = self.context.from_settings("panel_settings", {})
    env = self.context.from_settings("env", {})

    self.context.log("Executing {0}\n".format(command))
    self.context.window().run_command(
      "exec", {
        "shell_cmd": command,
        "working_dir": self.context.project_root(),
        "env": env,
        "file_regex": r"([^ ]*\.rb):?(\d*)",
        "syntax": pannel_settings.get("syntax"),
        "encoding": pannel_settings.get("encoding", "utf-8")
      }
    )
