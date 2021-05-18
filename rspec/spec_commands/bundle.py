import os


class Bundle:
    def __init__(self, context):
        self.context = context

    def result(self):
        if not self.context.from_settings("check_for_bundler"):
            return
        if self.gemfile_exists():
            return "bundle exec"

    def gemfile_exists(self):
        return self.context.gemfile_path()
