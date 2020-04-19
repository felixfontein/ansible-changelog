# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os


class PathsConfig(object):
    """Configuration for paths."""

    @staticmethod
    def _changelog_dir(base_dir):
        return os.path.join(base_dir, 'changelogs')

    @staticmethod
    def _config_path(changelog_dir):
        return os.path.join(changelog_dir, 'config.yaml')

    def __init__(self, base_dir, galaxy_path, ansible_doc_path):
        """Forces configuration with given base path.
        :type base_dir: str
        :type galaxy_path: str | None
        :type ansible_doc_path: str | None
        """
        self.base_dir = base_dir
        self.galaxy_path = galaxy_path
        self.changelog_dir = PathsConfig._changelog_dir(self.base_dir)
        self.config_path = PathsConfig._config_path(self.changelog_dir)
        self.ansible_doc_path = ansible_doc_path

    @staticmethod
    def force(base_dir):
        """Forces configuration with given base path.
        :type base_dir: str
        """
        base_dir = os.path.abspath(base_dir)
        return PathsConfig(base_dir, os.path.join(base_dir, 'galaxy.yml'), None)

    @staticmethod
    def detect():
        """Detect paths configuration from current working directory.
        :raises ValueError: cannot identify collection or ansible/ansible checkout
        """
        previous = None
        base_dir = os.getcwd()
        while True:
            changelog_dir = PathsConfig._changelog_dir(base_dir)
            config_path = PathsConfig._config_path(changelog_dir)
            if os.path.exists(changelog_dir) and os.path.exists(config_path):
                galaxy_path = os.path.join(base_dir, 'galaxy.yml')
                if os.path.exists(galaxy_path):
                    # We are in a collection and assume ansible-doc is available in $PATH
                    return PathsConfig(base_dir, galaxy_path, 'ansible-doc')
                if os.path.exists(os.path.join(base_dir, 'lib')) and os.path.exists(os.path.join(base_dir, 'lib', 'ansible')):
                    # We are in a checkout of ansible/ansible
                    return PathsConfig(base_dir, None, os.path.join(base_dir, 'bin', 'ansible-doc'))
            previous, base_dir = base_dir, os.path.dirname(base_dir)
            if previous == base_dir:
                raise ValueError()
