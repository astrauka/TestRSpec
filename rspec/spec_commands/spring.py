import os


class Spring:
    def __init__(self, context):
        self.context = context

    def result(self):
        if not self.context.from_settings("check_for_spring"):
            return
        if self.spring_included():
            return "spring"

    def spring_included(self):
        gemfile_path = self.context.gemfile_path()
        if not gemfile_path:
            return

        with open(gemfile_path, "r") as f:
            return f.read().find("spring-commands-rspec") > 0
