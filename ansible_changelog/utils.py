# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import logging
import os
import re

import yaml


LOGGER = logging.getLogger('changelog')


def makedirs(path):
    """Make sure directory and parents exists and are directories.
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


def load_galaxy_metadata(paths):
    """Load galaxy.yml metadata.
    :type paths: PathsConfig
    :rtype: dict
    """
    with open(paths.galaxy_path, 'r') as galaxy_fd:
        return yaml.safe_load(galaxy_fd)


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
