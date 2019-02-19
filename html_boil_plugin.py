# $Id: html_boil_plugin.py 154 2017-11-01 18:01:50Z jmcfarren $

import sublime
import sublime_plugin
from .html_boil import HtmlBoil

class HtmlBoilCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.settings = sublime.load_settings('HtmlBoil.sublime-settings')
        # get region and content
        region = sublime.Region(0, self.view.size())
        content = self.view.substr(region)
        if self.view.sel()[0].empty():
            # if there was no user text selection update the entire window buffer
            plain_text = self.boil(content)
            self.view.replace(edit, region, plain_text)
        else:
            # if selection(s), update each
            for region in self.view.sel():
                if not region.empty():
                    content = self.view.substr(region)
                    plain_text = self.boil(content)
                    self.view.replace(edit, region, plain_text)


    def boil(self, content):
        b = HtmlBoil(self.settings)
        content = b.removeIndent(content)
        b.feed(content)
        return b.removeIndent(b.get_data())

