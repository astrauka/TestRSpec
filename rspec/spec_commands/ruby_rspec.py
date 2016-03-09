class RubyRspec(object):
  def __init__(self, context):
    self.context = context

  def result(self):
    if not self.context: return
