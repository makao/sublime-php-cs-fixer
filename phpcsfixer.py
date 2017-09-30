import os
import re
import sublime
import sublime_plugin
import subprocess

STVER = int(sublime.version())

class PHPCSFixer():
    def __init__(self):
        self.settings = PhpCsFixerSettings()
        if sublime.active_window() is not None and sublime.active_window().active_view() is not None:
            self.file = sublime.active_window().active_view().file_name()

    def run(self, file=None):
        if file is None:
            file = self.file

        if not self.settings.isPHPFile():
            return

        if not self.settings.isAllowedExtension(file):
            return

        cmd = self.buildCommand(file)

        result = self.execute(cmd)

        self.showOutput(result)

    def buildCommand(self, file):
        rules = self.settings.get('rules')

        if (self.settings.get('executable')):
            cmd = [self.settings.get('executable')]
        else:
            cmd = ['php-cs-fixer']

        cmd.append('fix');

        cmd.append(os.path.normpath(file))
        cmd.append('-vvv')
        cmd.append('--using-cache=no')

        if rules is None or not rules:
            return cmd

        rules_list = '--rules='
        for rule in rules:
            rules_list += rule + ','

        cmd.append(rules_list[:-1])

        return cmd

    def execute(self, cmd):
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        return process.communicate()[0].decode()

    def showOutput(self, result):
        lines = re.finditer('.*(?P<line>\d+)\) (?P<file>.*)', result)
        files = []

        for line in lines:
            file = line.group('file')
            rules = file[file.find("(")+1:file.find(")")]
            file = re.sub('\(.*?\)','', file)
            files.append([os.path.basename(file), rules])

        sublime.active_window().show_quick_panel(files, self.onDone)

    def onDone(selected, self):
        return

class PhpCsFixerFixCommand(sublime_plugin.TextCommand):
    def run(edit, self):
        PHPCSFixer().run()

class PhpCsFixerEventListener(sublime_plugin.EventListener):
    def on_post_save(self, view):
        settings = PhpCsFixerSettings()
        if not settings.get('on_save'):
            return
        PHPCSFixer().run(view.file_name())

class PhpCsFixerSettings():
    def __init__(self):
        if sublime.active_window() is not None and sublime.active_window().active_view() is not None:
            self.sublime = sublime.active_window().active_view().settings()
            self.project = self.sublime.get('php-cs-fixer')
        else:
            self.sublime = {}
            self.project = {}

        self.plugin = sublime.load_settings('PHPCSFixer.sublime-settings')

    def get(self, key, default=None):
        if self.project is not None and self.project.get(key) is not None:
            return self.project.get(key)

        if self.plugin.get(key) is not None:
            return self.plugin.get(key)

        return default

    def isPHPFile(self):
        syntax = self.sublime.get('syntax')
        if syntax is None:
            return False

        if syntax.endswith('PHP.tmLanguage') or syntax.endswith('PHP.sublime-syntax'):
            return True

        return False

    def isAllowedExtension(self, filename):
        ignored = self.get('ignored_extensions', [])

        for ext in ignored:
            if filename.endswith(ext):
                return False

        return True

class PhpCsFixerOpenFileCommand(sublime_plugin.ApplicationCommand):
    @staticmethod
    def run(file):
        platform_name = {
            'osx': 'OSX',
            'windows': 'Windows',
            'linux': 'Linux',
        }[sublime.platform()]
        file = file.replace('${platform}', platform_name)
        sublime.run_command('open_file', {'file': file})

    @staticmethod
    def is_visible():
        return STVER < 3124

class PhpCsFixerEditSettingsCommand(sublime_plugin.ApplicationCommand):
    @staticmethod
    def run(**kwargs):
        sublime.run_command('edit_settings', kwargs)

    @staticmethod
    def is_visible():
        return STVER >= 3124
