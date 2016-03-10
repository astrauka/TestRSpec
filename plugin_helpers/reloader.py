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
  'rspec.spec_command',
  'rspec.spec_commands.bin_rspec',
  'rspec.spec_commands.ruby_rspec',
  'rspec.spec_commands.bundle',
  'rspec.spec_commands.rbenv',
  'rspec.spec_commands.rvm',
  'rspec.spec_commands.spring',
  'rspec.spec_commands.system_ruby',
]
sys_modules = sys.modules
modules_to_reload = [sys_modules.get(module) for module in modules if sys_modules.get(module)]
# print([module.__name__ for module in modules_to_reload])

for module in modules_to_reload:
  if 'on_module_reload' in module.__dict__:
    module.on_module_reload()
  imp.reload(module)
