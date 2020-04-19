# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Changelog generator and linter."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import argparse
import collections
import datetime
import docutils.utils
import json
import logging
import os
import packaging.version
import re
import rstcheck
import subprocess
import sys
import yaml

try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping

try:
    import argcomplete
except ImportError:
    argcomplete = None

from ansible import constants as C
from ansible.module_utils.six import string_types
from ansible.module_utils._text import to_bytes, to_text

from .config import PathsConfig


LOGGER = logging.getLogger('changelog')


def set_paths(force=None):
    if force:
        paths = PathsConfig.force(force)
    else:
        try:
            paths = PathsConfig.detect()
        except ValueError:
            print("Only the 'init' command can be used outside an Ansible checkout and outside"
                  " a collection repository set up to use Ansible's changelog generator.\n")
            sys.exit(3)

    return paths


def main():
    """Main program entry point."""
    parser = argparse.ArgumentParser(description='Changelog generator and linter.')

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('-v', '--verbose',
                        action='count',
                        default=0,
                        help='increase verbosity of output')

    subparsers = parser.add_subparsers(metavar='COMMAND')

    init_parser = subparsers.add_parser('init',
                                        parents=[common],
                                        help='set up changelog infrastructure for collection')
    init_parser.set_defaults(func=command_init)
    init_parser.add_argument('root',
                             metavar='COLLECTION_ROOT',
                             help='path to collection root')

    lint_parser = subparsers.add_parser('lint',
                                        parents=[common],
                                        help='check changelog fragments for syntax errors')
    lint_parser.set_defaults(func=command_lint)
    lint_parser.add_argument('fragments',
                             metavar='FRAGMENT',
                             nargs='*',
                             help='path to fragment to test')

    release_parser = subparsers.add_parser('release',
                                           parents=[common],
                                           help='add a new release to the change metadata')
    release_parser.set_defaults(func=command_release)
    release_parser.add_argument('--version',
                                help='override release version')
    release_parser.add_argument('--codename',
                                help='override/set release codename')
    release_parser.add_argument('--date',
                                default=str(datetime.date.today()),
                                help='override release date')
    release_parser.add_argument('--reload-plugins',
                                action='store_true',
                                help='force reload of plugin cache')

    generate_parser = subparsers.add_parser('generate',
                                            parents=[common],
                                            help='generate the changelog')
    generate_parser.set_defaults(func=command_generate)
    generate_parser.add_argument('--reload-plugins',
                                 action='store_true',
                                 help='force reload of plugin cache')

    if argcomplete:
        argcomplete.autocomplete(parser)

    formatter = logging.Formatter('%(levelname)s %(message)s')

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    LOGGER.addHandler(handler)
    LOGGER.setLevel(logging.WARN)

    args = parser.parse_args()
    if getattr(args, 'func', None) is None:
        parser.print_help()
        parser.exit(2)

    if args.verbose > 2:
        LOGGER.setLevel(logging.DEBUG)
    elif args.verbose > 1:
        LOGGER.setLevel(logging.INFO)
    elif args.verbose > 0:
        LOGGER.setLevel(logging.WARN)

    args.func(args)


def makedirs(path):
    """
    :type path: str
    """
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise Exception('Path {0} already exists and is not a folder.'.format(path))
        return
    try:
        os.makedirs(path)
    except Exception:
        if os.path.isdir(path):
            return
        raise


def command_init(args):
    """
    :type args: any
    """
    root = args.root  # type: str

    paths = set_paths(force=root)

    if not os.path.exists(paths.galaxy_path):
        print('The file galaxy.yml does not exists in the collection root!')
        sys.exit(3)
    if os.path.exists(paths.config_path):
        print('A configuration file already exists at "{0}"!'.format(paths.config_path))
        sys.exit(3)

    config = ChangelogConfig.default()
    fragments_dir = os.path.join(paths.changelog_dir, config.notes_dir)
    try:
        makedirs(fragments_dir)
        print('Created fragments directory "{0}"'.format(fragments_dir))
    except Exception:
        print('Cannot create fragments directory "{0}"'.format(fragments_dir))
        sys.exit(3)

    try:
        config.store(paths.config_path)
        print('Created config file "{0}"'.format(paths.config_path))
    except Exception:
        print('Cannot create config file "{0}"'.format(paths.config_path))
        sys.exit(3)


def command_lint(args):
    """
    :type args: any
    """
    paths = set_paths()

    fragment_paths = args.fragments  # type: list

    config = ChangelogConfig.load(paths.config_path)

    exceptions = []
    fragments = load_fragments(paths, config, fragment_paths, exceptions)
    lint_fragments(config, fragments, exceptions)


