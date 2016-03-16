import os

class Bundle(object):
  def __init__(self, context):
    self.context = context

  def result(self):
    if not self.context.from_settings("check_for", {}).get("bundler"): return
    if self.gemfile_exists(): return "bundle exec"

  def gemfile_exists(self):
    return self.context.gemfile_path()
