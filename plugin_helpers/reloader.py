import sys, imp, os
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
