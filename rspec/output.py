from plugin_helpers.decorators import memoize
import subprocess
from plugin_helpers.non_blocking_stream_reader import NonBlockingStreamReader

class Output(object):
  class Levels:
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"

  PANEL_NAME = "rspec"

  def __init__(self, window, edit):
    self.window = window
    self.edit = edit

  def log(self, message):
    self.panel().insert(self.edit, self.panel().size(), "{0}\n".format(message))

  # def log_chars(self, chars):
  #   self.panel().insert(self.edit, self.panel().size(), chars)

  # def execute(self, command, project_root, timeout=1):
  #   if isinstance(command, list): command = ' '.join(command)
  #   self.log("Executing {0}\n".format(command))

  #   process = subprocess.Popen(
  #     command,
  #     cwd=project_root,
  #     shell=True,
  #     bufsize=1,
  #     stdout=subprocess.PIPE,
  #     stderr=subprocess.PIPE
  #   )
  #   reader = NonBlockingStreamReader(process.stdout)

  #   output = reader.read()
  #   # if not output: break
  #   print('xx ' + output)
  #   self.log_chars(output)


    # # Poll process for new output until finished
    # while True:
    #     nextline = process.stdout.readline()
    #     if nextline == '' and process.poll() != None:
    #         break
    #     sys.stdout.write(nextline)
    #     sys.stdout.flush()

    # output = process.communicate()[0]
    # exitCode = process.returncode

    # if (exitCode == 0):
    #     return output
    # else:
    #     raise ProcessException(command, exitCode, output)

  # def execute2(self, command, project_root):
  #   if isinstance(command, list): command = ' '.join(command)
  #   shell = isinstance(command, str)
  #   proc = subprocess.Popen(
  #     command,
  #     cwd=project_root,
  #     shell=shell,
  #     stdout=subprocess.PIPE,
  #     stderr=subprocess.PIPE,
  #     bufsize=1,
  #     universal_newlines=True
  #   )

  #   self.log("Executing {0}\n".format(command))
  #   for line in iter(proc.stdout.readline, b''):
  #     self.log(line.decode('utf8'))

  #   for line in iter(proc.stderr.readline, b''):
  #     self.log(line.decode('utf8'))

  # def run_cmd(self, cwd, cmd, wait, input_str=None):
  #   shell = isinstance(cmd, str)
  #   if wait:
  #       proc = subprocess.Popen(cmd, cwd=cwd,
  #                                    shell=shell,
  #                                    stdout=subprocess.PIPE,
  #                                    stderr=subprocess.PIPE,
  #                                    stdin=(subprocess.PIPE if input_str else None))
  #       encoded_input = None if input_str == None else input_str.encode('utf8')
  #       output, error = proc.communicate(encoded_input)
  #       return_code = proc.poll()
  #       if return_code:
  #           show_in_output_panel("`%s` exited with a status code of %s\n\n%s"
  #                                % (cmd, return_code, error))
  #           return (False, None)
  #       else:
  #           return (True, output.decode('utf8'))
  #   else:
  #       subprocess.Popen(cmd, cwd=cwd, shell=shell)
  #       return (False, None)

  @memoize
  def panel(self):
    panel = self.window.get_output_panel(Output.PANEL_NAME)
    panel.settings().set("color_scheme", self.color_scheme())
    return panel

  @memoize
  def panel_name(self):
    return "output.{0}".format(Output.PANEL_NAME)

  def show_panel(self):
    self.window.run_command("show_panel", {"panel": self.panel_name()})

  def color_scheme(self):
    return "Packages/RubyTest/TestConsole.hidden-tmTheme"
