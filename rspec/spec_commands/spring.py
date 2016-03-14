import os

class Spring(object):
  def __init__(self, context):
    self.context = context

  def result(self):
    if not self.context.from_settings("check_for", {}).get("spring"): return None
    if self.spring_included(): return "spring"

  def spring_included(self):
    gemfile_path = self.context.gemfile_path()
    if not gemfile_path: return None

    return open(gemfile_path, 'r').read().find('spring') > 0

