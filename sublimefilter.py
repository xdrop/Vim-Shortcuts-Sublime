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

    def scan(self, point):
        view = self.view
        left_bound = self.get_bound(point, -1)
        right_bound = self.get_bound(point, +1)
        return sublime.Region(left_bound + 1, right_bound)
   

    def get_bound(self, point, direction):
        view = self.view
        for i in range(0, scan_limit):
            next_point = point + (i * direction)
            scanned_char = get_char(view, next_point)
            if not self.is_pass(scanned_char):
                return next_point


def get_char(view, point):
    one_char = sublime.Region(point, point + 1)
    char = view.substr(one_char)
    return char
