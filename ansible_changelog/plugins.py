# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import json
import os
import subprocess

import yaml

from ansible import constants as C
from ansible.module_utils._text import to_text

from .utils import LOGGER, load_galaxy_metadata


def load_plugin_metadata(paths, plugin_type, collection_name):
    command = [paths.ansible_doc_path, '--json', '-t', plugin_type, '--list']
    if collection_name:
        command.append(collection_name)
    output = subprocess.check_output(command)
    plugins_list = json.loads(to_text(output))

    if not collection_name:
        # Filter out FQCNs
        plugins_list = {
            name: data for name, data in plugins_list.items()
            if '.' not in name or name.startswith('ansible.builtin.')
        }

    result = dict()
    if not plugins_list:
        return result

    command = [paths.ansible_doc_path, '--json', '-t', plugin_type]
    command.extend(sorted(plugins_list.keys()))
    output = subprocess.check_output(command)
    plugins_data = json.loads(to_text(output))

    for name, data in plugins_data.items():
        namespace = None
        if collection_name and name.startswith(collection_name + '.'):
            name = name[len(collection_name) + 1:]
        docs = data.get('doc') or dict()
        if plugin_type == 'module':
            filename = docs.get('filename')
            if filename:
                if collection_name:
                    path = os.path.relpath(filename, os.path.join(paths.base_dir, 'plugins', 'modules'))
                else:
                    path = os.path.relpath(filename, os.path.join(paths.base_dir, 'lib', 'ansible', 'modules'))
                path = os.path.split(path)[0]
                namespace = []
                while True:
                    (path, last), prev = os.path.split(path), path
                    if path == prev:
                        break
                    if last not in ('', '.', '..'):
                        namespace.insert(0, last)
                namespace = '.'.join(namespace)
        result[name] = {
            'description': docs.get('short_description'),
            'name': name,
            'namespace': namespace,
            'version_added': docs.get('version_added'),
        }
    return result


def load_plugins(paths, version, force_reload):
    """Load plugins from ansible-doc.
    :type paths: PathsConfig
    :type version: str
    :type force_reload: bool
    :rtype: list[PluginDescription]
    """
    plugin_cache_path = os.path.join(paths.changelog_dir, '.plugin-cache.yaml')
    plugins_data = {}

    if not force_reload and os.path.exists(plugin_cache_path):
        with open(plugin_cache_path, 'r') as plugin_cache_fd:
            plugins_data = yaml.safe_load(plugin_cache_fd)

            if version != plugins_data['version']:
                LOGGER.info('version %s does not match plugin cache version %s', version, plugins_data['version'])
                plugins_data = {}

    if not plugins_data:
        LOGGER.info('refreshing plugin cache')

        plugins_data['version'] = version
        plugins_data['plugins'] = {}

        collection_name = None
        if paths.galaxy_path:
            galaxy = load_galaxy_metadata(paths)
            collection_name = '{0}.{1}'.format(galaxy['namespace'], galaxy['name'])

        for plugin_type in C.DOCUMENTABLE_PLUGINS:
            plugins_data['plugins'][plugin_type] = load_plugin_metadata(paths, plugin_type, collection_name)

        # remove empty namespaces from plugins
        for section in plugins_data['plugins'].values():
            for plugin in section.values():
                if plugin['namespace'] is None:
                    del plugin['namespace']

        with open(plugin_cache_path, 'w') as plugin_cache_fd:
            yaml.safe_dump(plugins_data, plugin_cache_fd, default_flow_style=False)

    plugins = PluginDescription.from_dict(plugins_data['plugins'])

    return plugins


class PluginDescription(object):
    """Plugin description."""
    def __init__(self, plugin_type, name, namespace, description, version_added):
        self.type = plugin_type
        self.name = name
        self.namespace = namespace
        self.description = description
        self.version_added = version_added

    @staticmethod
    def from_dict(data):
        """Return a list of PluginDescription objects from the given data.
        :type data: dict[str, dict[str, dict[str, any]]]
        :rtype: list[PluginDescription]
        """
        plugins = []

        for plugin_type, plugin_data in data.items():
            for plugin_name, plugin_details in plugin_data.items():
                plugins.append(PluginDescription(
                    plugin_type=plugin_type,
                    name=plugin_name,
                    namespace=plugin_details.get('namespace'),
                    description=plugin_details['description'],
                    version_added=plugin_details['version_added'],
                ))

        return plugins
