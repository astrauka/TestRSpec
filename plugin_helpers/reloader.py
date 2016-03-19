import sys, imp, os, sublime, sublime_plugin
from rspec.rspec_print import rspec_print

# Dependecy reloader
# The original idea is borrowed from
# https://github.com/wbond/sublime_package_control/blob/master/package_control/reloader.py

rspec_print('Reloading rspec modules')
CODE_DIRS = [
  'plugin_helpers',
  'rspec',
]
PYTHON_FILE_EXT = '.py'

def _reload(dir, file):
  (name, extension) = os.path.splitext(file)
  if not extension == PYTHON_FILE_EXT: return

  dirs = '.'.join(filter(None, os.path.split(dir)))
  module = sys.modules.get('.'.join([dirs, name]))
  if not module: return

  if 'on_module_reload' in module.__dict__:
    module.on_module_reload()
  imp.reload(module)

for _ in range(2): # double reload required to update dependencies
  for directory in CODE_DIRS:
    for dir, _, files in os.walk(directory):
      for file in files:
        _reload(dir, file)

class ReloadPlugin(sublime_plugin.EventListener):
  PLUGIN_RELOAD_TIME_MS = 200

  def on_post_save(self, view):
    plugin_python_file = sys._current_frames().values()[0].f_back.f_globals['__file__']
    file_name = view.file_name()
    if not os.path.dirname(plugin_python_file) in file_name: return
    if file_name == plugin_python_file: return

    original_file_name = view.file_name()

    def _open_original_file():
      view.window().open_file(original_file_name)

    plugin_view = view.window().open_file(plugin_python_file)
    print("save", plugin_view.file_name())
    plugin_view.run_command("save")
    sublime.set_timeout_async(_open_original_file, self.PLUGIN_RELOAD_TIME_MS)
