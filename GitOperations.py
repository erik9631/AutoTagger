import os
import warnings

class GitOperator:
    _remote = "origin"

    def __init__(self):
        pass

    def set_remote(self, remote_var):
        self._remote = remote_var

    def get_remote(self):
        return self._remote

    def _read_command(self, command_string):
        command_val = os.popen(command_string)
        return_val = command_val.read()
        command_val.close()
        return return_val

    def checkout(self, branch_name):
        command_val = self._read_command("git checkout " + branch_name)
        return command_val

    def push(self, target_branch, source_branch=""):
        if len(source_branch) == 0:
            command_val = self._read_command("git push " + self._remote + " " + target_branch)
        else:
            command_val = self._read_command("git push " + self._remote + " " + source_branch + ":" + target_branch)
        return command_val

    def pull(self, target_branch):
        command_val = self._read_command("git pull " + self._remote + " " + target_branch)
        return command_val

    def tag(self, version, message=""):
        if len(message) == 0:
            self._lightweight_tag(version)
        command_val = self._read_command("git tag -a " + '"' + version + '"' + ' -m "' + message + '"')
        return command_val

    def _lightweight_tag(self, version):
        command_val = self._read_command("git tag -a " + '"' + version + '"' + " -lw")
        return command_val

    def push_tags(self):
        command_val = self._read_command("git push " + self._remote + " --tags")
        return command_val

    def get_remote_url(self, remote):
        command_val = self._read_command("git remote show " + remote)
        return command_val

    def add_remote(self, name, url):
        command_val = self._read_command("git remote add " + name + " " + url)
        return command_val
