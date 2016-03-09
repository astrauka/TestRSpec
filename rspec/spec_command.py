from rspec.spec_commands.bin_rspec import BinRspec
from rspec.spec_commands.ruby_rspec import RubyRspec

class SpecCommand(object):
  def __init__(self, context):
    self.context = context

  def result(self):
    if not self.context: return

    return BinRspec(self.context).result() or RubyRspec(self.context).result()
