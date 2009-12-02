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

import re

import unittest
from zope.testing import doctest, renormalizing

import zc.buildout.testing


def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install('RestrictedPython', test)
    zc.buildout.testing.install('ZConfig', test)
    zc.buildout.testing.install('ZODB3', test)
    zc.buildout.testing.install('pytz', test)
    zc.buildout.testing.install('transaction', test)
    zc.buildout.testing.install('zc.lockfile', test)
    zc.buildout.testing.install('zc.recipe.egg', test)
    zc.buildout.testing.install('zdaemon', test)
    zc.buildout.testing.install('zope.annotation', test)
    zc.buildout.testing.install('zope.app.applicationcontrol', test)
    zc.buildout.testing.install('zope.app.appsetup', test)
    zc.buildout.testing.install('zope.app.basicskin', test)
    zc.buildout.testing.install('zope.app.component', test)
    zc.buildout.testing.install('zope.app.container', test)
    zc.buildout.testing.install('zope.app.form', test)
    zc.buildout.testing.install('zope.app.locales', test)
    zc.buildout.testing.install('zope.app.pagetemplate', test)
    zc.buildout.testing.install('zope.app.publication', test)
    zc.buildout.testing.install('zope.authentication', test)
    zc.buildout.testing.install('zope.broken', test)
    zc.buildout.testing.install('zope.browser', test)
    zc.buildout.testing.install('zope.cachedescriptors', test)
    zc.buildout.testing.install('zope.component', test)
    zc.buildout.testing.install('zope.componentvocabulary', test)
    zc.buildout.testing.install('zope.configuration', test)
    zc.buildout.testing.install('zope.container', test)
    zc.buildout.testing.install('zope.contenttype', test)
    zc.buildout.testing.install('zope.copy', test)
    zc.buildout.testing.install('zope.copypastemove', test)
    zc.buildout.testing.install('zope.datetime', test)
    zc.buildout.testing.install('zope.deferredimport', test)
    zc.buildout.testing.install('zope.deprecation', test)
    zc.buildout.testing.install('zope.dottedname', test)
    zc.buildout.testing.install('zope.dublincore', test)
    zc.buildout.testing.install('zope.error', test)
    zc.buildout.testing.install('zope.event', test)
    zc.buildout.testing.install('zope.exceptions', test)
    zc.buildout.testing.install('zope.filerepresentation', test)
    zc.buildout.testing.install('zope.formlib', test)
    zc.buildout.testing.install('zope.hookable', test)
    zc.buildout.testing.install('zope.i18n', test)
    zc.buildout.testing.install('zope.i18nmessageid', test)
    zc.buildout.testing.install('zope.interface', test)
    zc.buildout.testing.install('zope.lifecycleevent', test)
    zc.buildout.testing.install('zope.location', test)
    zc.buildout.testing.install('zope.minmax', test)
    zc.buildout.testing.install('zope.pagetemplate', test)
    zc.buildout.testing.install('zope.processlifetime', test)
    zc.buildout.testing.install('zope.proxy', test)
    zc.buildout.testing.install('zope.publisher', test)
    zc.buildout.testing.install('zope.schema', test)
    zc.buildout.testing.install('zope.security', test)
    zc.buildout.testing.install('zope.session', test)
    zc.buildout.testing.install('zope.site', test)
    zc.buildout.testing.install('zope.size', test)
    zc.buildout.testing.install('zope.tal', test)
    zc.buildout.testing.install('zope.tales', test)
    zc.buildout.testing.install('zope.testing', test)
    zc.buildout.testing.install('zope.traversing', test)
    zc.buildout.testing.install_develop('z3c.recipe.i18n', test)


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

    ])


def test_suite():
    return unittest.TestSuite(
        doctest.DocFileSuite('README.txt',
            setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            checker=checker),
        )


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