def command_release(args):
    """
    :type args: any
    """
    paths = set_paths()

    version = args.version  # type: str
    codename = args.codename  # type: str
    date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
    reload_plugins = args.reload_plugins  # type: bool

    config = ChangelogConfig.load(paths.config_path)

    if not version or not codename:
        if paths.galaxy_path is None:
            import ansible.release

            version = version or ansible.release.__version__
            codename = codename or ansible.release.__codename__

        elif not version:
            galaxy = load_galaxy_metadata(paths)
            version = galaxy['version']

    changes = load_changes(paths, config)
    plugins = load_plugins(paths=paths, version=version, force_reload=reload_plugins)
    fragments = load_fragments(paths, config)
    add_release(config, changes, plugins, fragments, version, codename, date)
    generate_changelog(paths, config, changes, plugins, fragments)


def command_generate(args):
    """
    :type args: any
    """
    paths = set_paths()

    reload_plugins = args.reload_plugins  # type: bool

    config = ChangelogConfig.load(paths.config_path)

    changes = load_changes(paths, config)
    if not changes.has_release:
        print('Cannot create changelog when not at least one release has been added.')
        sys.exit(2)
    plugins = load_plugins(paths=paths, version=changes.latest_version, force_reload=reload_plugins)
    fragments = load_fragments(paths, config)
    generate_changelog(paths, config, changes, plugins, fragments)


def load_galaxy_metadata(paths):
    with open(paths.galaxy_path, 'r') as galaxy_fd:
        return yaml.safe_load(galaxy_fd)


def load_changes(paths, config):
    """Load changes metadata.
    :type paths: PathsConfig
    :type config: ChangelogConfig
    :rtype: ChangesMetadata
    """
    path = os.path.join(paths.changelog_dir, config.changes_file)
    changes = ChangesMetadata(path)

    return changes


def load_plugin_metadata(paths, plugin_type, collection_name):
    command = [paths.ansible_doc_path, '--json', '-t', plugin_type, '--list']
    if collection_name:
        command.append(collection_name)
    output = subprocess.check_output(command)
    plugins_list = json.loads(to_text(output))

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
            namespace = collection_name
            name = name[len(collection_name) + 1:]
        docs = data.get('doc') or dict()
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


def load_fragments(paths, config, fragment_paths=None, exceptions=None):
    """
    :type path: PathsConfig
    :type config: ChangelogConfig
    :type fragment_paths: list[str] | None
    :type exceptions: list[tuple[str, Exception]] | None
    """
    if not fragment_paths:
        fragments_dir = os.path.join(paths.changelog_dir, config.notes_dir)
        fragment_paths = [os.path.join(fragments_dir, path) for path in os.listdir(fragments_dir) if not path.startswith('.')]

    fragments = []

    for path in fragment_paths:
        try:
            fragments.append(ChangelogFragment.load(path))
        except Exception as ex:
            if exceptions is not None:
                exceptions.append((path, ex))
            else:
                raise

    return fragments


def lint_fragments(config, fragments, exceptions):
    """
    :type config: ChangelogConfig
    :type fragments: list[ChangelogFragment]
    :type exceptions: list[tuple[str, Exception]]
    """
    linter = ChangelogFragmentLinter(config)

    errors = [(ex[0], 0, 0, 'yaml parsing error') for ex in exceptions]

    for fragment in fragments:
        errors += linter.lint(fragment)

    messages = sorted(set('%s:%d:%d: %s' % (error[0], error[1], error[2], error[3]) for error in errors))

    for message in messages:
        print(message)


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
    plugins = list(filter(lambda p: version.startswith('%s.' % p.version_added), plugins))

    changes.add_release(version, codename, date)

    for plugin in plugins:
        changes.add_plugin(plugin.type, plugin.name, version)

    for fragment in fragments:
        changes.add_fragment(fragment.name, version)

    changes.save()


def generate_changelog(paths, config, changes, plugins, fragments):
    """Generate the changelog.
    :type paths: PathsConfig
    :type config: ChangelogConfig
    :type changes: ChangesMetadata
    :type plugins: list[PluginDescription]
    :type fragments: list[ChangelogFragment]
    """
    changes.prune_plugins(plugins)
    changes.prune_fragments(fragments)
    changes.save()

    major_minor_version = '.'.join(changes.latest_version.split('.')[:2])
    changelog_path = os.path.join(paths.changelog_dir, 'CHANGELOG-v%s.rst' % major_minor_version)

    generator = ChangelogGenerator(paths, config, changes, plugins, fragments)
    rst = generator.generate()

    with open(changelog_path, 'wb') as changelog_fd:
        changelog_fd.write(to_bytes(rst))


