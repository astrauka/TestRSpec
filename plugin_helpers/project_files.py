import os

class ProjectFiles(object):
  def __init__(self, project_root, file_matcher, ignored_directories):
    self.project_root = project_root
    self.file_matcher = file_matcher
    self.ignored_directories = ignored_directories

  def filter(self):
    if not self.project_root: return

    matches = []
    for dirname, _, files in self._walk(self.project_root):
      for file in filter(self.file_matcher, files):
        matches.append(os.path.join(dirname, file))

    return matches

  def _walk(self, directory):
    for dir, dirnames, files in os.walk(directory):
      dirnames[:] = [dirname for dirname in dirnames if dirname not in self.ignored_directories]
      yield dir, dirnames, files
