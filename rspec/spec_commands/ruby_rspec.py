from .bundle import Bundle
from .spring import Spring
from .rbenv import Rbenv
from .rvm import Rvm
from .system_ruby import SystemRuby


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
