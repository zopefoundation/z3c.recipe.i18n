##############################################################################
#
# Copyright (c) 2008 Zope Corporation and Contributors.
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
$Id:$
"""
__docformat__ = 'restructuredtext'

import os
import logging

import zc.buildout
import zc.recipe.egg

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
os.chdir(%r)
"""


env_template = """os.environ['%s'] = %r
"""


class I18nSetup(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        if 'eggs' not in self.options:
            self.options['eggs'] = ''
        self.options['eggs'] = self.options['eggs'] + '\n' \
                             + 'zope.app.locales'
        self.egg = zc.recipe.egg.Egg(buildout, name, options)

    def install(self):
        logging.getLogger(self.name).info('setting up i18n tools')

        requirements, ws = self.egg.working_set()

        excludeDefaultDomain = self.options.get('excludeDefaultDomain',
            False)

        pythonOnly = self.options.get('pythonOnly', False) 

        # setup configuration file
        zcml = self.options.get('zcml', None)
        if zcml is None:
            raise zc.buildout.UserError('No zcml configuration defined.')
        zcml = zcmlTemplate % zcml

        # get domain
        domain = self.options.get('domain', None)
        if domain is None:
            raise zc.buildout.UserError('No domain given.')

        # get output path
        output = self.options.get('output', None)
        if output is None:
            raise zc.buildout.UserError('No output path given.')
        output = os.path.abspath(output)

        partsDir = os.path.join(
                self.buildout['buildout']['parts-directory'],
                self.name,
                )
        if not os.path.exists(partsDir):
            os.mkdir(partsDir)
        zcmlFilename = os.path.join(partsDir, 'configure.zcml')
        file(zcmlFilename, 'w').write(zcml)

        # Generate i18nextract
        arguments = ['%sextract'% self.name,
                     '-d', domain,
                     '-s', zcmlFilename,
                     '-o', output,
                    ]

        if excludeDefaultDomain:
            arguments.extend(['--exclude-default-domain'])

        if pythonOnly:
            arguments.extend(['--python-only'])

        makers = [m for m in self.options.get('maker', '').split() if m!='']
        for m in makers:
            arguments.extend(['-m', m])

        # add package names as -p multi option
        packages = [p for p in self.options.get('packages', '').split()
                    if p!='']
        for p in packages:
            arguments.extend(['-p', p])

        exludeDirNames = [x for x 
                          in self.options.get('exludeDirectoryName', '').split()
                          if x!='']
        for x in exludeDirNames:
            arguments.extend(['-x', x])

        initialization = initialization_template % this_loc
        env_section = self.options.get('environment', '').strip()
        if env_section:
            env = self.buildout[env_section]
            for key, value in env.items():
                initialization += env_template % (key, value)

        # Generate i18nextract
        generated = zc.buildout.easy_install.scripts(
            [('%sextract'% self.name, 'z3c.recipe.i18n.i18nextract', 'main')],
            ws, self.options['executable'],
            self.buildout['buildout']['bin-directory'],
            extra_paths = [this_loc],
            arguments = arguments,
            initialization = initialization,
            )

        # Generate i18nmergeall
        arguments = ['%smergeall'% self.name, '-l', output]
        generated.extend(
            zc.buildout.easy_install.scripts(
                [('%smergeall'% self.name,
                  'z3c.recipe.i18n.i18nmergeall',
                  'main')],
                ws, self.options['executable'],
                self.buildout['buildout']['bin-directory'],
                extra_paths = [this_loc],
                arguments = arguments,
            ))

        # Generate i18nstats
        arguments = ['%sstats'% self.name, '-l', output]
        generated.extend(
            zc.buildout.easy_install.scripts(
                [('%sstats'% self.name,
                  'z3c.recipe.i18n.i18nstats',
                  'main')],
                ws, self.options['executable'],
                self.buildout['buildout']['bin-directory'],
                extra_paths = [this_loc],
                arguments = arguments,
            ))

        return generated

    update = install