class ChangelogFragmentLinter(object):
    """Linter for ChangelogFragments."""
    def __init__(self, config):
        """
        :type config: ChangelogConfig
        """
        self.config = config

    def lint(self, fragment):
        """Lint a ChangelogFragment.
        :type fragment: ChangelogFragment
        :rtype: list[(str, int, int, str)]
        """
        errors = []

        if isinstance(fragment.content, Mapping):
            for section, lines in fragment.content.items():
                if section == self.config.prelude_name:
                    if not isinstance(lines, string_types):
                        errors.append((fragment.path, 0, 0, 'section "%s" must be type str not %s' % (section, type(lines).__name__)))
                else:
                    # doesn't account for prelude but only the RM should be adding those
                    if not isinstance(lines, list):
                        errors.append((fragment.path, 0, 0, 'section "%s" must be type list not %s' % (section, type(lines).__name__)))

                    if section not in self.config.sections:
                        errors.append((fragment.path, 0, 0, 'invalid section: %s' % section))

                if isinstance(lines, list):
                    for line in lines:
                        if not isinstance(line, string_types):
                            errors.append((fragment.path, 0, 0, 'section "%s" list items must be type str not %s' % (section, type(line).__name__)))
                            continue

                        results = rstcheck.check(line, filename=fragment.path, report_level=docutils.utils.Reporter.WARNING_LEVEL)
                        errors += [(fragment.path, 0, 0, result[1]) for result in results]
                elif isinstance(lines, string_types):
                    results = rstcheck.check(lines, filename=fragment.path, report_level=docutils.utils.Reporter.WARNING_LEVEL)
                    errors += [(fragment.path, 0, 0, result[1]) for result in results]

        else:
            errors.append((fragment.path, 0, 0, 'file must be a mapping not %s' % (type(fragment.content).__name__, )))

        return errors


def is_release_version(config, version):
    """Deterine the type of release from the given version.
    :type config: ChangelogConfig
    :type version: str
    :rtype: bool
    """
    tag_format = 'v%s' % version

    if re.search(config.pre_release_tag_re, tag_format):
        return False

    if re.search(config.release_tag_re, tag_format):
        return True

    raise Exception('unsupported version format: %s' % version)


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


class ChangelogGenerator(object):
    """Changelog generator."""
    def __init__(self, paths, config, changes, plugins, fragments):
        """
        :type paths: PathsConfig
        :type config: ChangelogConfig
        :type changes: ChangesMetadata
        :type plugins: list[PluginDescription]
        :type fragments: list[ChangelogFragment]
        """
        self.paths = paths
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
                    fragments=[],
                    modules=[],
                    plugins={},
                )

            entry_config = release_entries[entry_version]

            fragment_names = []

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
            entry_config['modules'] += release.get('modules', [])

            for plugin_type, plugin_names in release.get('plugins', {}).items():
                if plugin_type not in entry_config['plugins']:
                    entry_config['plugins'][plugin_type] = []

                entry_config['plugins'][plugin_type] += plugin_names

        builder = RstBuilder()
        if self.paths.galaxy_path:
            galaxy = load_galaxy_metadata(self.paths)
            collection_name = '{0}.{1}'.format(galaxy['namespace'].title(), galaxy['name'].title())
            if codename:
                builder.set_title('%s %s "%s" Release Notes' % (collection_name, major_minor_version, codename))
            else:
                builder.set_title('%s %s Release Notes' % (collection_name, major_minor_version))
        else:
            builder.set_title('Ansible %s "%s" Release Notes' % (major_minor_version, codename))
        builder.add_raw_rst('.. contents:: Topics\n\n')

        for version, release in release_entries.items():
            builder.add_section('v%s' % version)

            combined_fragments = ChangelogFragment.combine([self.fragments[fragment] for fragment in release['fragments']])

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


class ChangelogFragment(object):
    """Changelog fragment loader."""
    def __init__(self, content, path):
        """
        :type content: dict[str, list[str]]
        :type path: str
        """
        self.content = content
        self.path = path
        self.name = os.path.basename(path)

    @staticmethod
    def load(path):
        """Load a ChangelogFragment from a file.
        :type path: str
        """
        with open(path, 'r') as fragment_fd:
            content = yaml.safe_load(fragment_fd)

        return ChangelogFragment(content, path)

    @staticmethod
    def combine(fragments):
        """Combine fragments into a new fragment.
        :type fragments: list[ChangelogFragment]
        :rtype: dict[str, list[str] | str]
        """
        result = {}

        for fragment in fragments:
            for section, content in fragment.content.items():
                if isinstance(content, list):
                    if section not in result:
                        result[section] = []

                    result[section] += content
                else:
                    result[section] = content

        return result


