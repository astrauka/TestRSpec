import os


class PackageRoot:
    def __init__(self, file_name, spec_folder_name):
        self.file_name = file_name
        self.spec_folder_name = spec_folder_name

    def result(self):
        if not self.file_name:
            return
        if not self.spec_folder_name:
            return

        return self._via_inclusion() or self._via_upwards_search()

    def _via_inclusion(self):
        wrapped_folder_name = "/{0}/".format(self.spec_folder_name)
        if not wrapped_folder_name in self.file_name:
            return

        return self.file_name[: self.file_name.rindex(wrapped_folder_name)]

    def _via_upwards_search(self):
        path = self.file_name

        while True:
            (path, current_dir_name) = os.path.split(path)
            if not current_dir_name:
                return

            spec_folder_path = os.path.join(path, self.spec_folder_name)
            if os.path.isdir(spec_folder_path):
                return path
