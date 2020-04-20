# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import abc
import collections
import os

import packaging.version
import yaml

from ansible.module_utils import six

from .plugins import load_plugins, PluginResolver, SimplePluginResolver
from .utils import LOGGER, is_release_version


def load_changes(paths, config):
    """Load changes metadata.
    :type paths: PathsConfig
    :type config: ChangelogConfig
    :rtype: ChangesMetadata
    """
    path = os.path.join(paths.changelog_dir, config.changes_file)
    if config.changes_format == 'classic':
        changes = ChangesMetadata(paths, path)
    else:
        changes = ChangesData(config, path)

    return changes


def add_release(config, changes, plugins, fragments, version, codename, date):
    """Add a release to the change metadata.
    :type config: ChangelogConfig
    :type changes: ChangesMetadata
    :type plugins: list[PluginDescription]
    :type fragments: list[ChangelogFragment]
    :type version: str
    :type codename: str
    :type date: datetime.date
    """
    # make sure the version parses
    packaging.version.Version(version)

    LOGGER.info('release version %s is a %s version', version, 'release' if is_release_version(config, version) else 'pre-release')

    # filter out plugins which were not added in this release
    plugins = list(filter(lambda p: version.startswith('%s.' % p.version_added) or version == p.version_added, plugins))

    changes.add_release(version, codename, date)

    for plugin in plugins:
        changes.add_plugin(plugin, version)

    fragments_added = []
    for fragment in fragments:
        if changes.add_fragment(fragment, version):
            fragments_added.append(fragment)

    changes.save()

    if not config.keep_fragments:
        for fragment in fragments_added:
            fragment.remove()


@six.add_metaclass(abc.ABCMeta)
class ChangesBase(object):
    """Read, write and manage change metadata."""
    def __init__(self, path):
        self.path = path
        self.data = self.empty()
        self.known_plugins = set()

    @staticmethod
    def empty():
        """Empty change metadata."""
        return dict(
            releases=dict(
            ),
        )

    @property
    def latest_version(self):
        """Latest version in the changes.
        :rtype: str
        """
        return sorted(self.releases, reverse=True, key=packaging.version.Version)[0]

    @property
    def has_release(self):
        """Whether there is at least one release.
        :rtype: bool
        """
        return bool(self.releases)

    @property
    def releases(self):
        """Dictionary of releases.
        :rtype: dict[str, dict[str, any]]
        """
        return self.data['releases']

    def load(self):
        """Load the change metadata from disk."""
        if os.path.exists(self.path):
            with open(self.path, 'r') as meta_fd:
                self.data = yaml.safe_load(meta_fd)
        else:
            self.data = self.empty()

    @abc.abstractmethod
    def prune_plugins(self, plugins):
        """Remove plugins which are not in the provided list of plugins.
        :type plugins: list[PluginDescription]
        """

    @abc.abstractmethod
    def sort(self):
        """Sort change metadata in place."""

    def save(self):
        """Save the change metadata to disk."""
        self.sort()

        with open(self.path, 'w') as config_fd:
            yaml.safe_dump(self.data, config_fd, default_flow_style=False)

    def add_release(self, version, codename, release_date):
        """Add a new releases to the changes metadata.
        :type version: str
        :type codename: str
        :type release_date: datetime.date
        """
        if version not in self.releases:
            self.releases[version] = dict(
                release_date=str(release_date),
            )
            if codename:
                self.releases[version]['codename'] = codename
        else:
            LOGGER.warning('release %s already exists', version)

    @abc.abstractmethod
    def add_fragment(self, fragment, version):
        """Add a changelog fragment to the change metadata.
        :type fragment: ChangelogFragment
        :type version: str
        """

    def _create_plugin_entry(self, plugin):
        return plugin.name

    def add_plugin(self, plugin, version):
        """Add a plugin to the change metadata.
        :type plugin: PluginDescription
        :type version: str
        """
        composite_name = '%s/%s' % (plugin.type, plugin.name)

        if composite_name in self.known_plugins:
            return False

        self.known_plugins.add(composite_name)

        if plugin.type == 'module':
            if 'modules' not in self.releases[version]:
                self.releases[version]['modules'] = []

            modules = self.releases[version]['modules']
            modules.append(self._create_plugin_entry(plugin))
        else:
            if 'plugins' not in self.releases[version]:
                self.releases[version]['plugins'] = {}

            plugins = self.releases[version]['plugins']

            if plugin.type not in plugins:
                plugins[plugin.type] = []

            plugins[plugin.type].append(self._create_plugin_entry(plugin))

        return True

    @abc.abstractmethod
    def get_plugin_resolver(self, plugins=None):
        """Load plugins from ansible-doc.
        :type plugins: list[PluginDescription] | None
        :rtype: PluginResolver
        """


