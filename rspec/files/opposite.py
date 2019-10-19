from plugin_helpers.utils import rreplace
import os


class OppositeFile(object):
    def __init__(self, context):
        self.context = context

    def relative_name(self):
        return self.opposite(self.context.file_relative_name())

    def base_name(self):
        return self.opposite(self.context.file_base_name())

    def opposite(self, name):
        if self.context.is_test_file():
            return rreplace(name, self._spec_extension(), self._source_extension(), 1)
        else:
            return rreplace(name, self._source_extension(), self._spec_extension(), 1)

    def _spec_extension(self):
        return self.context.from_settings("spec_file_extension")

    def _source_extension(self):
        return self.context.from_settings("source_file_extension")

    def ignored_directories(self):
        directories = (
            self.context.from_settings("ignored_spec_path_building_directories") or []
        )
        return self._direct_match() + [directory + os.sep for directory in directories]

    def _direct_match(self):
        return [""]
