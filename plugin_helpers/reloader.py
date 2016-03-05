import sys, imp

# Dependecy reloader
# The original idea is borrowed from
# https://github.com/wbond/sublime_package_control/blob/master/package_control/reloader.py

print('Reloading rspec modules')

modules = [
  'plugin_helpers.decorators',
  'rspec.output',
  'rspec.project_root',
  'rspec.task_context',
  'rspec.execute_spec',
]
sys_modules = sys.modules
modules_to_reload = [sys_modules.get(module) for module in modules if sys_modules.get(module)]

for module in modules_to_reload:
  if 'on_module_reload' in module.__dict__:
    module.on_module_reload()
  imp.reload(module)
