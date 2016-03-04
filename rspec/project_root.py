from plugin_helpers.decorators import memoize

class ProjectRoot(object):
  def __init__(self, file_name):
    self.file_name = file_name

  def result(self):
    if not self.file_name: return
    if not self.spec_folder_name() in self.file_name: return

    return self.file_name[:self.file_name.index(self.spec_folder_name())]

  @memoize
  def spec_folder_name(self):
    return '/spec/'
