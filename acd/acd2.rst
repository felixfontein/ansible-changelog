====================
ACD Changelog Mockup
====================

This is an example mockup of what the ACD changelog file could look like in RST.

.. contents::
  :local:
  :depth: 2

v2.10
=====

Ansible Base
------------

.. contents::
  :local:
  :depth: 5

Minor Changes
~~~~~~~~~~~~~

- 'Edit on GitHub' link for plugin, cli documentation fixed to navigate to correct plugin, cli source.
- A `vmware` module_defaults group has been added to simplify parameters for multiple VMware tasks. This group includes all VMware modules.
- Add 'auth_url' field to galaxy server config stanzas in ansible.cfg The url should point to the token_endpoint of a Keycloak server.
- Add --ask-vault-password and --vault-pass-file options to ansible cli commands
- Add ``--pre`` flag to ``ansible-galaxy collection install`` to allow pulling in the most recent pre-release version of a collection (https://github.com/ansible/ansible/issues/64905)
- Add a global toggle to control when vars plugins are executed (per task by default for backward compatibility or after importing inventory).
- Add a new config parameter, WIN_ASYNC_STARTUP_TIMEOUT, which allows configuration of the named pipe connection timeout under Windows when launching async tasks.
- Add a per-plugin stage option to override the global toggle to control the execution of individual vars plugins (per task, after inventory, or both).
- Add new magic variable ``ansible_collection`` that contains the collection name
- Add new magic variable ``ansible_role_name`` that contains the FQCN of the role
- Added invalid-argument-name spec in ansible-test.
- Added the ability to set ``DEFAULT_NO_TARGET_SYSLOG`` through the ``ansible_no_target_syslog`` variable on a task
- Ansible CLI fails with warning if extra_vars parameter is used with filename without @ sign (https://github.com/ansible/ansible/issues/51857).
- Ansible modules created with ``add_file_common_args=True`` added a number of undocumented arguments which were mostly there to ease implementing certain action plugins. The undocumented arguments ``src``, ``follow``, ``force``, ``content``, ``backup``, ``remote_src``, ``regexp``, ``delimiter``, and ``directory_mode`` are now no longer added. Modules relying on these options to be added need to specify them by themselves. Also, action plugins relying on these extra elements in ``FILE_COMMON_ARGUMENTS`` need to be adjusted.
- Ansible should fail with error when non-existing limit file is provided in command line.
- Ansible.Basic.cs - Added support for ``deprecated_aliases`` to deprecated aliases in a standard way
- Ansible.ModuleUtils.WebRequest - Move username and password aliases out of util to avoid option name collision
- Change order of arguments in ansible cli to use --ask-vault-password and --vault-password-file by default
- CollectionRequirement - Add a metadata property to update and retrieve the _metadata attribute.
- Enable Ansible Collections loader to discover and import collections from ``site-packages`` dir and ``PYTHONPATH``-added locations.
- Enable testing the AIX platform as a remote OS in ansible-test
- Ignore plesk-release file while parsing distribution release (https://github.com/ansible/ansible/issues/64101).
- Minor typo fixes in vmware_httpapi related modules and module_utils.
- Openstack inventory script is migrated to ansible-openstack-collection, adjusted the link in documentation accordingly.
- Openstack inventory script is moved to openstack.cloud from community.general.
- PowerShell Add-Type - Add an easier way to reference extra types when compiling C# code on PowerShell Core
- PowerShell Add-Type - Added the ``X86`` and ``AMD64`` preprocessor symbols for conditional compiling
- Provides additional information about collection namespace name restrictions (https://github.com/ansible/ansible/issues/65151).
- Raise error when no task file is provided to import_tasks (https://github.com/ansible/ansible/issues/54095).
- Removed extras_require support from setup.py (and [azure] extra). Requirements will float with the collections, so it's not appropriate for ansible-base to host requirements for them any longer.
- Simplify dict2items filter example in loop documentation (https://github.com/ansible/ansible/issues/65505).
- Update required library message with correct grammer in basic.py.
- Updated inventory script location for EC2, Openstack, and Cobbler after collection (https://github.com/ansible/ansible/issues/68897).
- Updates ``ansible_role_names``, ``ansible_play_role_names``, and ``ansible_dependent_role_names`` to include the FQCN
- Windows - Add a check for the minimum PowerShell version so we can create a friendly error message on older hosts
- Windows - add deprecation notice in the Windows setup module when running on Server 2008, 2008 R2, and Windows 7
- `AnsibleModule.fail_json()` has always required that a message be passed in which informs the end user why the module failed.  In the past this message had to be passed as the `msg` keyword argument but it can now be passed as the first positional argument instead.
- ``AnsibleModule.load_file_common_arguments`` now allows to simply override ``path``.
- add mechanism for storing warnings and deprecations globally and not attached to an ``AnsibleModule`` object (https://github.com/ansible/ansible/pull/58993)
- ansible-galaxy - Add ``download`` option for ``ansible-galaxy collection`` to download collections and their dependencies for an offline install
- ansible-galaxy - Add a `verify` subcommand to `ansible-galaxy collection`. The collection found on the galaxy server is downloaded to a tempfile to compare the checksums of the files listed in the MANIFEST.json and the FILES.json with the contents of the installed collection.
- ansible-galaxy - Added the ability to display the progress wheel through the C.GALAXY_DISPLAY_PROGRESS config option. Also this now defaults to displaying the progress wheel if stdout has a tty.
- ansible-galaxy - Added the ability to ignore further files and folders using a pattern with the ``build_ignore`` key in a collection's ``galaxy.yml`` (https://github.com/ansible/ansible/issues/59228).
- ansible-galaxy - Always ignore the ``tests/output`` directory when building a collection as it is used by ``ansible-test`` for test output (https://github.com/ansible/ansible/issues/59228).
- ansible-galaxy - add ``--token`` argument which is the same as ``--api-key`` (https://github.com/ansible/ansible/issues/65955)
- ansible-galaxy - add ``collection list`` command for listing installed collections (https://github.com/ansible/ansible/pull/65022)
- ansible-galaxy - add ``validate_collection_path()`` utility function ()
- ansible-galaxy - add collections path argument
- ansible-test - --docker flag now has an associated --docker-terminate flag which controls if and when the docker container is removed following tests
- ansible-test - Add a test to prevent ``state=get``
- ansible-test - Add a test to prevent ``state=list`` and ``state=info``
- ansible-test - Add a verbosity option for displaying warnings.
- ansible-test - Add support for Python 3.9.
- ansible-test - Added a ``ansible-test coverage analyze targets filter`` command to filter aggregated coverage reports by path and/or target name.
- ansible-test - Added a ``ansible-test coverage analyze targets`` command to analyze integration test code coverage by test target.
- ansible-test - General code cleanup.
- ansible-test - Refactor code to consolidate filesystem access and improve handling of encoding.
- ansible-test - Support writing compact JSON files instead of formatting and indenting the output.
- ansible-test - Update Ubuntu 18.04 test container to version 1.13 which includes ``venv``
- ansible-test - Update ``default-test-container`` to version 1.11, which includes Python 3.9.0a4.
- ansible-test - Upgrade OpenSUSE containers to use Leap 15.1.
- ansible-test - ``mutually_exclusive``, ``required_if``, ``required_by``, ``required_together`` and ``required_one_of`` in modules are now validated.
- ansible-test - add check for ``print()`` calls in modules and module_utils.
- ansible-test - added a ``--no-pip-check`` option
- ansible-test - added a ``--venv-system-site-packages`` option for use with the ``--venv`` option
- ansible-test - allow delegation config to specify equivalents to the ``--no-pip-check``, ``--disable-httptester`` and `--no-temp-unicode`` options
- ansible-test - extend alias validation.
- ansible-test - module validation will now consider arguments added by ``add_file_common_arguments=True`` correctly.
- ansible-test - switch from testing RHEL 8.0 and RHEL 8.1 Beta to RHEL 8.1
- ansible-test - the argument spec of modules is now validated by a YAML schema.
- ansible-test - the module validation code now checks whether ``elements`` documentation for options matches the argument_spec.
- ansible-test - the module validation code now checks whether ``elements`` is defined when ``type=list``
- ansible-test - the module validation code now checks whether ``requirement`` for options is documented correctly.
- ansible-test defaults to redacting sensitive values (disable with the ``--no-redact`` option)
- ansible-test no longer detects ``git`` submodule directories as files.
- ansible-test no longer provides a ``--tox`` option. Use the ``--venv`` option instead. This only affects testing the Ansible source. The feature was never available for Ansible Collections or when running from an Ansible install.
- ansible-test no longer tries to install sanity test dependencies on unsupported Python versions
- ansible-test now checks for the minimum and maximum supported versions when importing ``coverage``
- ansible-test now has a ``--list-files`` option to list files using the ``env`` command.
- ansible-test now places the ansible source and collections content in separate directories when using the ``--docker`` or ``--remote`` options.
- ansible-test now provides a more helpful error when loading coverage files created by ``coverage`` version 5 or later
- ansible-test now supports provisioning of network resources when testing network collections
- ansible-test now supports skip aliases in the format ``skip/{arch}/{platform}`` and ``skip/{arch}/{platform}/{version}`` where ``arch`` can be ``power``. These aliases are only effective for the ``--remote`` option.
- ansible-test now supports skip aliases in the format ``skip/{platform}/{version}`` for the ``--remote`` option. This is preferred over the older ``skip/{platform}{version}`` format which included no ``/`` between the platform and version.
- ansible-test now supports testing against RHEL 7.8 when using the ``--remote`` option.
- ansible-test now supports the ``--remote power/centos/7`` platform option.
- ansible-test provides clearer error messages when failing to detect the provider to use with the ``--remote`` option.
- ansible-test provisioning of network devices for ``network-integration`` has been updated to use collections.
- ansible_native_concat() - use ``to_text`` function rather than Jinja2's ``text_type`` which has been removed in Jinja2 master branch.
- apt - Implemented an exponential backoff behaviour when retrying to update the cache with new params ``update_cache_retry_max_delay`` and ``update_cache_retries`` to control the behavior.
- apt_repository - Implemented an exponential backoff behaviour when retrying to update the apt cache with new params ``update_cache_retry_max_delay`` and ``update_cache_retries`` to control the behavior.
- callbacks - Allow modules to return `None` as before/after entries for diff. This should make it easier for modules to report the "not existing" state of the entity they touched.
- combine filter - now accept a ``list_merge`` argument which modifies its behaviour when the hashes to merge contain arrays/lists.
- core filters - Adding ``path_join`` filter to the core filters list
- dnf - Properly handle idempotent transactions with package name wildcard globs (https://github.com/ansible/ansible/issues/62809)
- dnf - Properly handle module AppStreams that don't define stream (https://github.com/ansible/ansible/issues/63683)
- file - specifying ``src`` without ``state`` is now an error
- get_bin_path() - change the interface to always raise ``ValueError`` if the command is not found (https://github.com/ansible/ansible/pull/56813)
- get_url - Remove deprecated string format support for the headers option (https://github.com/ansible/ansible/issues/61891)
- git - added an ``archive_prefix`` option to set a prefix to add to each file path in archive
- host_group_vars plugin - Require whitelisting and whitelist by default.
- netbox - use inventory cache if configured
- new magic variable - ``ansible_config_file`` - full path of used Ansible config file
- package_facts.py - Add support for Pacman package manager.
- plugin loader - Add MODULE_IGNORE_EXTS config option to skip over certain extensions when looking for script and binary modules.
- powershell (shell plugin) - Fix `join_path` to support UNC paths (https://github.com/ansible/ansible/issues/66341)
- regexp_replace filter - add multiline support for regex_replace filter (https://github.com/ansible/ansible/issues/61985)
- rename ``_find_existing_collections()`` to ``find_existing_collections()`` to reflect its use across multiple files

- reorganized code for the ``ansible-test coverage`` command for easier maintenance and feature additions
- tests - Add new ``truthy`` and ``falsy`` jinja2 tests to evaluate the truthiness or falsiness of a value
- to_nice_json filter - Removed now-useless exception handler
- to_uuid - add a named parameter to let the user optionally set a custom namespace
- update ansible-test default-test-container from version 1.9.1 to 1.9.2
- update ansible-test default-test-container from version 1.9.2 to 1.9.3
- update ansible-test default-test-container from version 1.9.3 to 1.10.1
- url_lookup_plugin - add parameters to match what is available in ``module_utils/urls.py``
- user - allow groups, append parameters with local
- user - usage of ``append: True`` without setting a list of groups. This is currently a no-op with a warning, and will change to an error in 2.14. (https://github.com/ansible/ansible/pull/65795)
- validation - Sort missing parameters in exception message thrown by check_required_arguments
- vars plugins - Support vars plugins in collections by adding the ability to whitelist plugins.
- vars_prompt - throw error when encountering unsupported key
- win_command, win_shell - Add the ability to override the console output encoding with ``output_encoding_override`` - https://github.com/ansible/ansible/issues/54896
- win_disk_facts - Adds Win32_DiskDrive class object as `win32_disk_drive` key to return of the module
- win_disk_facts - Set output array order to be by disk number property - https://github.com/ansible/ansible/issues/63998
- win_domain_user - Added the ``identity`` module option to explicitly set the identity of the user when searching for it - https://github.com/ansible/ansible/issues/45298
- win_firewall- Change req check from wmf version to cmdlets presence - https://github.com/ansible/ansible/issues/63003
- win_firewall_rule - add parameter to support ICMP Types and Codes (https://github.com/ansible/ansible/issues/46809)
- win_group_membership - Add multi-domain forest support - https://github.com/ansible/ansible/issues/59829
- win_iis_webapplication - add new options ``connect_as``, ``username``, ``password``.
- win_iis_webapplication - now uses the current application pool of the website instead of the DefaultAppPool if none was specified.
- win_nssm - Implement additional parameters - (https://github.com/ansible/ansible/issues/62620)
- win_package - Added proxy support for retrieving packages from a URL - https://github.com/ansible/ansible/issues/43818
- win_package - Added support for ``.appx``, ``.msix``, ``.appxbundle``, and ``.msixbundle`` package - https://github.com/ansible/ansible/issues/50765
- win_package - Added support for ``.msp`` packages - https://github.com/ansible/ansible/issues/22789
- win_package - Added support for specifying the HTTP method when getting files from a URL - https://github.com/ansible/ansible/issues/35377
- win_package - Read uninstall strings from the ``QuietUninstallString`` if present to better support argumentless uninstalls of registry based packages.
- win_package - Scan packages in the current user's registry hive - https://github.com/ansible/ansible/issues/45950
- win_pester - Only execute ``*.tests.ps1`` in ``path`` to match the default behaviour in Pester - https://github.com/ansible/ansible/issues/55736
- windows collections - Support relative module util imports in PowerShell modules and module_utils

Deprecated Features
~~~~~~~~~~~~~~~~~~~

- hash_behaviour - Deprecate ``hash_behaviour`` for future removal.
- script inventory plugin - The 'cache' option is deprecated and will be removed in 2.12. Its use has been removed from the plugin since it has never had any effect.

Removed Features (previously deprecated)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- core - remove support for ``check_invalid_arguments`` in ``AnsibleModule``, ``AzureModule`` and ``UTMModule``.

Bugfixes
~~~~~~~~

- **security issue** - Convert CLI provided passwords to text initially, to prevent unsafe context being lost when converting from bytes->text during post processing of PlayContext. This prevents CLI provided passwords from being incorrectly templated (CVE-2019-14856)

- **security issue** - Redact cloud plugin secrets in ansible-test when running integration tests using cloud plugins. Only present in 2.9.0b1.

- **security issue** - TaskExecutor - Ensure we don't erase unsafe context in TaskExecutor.run on bytes. Only present in 2.9.0beta1 (https://github.com/ansible/ansible/issues/62237)

- **security issue** - The ``subversion`` module provided the password via the svn command line option ``--password`` and can be retrieved from the host's /proc/<pid>/cmdline file. Update the module to use the secure ``--password-from-stdin`` option instead, and add a warning in the module and in the documentation if svn version is too old to support it. (CVE-2020-1739)

- **security issue** - Update ``AnsibleUnsafeText`` and ``AnsibleUnsafeBytes`` to maintain unsafe context by overriding ``.encode`` and ``.decode``. This prevents future issues with ``to_text``, ``to_bytes``, or ``to_native`` removing the unsafe wrapper when converting between string types (CVE-2019-14856)

- **security issue** - properly hide parameters marked with ``no_log`` in suboptions when invalid parameters are passed to the module (CVE-2019-14858)
- **security issue** win_unzip - normalize paths in archive to ensure extracted files do not escape from the target directory (CVE-2020-1737)

- **security_issue** - create temporary vault file with strict permissions when editing and prevent race condition (CVE-2020-1740)
- ActionBase - Add new ``cleanup`` method that is explicitly run by the ``TaskExecutor`` to ensure that the shell plugins ``tmpdir`` is always removed. This change means that individual action plugins need not be responsible for removing the temporary directory, which ensures that we don't have code paths that accidentally leave behind the temporary directory.
- Add missing gcp modules to gcp module defaults group
- Added support for OSMC distro in hostname module (https://github.com/ansible/ansible/issues/66189).
- Allow tasks to notify a fqcn handler name (https://github.com/ansible/ansible/issues/68181)
- An invalid value is hard to track down if you don't know where it came from, return field name instead.
- Ansible.Basic - Fix issue when setting a ``no_log`` parameter to an empty string - https://github.com/ansible/ansible/issues/62613
- Ansible.ModuleUtils.WebRequest - actually set no proxy when ``use_proxy: no`` is set on a Windows module - https://github.com/ansible/ansible/issues/68528
- AnsibleDumper - Add a representer for AnsibleUnsafeBytes (https://github.com/ansible/ansible/issues/62562).
- AnsibleModule.run_command() - set ``close_fds`` to ``False`` on Python 2 if ``pass_fds`` are passed to ``run_command()``. Since ``subprocess.Popen()`` on Python 2 does not have the ``pass_fds`` option, there is no way to exclude a specific list of file descriptors from being closed.

- By passing the module_tmpdir as a parameter in the write_ssh_wrapper function instead of initalizing module_tmpdir via get_module_path()
- CLI - the `ANSIBLE_PLAYBOOK_DIR` envvar or `playbook_dir` config can now substitute for the --playbook-dir arg on CLIs that support it (https://github.com/ansible/ansible/issues/59464)
- Check NoneType for raw_params before proceeding in include_vars (https://github.com/ansible/ansible/issues/64939).
- Collections - Allow a collection role to call a stand alone role, without needing to explicitly add ``ansible.legacy`` to the collection search order within the collection role. (https://github.com/ansible/ansible/issues/69101)
- Create an ``import_module`` compat util, for use across the codebase, to allow collection loading to work properly on Python26
- DUPLICATE_YAML_DICT_KEY - Fix error output when configuration option DUPLICATE_YAML_DICT_KEY is set to error (https://github.com/ansible/ansible/issues/65366)
- Ensure DataLoader temp files are removed at appropriate times and that we observe the LOCAL_TMP setting.
- Ensure we don't allow ansible_facts subkey of ansible_facts to override top level, also fix 'deprefixing' to prevent key transforms.
- Ensure we get an error when creating a remote tmp if it already exists. CVE-2020-1733
- Fact Delegation - Add ability to indicate which facts must always be delegated. Primarily for ``discovered_interpreter_python`` right now, but extensible later. (https://github.com/ansible/ansible/issues/61002)
- Fix a bug when a host was not removed from a play after ``meta: end_host`` and as a result the host was still present in ``ansible_play_hosts`` and ``ansible_play_batch`` variables.
- Fix case sensitivity for ``lookup()`` (https://github.com/ansible/ansible/issues/66464)
- Fix collection install error that happened if a dependency specified dependencies to be null (https://github.com/ansible/ansible/issues/67574).
- Fix https://github.com/ansible/galaxy-dev/issues/96 Add support for automation-hub authentication to ansible-galaxy
- Fix incorrect "Could not match supplied host pattern" warning (https://github.com/ansible/ansible/issues/66764)
- Fix issue git module cannot use custom `key_file` or `ssh_opts` as non-root user on system with noexec `/tmp` (https://github.com/ansible/ansible/issues/30064).
- Fix issue git module ignores remote_tmp (https://github.com/ansible/ansible/issues/33947).
- Fix issue where the collection loader tracebacks if ``collections_paths = ./`` is set in the config
- Fix issue with callbacks ``set_options`` method that was not called with collections
- Fix label lookup in the default callback for includes (https://github.com/ansible/ansible/issues/65904)
- Fix regression when ``ansible_failed_task`` and ``ansible_failed_result`` are not defined in the rescue block (https://github.com/ansible/ansible/issues/64789)
- Fix string parsing of inline vault strings for plugin config variable sources
- Fix traceback when printing ``HostVars`` on native Jinja2 (https://github.com/ansible/ansible/issues/65365)
- Fixes in network action plugins load from collections using module prefix (https://github.com/ansible/ansible/issues/65071)
- Force collection names to be static so that a warning is generated because templating currently does not work (see https://github.com/ansible/ansible/issues/68704).
- Handle empty extra vars in ansible cli (https://github.com/ansible/ansible/issues/61497).
- Handle exception encountered while parsing the argument description in module when invoked via ansible-doc command (https://github.com/ansible/ansible/issues/60587).
- Handle exception when /etc/shadow file is missing or not found, while operating user operation in user module (https://github.com/ansible/ansible/issues/63490).
- HostVarsVars - Template the __repr__ value (https://github.com/ansible/ansible/issues/64128).
- In fetch action, avoid using slurp return to set up dest, also ensure no dir traversal CVE-2020-1735.
- Make netconf plugin configurable to set ncclient device handler name in netconf plugin (https://github.com/ansible/ansible/pull/65718)
- Misc typo fixes in various documentation pages.
- Module arguments in suboptions which were marked as deprecated with ``removed_in_version`` did not result in a warning.
- On HTTP status code 304, return status_code
- Prevent rewriting nested Block's data in filter_tagged_tasks
- Prevent templating unused variables for {% include %} (https://github.com/ansible/ansible/issues/68699)
- Remove a temp directory created by wait_for_connection action plugin (https://github.com/ansible/ansible/issues/62407).
- Remove the unnecessary warning about aptitude not being installed (https://github.com/ansible/ansible/issues/56832).
- Replace parameter 'message' with appropriate parameter name in several modules, as 'message' is used internally in Ansible Core engine (https://github.com/ansible/ansible/issues/39295).
- RoleRequirement - include stderr in the error message if a scm command fails (https://github.com/ansible/ansible/issues/41336)
- Skipping of become for ``network_cli`` connections now works when ``network_cli`` is sourced from a collection.
- Strictly check string datatype for 'tasks_from', 'vars_from', 'defaults_from', and 'handlers_from' in include_role (https://github.com/ansible/ansible/issues/68515).
- Support virtualization for podman container (https://github.com/ansible/ansible/issues/64954).
- TaskQueueManager - Explicitly set the mutliprocessing start method to ``fork`` to avoid issues with the default on macOS now being ``spawn``.
- Templating - Ansible was caching results of Jinja2 expressions in some cases where these expressions could have dynamic results, like password generation (https://github.com/ansible/ansible/issues/34144).
- The ansible-galaxy publish command was using an incorrect URL for v3 servers. The configuration for v3 servers includes part of the path fragment that was added in the new test.
- Update ActionBase._low_level_execute_command to honor executable (https://github.com/ansible/ansible/issues/68054)
- Update the warning message for ``CONDITIONAL_BARE_VARS`` to list the original conditional not the value of the original conditional (https://github.com/ansible/ansible/issues/67735)
- Use hostnamectl command to get current hostname for host while using systemd strategy (https://github.com/ansible/ansible/issues/59438).
- Using --start-at-task would fail when it attempted to skip over tasks with no name.
- ``AnsibleUnsafe``/``AnsibleContext``/``Templar`` - Do not treat ``AnsibleUndefined`` as being "unsafe" (https://github.com/ansible/ansible/issues/65198)
- account for empty strings in when splitting the host pattern (https://github.com/ansible/ansible/issues/61964)
- adhoc CLI - when playbook-dir is specified and inside a collection, use default collection logic to resolve modules/actions
- allow external collections to be created in the 'ansible' collection namespace (https://github.com/ansible/ansible/issues/59988)
- also strip spaces around config values in pathlist as we do in list types
- ansible command now correctly sends v2_playbook_on_start to callbacks
- ansible-connection persists even after playbook run is completed (https://github.com/ansible/ansible/pull/61591)
- ansible-doc now properly handles removed modules/plugins
- ansible-galaxy - Default collection install path to first path in COLLECTIONS_PATHS (https://github.com/ansible/ansible/pull/62870)
- ansible-galaxy - Display proper error when invalid token is used for Galaxy servers
- ansible-galaxy - Ensure we preserve the new URL when appending ``/api`` for the case where the GET succeeds on galaxy.ansible.com
- ansible-galaxy - Error when install finds a tar with a file that will be extracted outside the collection install directory - CVE-2020-10691
- ansible-galaxy - Expand the ``User-Agent`` to include more information and add it to more calls to Galaxy endpoints.
- ansible-galaxy - Fix ``collection install`` when installing from a URL or a file - https://github.com/ansible/ansible/issues/65109
- ansible-galaxy - Fix issue when compared installed dependencies with a collection having no ``MANIFEST.json`` or an empty version string in the json
- ansible-galaxy - Fix pagination issue when retrieving role versions for install - https://github.com/ansible/ansible/issues/64355
- ansible-galaxy - Fix up pagination searcher for collection versions on Automation Hub
- ansible-galaxy - Fix url building to not truncate the URL (https://github.com/ansible/ansible/issues/61624)
- ansible-galaxy - Handle the different task resource urls in API responses from publishing collection artifacts to galaxy servers using v2 and v3 APIs.
- ansible-galaxy - Remove uneeded verbose messages when accessing local token file
- ansible-galaxy - Return the HTTP code reason if no error msg was returned by the server - https://github.com/ansible/ansible/issues/64850
- ansible-galaxy - Send SHA256 hashes when publishing a collection
- ansible-galaxy - Set ``User-Agent`` to Ansible version when interacting with Galaxy or Automation Hub
- ansible-galaxy - Treat the ``GALAXY_SERVER_LIST`` config entry that is defined but with no values as an empty list
- ansible-galaxy - Utilize ``Templar`` for templating skeleton files, so that they have access to Ansible filters/tests/lookups (https://github.com/ansible/ansible/issues/69104)
- ansible-galaxy - fix a bug where listing a specific role if it was not in the first path failed to find the role

- ansible-galaxy - fix regression that prenented roles from being listed
- ansible-galaxy - properly list roles when the role name also happens to be in the role path (https://github.com/ansible/ansible/issues/67365)
- ansible-galaxy - properly show the role description when running offline (https://github.com/ansible/ansible/issues/60167)
- ansible-galaxy cli - fixed ``--version`` argument
- ansible-galaxy collection - Preserve executable bit on build and preserve mode on install from what tar member is set to - https://github.com/ansible/ansible/issues/68415
- ansible-galaxy role - Fix issue where ``--server`` was not being used for certain ``ansible-galaxy role`` actions - https://github.com/ansible/ansible/issues/61609
- ansible-inventory - Fix long standing bug not loading vars plugins for group vars relative to the playbook dir when the '--playbook-dir' and '--export' flags are used together.
- ansible-inventory - Fix regression loading vars plugins. (https://github.com/ansible/ansible/issues/65064)
- ansible-inventory - Properly hide arguments that should not be shown (https://github.com/ansible/ansible/issues/61604)
- ansible-inventory - Restore functionality to allow ``--graph`` to be limited by a host pattern
- ansible-test - Do not warn on missing PowerShell or C# util that are in other collections
- ansible-test - Fix PowerShell module util analysis to properly detect the names of a util when running in a collection
- ansible-test - Fix regression introduced in https://github.com/ansible/ansible/pull/67063 which caused module_utils analysis to fail on Python 2.x.
- ansible-test - Fix traceback in validate-modules test when argument_spec is None.
- ansible-test - Make sure import sanity test virtual environments also remove ``pkg-resources`` if it is not removed by uninstalling ``setuptools``.
- ansible-test - Remove out-of-date constraint on installing paramiko versions 2.5.0 or later in tests.
- ansible-test - The shebang sanity test now correctly identifies modules in subdirectories in collections.
- ansible-test - Updated Python constraints for installing ``coverage`` to resolve issues on multiple Python versions when using the ``--coverage`` option.
- ansible-test - Updated requirements to limit ``boto3`` and ``botocore`` versions on Python 2.6 to supported versions.
- ansible-test - Use ``virtualenv`` versions before 20 on provisioned macOS instances to remain compatible with an older pip install.
- ansible-test - bump version of ACME test container. The new version includes updated dependencies.
- ansible-test - during module validation, handle add_file_common_args only for top-level arguments.
- ansible-test - during module validation, improve alias handling.
- ansible-test - improve ``deprecate()`` call checker.
- ansible-test can now install argparse with ``--requirements`` or delegation when the pip version in use is older than version 7.1
- ansible-test change detection - Run only sanity tests on ``docs/`` and ``changelogs/`` in collections, to avoid triggering full CI runs of integration and unit tests when files in these directories change.
- ansible-test coverage - Fix the ``--all`` argument when generating coverage reports - https://github.com/ansible/ansible/issues/62096
- ansible-test import sanity test now consistently reports errors against the file being tested.
- ansible-test import sanity test now consistently reports warnings as errors.
- ansible-test import sanity test now properly handles relative imports.
- ansible-test import sanity test now properly invokes Ansible modules as scripts.
- ansible-test is now able to find its ``egg-info`` directory when it contains the Ansible version number
- ansible-test no longer errors reporting coverage when no Python coverage exists. This fixes issues reporting on PowerShell only coverage from collections.
- ansible-test no longer fails when downloading test results for a collection without a ``tests`` directory when using the ``--docker`` option.
- ansible-test no longer optimizes setting ``PATH`` by prepending the directory containing the selected Python interpreter when it is named ``python``. This avoids unintentionally making other programs available on ``PATH``, including an already installed version of Ansible.
- ansible-test no longer tracebacks during change analysis due to processing an empty python file
- ansible-test no longer tries to install ``coverage`` 5.0+ since those versions are unsupported
- ansible-test no longer tries to install ``setuptools`` 45+ on Python 2.x since those versions are unsupported
- ansible-test now correctly collects code coverage on the last task in a play. This should resolve issues with missing code coverage, empty coverage files and corrupted coverage files resulting from early worker termination.
- ansible-test now correctly enumerates submodules when a collection resides below the repository root
- ansible-test now correctly excludes the test results temporary directory when copying files from the remote test system to the local system
- ansible-test now correctly includes inventory files ignored by git when running tests with the ``--docker`` option
- ansible-test now correctly installs the requirements specified by the collection's unit and integration tests instead of the requirements specified for Ansible's own unit and integration tests
- ansible-test now correctly recognizes imports in collections when using the ``--changed`` option.
- ansible-test now correctly rewrites coverage paths for PowerShell files when testing collections
- ansible-test now creates its integration test temporary directory within the collection so ansible-playbook can properly detect the default collection
- ansible-test now enables color ``ls`` on a remote host only if the host supports the feature
- ansible-test now ignores empty ``*.py`` files when analyzing module_utils imports for change detection
- ansible-test now ignores version control within subdirectories of collections. Previously this condition was an error.
- ansible-test now ignores warnings when comparing pip versions before and after integration tests run
- ansible-test now installs the correct version of ``cryptography`` with ``--requirements`` or delegation when setuptools is older than version 18.5
- ansible-test now limits Jinja2 installs to version 2.10 and earlier on Python 2.6
- ansible-test now limits ``pathspec`` to versions prior to 0.6.0 on Python 2.6 to avoid installation errors
- ansible-test now limits installation of ``hcloud`` to Python 2.7 and 3.5 - 3.8 since other versions are unsupported
- ansible-test now limits the version of ``setuptools`` on Python 2.6 to versions older than 37
- ansible-test now loads the collection loader plugin early enough for ansible_collections imports to work in unit test conftest.py modules
- ansible-test now preserves existing SSH authorized keys when provisioning a remote host
- ansible-test now properly activates the vcenter plugin for vcenter tests when docker is available
- ansible-test now properly activates virtual environments created using the --venv option
- ansible-test now properly creates a virtual environment using ``venv`` when running in a ``virtualenv`` created virtual environment
- ansible-test now properly excludes the ``tests/output/`` directory from code coverage
- ansible-test now properly handles creation of Python execv wrappers when the selected interpreter is a script
- ansible-test now properly handles enumeration of git submodules. Enumeration is now done with ``git submodule status --recursive`` without specifying ``.`` for the path, since that could cause the command to fail. Instead, relative paths outside the current directory are filtered out of the results. Errors from ``git`` commands will now once again be reported as errors instead of warnings.
- ansible-test now properly handles warnings for removed modules/plugins
- ansible-test now properly ignores the ``tests/output//`` directory when not using git
- ansible-test now properly installs requirements for multiple Python versions when running sanity tests
- ansible-test now properly recognizes modules and module_utils in collections when using the ``blacklist`` plugin for the ``pylint`` sanity test
- ansible-test now properly registers its own code in a virtual environment when running from an install
- ansible-test now properly reports import errors for collections when running the import sanity test
- ansible-test now properly searches for ``pythonX.Y`` instead of ``python`` when looking for the real python that created a ``virtualenv``
- ansible-test now properly sets PYTHONPATH for tests when running from an Ansible installation
- ansible-test now properly sets ``ANSIBLE_PLAYBOOK_DIR`` for integration tests so unqualified collection references work for adhoc ``ansible`` usage
- ansible-test now properly uses a fresh copy of environment variables for each command invocation to avoid mixing vars between commands
- ansible-test now shows sanity test doc links when installed (previously the links were only visible when running from source)
- ansible-test now shows the correct source path instead of ``%s`` for collection role based test targets when the ``-v`` option is used
- ansible-test now supports submodules using older ``git`` versions which require querying status from the top level directory of the repo.
- ansible-test now updates SSH keys it generates with newer versions of ssh-keygen to function with Paramiko
- ansible-test now upgrades ``pip`` with `--requirements`` or delegation as needed when the pip version in use is older than version 7.1
- ansible-test now uses GNU tar format instead of the Python default when creating payloads for remote systems
- ansible-test now uses modules from the ``ansible.windows`` collection for setup and teardown of ``windows-integration`` tests and code coverage
- ansible-test once again properly collects code coverage for ``ansible-connection``
- ansible-test validate-modules - Fix arg spec collector for PowerShell to find utils in both a collection and base.
- ansible-test validate-modules sanity test code ``missing-module-utils-import-c#-requirements`` is now ``missing-module-utils-import-csharp-requirements`` (fixes ignore bug).
- ansible-test validate-modules sanity test code ``multiple-c#-utils-per-requires`` is now ``multiple-csharp-utils-per-requires`` (fixes ignore bug).
- ansible-test validate-modules sanity test now checks for AnsibleModule initialization instead of module_utils imports, which did not work in many cases.
- ansible-test validate-modules sanity test now properly handles collections imports using the Ansible collection loader.
- ansible-test validate-modules sanity test now properly handles relative imports.
- ansible-test validate-modules sanity test now properly handles sys.exit in modules.
- ansible-test validate-modules sanity test now properly invokes Ansible modules as scripts.
- ansible-test windows coverage - Ensure coverage reports are UTF-8 encoded without a BOM
- ansible-test windows coverage - Output temp files as UTF-8 with BOM to standardise against non coverage runs
- ansible-vault - Fix ``encrypt_string`` output in a tty when using ``--sdtin-name`` option (https://github.com/ansible/ansible/issues/65121)
- ansible-vault create - Fix exception on no arguments given
- apt - Fixed the issue the cache being updated while auto-installing its dependencies even when ``update_cache`` is set to false.
- become - Fix various plugins that still used play_context to get the become password instead of through the plugin - https://github.com/ansible/ansible/issues/62367
- clean_facts - use correct variable to avoid unnecessary handling of ``AttributeError``
- code - removes some Python compatibility code for dealing with socket timeouts in ``wait_for``
- collection loader - ensure Jinja function cache is fully-populated before lookup
- collection loader - fixed relative imports on Python 2.7, ensure pluginloader caches use full name to prevent names from being clobbered (https://github.com/ansible/ansible/pull/60317)
- collection_loader - sort Windows modules below other plugin types so the correct builtin plugin inside a role is selected (https://github.com/ansible/ansible/issues/65298)
- collections - Handle errors better for filters and tests in collections, where a non-existent collection is specified, or importing the plugin results in an exception (https://github.com/ansible/ansible/issues/66721)
- combine filter - ``[dict1, [dict2]] | combine`` now raise an error; previously ``combine`` had an undocumented behaviour where it was flattening the list before combining it (https://github.com/ansible/ansible/pull/57894#discussion_r339517518).
- config - encoding failures on config values should be non-fatal (https://github.com/ansible/ansible/issues/63310)
- copy - Fixed copy module not working in case that remote_src is enabled and dest ends in a / (https://github.com/ansible/ansible/pull/47238)
- copy - recursive copy with ``remote_src=yes`` now recurses beyond first level. (Fixes https://github.com/ansible/ansible/issues/58284)
- core - remove unneeded Python version checks.
- core - replace a compatibility import of pycompat24.literal_eval with ast.literal_eval.
- core filters - fix ``extract()`` filter when key does not exist in container (https://github.com/ansible/ansible/issues/64957)
- cron and cronvar - use get_bin_path utility to locate the default crontab executable instead of the hardcoded /usr/bin/crontab. (https://github.com/ansible/ansible/pull/59765)
- cron cronvar - only run ``get_bin_path()`` once
- cronvar - use correct binary name (https://github.com/ansible/ansible/issues/63274)
- deal with cases in which just a file is pased and not a path with directories, now fileglob correctly searches in 'files/' subdirs.
- debug - fixed an issue introduced in Ansible 2.4 where a loop of debug tasks would lose the "changed" status on each item.
- display - Improve method of removing extra new line after warnings so it does not break Tower/Runner (https://github.com/ansible/ansible/pull/68517)
- display - remove extra new line after warnings (https://github.com/ansible/ansible/pull/65199)
- display - remove leading space when displaying WARNING messages
- display logging - Fix issue where 3rd party modules will print tracebacks when attempting to log information when ``ANSIBLE_LOG_PATH`` is set - https://github.com/ansible/ansible/issues/65249
- display logging - Fixed up the logging formatter to use the proper prefixes for ``u=user`` and ``p=process``
- display logging - Re-added the ``name`` attribute to the log formatter so that the source of the log can be seen
- dnf - Fix idempotence of `state: installed` (https://github.com/ansible/ansible/issues/64963)
- dnf - remove custom ``fetch_rpm_from_url`` method in favor of more general ``ansible.module_utils.urls.fetch_file``.
- dnf module - Ensure the modules exit_json['msg'] response is always string, not sometimes a tuple.
- docker_node_info - improve error handling when service inspection fails, for example because node name being ambiguous (https://github.com/ansible/ansible/issues/63353, PR https://github.com/ansible/ansible/pull/63418).
- ecs_certificate - Always specify header ``connection: keep-alive`` for ECS API connections.
- env lookup plugin - Fix handling of environment variables values containing utf-8 characters. (https://github.com/ansible/ansible/issues/65298)
- fact gathering - Display warnings and deprecation messages that are created during the fact gathering phase
- facts - fix detection of virtualization type when dmi product name is KVM Server
- file - Removed unreachable code in module
- file - change ``_diff_peek`` in argument spec to be the correct type, which is ``bool`` (https://github.com/ansible/ansible/issues/59433)
- find - clarify description of ``contains`` (https://github.com/ansible/ansible/issues/61983)
- fix wrong command line length calculation in ``ansible-console`` when long command inputted
- fixed issues when using net_get & net_put before the persistent connection has been started
- for those running uids for invalid users (containers), fallback to uid=<uid> when logging fixes #68007
- free strategy - Include failed hosts when filtering notified hosts for handlers. The strategy base should determine whether or not to run handlers on those hosts depending on whether forcing handlers is enabled (https://github.com/ansible/ansible/issues/65254).
- galaxy - Fix an AttributeError on ansible-galaxy install with an empty requirements.yml (https://github.com/ansible/ansible/issues/66725).
- get_url - Don't treat no checksum as a checksum match (https://github.com/ansible/ansible/issues/61978)
- get_url pass incorrect If-Modified-Since header (https://github.com/ansible/ansible/issues/67417)
- git - when force=True, apply --force flag to git fetches as well
- group - The group module was not correctly detecting whether a local group is existing or not with local set to yes if the same group exists in a non local group repository e.g. LDAP. (https://github.com/ansible/ansible/issues/58619)

- hcloud - Added missing host variables in Compose section
- hostname - Fixed an issue where the hostname on the cloudlinux 6 server could not be set.
- hostname - make module work on Manjaro Linux (https://github.com/ansible/ansible/issues/61382)
- include_vars - fix stack trace when passing ``dirs`` in an ad-hoc command (https://github.com/ansible/ansible/issues/62633)
- lineinfile - don't attempt mkdirs when path doesn't contain directory path
- lineinfile - fix bug that caused multiple line insertions (https://github.com/ansible/ansible/issues/58923).
- lineinfile - properly handle inserting a line when backrefs are enabled and the line already exists in the file (https://github.com/ansible/ansible/issues/63756)
- lineinfile - use correct index value when inserting a line at the end of a file (https://github.com/ansible/ansible/issues/63684)
- loops - Do not indiscriminately mark loop items as unsafe, only apply unsafe to ``with_`` style loops. The items from ``loop`` should not be explicitly wrapped in unsafe. The underlying templating mechanism should dictate this. (https://github.com/ansible/ansible/issues/64379)
- make ``no_log=False`` on a module option silence the ``no_log`` warning (https://github.com/ansible/ansible/issues/49465 https://github.com/ansible/ansible/issues/64656)
- module executor - Address issue where changes to Ansiballz module code, change the behavior of module execution as it pertains to ``__file__`` and ``sys.modules`` (https://github.com/ansible/ansible/issues/64664)
- mysql - dont mask ``mysql_connect`` function errors from modules (https://github.com/ansible/ansible/issues/64560).
- openssl_certificate - When provider is ``entrust``, use a ``connection: keep-alive`` header for ECS API connections.
- package_facts - fix value of ``vital`` attribute which is returned when ``pkg`` manager is used
- package_facts - use module warnings rather than a custom implementation for reporting warnings
- packaging_yum - replace legacy file handling with a file manager.
- paramiko - catch and handle exception to prevent stack trace when running in FIPS mode
- paramiko_ssh - improve authentication error message so it is less confusing
- paramiko_ssh - optimized file handling by using a context manager.
- pip - The virtualenv_command option can now include arguments without requiring the full path to the binary. (https://github.com/ansible/ansible/issues/52275)
- pip - check_mode with ``state: present`` now returns the correct state for pre-release versioned packages
- plugins - Allow ensure_type to decrypt the value for string types (and implicit string types) when value is an inline vault.
- postgresql_user - allow to pass user name which contains dots (https://github.com/ansible/ansible/issues/63204).
- psexec - Fix issue where the Kerberos package was not detected as being available.
- psexec - Fix issue where the ``interactive`` option was not being passed down to the library.
- reboot, win_reboot - add ``boot_time_command`` parameter to override the default command used to determine whether or not a system was rebooted (https://github.com/ansible/ansible/issues/58868)
- replace use of deprecated functions from ``ansible.module_utils.basic``.
- roles - Ensure that ``allow_duplicates: true`` enables to run single role multiple times (https://github.com/ansible/ansible/issues/64902)
- runas - Fix the ``runas`` ``become_pass`` variable fallback from ``ansible_runas_runas`` to ``ansible_runas_pass``
- service_facts - Now correctly parses systemd list-unit-files for systemd >=245
- setup - service_mgr - detect systemd even if it isn't running, such as during a container build
- shell cmd - Properly escape double quotes in the command argument
- synchronize - allow data to be passed between two managed nodes when using the docker connection plugin (https://github.com/ansible/ansible/pull/65698)
- synchronize - fix password authentication on Python 2 (https://github.com/ansible/ansible/issues/56629)
- systemd - don't require systemd to be running to enable/disable or mask/unmask units
- template lookup - ensure changes to the templar in the lookup, do not affect the templar context outside of the lookup (https://github.com/ansible/ansible/issues/60106)
- template lookup - fix regression when templating hostvars (https://github.com/ansible/ansible/issues/63940)
- throttle: the linear strategy didn't always stuck with the throttle limit
- unsafe_proxy - Ensure that data within a tuple is marked as unsafe (https://github.com/ansible/ansible/issues/65722)
- update ``user`` module to support silencing ``no_log`` warnings in the future (see: https://github.com/ansible/ansible/pull/64733)
- user - allow 13 asterisk characters in password field without warning
- user - fix comprasion on macOS so module does not improperly report a change (https://github.com/ansible/ansible/issues/62969)
- user - fix stack trace on AIX when attempting to parse shadow file that does not exist (https://github.com/ansible/ansible/issues/62510)
- user - on systems using busybox, honor the ``on_changed`` parameter to prevent unnecessary password changing (https://github.com/ansible/ansible/issues/65711)
- user - update docs to reflect proper way to remove account from all groups
- validate-modules - Fix hang when inspecting module with a delegate args spec type
- virtual facts - detect generic container environment based on non-empty "container" env var
- wait_for_connection - with pipelining enabled, interpreter discovery would fail if the first connection attempt was not successful
- win_become - Do not dispose of one of the logon tokens until after the process has run
- win_credential - Fix issue that errors when trying to add a ``name`` with wildcards.
- win_domain_computer - Fix idempotence checks when ``sAMAccountName`` is different from ``name``
- win_domain_computer - Honour the explicit domain server and credentials when moving or removing a computer object - https://github.com/ansible/ansible/pull/63093
- win_domain_user - Better handle cases when getting a new user's groups fail - https://github.com/ansible/ansible/issues/54331
- win_exec_wrapper - Be more defensive when it comes to getting unhandled exceptions
- win_format - Idem not working if file exist but same fs (https://github.com/ansible/ansible/issues/58302)
- win_format - fixed issue where module would not change allocation unit size (https://github.com/ansible/ansible/issues/56961)
- win_iis_webapppool - Do not try and set attributes in check mode when the pool did not exist
- win_iis_website - Actually restart the site when ``state=restarted`` - https://github.com/ansible/ansible/issues/63828
- win_package - Handle quoted and unquoted strings in the registry ``UninstallString`` value - https://github.com/ansible/ansible/issues/40973
- win_partition - Fix invalid variable name causing a failure on checks - https://github.com/ansible/ansible/issues/62401
- win_partition - don't resize partitions if size difference is < 1 MiB
- win_timezone - Allow for _dstoff timezones
- win_unzip - Fix support for paths with square brackets not being detected properly
- win_uri win_get_url - Fix the behaviour of ``follow_redirects: safe`` to actual redirect on ``GET`` and ``HEAD`` requests - https://github.com/ansible/ansible/issues/65556
- windows environment - Support env vars that contain the unicode variant of single quotes - https://github.com/ansible-collections/ansible.windows/issues/45
- yum - fix bug that caused ``enablerepo`` to not be honored when used with disablerepo all wildcard/glob (https://github.com/ansible/ansible/issues/66549)
- yum - fixed the handling of releasever parameter
- yum - performance bugfix, the YumBase object was being  instantiated multiple times unnecessarily, which lead to considerable overhead when operating against large sets of packages.

Community.Crypto
----------------

Changes for collection ``community.crypto`` after version 0.0.0 (included in the previous ACD version) until version 1.0.0.

.. contents::
  :local:
  :depth: 5

Minor Changes
~~~~~~~~~~~~~

- luks_device - accept ``passphrase``, ``new_passphrase`` and ``remove_passphrase``.
- luks_device - add ``keysize`` parameter to set key size at LUKS container creation
- luks_device - added support to use UUIDs, and labels with LUKS2 containers
- luks_device - added the ``type`` option that allows user explicit define the LUKS container format version
- openssh_keypair - instead of regenerating some broken or password protected keys, fail the module. Keys can still be regenerated by calling the module with ``force=yes``.
- openssh_keypair - the ``regenerate`` option allows to configure the module's behavior when it should or needs to regenerate private keys.
- openssl_certificate - Add option for changing which ACME directory to use with acme-tiny. Set the default ACME directory to Let's Encrypt instead of using acme-tiny's default. (acme-tiny also uses Let's Encrypt at the time being, so no action should be neccessary.)
- openssl_certificate - Change the required version of acme-tiny to >= 4.0.0
- openssl_certificate - allow to provide content of some input files via the ``csr_content``, ``privatekey_content``, ``ownca_privatekey_content`` and ``ownca_content`` options.
- openssl_certificate - allow to return the existing/generated certificate directly as ``certificate`` by setting ``return_content`` to ``yes``.
- openssl_certificate_info - allow to provide certificate content via ``content`` option (https://github.com/ansible/ansible/issues/64776).
- openssl_csr - allow to provide private key content via ``private_key_content`` option.
- openssl_csr - allow to return the existing/generated CSR directly as ``csr`` by setting ``return_content`` to ``yes``.
- openssl_csr_info - allow to provide CSR content via ``content`` option.
- openssl_dhparam - allow to return the existing/generated DH params directly as ``dhparams`` by setting ``return_content`` to ``yes``.
- openssl_dhparam - now supports a ``cryptography``-based backend. Auto-detection can be overwritten with the ``select_crypto_backend`` option.
- openssl_pkcs12 - allow to return the existing/generated PKCS#12 directly as ``pkcs12`` by setting ``return_content`` to ``yes``.
- openssl_privatekey - add ``format`` and ``format_mismatch`` options.
- openssl_privatekey - allow to return the existing/generated private key directly as ``privatekey`` by setting ``return_content`` to ``yes``.
- openssl_privatekey - the ``regenerate`` option allows to configure the module's behavior when it should or needs to regenerate private keys.
- openssl_privatekey_info - allow to provide private key content via ``content`` option.
- openssl_publickey - allow to provide private key content via ``private_key_content`` option.
- openssl_publickey - allow to return the existing/generated public key directly as ``publickey`` by setting ``return_content`` to ``yes``.

Deprecated Features
~~~~~~~~~~~~~~~~~~~

- openssl_csr - all values for the ``version`` option except ``1`` are deprecated.

Bugfixes
~~~~~~~~

- ACME modules: fix bug in ACME v1 account update code
- ACME modules: make sure some connection errors are handled properly
- ACME modules: support Buypass' ACME v1 endpoint
- acme_certificate - fix crash when module is used with Python 2.x.
- acme_certificate - fix misbehavior when ACME v1 is used with ``modify_account`` set to ``false``.
- ecs_certificate - Always specify header ``connection: keep-alive`` for ECS API connections.
- ecs_certificate - Fix formatting of contents of ``full_chain_path``.
- get_certificate - Fix cryptography backend when pyopenssl is unavailable (https://github.com/ansible/ansible/issues/67900)
- openssh_keypair - add logic to avoid breaking password protected keys.
- openssh_keypair - fixes idempotence issue with public key (https://github.com/ansible/ansible/issues/64969).
- openssh_keypair - public key's file attributes (permissions, owner, group, etc.) are now set to the same values as the private key.
- openssl_* modules - prevent crash on fingerprint determination in FIPS mode (https://github.com/ansible/ansible/issues/67213).
- openssl_certificate - When provider is ``entrust``, use a ``connection: keep-alive`` header for ECS API connections.
- openssl_certificate - ``provider`` option was documented as required, but it was not checked whether it was provided. It is now only required when ``state`` is ``present``.
- openssl_certificate - fix ``assertonly`` provider certificate verification, causing 'private key mismatch' and 'subject mismatch' errors.
- openssl_certificate and openssl_csr - fix Ed25519 and Ed448 private key support for ``cryptography`` backend. This probably needs at least cryptography 2.8, since older versions have problems with signing certificates or CSRs with such keys. (https://github.com/ansible/ansible/issues/59039, PR https://github.com/ansible/ansible/pull/63984)
- openssl_csr - a warning is issued if an unsupported value for ``version`` is used for the ``cryptography`` backend.
- openssl_csr - the module will now enforce that ``privatekey_path`` is specified when ``state=present``.
- openssl_publickey - fix a module crash caused when pyOpenSSL is not installed (https://github.com/ansible/ansible/issues/67035).

New Modules
~~~~~~~~~~~

- ecs_domain - Request validation of a domain with the Entrust Certificate Services (ECS) API
- x509_crl - Generate Certificate Revocation Lists (CRLs)
- x509_crl_info - Retrieve information on Certificate Revocation Lists (CRLs)

Community.General
-----------------

Changes for collection ``community.general`` after version 0.0.0 (included in the previous ACD version) until version 1.0.0.

.. contents::
  :local:
  :depth: 5

Minor Changes
~~~~~~~~~~~~~

- Add a make option to the make module to be able to choose a specific make executable
- Add information about changed packages in homebrew returned facts (https://github.com/ansible/ansible/issues/59376).
- Follow up changes in homebrew_cask (https://github.com/ansible/ansible/issues/34696).
- Moved OpenStack dynamic inventory script to Openstack Collection.
- Remove redundant encoding in json.load call in ipa module_utils (https://github.com/ansible/ansible/issues/66592).
- ali_instance - Add params ``unique_suffix``, ``tags``, ``purge_tags``, ``ram_role_name``, ``spot_price_limit``, ``spot_strategy``, ``period_unit``, ``dry_run``, ``include_data_disks``
- ali_instance and ali_instance_info - the required package footmark needs a version higher than 1.19.0
- ali_instance_info - Add params ``name_prefix``, ``filters``
- alicloud modules - Add authentication params to all modules
- alicloud modules - now only support Python 3.6, not support Python 2.x
- database - add support to unique indexes in postgresql_idx
- docker connection plugin - run Powershell modules on Windows containers.
- docker_container - add ``cpus`` option (https://github.com/ansible/ansible/issues/34320).
- docker_container - add new ``container_default_behavior`` option (PR https://github.com/ansible/ansible/pull/63419).
- docker_container - allow to configure timeout when the module waits for a container's removal.
- docker_container - only passes anonymous volumes to docker daemon as ``Volumes``. This increases compatibility with the ``docker`` CLI program. Note that if you specify ``volumes: strict`` in ``comparisons``, this could cause existing containers created with docker_container from Ansible 2.9 or earlier to restart.
- docker_container - support for port ranges was adjusted to be more compatible to the ``docker`` command line utility: a one-port container range combined with a multiple-port host range will no longer result in only the first host port be used, but the whole range being passed to Docker so that a free port in that range will be used.
- docker_container.py - update a containers restart_policy without restarting the container (https://github.com/ansible/ansible/issues/65993)
- docker_stack - Added ``stdout``, ``stderr``, and ``rc`` to return values.
- docker_swarm_service - Sort lists when checking for changes.
- gitlab_project_variable - implement masked and protected attributes
- homebrew - Added environment variable to honor update_homebrew setting (https://github.com/ansible/ansible/issues/56650).
- homebrew - New option ``upgrade_options`` allows to pass flags to upgrade
- homebrew - ``install_options`` is now validated to be a list of strings.
- homebrew_tap - ``name`` is now validated to be a list of strings.
- idrac_redfish_config - Support for multiple manager attributes configuration
- jira - added search function with support for Jira JQL (https://github.com/ansible-collections/community.general/pull/22).
- jira - added update function which can update Jira Selects etc (https://github.com/ansible-collections/community.general/pull/22).
- mysql_db - add ``master_data`` parameter (https://github.com/ansible/ansible/pull/66048).
- mysql_db - add ``skip_lock_tables`` option (https://github.com/ansible/ansible/pull/66688).
- mysql_db - add the ``dump_extra_args`` parameter (https://github.com/ansible/ansible/pull/67747).
- mysql_db - add the ``executed_commands`` returned value (https://github.com/ansible/ansible/pull/65498).
- mysql_db - add the ``force`` parameter (https://github.com/ansible/ansible/pull/65547).
- mysql_db - add the ``use_shell`` parameter (https://github.com/ansible/ansible/issues/20196).
- mysql_info - add ``exclude_fields`` parameter (https://github.com/ansible/ansible/issues/63319).
- mysql_info - add ``global_status`` filter parameter option and return (https://github.com/ansible/ansible/pull/63189).
- mysql_info - add ``return_empty_dbs`` parameter to list empty databases (https://github.com/ansible/ansible/issues/65727).
- mysql_replication - add ``channel`` parameter (https://github.com/ansible/ansible/issues/29311).
- mysql_replication - add ``connection_name`` parameter (https://github.com/ansible/ansible/issues/46243).
- mysql_replication - add ``fail_on_error`` parameter (https://github.com/ansible/ansible/pull/66252).
- mysql_replication - add ``master_delay`` parameter (https://github.com/ansible/ansible/issues/51326).
- mysql_replication - add ``master_use_gtid`` parameter (https://github.com/ansible/ansible/pull/62648).
- mysql_replication - add ``queries`` return value (https://github.com/ansible/ansible/pull/63036).
- mysql_replication - add support of ``resetmaster`` choice to ``mode`` parameter (https://github.com/ansible/ansible/issues/42870).
- mysql_user - ``priv`` parameter can be string or dictionary (https://github.com/ansible/ansible/issues/57533).
- mysql_user - add ``plugin_auth_string`` parameter (https://github.com/ansible/ansible/pull/44267).
- mysql_user - add ``plugin_hash_string`` parameter (https://github.com/ansible/ansible/pull/44267).
- mysql_user - add ``plugin`` parameter (https://github.com/ansible/ansible/pull/44267).
- mysql_user - add the resource_limits parameter (https://github.com/ansible-collections/community.general/issues/133).
- mysql_variables - add ``mode`` parameter (https://github.com/ansible/ansible/issues/60119).
- nagios module - a start parameter has been added, allowing the time a Nagios outage starts to be set. It defaults to the current time if not provided, preserving the previous behavior and ensuring compatibility with existing playbooks.
- nsupdate - Use provided TSIG key to not only sign update queries but also lookup queries
- postgresql_db - add ``dump_extra_args`` parameter (https://github.com/ansible/ansible/pull/66717).
- postgresql_db - add support for .pgc file format for dump and restores.
- postgresql_db - add the ``executed_commands`` returned value (https://github.com/ansible/ansible/pull/65542).
- postgresql_db - add the ``trust_input`` parameter (https://github.com/ansible-collections/community.general/issues/106).
- postgresql_ext - use query parameters with cursor object (https://github.com/ansible/ansible/pull/64994).
- postgresql_info - add collecting info about logical replication publications in databases (https://github.com/ansible/ansible/pull/67614).
- postgresql_info - add collection info about replication subscriptions (https://github.com/ansible/ansible/pull/67464).
- postgresql_lang - add ``owner`` parameter (https://github.com/ansible/ansible/pull/62999).
- postgresql_membership - add the ``trust_input`` parameter (https://github.com/ansible-collections/community.general/pull/158).
- postgresql_privs - add support for TYPE as object types in postgresql_privs module (https://github.com/ansible/ansible/issues/62432).
- postgresql_privs - add the ``trust_input`` parameter (https://github.com/ansible-collections/community.general/pull/177).
- postgresql_query - add the ``encoding`` parameter (https://github.com/ansible/ansible/issues/65367).
- postgresql_user - add scram-sha-256 support (https://github.com/ansible/ansible/issues/49878).
- postgresql_user - add the ``trust_input`` parameter (https://github.com/ansible-collections/community.general/pull/116).
- postgresql_user - add the comment parameter (https://github.com/ansible/ansible/pull/66711).
- redfish_config - New ``bios_attributes`` option to allow setting multiple BIOS attributes in one command.
- redfish_config, redfish_command - Add ``resource_id`` option to specify which System, Manager, or Chassis resource to modify.
- rhn_channel - Added ``validate_certs`` option (https://github.com/ansible/ansible/issues/68374).
- rundeck modules - added new options ``client_cert``, ``client_key``, ``force``, ``force_basic_auth``, ``http_agent``, ``url_password``, ``url_username``, ``use_proxy``, ``validate_certs`` to allow changing fetch_url parameters.
- slack - Add support for user/bot/application tokens (using Slack WebAPI)
- slack - Return ``thread_id`` with thread timestamp when user/bot/application tokens are used
- ufw - accept ``interface_in`` and ``interface_out`` as parameters.
- zabbix_action - allow str values for ``esc_period`` options (https://github.com/ansible/ansible/pull/66841).
- zabbix_host - now supports configuring user macros and host tags on the managed host (see https://github.com/ansible/ansible/pull/66777)
- zabbix_host_info - ``host_name`` based search results now include host groups.
- zabbix_hostmacro - ``macro_name`` now accepts macros in zabbix native format as well (e.g. ``{$MACRO}``)
- zabbix_hostmacro - ``macro_value`` is no longer required when ``state=absent``
- zabbix_proxy - ``interface`` sub-options ``type`` and ``main`` are now deprecated and will be removed in Ansible 2.14. Also, the values passed to ``interface`` are now checked for correct types and unexpected keys.
- zabbix_proxy - added option proxy_address for comma-delimited list of IP/CIDR addresses or DNS names to accept active proxy requests from
- zabbix_template - add new option omit_date to remove date from exported/dumped template (https://github.com/ansible/ansible/pull/67302)
- zabbix_template - adding new update rule templateLinkage.deleteMissing for newer zabbix versions (https://github.com/ansible/ansible/pull/66747).
- zabbix_template_info - add new option omit_date to remove date from exported/dumped template (https://github.com/ansible/ansible/pull/67302)

Deprecated Features
~~~~~~~~~~~~~~~~~~~

- clc_aa_policy - The ``wait`` option had no effect and will be removed in Ansible 2.14
- docker_container - the ``trust_image_content`` option is now deprecated and will be removed in Ansible 2.14. It has never been used by the module.
- docker_container - the default of ``container_default_behavior`` will change from ``compatibility`` to ``no_defaults`` in Ansible 2.14. Set the option to an explicit value to avoid a deprecation warning.
- docker_container - the default value for ``network_mode`` will change in Ansible 2.14, provided at least one network is specified and ``networks_cli_compatible`` is ``true``. See porting guide, module documentation or deprecation warning for more details.
- docker_stack - Return values ``out`` and ``err`` have been deprecated and will be removed in Ansible 2.14. Use ``stdout`` and ``stderr`` instead.
- redfish_config - Deprecate ``bios_attribute_name`` and ``bios_attribute_value`` in favor of new `bios_attributes`` option.
- redfish_config, redfish_command - Behavior to modify the first System, Mananger, or Chassis resource when multiple are present is deprecated. Use the new ``resource_id`` option to specify target resource to modify.

Removed Features (previously deprecated)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- core - remove support for ``check_invalid_arguments`` in ``UTMModule``.
- ldap_attr, ldap_entry - The ``params`` option has been removed in Ansible-2.10 as it circumvents Ansible's option handling.  Setting ``bind_pw`` with the ``params`` option was disallowed in Ansible-2.7, 2.8, and 2.9 as it was insecure.  For information about this policy, see the discussion at: https://meetbot.fedoraproject.org/ansible-meeting/2017-09-28/ansible_dev_meeting.2017-09-28-15.00.log.html This fixes CVE-2020-1746
- pacman - Removed deprecated ``recurse`` option, use ``extra_args=--recursive`` instead

Bugfixes
~~~~~~~~

- **SECURITY** - CVE-2019-14904 - solaris_zone module accepts zone name and performs actions related to that. However, there is no user input validation done while performing actions. A malicious user could provide a crafted zone name which allows executing commands into the server manipulating the module behaviour. Adding user input validation as per Solaris Zone documentation fixes this issue.
- **security issue** - Ansible: Splunk and Sumologic callback plugins leak sensitive data in logs (CVE-2019-14864)
- Convert MD5SUM to lowercase before comparison in maven_artifact module (https://github.com/ansible-collections/community.general/issues/186).
- Fix GitLab modules authentication by handling `python-gitlab` library version >= 1.13.0 (https://github.com/ansible/ansible/issues/64770)
- Fix SSL protocol references in the ``mqtt`` module to prevent failures on Python 2.6.
- Fix the ``xml`` module to use ``list(elem)`` instead of ``elem.getchildren()`` since it is being removed in Python 3.9
- Fix to return XML as a string even for python3 (https://github.com/ansible/ansible/pull/64032).
- Fixes the url handling in lxd_container module that url cannot be specified in lxd environment created by snap.
- Fixes the url handling in lxd_profile module that url cannot be specified in lxd environment created by snap.
- Redact GitLab Project variables which might include sensetive information such as password, api_keys and other project related details.
- Run command in absent state in atomic_image module.
- While deleting gitlab user, name, email and password is no longer required ini gitlab_user module (https://github.com/ansible/ansible/issues/61921).
- become - Fix various plugins that still used play_context to get the become password instead of through the plugin - https://github.com/ansible/ansible/issues/62367
- cronvar - only run ``get_bin_path()`` once
- cronvar - use correct binary name (https://github.com/ansible/ansible/issues/63274)
- cronvar - use get_bin_path utility to locate the default crontab executable instead of the hardcoded /usr/bin/crontab. (https://github.com/ansible/ansible/pull/59765)
- cyberarkpassword - fix invalid attribute access (https://github.com/ansible/ansible/issues/66268)
- dense callback - fix plugin access to its configuration variables and remove a warning message (https://github.com/ansible/ansible/issues/64628).
- digital_ocean_droplet - Fix creation of DigitalOcean droplets using digital_ocean_droplet module (https://github.com/ansible/ansible/pull/61655)
- docker connection plugin - do not prefix remote path if running on Windows containers.
- docker_compose - fix issue where docker deprecation warning results in ansible erroneously reporting a failure
- docker_container - fix idempotency for IP addresses for networks. The old implementation checked the effective IP addresses assigned by the Docker daemon, and not the specified ones. This causes idempotency issues for containers which are not running, since they have no effective IP addresses assigned.
- docker_container - fix network idempotence comparison error.
- docker_container - improve error behavior when parsing port ranges fails.
- docker_container - make sure that when image is missing, check mode indicates a change (image will be pulled).
- docker_container - passing ``test: [NONE]`` now actually disables the image's healthcheck, as documented.
- docker_container - wait for removal of container if docker API returns early (https://github.com/ansible/ansible/issues/65811).
- docker_image - fix validation of build options.
- docker_image - improve file handling when loading images from disk.
- docker_image - make sure that deprecated options also emit proper deprecation warnings next to warnings which indicate how to replace them.
- docker_login - Use ``with`` statement when accessing files, to prevent that invalid JSON output is produced.
- docker_login - correct broken fix for https://github.com/ansible/ansible/pull/60381 which crashes for Python 3.
- docker_login - fix error handling when ``username`` or ``password`` is not specified when ``state`` is ``present``.
- docker_login - make sure that ``~/.docker/config.json`` is created with permissions ``0600``.
- docker_network - fix idempotence comparison error.
- docker_network - fix idempotency for multiple IPAM configs of the same IP version (https://github.com/ansible/ansible/issues/65815).
- docker_network - validate IPAM config subnet CIDR notation on module setup and not during idempotence checking.
- docker_node_info - improve error handling when service inspection fails, for example because node name being ambiguous (https://github.com/ansible/ansible/issues/63353, PR https://github.com/ansible/ansible/pull/63418).
- docker_swarm_service - ``source`` must no longer be specified for ``tmpfs`` mounts.
- docker_swarm_service - fix task always reporting as changed when using ``healthcheck.start_period``.
- docker_swarm_service - passing ``test: [NONE]`` now actually disables the image's healthcheck, as documented.
- firewalld - enable the firewalld module to function offline with firewalld version 0.7.0 and newer (https://github.com/ansible/ansible/issues/63254)
- github_deploy_key - added support for pagination
- gitlab_user - Fix adding ssh key to new/changed user and adding group membership for new/changed user
- hashi_vault - Fix KV v2 lookup to always return latest version
- homebrew - fix Homebrew module's some functions ignored check_mode option (https://github.com/ansible/ansible/pull/65387).
- influxdb_user - Don't grant admin privilege in check mode
- intersight_rest_api, intersight_info - improve file handling by using a context manager.
- jenkins_plugin - make compatible to Ansible 2.10 by fixing import.
- jira - printing full error message from jira server (https://github.com/ansible-collections/community.general/pull/22).
- jira - transition issue not working (https://github.com/ansible-collections/community.general/issues/109).
- manageiq_provider - fix serialization error when running on python3 environment.
- mysql - dont mask ``mysql_connect`` function errors from modules (https://github.com/ansible/ansible/issues/64560).
- mysql_db - fix Broken pipe error appearance when state is import and the target file is compressed (https://github.com/ansible/ansible/issues/20196).
- mysql_db - fix bug in the ``db_import`` function introduced by https://github.com/ansible/ansible/pull/56721 (https://github.com/ansible/ansible/issues/65351).
- mysql_info - add parameter for __collect to get only what are wanted (https://github.com/ansible-collections/community.general/pull/136).
- mysql_replication - allow to pass empty values to parameters (https://github.com/ansible/ansible/issues/23976).
- mysql_user - Fix idempotence when long grant lists are used (https://github.com/ansible/ansible/issues/68044)
- mysql_user - Remove false positive ``no_log`` warning for ``update_password`` option
- mysql_user - fix support privileges with underscore (https://github.com/ansible/ansible/issues/66974).
- mysql_user - fix the error No database selected (https://github.com/ansible/ansible/issues/68070).
- mysql_user - make sure current_pass_hash is a string before using it in comparison (https://github.com/ansible/ansible/issues/60567).
- mysql_variable - fix the module doesn't support variables name with dot (https://github.com/ansible/ansible/issues/54239).
- nsupdate - Do not try fixing non-existing TXT values (https://github.com/ansible/ansible/issues/63364)
- nsupdate - Fix zone name lookup of internal/private zones (https://github.com/ansible/ansible/issues/62052)
- one_vm - improve file handling by using a context manager.
- ovirt - don't ignore ``instance_cpus`` parameter
- pacman - Fix pacman output parsing on localized environment. (https://github.com/ansible/ansible/issues/65237)
- pacman - fix module crash with ``IndexError: list index out of range`` (https://github.com/ansible/ansible/issues/63077)
- pamd - Bugfix for attribute error when removing the first or last line
- passwordstore lookup - Honor equal sign in userpass
- pmrun plugin - The success_command string was no longer quoted. This caused unusual use-cases like ``become_flags=su - root -c`` to fail.
- postgres - use query params with cursor.execute in module_utils.postgres.PgMembership class (https://github.com/ansible/ansible/pull/65164).
- postgres.py - add a new keyword argument ``query_params`` (https://github.com/ansible/ansible/pull/64661).
- postgres_user - Remove false positive ``no_log`` warning for ``no_password_changes`` option
- postgresql_db - Removed exception for 'LibraryError' (https://github.com/ansible/ansible/issues/65223).
- postgresql_db - allow to pass users names which contain dots (https://github.com/ansible/ansible/issues/63204).
- postgresql_idx.py - use the ``query_params`` arg of exec_sql function (https://github.com/ansible/ansible/pull/64661).
- postgresql_lang - use query params with cursor.execute (https://github.com/ansible/ansible/pull/65093).
- postgresql_membership - make the ``groups`` and ``target_roles`` parameters required (https://github.com/ansible/ansible/pull/67046).
- postgresql_membership - remove unused import of exec_sql function (https://github.com/ansible-collections/community.general/pull/178).
- postgresql_owner - use query_params with cursor object (https://github.com/ansible/ansible/pull/65310).
- postgresql_privs - fix sorting lists with None elements for python3 (https://github.com/ansible/ansible/issues/65761).
- postgresql_privs - sort results before comparing so that the values are compared and not the result of ``.sort()`` (https://github.com/ansible/ansible/pull/65125)
- postgresql_privs.py - fix reports as changed behavior of module when using ``type=default_privs`` (https://github.com/ansible/ansible/issues/64371).
- postgresql_publication - fix typo in module.warn method name (https://github.com/ansible/ansible/issues/64582).
- postgresql_publication - use query params arg with cursor object (https://github.com/ansible/ansible/issues/65404).
- postgresql_query - improve file handling by using a context manager.
- postgresql_query - the module doesn't support non-ASCII characters in SQL files with Python3 (https://github.com/ansible/ansible/issues/65367).
- postgresql_schema - use query parameters with cursor object (https://github.com/ansible/ansible/pull/65679).
- postgresql_sequence - use query parameters with cursor object (https://github.com/ansible/ansible/pull/65787).
- postgresql_set - fix converting value to uppercase (https://github.com/ansible/ansible/issues/67377).
- postgresql_set - use query parameters with cursor object (https://github.com/ansible/ansible/pull/65791).
- postgresql_slot - make the ``name`` parameter required (https://github.com/ansible/ansible/pull/67046).
- postgresql_slot - use query parameters with cursor object (https://github.com/ansible/ansible/pull/65791).
- postgresql_subscription - fix typo in module.warn method name (https://github.com/ansible/ansible/pull/64583).
- postgresql_subscription - use query parameters with cursor object (https://github.com/ansible/ansible/pull/65791).
- postgresql_table - use query parameters with cursor object (https://github.com/ansible/ansible/pull/65862).
- postgresql_tablespace - make the ``tablespace`` parameter required (https://github.com/ansible/ansible/pull/67046).
- postgresql_tablespace - use query parameters with cursor object (https://github.com/ansible/ansible/pull/65862).
- postgresql_user - allow to pass user name which contains dots (https://github.com/ansible/ansible/issues/63204).
- postgresql_user - use query parameters with cursor object (https://github.com/ansible/ansible/pull/65862).
- proxmox - fix version detection of proxmox 6 and up (Fixes https://github.com/ansible/ansible/issues/59164)
- proxysql - fixed mysql dictcursor
- pulp_repo - the ``client_cert`` and ``client_key`` options were used for both requests to the Pulp instance and for the repo to sync with, resulting in errors when they were used. Use the new options ``feed_client_cert`` and ``feed_client_key`` for client certificates that should only be used for repo synchronisation, and not for communication with the Pulp instance. (https://github.com/ansible/ansible/issues/59513)
- puppet - fix command line construction for check mode and ``manifest:``
- pure - fix incorrect user_string setting in module_utils file (https://github.com/ansible/ansible/pull/66914)
- redfish_command - fix EnableAccount if Enabled property is not present in Account resource (https://github.com/ansible/ansible/issues/59822)
- redfish_command - fix error when deleting a disabled Redfish account (https://github.com/ansible/ansible/issues/64684)
- redfish_command - fix power ResetType mapping logic (https://github.com/ansible/ansible/issues/59804)
- redfish_config - fix support for boolean bios attrs (https://github.com/ansible/ansible/pull/68251)
- redfish_facts - fix KeyError exceptions in GetLogs (https://github.com/ansible/ansible/issues/59797)
- redhat_subscription - do not set the default quantity to ``1`` when no quantity is provided (https://github.com/ansible/ansible/issues/66478)
- replace use of deprecated functions from ``ansible.module_utils.basic``.
- runas - Fix the ``runas`` ``become_pass`` variable fallback from ``ansible_runas_runas`` to ``ansible_runas_pass``
- scaleway: use jsonify unmarshaller only for application/json requests to avoid breaking the multiline configuration with requests in text/plain (https://github.com/ansible/ansible/issues/65036)
- scaleway_compute(check_image_id): use get image instead loop on first page of images results
- slack - Fix ``thread_id`` data type
- spacewalk inventory - improve file handling by using a context manager.
- syslogger callback plugin - remove check mode support since it did nothing anyway
- terraform - adding support for absolute paths additionally to the relative path within project_path (https://github.com/ansible/ansible/issues/58578)
- terraform - reset out and err before plan creation (https://github.com/ansible/ansible/issues/64369)
- terraform module - fixes usage for providers not supporting workspaces
- yarn - handle no version when installing module by name (https://github.com/ansible/ansible/issues/55097)
- zabbix_action - arguments ``event_source`` and ``esc_period`` no longer required when ``state=absent``
- zabbix_host - fixed inventory_mode key error, which occurs with Zabbix 4.4.1 or more (https://github.com/ansible/ansible/issues/65304).
- zabbix_host - was not possible to update a host where visible_name was not set in zabbix
- zabbix_mediatype - Fixed to support zabbix 4.4 or more and python3 (https://github.com/ansible/ansible/pull/67693)
- zabbix_template - fixed error when providing empty ``link_templates`` to the module (see https://github.com/ansible/ansible/issues/66417)
- zabbix_template - fixed invalid (non-importable) output provided by exporting XML (see https://github.com/ansible/ansible/issues/66466)
- zabbix_user - Fixed an issue where module failed with zabbix 4.4 or above (see https://github.com/ansible/ansible/pull/67475)

New Plugins
~~~~~~~~~~~

Lookup
^^^^^^

- etcd3 - Get key values from etcd3 server
- lmdb_kv - fetch data from LMDB

New Modules
~~~~~~~~~~~

Cloud
^^^^^

huawei
......

- hwc_ecs_instance - Creates a resource of Ecs/Instance in Huawei Cloud
- hwc_evs_disk - Creates a resource of Evs/Disk in Huawei Cloud
- hwc_vpc_eip - Creates a resource of Vpc/EIP in Huawei Cloud
- hwc_vpc_peering_connect - Creates a resource of Vpc/PeeringConnect in Huawei Cloud
- hwc_vpc_port - Creates a resource of Vpc/Port in Huawei Cloud
- hwc_vpc_private_ip - Creates a resource of Vpc/PrivateIP in Huawei Cloud
- hwc_vpc_route - Creates a resource of Vpc/Route in Huawei Cloud
- hwc_vpc_security_group - Creates a resource of Vpc/SecurityGroup in Huawei Cloud
- hwc_vpc_security_group_rule - Creates a resource of Vpc/SecurityGroupRule in Huawei Cloud
- hwc_vpc_subnet - Creates a resource of Vpc/Subnet in Huawei Cloud

ovh
...

- ovh_monthly_billing - Manage OVH monthly billing

packet
......

- packet_ip_subnet - Assign IP subnet to a bare metal server.
- packet_project - Create/delete a project in Packet host.
- packet_volume - Create/delete a volume in Packet host.
- packet_volume_attachment - Attach/detach a volume to a device in the Packet host.

Database
^^^^^^^^

mysql
.....

- mysql_query - Run MySQL queries

postgresql
..........

- postgresql_subscription - Add, update, or remove PostgreSQL subscription
- postgresql_user_obj_stat_info - Gather statistics about PostgreSQL user objects

Net Tools
^^^^^^^^^

- hetzner_firewall - Manage Hetzner's dedicated server firewall
- hetzner_firewall_info - Manage Hetzner's dedicated server firewall
- ipwcli_dns - Manage DNS Records for Ericsson IPWorks via ipwcli

ldap
....

- ldap_attrs - Add or remove multiple LDAP attribute values
- ldap_search - Search for entries in a LDAP server

Packaging
^^^^^^^^^

os
..

- mas - Manage Mac App Store applications with mas-cli

System
^^^^^^

- lbu - Local Backup Utility for Alpine Linux

Community.Network
-----------------

Changes for collection ``community.network`` after version 0.0.0 (included in the previous ACD version) until version 1.0.0.

.. contents::
  :local:
  :depth: 5

Minor Changes
~~~~~~~~~~~~~

- ce_bgp_neighbor_af - Rename the parameter ``redirect_ip_vaildation`` to ``redirect_ip_validation`` (https://github.com/ansible/ansible/pull/62403).

Bugfixes
~~~~~~~~

- Cloudengine module_utils - the ``set-id`` (RPC-REPLY XML attribute) may change over the time althougth ``set-id`` is the identity of the next RPC packet.
- Cloudengine netconf plugin - add a dispatch RPC function,just return original RPC-REPLY, the function is used by ``Cloudengine module_utils``.
- Fixes in network action plugins to work in network connection plugin and modules in collection
- Make netconf plugin configurable to set ncclient device handler name in netconf plugin (https://github.com/ansible/ansible/pull/65718)
- Some cloudengine modules were missing ``import __future__`` and ``metaclass``. (https://github.com/ansible/ansible/pull/67634).
- Some cloudengine modules were missing ``import __future__`` and ``metaclass``. (https://github.com/ansible/ansible/pull/67635).
- action/ce - fix a bug, some new version os will not discard uncommitted configure with a return directly.(https://github.com/ansible/ansible/pull/63513).
- ce_config - fixed issue - Re-building commands(config src) by replacing '#' with 'quit','quit' commands may close connection (https://github.com/ansible/ansible/issues/62872)
- edgeos_config - fix issue where module would silently filter out encrypted passwords
- edgeos_config - fixed issue of handling single quotation marks. Now fails when unmatched (odd numbers)
- plugins-netconf-ce - Fix failed to get version information.
- plugins-netconf-ce - to get attribute 'set-id' from rpc-reply.
- routeros_facts - Prevent crash of module when ``ipv6`` package is not installed

New Modules
~~~~~~~~~~~

Network
^^^^^^^

aci
...

- mso_schema_template_external_epg_contract - Manage Extrnal EPG contracts in schema templates
- mso_schema_template_external_epg_subnet - Manage External EPG subnets in schema templates

apconos
.......

- apconos_command - Run arbitrary commands on APCON devices

cloudengine
...........

- ce_is_is_instance - Manages isis process id configuration on HUAWEI CloudEngine devices.
- ce_is_is_interface - Manages isis interface configuration on HUAWEI CloudEngine devices.
- ce_is_is_view - Manages isis view configuration on HUAWEI CloudEngine devices.
- ce_lacp - Manages Eth-Trunk interfaces on HUAWEI CloudEngine switches
- ce_lldp - Manages LLDP configuration on HUAWEI CloudEngine switches.
- ce_lldp_interface - Manages INTERFACE LLDP configuration on HUAWEI CloudEngine switches.
- ce_mdn_interface - Manages MDN configuration on HUAWEI CloudEngine switches.
- ce_multicast_global - Manages multicast global configuration on HUAWEI CloudEngine switches.
- ce_multicast_igmp_enable - Manages multicast igmp enable configuration on HUAWEI CloudEngine switches.
- ce_static_route_bfd - Manages static route configuration on HUAWEI CloudEngine switches.

exos
....

- exos_l2_interfaces - Manage L2 interfaces on Extreme Networks EXOS devices.
- exos_lldp_interfaces - Manage link layer discovery protocol (LLDP) attributes of interfaces on EXOS platforms.
- exos_vlans - Manage VLANs on Extreme Networks EXOS devices.

onyx
....

- onyx_aaa - Configures AAA parameters
- onyx_bfd - Configures BFD parameters
- onyx_ntp - Manage NTP general configurations and ntp keys configurations on Mellanox ONYX network devices
- onyx_ntp_servers_peers - Configures NTP peers and servers parameters
- onyx_snmp - Manages SNMP general configurations on Mellanox ONYX network devices
- onyx_snmp_hosts - Configures SNMP host parameters
- onyx_snmp_users - Configures SNMP User parameters
- onyx_syslog_files - Configure file management syslog module
- onyx_syslog_remote - Configure remote syslog module
- onyx_username - Configure username module
