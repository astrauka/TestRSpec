import os
from plugin_helpers.decorators import memoize

class SystemRuby(object):
  def __init__(self, context):
    self.context = context

  def result(self):
    return None
