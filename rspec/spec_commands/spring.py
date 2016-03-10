import os
from plugin_helpers.decorators import memoize

class Spring(object):
  def __init__(self, context):
    self.context = context

  def result(self):
    return None
