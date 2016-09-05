import sublime
import sublime_plugin
import re
from .sublimefilter import SublimeFilter


spaceRe = re.compile(r'^\s*')


class ChangeWordCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        cursors = view.sel()
        for cur in cursors:
            word_sel = view.word(cur)
            clearToEnd(view, edit, word_sel)


class ReplaceLineCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        cursors = view.sel()
        for i in range(len(cursors)):
            cur = cursors[i]
            cur_line = view.line(cur)
            indentation = get_indentation(view, cur_line)
            clear_contents(view, edit, cur_line)
            # refresh the cursor list
            cursors = view.sel()
            new_cur = cursors[i]
            # reinsert indentation
            view.insert(edit, new_cur.begin(), indentation)


class DeleteToEolCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        cursors = view.sel()
        for i in range(len(cursors)):
            cur = cursors[i]
            line = view.line(cur)
            del_region = sublime.Region(cur.begin(), line.end())
            clear_contents(view, edit, del_region)


class ChangeUntilCommand(sublime_plugin.TextCommand):

    def run(self, edit, **args):
        if args["replace_until"]:
            wait_until = args["replace_until"]
        else:
            wait_until = "\""
        view = self.view
        if len(view.sel()) > 1:
            return
        cursor = view.sel()[0]
        fltr = SublimeFilter(view, [wait_until])
        end = fltr.suffix(cursor.begin())
        del_region = sublime.Region(cursor.begin(), en)
        clear_contents(view, edit, del_region)


class YankWordCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        cur = view.sel()[0]
        word_region = view.word(cur)
        word = view.substr(word_region)
        sublime.set_clipboard(word)


class DeleteWordCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        cursors = view.sel()
        for cur in cursors:
            word_region = view.word(cur)
            clear_contents(view, edit, word_region)


class RepeatLastCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        (name, args, count) = view.command_history(0, True)
        view.run_command(name, args)


class ReplaceCurrentWord(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        if 0 >= len(view.sel()) > 1:
            return
        view.run_command(" dsad dsdsd sdsd ")
        view.run_command("")




def get_indentation(view, region):
    region_content = view.substr(region)
    return spaceRe.search(region_content).group(0)


def clear_contents(view, edit, word_sel):
    view.replace(edit, word_sel, "")
