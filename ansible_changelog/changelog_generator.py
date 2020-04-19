# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import collections
import os

import packaging.version

from ansible.module_utils._text import to_bytes

from .fragment import ChangelogFragment
from .rst import RstBuilder
from .utils import LOGGER, load_galaxy_metadata, is_release_version


def generate_changelog(paths, config, changes, plugins, fragments):
    """Generate the changelog.
    :type paths: PathsConfig
    :type config: ChangelogConfig
    :type changes: ChangesBase
    :type plugins: list[PluginDescription]
    :type fragments: list[ChangelogFragment]
    """
    changes.prune_plugins(plugins)
    if config.changes_format == 'classic':
        changes.prune_fragments(fragments)
    changes.save()

    major_minor_version = '.'.join(changes.latest_version.split('.')[:2])
    changelog_path = os.path.join(paths.changelog_dir, 'CHANGELOG-v%s.rst' % major_minor_version)

    generator = ChangelogGenerator(config, changes, plugins, fragments)
    rst = generator.generate()

    with open(changelog_path, 'wb') as changelog_fd:
        changelog_fd.write(to_bytes(rst))


class ChangelogGenerator(object):
    """Changelog generator."""
    def __init__(self, config, changes, plugins, fragments):
        """
        :type config: ChangelogConfig
        :type changes: ChangesBase
        :type plugins: list[PluginDescription]
        :type fragments: list[ChangelogFragment]
        """
        self.config = config
        self.changes = changes
        self.plugins = {}
        self.modules = []

        for plugin in plugins:
            if plugin.type == 'module':
                self.modules.append(plugin)
            else:
                if plugin.type not in self.plugins:
                    self.plugins[plugin.type] = []

                self.plugins[plugin.type].append(plugin)

        self.fragments = dict((fragment.name, fragment) for fragment in fragments)

    def generate(self):
        """Generate the changelog.
        :rtype: str
        """
        latest_version = self.changes.latest_version
        codename = self.changes.releases[latest_version].get('codename')
        major_minor_version = '.'.join(latest_version.split('.')[:2])

        release_entries = collections.OrderedDict()
        entry_version = latest_version
        entry_fragment = None

        for version in sorted(self.changes.releases, reverse=True, key=packaging.version.Version):
            release = self.changes.releases[version]

            if is_release_version(self.config, version):
                entry_version = version  # next version is a release, it needs its own entry
                entry_fragment = None
            elif not is_release_version(self.config, entry_version):
                entry_version = version  # current version is a pre-release, next version needs its own entry
                entry_fragment = None

            if entry_version not in release_entries:
                release_entries[entry_version] = dict(
                    modules=[],
                    plugins={},
                )
                if self.config.changes_format == 'classic':
                    release_entries[entry_version]['fragments'] = []
                else:
                    release_entries[entry_version]['changes'] = dict()

            entry_config = release_entries[entry_version]

            fragment_names = []

            if self.config.changes_format == 'classic':
                # only keep the latest prelude fragment for an entry
                for fragment_name in release.get('fragments', []):
                    fragment = self.fragments[fragment_name]

                    if self.config.prelude_name in fragment.content:
                        if entry_fragment:
                            LOGGER.info('skipping fragment %s in version %s due to newer fragment %s in version %s',
                                        fragment_name, version, entry_fragment, entry_version)
                            continue

                        entry_fragment = fragment_name

                    fragment_names.append(fragment_name)

                entry_config['fragments'] += fragment_names
            else:
                changes = release.get('changes', dict())
                dest_changes = entry_config['changes']
                for section, lines in changes.items():
                    if section == self.config.prelude_name:
                        if entry_fragment:
                            LOGGER.info('skipping prelude in version %s due to newer prelude in version %s',
                                        version, entry_version)
                            continue

                        entry_fragment = changes[self.config.prelude_name]
                        dest_changes[section] = lines
                    elif section in dest_changes:
                        dest_changes[section].extend(lines)
                    else:
                        dest_changes[section] = list(lines)

            entry_config['modules'] += release.get('modules', [])

            for plugin_type, plugin_names in release.get('plugins', {}).items():
                if plugin_type not in entry_config['plugins']:
                    entry_config['plugins'][plugin_type] = []

                entry_config['plugins'][plugin_type] += plugin_names

        builder = RstBuilder()
        title = self.config.title or 'Ansible'
        if codename:
            builder.set_title('%s %s "%s" Release Notes' % (title, major_minor_version, codename))
        else:
            builder.set_title('%s %s Release Notes' % (title, major_minor_version))
        builder.add_raw_rst('.. contents:: Topics\n\n')

        for version, release in release_entries.items():
            builder.add_section('v%s' % version)

            if self.config.changes_format == 'classic':
                combined_fragments = ChangelogFragment.combine([self.fragments[fragment] for fragment in release['fragments']])
            else:
                combined_fragments = release['changes']

            for section_name in self.config.sections:
                self._add_section(builder, combined_fragments, section_name)

            self._add_plugins(builder, release['plugins'])
            self._add_modules(builder, release['modules'])

        return builder.generate()

    def _add_section(self, builder, combined_fragments, section_name):
        if section_name not in combined_fragments:
            return

        section_title = self.config.sections[section_name]

        builder.add_section(section_title, 1)

        content = combined_fragments[section_name]

        if isinstance(content, list):
            for rst in sorted(content):
                builder.add_raw_rst('- %s' % rst)
        else:
            builder.add_raw_rst(content)

        builder.add_raw_rst('')

    def _add_plugins(self, builder, plugin_types_and_names):
        if not plugin_types_and_names:
            return

        have_section = False

        for plugin_type in sorted(self.plugins):
            plugins = dict((plugin.name, plugin) for plugin in self.plugins[plugin_type] if plugin.name in plugin_types_and_names.get(plugin_type, []))

            if not plugins:
                continue

            if not have_section:
                have_section = True
                builder.add_section('New Plugins', 1)

            builder.add_section(plugin_type.title(), 2)

            for plugin_name in sorted(plugins):
                plugin = plugins[plugin_name]

                builder.add_raw_rst('- %s - %s' % (plugin.name, plugin.description))

            builder.add_raw_rst('')

    def _add_modules(self, builder, module_names):
        if not module_names:
            return

        modules = dict((module.name, module) for module in self.modules if module.name in module_names)
        previous_section = None

        modules_by_namespace = collections.defaultdict(list)

        for module_name in sorted(modules):
            module = modules[module_name]

            modules_by_namespace[module.namespace].append(module.name)

        for namespace in sorted(modules_by_namespace):
            parts = namespace.split('.')

            section = parts.pop(0).replace('_', ' ').title()

            if not previous_section:
                builder.add_section('New Modules', 1)

            if section != previous_section:
                builder.add_section(section, 2)

            previous_section = section

            subsection = '.'.join(parts)

            if subsection:
                builder.add_section(subsection, 3)

            for module_name in modules_by_namespace[namespace]:
                module = modules[module_name]

                builder.add_raw_rst('- %s - %s' % (module.name, module.description))

            builder.add_raw_rst('')
