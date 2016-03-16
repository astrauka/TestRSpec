# Sublime RSpec

THIS IS WIP, please do not use it!!!

RSpec plugin for Sublime Text 3

# Output

Executed using sublime build tools `exec` command.

When preconditions are not satisfied outputs to panel.

# Spec command generation

```
# output example
# /home/user/.rbenv/bin/rbenv exec bundle exec spring rspec /home/user/dev/project/spec/models/user_spec.rb:2
#
# ProjectRoot
#   project root by ../spec
#
# SpecTarget
#   file + line
#
# Rspec
#   Environment variables
#     take from configuration
#
#   (BinRspec || RubyRspec) + SpecTarget
#
#   BinRspec
#     find /bin/rspec from project root
#
#   on ./bin/rspec not found
#     RubyRspec : (Rbenv || Rvm || SystemRuby) + Bundle + Spring
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
```

# TODO

* last run X
* show test panel X
* go to file X
* go to spec X
* spec file
* save_all
* create spec file
* shortcuts/hotkeys, commands X
* readme
  * description
  * screenshots
  * usage
  * shortcuts
* configuration

# Thanks to

Inspired by https://github.com/maltize/sublime-text-2-ruby-tests

Parts that are taken:
* test console theme
* key bindings
