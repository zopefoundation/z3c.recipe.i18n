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

from zope.testing import renormalizing
import doctest
import re
import unittest
import zc.buildout.testing


def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install('ZConfig', test)
    zc.buildout.testing.install('ZODB3', test)
    zc.buildout.testing.install('pytz', test)
    zc.buildout.testing.install('six', test)
    zc.buildout.testing.install('transaction', test)
    zc.buildout.testing.install('zc.lockfile', test)
    zc.buildout.testing.install('zc.recipe.egg', test)
    zc.buildout.testing.install('z3c.recipe.scripts', test)
    zc.buildout.testing.install('zdaemon', test)
    zc.buildout.testing.install('zope.annotation', test)
    zc.buildout.testing.install('zope.app.applicationcontrol', test)
    zc.buildout.testing.install('zope.app.appsetup', test)
    zc.buildout.testing.install('zope.app.locales', test)
    zc.buildout.testing.install('zope.app.publication', test)
    try:
        zc.buildout.testing.install('zope.applicationcontrol', test)
    except AttributeError:
        # BBB: for running tests with zopetoolkit < 1.0, e.g. Zope 2.12
        pass
    zc.buildout.testing.install('zope.authentication', test)
    zc.buildout.testing.install('zope.broken', test)
    zc.buildout.testing.install('zope.browser', test)
    zc.buildout.testing.install('zope.component', test)
    zc.buildout.testing.install('zope.configuration', test)
    zc.buildout.testing.install('zope.container', test)
    zc.buildout.testing.install('zope.contenttype', test)
    zc.buildout.testing.install('zope.dottedname', test)
    zc.buildout.testing.install('zope.error', test)
    zc.buildout.testing.install('zope.event', test)
    zc.buildout.testing.install('zope.exceptions', test)
    zc.buildout.testing.install('zope.filerepresentation', test)
    zc.buildout.testing.install('zope.i18n', test)
    zc.buildout.testing.install('zope.i18nmessageid', test)
    zc.buildout.testing.install('zope.interface', test)
    zc.buildout.testing.install('zope.lifecycleevent', test)
    zc.buildout.testing.install('zope.location', test)
    zc.buildout.testing.install('zope.minmax', test)
    zc.buildout.testing.install('zope.processlifetime', test)
    zc.buildout.testing.install('zope.proxy', test)
    zc.buildout.testing.install('zope.publisher', test)
    zc.buildout.testing.install('zope.schema', test)
    zc.buildout.testing.install('zope.security', test)
    zc.buildout.testing.install('zope.session', test)
    zc.buildout.testing.install('zope.site', test)
    zc.buildout.testing.install('zope.size', test)
    zc.buildout.testing.install('zope.tal', test)
    zc.buildout.testing.install('zope.testing', test)
    zc.buildout.testing.install('zope.traversing', test)
    zc.buildout.testing.install_develop('z3c.recipe.i18n', test)

    # BBB: for running tests with zopetoolkit < 1.0, e.g. Zope 2.12
    for project in ('RestrictedPython',
                    'zope.app.basicskin',
                    'zope.app.component',
                    'zope.app.container',
                    'zope.app.form',
                    'zope.app.pagetemplate',
                    'zope.app.publisher',
                    'zope.cachedescriptors',
                    'zope.componentvocabulary',
                    'zope.copy',
                    'zope.copypastemove',
                    'zope.datetime',
                    'zope.deferredimport',
                    'zope.deprecation',
                    'zope.dublincore',
                    'zope.formlib',
                    'zope.hookable',
                    'zope.pagetemplate',
                    'zope.tales'):
        try:
            zc.buildout.testing.install(project, test)
        except AttributeError:
            pass


checker = renormalizing.RENormalizing([
    zc.buildout.testing.normalize_path,
    (re.compile(
    "Couldn't find index page for '[a-zA-Z0-9.]+' "
    "\(maybe misspelled\?\)"
    "\n"
    ), ''),
    (re.compile("""['"][^\n"']+z3c.recipe.i18n[^\n"']*['"],"""),
     "'/z3c.recipe.i18n',"),
    (re.compile('#![^\n]+\n'), ''),
    (re.compile('-\S+-py\d[.]\d(-\S+)?.egg'), '-pyN.N.egg',),
    # the following are for compatibility with Windows
    (re.compile('-  .*\.exe\n'), ''),
    (re.compile('-script.py'), ''),
    (re.compile(r'\\[\\]?'), '/'),
    (re.compile('outputDir'), 'outputdir'),
    ])


def test_suite():
    return unittest.TestSuite(
        doctest.DocFileSuite('README.txt',
            setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            checker=checker),
        )
