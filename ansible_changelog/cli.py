# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Changelog generator and linter."""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import argparse
import datetime
import logging
import os
import sys

try:
    import argcomplete
except ImportError:
    argcomplete = None

from .changelog_generator import generate_changelog
from .changes import load_changes, add_release
from .config import PathsConfig, ChangelogConfig
from .fragment import load_fragments, ChangelogFragmentLinter
from .plugins import load_plugins
from .utils import LOGGER, makedirs, load_galaxy_metadata


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


def command_init(args):
    """
    :type args: any
    """
    root = args.root  # type: str

    paths = set_paths(force=root)

    LOGGER.debug('Checking "{0}" for existance'.format(paths.galaxy_path))
    if not os.path.exists(paths.galaxy_path):
        LOGGER.error('The file galaxy.yml does not exists in the collection root!')
        sys.exit(3)
    LOGGER.debug('Checking "{0}" for existance'.format(paths.config_path))
    if os.path.exists(paths.config_path):
        LOGGER.error('A configuration file already exists at "{0}"!'.format(paths.config_path))
        sys.exit(3)

    galaxy = load_galaxy_metadata(paths)

    config = ChangelogConfig.default(
        title='{0}.{1}'.format(galaxy['namespace'].title(), galaxy['name'].title())
    )

    fragments_dir = os.path.join(paths.changelog_dir, config.notes_dir)
    try:
        makedirs(fragments_dir)
        print('Created fragments directory "{0}"'.format(fragments_dir))
    except Exception as e:
        LOGGER.error('Cannot create fragments directory "{0}"'.format(fragments_dir))
        LOGGER.info('Exception: {0}'.format(to_native(e)))
        sys.exit(3)

    try:
        config.store(paths.config_path)
        print('Created config file "{0}"'.format(paths.config_path))
    except Exception as e:
        LOGGER.error('Cannot create config file "{0}"'.format(paths.config_path))
        LOGGER.info('Exception: {0}'.format(to_native(e)))
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

    flatmap = True
    if paths.galaxy_path is not None:
        galaxy = load_galaxy_metadata(paths)
        flatmap = galaxy.get('type', '') == 'flatmap'

    if not version or not codename:
        if paths.galaxy_path is None:
            import ansible.release

            version = version or ansible.release.__version__
            codename = codename or ansible.release.__codename__

        elif not version:
            version = galaxy['version']

    changes = load_changes(paths, config)
    plugins = load_plugins(paths=paths, version=version, force_reload=reload_plugins)
    fragments = load_fragments(paths, config)
    add_release(config, changes, plugins, fragments, version, codename, date)
    generate_changelog(paths, config, changes, plugins, fragments, flatmap=flatmap)


def command_generate(args):
    """
    :type args: any
    """
    paths = set_paths()

    reload_plugins = args.reload_plugins  # type: bool

    config = ChangelogConfig.load(paths.config_path)

    flatmap = True
    if paths.galaxy_path is not None:
        galaxy = load_galaxy_metadata(paths)
        flatmap = galaxy.get('type', '') == 'flatmap'

    changes = load_changes(paths, config)
    if not changes.has_release:
        print('Cannot create changelog when not at least one release has been added.')
        sys.exit(2)
    plugins = load_plugins(paths=paths, version=changes.latest_version, force_reload=reload_plugins)
    fragments = load_fragments(paths, config)
    generate_changelog(paths, config, changes, plugins, fragments, flatmap=flatmap)


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


if __name__ == '__main__':
    main()
