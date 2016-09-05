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
            wait_until = ["\""]
        view = self.view
        if len(view.sel()) > 1:
            return
        cursor = view.sel()[0]
        fltr = SublimeFilter(view, wait_until)
        # get the region from cursor to line end
        end = fltr.suffix(cursor.begin())
        del_region = sublime.Region(cursor.begin(), end)
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


class ReplaceCurrentWordCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        if len(view.sel()) > 1:
            return
        # expand current selection to the word
        view.run_command("expand_selection", {'to': 'word'})
        # execute the find all under command
        self.view.window().run_command("find_all_under")


class SelectBetweenCommand(sublime_plugin.TextCommand):

    def run(self, edit, **args):
        view = self.view
        if len(view.sel()) > 1:
            return
        if args["wait_until"]:
            wait_until = args["wait_until"]
        else:
            wait_until = ["\""]
        fltr = SublimeFilter(view, wait_until)
        # Get the bounding box of the selection
        region = fltr.scan(view.sel()[0].begin())
        move_cursor(view, region)


def move_cursor(view, region):
    view.sel().clear()
    view.sel().add(region)


def get_indentation(view, region):
    region_content = view.substr(region)
    return spaceRe.search(region_content).group(0)


def clear_contents(view, edit, word_sel):
    view.replace(edit, word_sel, "")
