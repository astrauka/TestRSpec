from rspec.spec_commands.bundle import Bundle
from rspec.spec_commands.spring import Spring
from rspec.spec_commands.rbenv import Rbenv
from rspec.spec_commands.rvm import Rvm
from rspec.spec_commands.system_ruby import SystemRuby


class RubyRspec(object):
    def __init__(self, context):
        self.context = context

    def result(self):
        if not self.context:
            return

        return " ".join(
            filter(
                None,
                [
                    self._ruby(),
                    Bundle(self.context).result(),
                    Spring(self.context).result(),
                    self.context.from_settings("rspec_command"),
                ],
            )
        )

    def _ruby(self):
        return (
            Rbenv(self.context).result()
            or Rvm(self.context).result()
            or SystemRuby(self.context).result()
        )
