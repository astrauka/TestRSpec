import sublime


class LastRun:
    SETTINGS_FILE = "TestRSpec.last-run"

    @classmethod
    def save(klass, command_hash):
        settings = sublime.load_settings(klass.SETTINGS_FILE)
        settings.set("command_hash", command_hash)
        sublime.save_settings(klass.SETTINGS_FILE)

    @classmethod
    def command_hash(klass):
        settings = sublime.load_settings(klass.SETTINGS_FILE)
        return settings.get("command_hash")