class ChangesMetadata(ChangesBase):
    """Read, write and manage change metadata."""
    def __init__(self, paths, path):
        super(ChangesMetadata, self).__init__(path)
        self.paths = paths
        self.known_fragments = set()
        self.load()

    def load(self):
        """Load the change metadata from disk."""
        super(ChangesMetadata, self).load()

        for version, config in self.releases.items():
            for plugin_type, plugin_names in config.get('plugins', {}).items():
                self.known_plugins |= set('%s/%s' % (plugin_type, plugin_name) for plugin_name in plugin_names)

            module_names = config.get('modules', [])

            self.known_plugins |= set('module/%s' % module_name for module_name in module_names)

            self.known_fragments |= set(config.get('fragments', []))

    def prune_fragments(self, fragments):
        """Remove fragments which are not in the provided list of fragments.
        :type fragments: list[ChangelogFragment]
        """
        valid_fragments = set(fragment.name for fragment in fragments)

        for version, config in self.releases.items():
            if 'fragments' not in config:
                continue

            invalid_fragments = set(fragment for fragment in config['fragments'] if fragment not in valid_fragments)
            config['fragments'] = [fragment for fragment in config['fragments'] if fragment not in invalid_fragments]
            self.known_fragments -= set(config['fragments'])

    def prune_plugins(self, plugins):
        """Remove plugins which are not in the provided list of plugins.
        :type plugins: list[PluginDescription]
        """
        valid_plugins = collections.defaultdict(set)

        for plugin in plugins:
            valid_plugins[plugin.type].add(plugin.name)

        for version, config in self.releases.items():
            if 'modules' in config:
                invalid_modules = set(module for module in config['modules'] if module not in valid_plugins['module'])
                config['modules'] = [module for module in config['modules'] if module not in invalid_modules]
                self.known_plugins -= set('module/%s' % module for module in invalid_modules)

            if 'plugins' in config:
                for plugin_type in config['plugins']:
                    invalid_plugins = set(plugin for plugin in config['plugins'][plugin_type] if plugin not in valid_plugins[plugin_type])
                    config['plugins'][plugin_type] = [plugin for plugin in config['plugins'][plugin_type] if plugin not in invalid_plugins]
                    self.known_plugins -= set('%s/%s' % (plugin_type, plugin) for plugin in invalid_plugins)

    def sort(self):
        """Sort change metadata in place."""
        for release, config in self.data['releases'].items():
            if 'modules' in config:
                config['modules'] = sorted(config['modules'])

            if 'plugins' in config:
                for plugin_type in config['plugins']:
                    config['plugins'][plugin_type] = sorted(config['plugins'][plugin_type])

            if 'fragments' in config:
                config['fragments'] = sorted(config['fragments'])

    def add_fragment(self, fragment, version):
        """Add a changelog fragment to the change metadata.
        :type fragment: ChangelogFragment
        :type version: str
        """
        if fragment.name in self.known_fragments:
            return False

        self.known_fragments.add(fragment.name)

        if 'fragments' not in self.releases[version]:
            self.releases[version]['fragments'] = []

        fragments = self.releases[version]['fragments']
        fragments.append(fragment.name)
        return True

    def get_plugin_resolver(self, plugins=None):
        """Load plugins from ansible-doc.
        :type plugins: list[PluginDescription] | None
        :rtype: PluginResolver
        """
        if plugins is None:
            plugins = load_plugins(paths=self.paths, version=self.latest_version, force_reload=False)
        return SimplePluginResolver(plugins)


