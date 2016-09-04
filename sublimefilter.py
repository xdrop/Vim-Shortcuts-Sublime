import sublime
import re

scan_limit = 1000


class SublimeFilter:

    def __init__(self, view, passthrough):
        self.passthrough = passthrough
        self.view = view

    def is_pass(self, char):
        return char not in self.passthrough

    def suffix(self, point):
        for i in range(0, scan_limit):
            next_point = point + i
            if not self.is_pass(get_char(self.view, next_point)):
                return next_point


def get_char(view, point):
    one_char = sublime.Region(point, point + 1)
    char = view.substr(one_char)
    return char
