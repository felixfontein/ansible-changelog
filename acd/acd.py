#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Changelog generator and linter."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import os
import shlex
import subprocess

import packaging.version
import yaml

from ansible_changelog.config import PathsConfig, ChangelogConfig
from ansible_changelog.changes import load_changes
from ansible_changelog.changelog_generator import ChangelogGenerator
from ansible_changelog.fragment import load_fragments
from ansible_changelog.plugins import load_plugins
from ansible_changelog.rst import RstBuilder

class GitCheckout:
    def _get_path(self, url):
        components = []
        if url.startswith('git@'):
            i = url.index(':')
            components = [url[4:i]]
            components.extend(url[i+1:].split('/'))
        else:
            raise Exception('Cannot parse repository URL "{0}"'.format(url))
        result = self._path
        for c in components:
            if not os.path.exists(result):
                os.mkdir(result)
            result = os.path.join(result, c)
        return result

    def __init__(self, path):
        self._path = path
        self._repositories = dict()
        if not os.path.exists(self._path):
            os.mkdir(self._path)

    def _clone(self, url, path, branch=None):
        command = ['git', 'clone', url, path, '--no-single-branch', '--no-remote-submodules', '--depth', '1']
        if branch:
            command.extend(['--branch', branch])
        print('[{0}] Running {1}...'.format(path, shlex.join(command)))
        subprocess.check_call(command)

    def _fetch(self, path):
        command = ['git', 'fetch', '-a', 'origin']
        print('[{0}] Running {1}...'.format(path, shlex.join(command)))
        subprocess.call(command, cwd=path)

    def _current_branch(self, path):
        command = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
        print('[{0}] Running {1}...'.format(path, shlex.join(command)))
        p = subprocess.run(command, cwd=path, stdout=subprocess.PIPE)
        return p.stdout.decode('utf-8').strip()

    def _select_branch(self, path, branch):
        command = ['git', 'switch', '--no-guess', branch]
        print('[{0}] Running {1}...'.format(path, shlex.join(command)))
        rc = subprocess.call(command, cwd=path)
        if rc != 0:
            command = ['git', 'checkout', '-b', branch, '--track', 'origin/{0}'.format(branch)]
            print('[{0}] Running {1}...'.format(path, shlex.join(command)))
            rc = subprocess.check_call(command, cwd=path)

    def checkout(self, repository, branch=None, no_fetch=False):
        url = repository['repo']
        branch = branch or repository['branch']
        print('Checking out {0} for branch {1}'.format(url, branch))
        if url not in self._repositories:
            path = self._get_path(url)
            if not os.path.exists(path) or not os.path.exists(os.path.join(path, '.git')):
                if os.path.exists(path):
                    raise Exception('Path "{0}" exists, but is no git checkout!'.format(path))
                self._clone(url, path, branch)
            elif not no_fetch:
                self._fetch(path)
            self._repositories[url] = path

        path = self._repositories[url]
        current_branch = self._current_branch(path)
        if current_branch != branch:
            self._select_branch(path, branch)

        command = ['git', 'reset', '--hard', 'origin/{0}'.format(branch)]
        print('[{0}] Running {1}...'.format(path, shlex.join(command)))
        subprocess.check_call(command, cwd=path)

        return path


