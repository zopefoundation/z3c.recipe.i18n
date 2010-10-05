##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
A Buildout recipe for i18n scripts.
"""
__docformat__ = 'restructuredtext'

import logging
import os
import sys

import zc.buildout
import z3c.recipe.scripts.scripts

import pkg_resources

this_loc = pkg_resources.working_set.find(
    pkg_resources.Requirement.parse('z3c.recipe.i18n')).location


zcmlTemplate = """<configure xmlns='http://namespaces.zope.org/zope'
           xmlns:meta="http://namespaces.zope.org/meta"
           >

  %s

</configure>
"""

initialization_template = """import os
sys.argv[0] = os.path.abspath(sys.argv[0])
os.chdir(%s)
"""


env_template = """os.environ['%s'] = %r
"""


class I18nSetup(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        # We do this early so the "extends" functionality works before we get
        # to the other options below.
        self._delegated = z3c.recipe.scripts.scripts.Base(
            buildout, name, options)
        if 'eggs' not in self.options:
            self.options['eggs'] = ''
        self.options['eggs'] = self.options['eggs'] + '\n' \
                             + 'zope.app.locales [extract]'

    def install(self):
        logging.getLogger(self.name).info('setting up i18n tools')
        requirements, ws = self._delegated.working_set()
        options = self.options
        excludeDefaultDomain = options.get('excludeDefaultDomain',
            False)

        pythonOnly = options.get('pythonOnly', False)
        verify_domain = options.get('verify_domain', False)

        # setup configuration file
        zcml = options.get('zcml', None)
        if zcml is None:
            raise zc.buildout.UserError('No zcml configuration defined.')
        zcml = zcmlTemplate % zcml

        # get domain
        domain = options.get('domain', None)
        if domain is None:
            raise zc.buildout.UserError('No domain given.')

        # get output path
        output = options.get('output', None)
        if output is None:
            raise zc.buildout.UserError('No output path given.')
        output = os.path.abspath(output)

        generated = []
        partsDir = options['parts-directory']
        if not os.path.exists(partsDir):
            os.mkdir(partsDir)
            generated.append(partsDir)
        zcmlFilename = os.path.join(partsDir, 'configure.zcml')
        file(zcmlFilename, 'w').write(zcml)
        generated.append(zcmlFilename)

        if self._delegated._relative_paths:
            _maybe_relativize = lambda path: _relativize(
                self._delegated._relative_paths, path)
        else:
            _maybe_relativize = lambda path: repr(path)

        zcmlFilename = _maybe_relativize(zcmlFilename)
        output = _maybe_relativize(output)

        # Generate i18nextract
        arguments = ['sys.argv[0]']
        def add_reprs(*args):
            args = list(args)
            arguments.append("\n         " + repr(args.pop(0)))
            arguments.extend(repr(arg) for arg in args)
        add_reprs('-d', domain)
        arguments.extend(["\n         " + repr('-s'), zcmlFilename])
        arguments.extend(["\n         " + repr('-o'), output])

        if excludeDefaultDomain:
            add_reprs('--exclude-default-domain')

        if pythonOnly:
            add_reprs('--python-only')

        if verify_domain:
            add_reprs('--verify-domain')

        makers = [m for m in options.get('maker', '').split() if m!='']
        for m in makers:
            add_reprs('-m', m)

        # add package names as -p multi option
        packages = [p for p in options.get('packages', '').split()
                    if p!='']
        for p in packages:
            add_reprs('-p', p)

        # This code used to have a typo: the option was exludeDirectoryName
        # instead of excludeDirectoryName.  For backwards compatibility,
        # allow the old value, though prefer the properly-spelled one.
        excludeDirNames_raw = options.get(
            'excludeDirectoryName', options.get('exludeDirectoryName', ''))
        excludeDirNames = [x for x in excludeDirNames_raw.split() if x!='']
        for x in excludeDirNames:
            arguments.extend(
                ["\n         " + repr('-x'), _maybe_relativize(x)])

        header_template = options.get('headerTemplate', None)
        if header_template is not None:
            header_template = os.path.normpath(
                os.path.join(self.buildout['buildout']['directory'],
                             header_template.strip()))
            arguments.extend(
                ["\n         " + repr('-t'),
                 _maybe_relativize(header_template)])

        arguments = '\n        [' + ', '.join(arguments) + '\n        ]'
        initialization = initialization_template % _maybe_relativize(this_loc)
        env_section = options.get('environment', '').strip()
        if env_section:
            env = self.buildout[env_section]
            for key, value in env.items():
                initialization += env_template % (key, value)
        extra_paths = (
            [this_loc] + options.get('extraPaths', '').split('\n'))
        extra_paths = [p for p in extra_paths if p]

        # Generate i18nextract
        generated.extend(zc.buildout.easy_install.sitepackage_safe_scripts(
            self.buildout['buildout']['bin-directory'], ws,
            options['executable'], partsDir,
            reqs=[('%sextract'% self.name,
                   'z3c.recipe.i18n.i18nextract',
                   'main')],
            extra_paths=extra_paths,
            include_site_packages=self._delegated.include_site_packages,
            exec_sitecustomize=self._delegated.exec_sitecustomize,
            relative_paths=self._delegated._relative_paths,
            script_arguments=arguments,
            script_initialization=initialization,
            ))

        # Generate i18nmergeall
        generated.extend(
            item for item in
            zc.buildout.easy_install.sitepackage_safe_scripts(
                self.buildout['buildout']['bin-directory'], ws,
                options['executable'], partsDir,
                reqs=[('%smergeall'% self.name,
                       'z3c.recipe.i18n.i18nmergeall',
                       'main')],
                extra_paths=extra_paths,
                include_site_packages=self._delegated.include_site_packages,
                exec_sitecustomize=self._delegated.exec_sitecustomize,
                relative_paths=self._delegated._relative_paths,
                script_arguments="[sys.argv[0], '-l', %s]" % output,)
            if item not in generated)

        # Generate i18nstats
        generated.extend(
            item for item in
            zc.buildout.easy_install.sitepackage_safe_scripts(
                self.buildout['buildout']['bin-directory'], ws,
                options['executable'], partsDir,
                reqs=[('%sstats'% self.name,
                       'z3c.recipe.i18n.i18nstats',
                       'main')],
                extra_paths=extra_paths,
                include_site_packages=self._delegated.include_site_packages,
                exec_sitecustomize=self._delegated.exec_sitecustomize,
                relative_paths=self._delegated._relative_paths,
                script_arguments="[sys.argv[0], '-l', %s]" % output,)
            if item not in generated)

        # Generate i18ncompile
        generated.extend(
            item for item in
            zc.buildout.easy_install.sitepackage_safe_scripts(
                self.buildout['buildout']['bin-directory'], ws,
                options['executable'], partsDir,
                reqs=[('%scompile'% self.name,
                       'z3c.recipe.i18n.i18ncompile',
                       'main')],
                extra_paths=extra_paths,
                include_site_packages=self._delegated.include_site_packages,
                exec_sitecustomize=self._delegated.exec_sitecustomize,
                relative_paths=self._delegated._relative_paths,
                script_arguments="[sys.argv[0], '-l', %s]" % output,)
            if item not in generated)

        return generated

    update = install


def _relativize(base, path):
    base += os.path.sep
    if sys.platform == 'win32':
        #windoze paths are case insensitive, but startswith is not
        base = base.lower()
        path = path.lower()

    if path.startswith(base):
        path = 'join(base, %r)' % path[len(base):]
    else:
        path = repr(path)
    return path
