import os

class Zeus(object):
  def __init__(self, context):
    self.context = context

  def result(self):
    if not self.context.from_settings("use_zeus"): return
    return "zeus"
