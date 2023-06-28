import os

from .package_root import PackageRoot


class ProjectRoot:
    def __init__(self, file_name, spec_folder_name, sublime_command):
        self.file_name = file_name
        self.spec_folder_name = spec_folder_name
        self.sublime_command = sublime_command

    def result(self):
        if not self.file_name:
            return
        if not self.spec_folder_name:
            return

        return self._via_open_folders() or self._package_root()

    def _via_open_folders(self):
        view = self.sublime_command.view
        if not view:
            return

        window = view.window()
        if not window:
            return

        for folder in window.folders():
            if not self.file_name.startswith(folder):
                continue

            spec_folder_path = os.path.join(folder, self.spec_folder_name)
            if os.path.isdir(spec_folder_path):
                return folder

    def _package_root(self):
        return PackageRoot(self.file_name, self.spec_folder_name).result()
