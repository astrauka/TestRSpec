import sublime_plugin, sys, os.path, imp

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path += [BASE_PATH]

# Make sure all dependencies are reloaded
if 'plugin_helpers.reloader' in sys.modules:
  imp.reload(sys.modules['plugin_helpers.reloader'])
import plugin_helpers.reloader

from rspec.execute_spec import ExecuteSpec
from rspec.task_context import TaskContext
from rspec.switch_between_code_and_test import SwitchBetweenCodeAndTest

class TestCurrentLineCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    print("Preparing to run rspec")
    context = TaskContext(self, edit)
    ExecuteSpec(context).current_line()

class TestCurrentFileCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    print("Preparing to run rspec")
    context = TaskContext(self, edit)
    ExecuteSpec(context).current_line() # TODO RUN FILE

class RunLastSpecCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    print("Preparing to run last rspec command")
    context = TaskContext(self, edit)
    ExecuteSpec(context).last_run()

class DisplayOutputPanelCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    print("Preparing to display output panel")
    context = TaskContext(self, edit)
    context.display_output_panel()

class SwitchBetweenCodeAndTestCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    print("Preparing to swith between code and test")
    context = TaskContext(self, edit)
    SwitchBetweenCodeAndTest(context).run()


  # def run(self, args, split_view):
  #   self.load_config()
  #   possible_alternates = self.file_type().possible_alternate_files()
  #   alternates = self.project_files(lambda file: file in possible_alternates)

  #   for alternate in alternates:
  #     if re.search(self.file_type().parent_dir_name(), alternate):
  #       alternates = [alternate]
  #       break

  #   if alternates:
  #     if split_view:
  #       ShowPanels(self.window()).split()
  #     if len(alternates) == 1:
  #       self.window().open_file(alternates.pop())
  #     else:
  #       callback = functools.partial(self.on_selected, alternates)
  #       self.window().show_quick_panel(alternates, callback)
  #   else:
  #     GenerateTestFile(self.window(), split_view).doIt()

# Execute spec
# /home/user/.rbenv/bin/rbenv  exec  bundle  exec  spring  rspec  spec/models/user_spec.rb:2
# file_path:line
#
# ProjectRoot
#   project root by ../spec
#
# SpecTarget
#   file + line
#
# Rspec
#   EnvironmentVariables
#     take from configuration
#
#   BinRspec || RubyRspec
#
#   BinRspec
#     find /bin/rspec from project root
#     (cd ProjectRoot && ./bin/rspec SpecTarget)
#
#   on ./bin/rspec not found
#     RubyRspec : (Rbenv || Rvm || SystemRuby) + Bundle + Spring + SpecTarget
#       Rbenv on configuration
#         find $HOME/.rbenv/bin/rbenv exec
#
#       Bundle on configuration
#         check if Gemfile is present
#         bundle exec
#
#       Spring on configuration
#         check if Gemfile contains spring
#         spring
#

# Switch between code and spec
# find matches
# on single, go to file
# on multiple, display selection
