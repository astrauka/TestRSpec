import os
from plugin_helpers.decorators import memoize

class Bundle(object):
  def __init__(self, context):
    self.context = context

  def result(self):
    return None