class ChangelogConfig(object):
    """Configuration for changelogs."""
    def __init__(self, config):
        """
        :type config: dict
        """
        self.config = config

        self.notes_dir = self.config.get('notesdir', 'fragments')
        self.prelude_name = self.config.get('prelude_section_name', 'release_summary')
        self.prelude_title = self.config.get('prelude_section_title', 'Release Summary')
        self.new_plugins_after_name = self.config.get('new_plugins_after_name', '')
        self.release_tag_re = self.config.get('release_tag_re', r'((?:[\d.ab]|rc)+)')
        self.pre_release_tag_re = self.config.get('pre_release_tag_re', r'(?P<pre_release>\.\d+(?:[ab]|rc)+\d*)$')
        self.changes_file = self.config.get('changes_file', '.changes.yml')

        self.sections = collections.OrderedDict([(self.prelude_name, self.prelude_title)])

        for section_name, section_title in self.config['sections']:
            self.sections[section_name] = section_title

    def store(self, path):
        """
        :type path: str
        """
        config = {
            'notesdir': self.notes_dir,
            'changes_file': self.changes_file,
            'prelude_section_name': self.prelude_name,
            'prelude_section_title': self.prelude_title,
            'new_plugins_after_name': self.new_plugins_after_name,
            'release_tag_re': self.release_tag_re,
            'pre_release_tag_re': self.pre_release_tag_re,
            'sections': [],
        }
        for k, v in self.sections.items():
            if k == self.prelude_name and v == self.prelude_title:
                continue
            config['sections'].append([k, v])

        with open(path, 'wb') as f:
            yaml.safe_dump(config, f, default_flow_style=False, encoding='utf-8')

    @staticmethod
    def load(path):
        """
        :type path: str
        """
        with open(path, 'r') as config_fd:
            config = yaml.safe_load(config_fd)
        return ChangelogConfig(config)

    @staticmethod
    def default():
        config = {
            'changes_file': 'changelog.yml',
            'release_tag_re': r'(v(?:[\d.ab\-]|rc)+)',  # from Ansible's config.yml
            'pre_release_tag_re': r'(?P<pre_release>(?:[ab]|rc)+\d*)$',  # from Ansible's config.yml
            'new_plugins_after_name': 'removed_features',
            'sections': [
                ['major_changes', 'Major Changes'],
                ['minor_changes', 'Minor Changes'],
                ['deprecated_features', 'Deprecated Features'],
                ['removed_features', 'Removed Features (previously deprecated)'],
                ['bugfixes', 'Bugfixes'],
                ['known_issues', 'Known Issues'],
            ],
        }
        return ChangelogConfig(config)


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


class ChangesMetadata(object):
    """Read, write and manage change metadata."""
    def __init__(self, path):
        self.path = path
        self.data = self.empty()
        self.known_fragments = set()
        self.known_plugins = set()
        self.load()

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

        for version, config in self.releases.items():
            self.known_fragments |= set(config.get('fragments', []))

            for plugin_type, plugin_names in config.get('plugins', {}).items():
                self.known_plugins |= set('%s/%s' % (plugin_type, plugin_name) for plugin_name in plugin_names)

            module_names = config.get('modules', [])

            self.known_plugins |= set('module/%s' % module_name for module_name in module_names)

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

    def sort(self):
        """Sort change metadata in place."""
        for release, config in self.data['releases'].items():
            if 'fragments' in config:
                config['fragments'] = sorted(config['fragments'])

            if 'modules' in config:
                config['modules'] = sorted(config['modules'])

            if 'plugins' in config:
                for plugin_type in config['plugins']:
                    config['plugins'][plugin_type] = sorted(config['plugins'][plugin_type])

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

    def add_fragment(self, fragment_name, version):
        """Add a changelog fragment to the change metadata.
        :type fragment_name: str
        :type version: str
        """
        if fragment_name in self.known_fragments:
            return False

        self.known_fragments.add(fragment_name)

        if 'fragments' not in self.releases[version]:
            self.releases[version]['fragments'] = []

        fragments = self.releases[version]['fragments']
        fragments.append(fragment_name)
        return True

    def add_plugin(self, plugin_type, plugin_name, version):
        """Add a plugin to the change metadata.
        :type plugin_type: str
        :type plugin_name: str
        :type version: str
        """
        composite_name = '%s/%s' % (plugin_type, plugin_name)

        if composite_name in self.known_plugins:
            return False

        self.known_plugins.add(composite_name)

        if plugin_type == 'module':
            if 'modules' not in self.releases[version]:
                self.releases[version]['modules'] = []

            modules = self.releases[version]['modules']
            modules.append(plugin_name)
        else:
            if 'plugins' not in self.releases[version]:
                self.releases[version]['plugins'] = {}

            plugins = self.releases[version]['plugins']

            if plugin_type not in plugins:
                plugins[plugin_type] = []

            plugins[plugin_type].append(plugin_name)

        return True


if __name__ == '__main__':
    main()