class ChangesDataPluginResolver(PluginResolver):
    def __init__(self, changes):
        self.changes = changes
        self.plugins = dict()
        for version, config in changes.releases.items():
            if 'modules' in config:
                if 'module' not in self.plugins:
                    self.plugins['module'] = dict()
                for plugin in config['modules']:
                    self.plugins['module'][plugin['name']] = plugin
            if 'plugins' in config:
                for plugin_type, plugins in config['plugins'].items():
                    if plugin_type not in self.plugins:
                        self.plugins[plugin_type] = dict()
                    for plugin in plugins:
                        self.plugins[plugin_type][plugin['name']] = plugin

    def resolve(self, plugin_type, plugin_names):
        """Return a list of PluginDescription objects from the given data.
        :type plugin_type: str
        :type plugin_names: list[str]
        :rtype: list[dict]
        """
        if plugin_type not in self.plugins:
            return []
        return [
            self.plugins[plugin_type][plugin_name]
            for plugin_name in plugin_names
            if plugin_name in self.plugins[plugin_type]
        ]


class ChangesData(ChangesBase):
    """Read, write and manage change data."""
    def __init__(self, config, path):
        super(ChangesData, self).__init__(path)
        self.config = config
        self.load()

    def load(self):
        """Load the change metadata from disk."""
        super(ChangesData, self).load()

        for version, config in self.releases.items():
            for plugin_type, plugins in config.get('plugins', {}).items():
                self.known_plugins |= set('%s/%s' % (plugin_type, plugin.name) for plugin in plugins)

            modules = config.get('modules', [])

            self.known_plugins |= set('module/%s' % module.name for module in modules)

    def prune_plugins(self, plugins):
        """Remove plugins which are not in the provided list of plugins.
        :type plugins: list[PluginDescription]
        """
        valid_plugins = collections.defaultdict(set)

        for plugin in plugins:
            valid_plugins[plugin.type].add(plugin.name)

        for version, config in self.releases.items():
            if 'modules' in config:
                invalid_module_names = set(module['name'] for module in config['modules'] if module['name'] not in valid_plugins['module'])
                config['modules'] = [module for module in config['modules'] if module['name'] not in invalid_module_names]
                self.known_plugins -= set('module/%s' % module_name for module_name in invalid_module_names)

            if 'plugins' in config:
                for plugin_type in config['plugins']:
                    invalid_plugin_names = set(plugin['name'] for plugin in config['plugins'][plugin_type] if plugin['name'] not in valid_plugins[plugin_type])
                    config['plugins'][plugin_type] = [plugin for plugin in config['plugins'][plugin_type] if plugin['name'] not in invalid_plugin_names]
                    self.known_plugins -= set('%s/%s' % (plugin_type, plugin_name) for plugin_name in invalid_plugin_names)

    def sort(self):
        """Sort change metadata in place."""
        super(ChangesData, self).sort()

        for release, config in self.data['releases'].items():
            if 'modules' in config:
                config['modules'] = sorted(config['modules'], key=lambda module: module['name'])

            if 'plugins' in config:
                for plugin_type in config['plugins']:
                    config['plugins'][plugin_type] = sorted(config['plugins'][plugin_type], key=lambda plugin: plugin['name'])

            if 'fragments' in config:
                config['fragments'] = sorted(config['fragments'])

            if 'changes' in config:
                config['changes'] = {
                    section: sorted(entries) if section != self.config.prelude_name else entries
                    for section, entries in sorted(config['changes'].items())
                }

    def add_fragment(self, fragment, version):
        """Add a changelog fragment to the change metadata.
        :type fragment: ChangelogFragment
        :type version: str
        """
        if 'fragments' in self.releases[version] and fragment.name in self.releases[version]['fragments']:
            return False

        if 'changes' not in self.releases[version]:
            self.releases[version]['changes'] = dict()
        changes = self.releases[version]['changes']

        if 'fragments' not in self.releases[version]:
            self.releases[version]['fragments'] = []

        for section, lines in fragment.content.items():
            if section == self.config.prelude_name:
                if section in changes:
                    raise ValueError('Found prelude section "{0}" more than once!'.format(section))
                changes[section] = lines
            elif section not in self.config.sections:
                raise ValueError('Found unknown section "{0}"'.format(section))
            else:
                if section not in changes:
                    changes[section] = []
                changes[section].extend(lines)

        self.releases[version]['fragments'].append(fragment.name)
        return True

    def _create_plugin_entry(self, plugin):
        return dict(
            name=plugin.name,
            namespace=plugin.namespace,
            description=plugin.description,
        )

    def get_plugin_resolver(self, plugins=None):
        """Load plugins from ansible-doc.
        :type plugins: list[PluginDescription] | None
        :rtype: PluginResolver
        """
        return ChangesDataPluginResolver(self)
