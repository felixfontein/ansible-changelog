# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


class RstBuilder(object):
    """Simple RST builder."""
    def __init__(self):
        self.lines = []
        self.section_underlines = '''=-~^.*+:`'"_#'''

    def set_title(self, title):
        """Set the title.
        :type title: str
        """
        self.lines.append(self.section_underlines[0] * len(title))
        self.lines.append(title)
        self.lines.append(self.section_underlines[0] * len(title))
        self.lines.append('')

    def add_section(self, name, depth=0):
        """Add a section.
        :type name: str
        :type depth: int
        """
        self.lines.append(name)
        self.lines.append(self.section_underlines[depth] * len(name))
        self.lines.append('')

    def add_raw_rst(self, content):
        """Add a raw RST.
        :type content: str
        """
        self.lines.append(content)

    def generate(self):
        """Generate RST content.
        :rtype: str
        """
        return '\n'.join(self.lines)