def main():
    with open('acd.yml', 'r') as f:
        data = yaml.safe_load(f)
    ansible = data['ansible']
    collections = data['collections']

    no_fetch = True  # FIXME

    git = GitCheckout('cache')

    # Update git repositories
    ansible['path'] = git.checkout(ansible, no_fetch=no_fetch)
    for name, collection in collections.items():
        collection['name'] = name
        collection['path'] = git.checkout(collection, no_fetch=no_fetch)

    collections = sorted(collections.values(), key=lambda c: c['name'])

    # Read Ansible Base changelog data
    ansible_paths = PathsConfig.force_ansible(ansible['path'])
    ansible_config = ChangelogConfig.load(ansible_paths.config_path)
    ansible_changes = load_changes(ansible_paths, ansible_config)

    ansible_fragments = load_fragments(ansible_paths, ansible_config)
    ansible_plugins = load_plugins(ansible_paths, ansible_changes.latest_version, False)

    # Read collection changelog data
    for collection in collections:
        print('Loading changelog data for {0}...'.format(collection['name']))
        paths = PathsConfig.force_collection(collection['path'])
        config = ChangelogConfig.load(paths.config_path)
        changes = load_changes(paths, config)
        collection['path_config'] = paths
        collection['config'] = config
        collection['changes'] = changes

    # CHANGELOG TYPE 1

    builder = RstBuilder()
    builder.set_title('ACD Changelog Mockup')
    builder.add_raw_rst('This is an example mockup of what the ACD changelog file could look like in RST.\n')
    builder.add_raw_rst('.. contents::\n  :local:\n  :depth: 1\n')

    builder.add_section('Ansible Base', 0)
    builder.add_raw_rst('.. contents::\n  :local:\n  :depth: 5\n')
    major_minor_version = '.'.join(ansible_changes.latest_version.split('.')[:ansible_config.changelog_filename_version_depth])
    generator = ChangelogGenerator(ansible_config, ansible_changes, plugins=ansible_plugins, fragments=ansible_fragments, flatmap=True)
    generator.generate_to(builder, 1)

    for collection in collections:
        major_minor_version = '.'.join(collection['changes'].latest_version.split('.')[:collection['config'].changelog_filename_version_depth])
        generator = ChangelogGenerator(collection['config'], collection['changes'], plugins=None, fragments=[], flatmap=True)

        builder.add_section(collection['config'].title, 0)
        builder.add_raw_rst('.. contents::\n  :local:\n  :depth: 5\n')

        generator.generate_to(builder, 1)

    with open('acd.rst', 'wb') as changelog_fd:
        changelog_fd.write(builder.generate().encode('utf-8'))

    # CHANGELOG TYPE 2

    builder = RstBuilder()
    builder.set_title('ACD Changelog Mockup')
    builder.add_raw_rst('This is an example mockup of what the ACD changelog file could look like in RST.\n')
    builder.add_raw_rst('.. contents::\n  :local:\n  :depth: 2\n')

    previous_version = ansible['previous_version']
    for version in sorted(ansible_changes.releases, key=packaging.version.Version):
        builder.add_section('v{0}'.format(version), 0)

        builder.add_section('Ansible Base', 1)
        builder.add_raw_rst('.. contents::\n  :local:\n  :depth: 5\n')
        major_minor_version = '.'.join(ansible_changes.latest_version.split('.')[:ansible_config.changelog_filename_version_depth])
        generator = ChangelogGenerator(ansible_config, ansible_changes, plugins=ansible_plugins, fragments=ansible_fragments, flatmap=True)
        generator.generate_to(builder, 1, squash=True, after_version=previous_version, until_version=version)

        for collection in collections:
            major_minor_version = '.'.join(collection['changes'].latest_version.split('.')[:collection['config'].changelog_filename_version_depth])
            generator = ChangelogGenerator(collection['config'], collection['changes'], plugins=None, fragments=[], flatmap=True)

            builder.add_section(collection['config'].title, 1)
            if collection['versions'][previous_version] == '0.0.0':
                builder.add_raw_rst('Changes for collection ``{0}`` until version {1}.\n'.format(collection['name'], collection['versions'][version]))
            else:
                builder.add_raw_rst('Changes for collection ``{0}`` after version {1} (included in the previous ACD version) until version {2}.\n'.format(
                    collection['name'], collection['versions'][previous_version], collection['versions'][version]
                ))

            builder.add_raw_rst('.. contents::\n  :local:\n  :depth: 5\n')

            generator.generate_to(builder, 1, squash=True, after_version=collection['versions'][previous_version], until_version=collection['versions'][version])

        previous_version = version

    with open('acd2.rst', 'wb') as changelog_fd:
        changelog_fd.write(builder.generate().encode('utf-8'))

if __name__ == '__main__':
    main()
