class SaveFiles(object):
  def __init__(self, context):
    self.context = context

  def run(self):
    self._save_current_file_on_run()
    self._save_all_files_on_run()

  def _save_current_file_on_run(self):
    if self.context.from_settings("save_current_file_on_run"):
      self.context.window().run_command("save")

  def _save_all_files_on_run(self):
    if self.context.from_settings("save_all_files_on_run"):
      self.context.window().run_command("save_all")

