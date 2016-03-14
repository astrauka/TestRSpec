import os

class ProjectFiles(object):
  def __init__(self, project_root, file_matcher, ignored_directories):
    self.project_root = project_root
    self.file_matcher = file_matcher
    self.ignored_directories = ignored_directories

  def filter(self):
    matches = []
    for dirname, _, files in self._walk(self.project_root):
      for file in filter(self.file_matcher, files):
        matches.append(os.path.join(dirname, file))

    return matches

  def _walk(self, directory):
    for dir, dirnames, files in os.walk(directory):
      dirnames[:] = [dirname for dirname in dirnames if dirname not in self.ignored_directories]
      yield dir, dirnames, files


# import os
# ignored_directories = [".git", "vendor", "tmp", "migrate"]
# project_root = "/home/astrauka/dev/vinted/admin"
# file_matcher = ".rb"

# def _walk(directory):
#   for dir, dirnames, files in os.walk(directory):
#     dirnames[:] = [dirname for dirname in dirnames if dirname not in ignored_directories]
#     yield dir, dirnames, files

# matches = []
# for dirname, _, files in _walk(project_root):
#   for file in filter(lambda file: file.endswith(file_matcher), files):
#     matches.append(os.path.join(dirname, file))

# matches

# matches = []
# for dirname, _, files in _walk(project_root):
#   print(files)
