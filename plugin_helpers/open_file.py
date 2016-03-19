import functools

class OpenFile(object):
  def __init__(self, window, files):
    self.window = window
    self.files = files if isinstance(files, list) else [files]

  def run(self):
    if self._single_file():
      self.window.open_file(self.files[0])
    else:
      self.window.show_quick_panel(self.files, self._callback())

  def _single_file(self):
    return len(self.files) == 1

  def _callback(self):
    return functools.partial(self._on_selected, self.files)

  def _on_selected(self, files, index):
    if index == -1: return

    self.window.open_file(files[index])
