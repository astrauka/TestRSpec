import sys, os.path, imp, sublime, sublime_plugin

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
CODE_DIRS = [
  'plugin_helpers',
  'rspec',
]
sys.path += [BASE_PATH] + [os.path.join(BASE_PATH, f) for f in CODE_DIRS]

# =======
# reload plugin files on change
if 'plugin_helpers.reloader' in sys.modules:
  imp.reload(sys.modules['plugin_helpers.reloader'])
import plugin_helpers.reloader

class ReloadPlugin(sublime_plugin.EventListener):
  PACKAGE_NAME = 'TestRSpec'
  PLUGIN_RELOAD_TIME_MS = 200
  PLUGIN_PYTHON_FILE = os.path.join(PACKAGE_NAME, "test_rspec.py")

  def on_post_save(self, view):
    file_name = view.file_name()
    if not ReloadPlugin.PACKAGE_NAME in file_name: return
    if ReloadPlugin.PLUGIN_PYTHON_FILE in file_name: return

    original_file_name = view.file_name()
    plugin_python_file = os.path.join(sublime.packages_path(), ReloadPlugin.PLUGIN_PYTHON_FILE)
    if not os.path.isfile(plugin_python_file): return

    def _open_original_file():
      view.window().open_file(original_file_name)

    plugin_view = view.window().open_file(plugin_python_file)
    print("save", plugin_view.file_name())
    plugin_view.run_command("save")
    sublime.set_timeout_async(_open_original_file, self.PLUGIN_RELOAD_TIME_MS)

# =======
# Commands
from rspec.rspec_print import rspec_print
from rspec.execute_spec import ExecuteSpec
from rspec.task_context import TaskContext
from rspec.switch_between_code_and_test import SwitchBetweenCodeAndTest
from rspec.create_spec_file import CreateSpecFile

class TestCurrentLineCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    rspec_print("Running rspec")
    context = TaskContext(self, edit)
    ExecuteSpec(context).current()

class TestCurrentFileCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    rspec_print("Running rspec")
    context = TaskContext(self, edit, spec_target_is_file = True)
    ExecuteSpec(context).current()

class RunLastSpecCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    rspec_print("Running last rspec command")
    context = TaskContext(self, edit)
    ExecuteSpec(context).last_run()

class DisplayOutputPanelCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    rspec_print("Displaying output panel")
    context = TaskContext(self, edit)
    context.display_output_panel()

class SwitchBetweenCodeAndTestCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    rspec_print("Switching between code and test")
    context = TaskContext(self, edit)
    SwitchBetweenCodeAndTest(context).run()

class CreateSpecFileCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    rspec_print("Creating sepc file")
    context = TaskContext(self, edit)
    CreateSpecFile(context).run()
