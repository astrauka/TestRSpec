# Sublime TestRSpec

RSpec plugin for Sublime Text 3.

Run, navigate and create specs from Sublime Text.

![Features](recordings/features.gif)

## Installation

Using [Package Control](http://wbond.net/sublime_packages/package_control):

1. Run “Package Control: Install Package” command, find and install `TestRspec`.
2. Define key bindings (see Configuration section below).
3. Restart Sublime Text.

Manually:

1. Clone this repository into your packages folder (in Sublime Text: Preferences -> Browse Packages).
2. Define key bindings (see Configuration section below).
3. Restart Sublime Text.

## Configuration

TestRSpec tries its best to autodetect how to run RSpec. However, you might need to make adjustments to plugin's
configuration if you have an uncommon setup.

There are no key bindings enabled by default. Go to Preferences -> Package Settings -> TestRSpec -> Key Bindings to define key bindings.

Find settings in Preferences -> Package Settings -> TestRSpec.

[Default settings](https://github.com/astrauka/TestRSpec/blob/master/TestRSpec.sublime-settings)

## Features

### Run RSpec

Launch RSpec for:

* Current file
* Current line
* Rerun last run spec

### Switch between code and spec

Jumps from code to spec and vice versa. If there multiple matches, it shows a list with matches.

### Create a spec file

Creates a spec file when run in a source file.

Uses code snippet defined in settings (`create_spec_snippet`).

### Copy last ran RSpec command

Copies the command of the last run spec.
It can be useful e.g. when you want to debug your application within a 'real' terminal.

## Tips

### Hide inline errors

By default, inline error messages will be displayed whenever a spec fails. Set `show_errors_inline` to false in global
settings to prevent this.

### Ignore binding.pry when running specs

Sublime does not allow input in the output panel, so if you add `binding.pry`, tests get stuck
waiting on input.

To work around this, you can disable the debugger by modifying TestRSpec configuration:

```json
{
  "env": {
    "DISABLE_PRY": "true"
  }
}
```

Alternatively, use [pry-remote](https://github.com/Mon-Ouie/pry-remote).

## Troubleshooting

### Ruby not found or wrong ruby version used

Example error:

```
/usr/bin/env: ruby: No such file or directory
```

Override `PATH` variable in your shell configuration (`~/.bashrc` or `~/.bash_profile`).
Make sure `ruby` command runs the right Ruby version in `bash`.

Alternatively, update package settings with path to ruby, e.g.:

```json
{
  "rspec_add_to_path": "$HOME/.rbenv/shims"
}
```

### Spring is not used

Make sure you have both `spring` and `spring-commands-rspec` in your Gemfile.

If you use binstubs, you also need to run

```bash
bundle exec spring binstub rspec
```

## Acknowledgments

Inspired by and uses code from https://github.com/maltize/sublime-text-2-ruby-tests

## Contribution

Help is always welcome. Create an issue if you need help.

## Copyright and license

Copyright © 2016 [@astrauka](https://twitter.com/astrauka)

Licensed under the [**MIT**](https://mit-license.org/) license.
