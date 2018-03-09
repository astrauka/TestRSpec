from plugin_helpers.utils import memoize
from rspec.output import Output
from rspec.spec_command import SpecCommand
from rspec.last_run import LastRun
from rspec.files.save import SaveFiles

class ExecuteSpec(object):
  def __init__(self, context):
    self.context = context

  def current(self):
    self._validate_can_run_spec()
    self._prepare_output_panel()
    self._execute(self._command_hash())

  def last_run(self):
    self._execute(LastRun.command_hash())

  def _validate_can_run_spec(self):
    if not self.context.project_root(): return self._notify_missing_project_root()
    if not self.context.is_test_file(): return self._notify_not_test_file()

  def _prepare_output_panel(self):
    self.context.log("Error occurred, see more in 'View -> Show Console'")
    self.context.log("Project root {0}".format(self.context.project_root()))
    self.context.log("Spec target {0}".format(self.context.spec_target()))
    self.context.display_output_panel()

  def _execute(self, command_hash):
    self._before_execute()
    self.context.log("Executing {0}\n".format(command_hash.get("shell_cmd")))
    self.context.window().run_command(self.context.from_settings("target"), command_hash)
    LastRun.save(command_hash)

  def _before_execute(self):
    SaveFiles(self.context).run()

  def _notify_missing_project_root(self):
    self.context.log(
      "Could not find '{0}/' folder traversing back from {1}".format(
        self.context.from_settings("spec_folder"),
        self.context.file_name()
      ),
      level=Output.Levels.ERROR
    )
    self.context.display_output_panel()

  def _notify_not_test_file(self):
    self.context.log(
      "Trying to test not a test file: {0}".format(self.context.file_name()),
      level=Output.Levels.ERROR
    )
    self.context.display_output_panel()

  @memoize
  def _command_hash(self):
    add_to_path = self.context.from_settings("rspec_add_to_path", "")
    append_path = "export PATH={0}:$PATH;".format(add_to_path) if add_to_path else ""

    command = "({append_path} cd '{project_root}' && {rspec_command} {target})".format(
      append_path = append_path,
      project_root = self.context.project_root(),
      rspec_command = SpecCommand(self.context).result(),
      target = self.context.spec_target()
    )
    pannel_settings = self.context.from_settings("panel_settings", {})
    env = self.context.from_settings("env", {})

    return {
      "shell_cmd": command,
      "working_dir": self.context.project_root(),
      "env": env,
      "file_regex": r"([^ ]*\.rb):?(\d*)",
      "syntax": pannel_settings.get("syntax"),
      "encoding": pannel_settings.get("encoding", "utf-8")
    }
