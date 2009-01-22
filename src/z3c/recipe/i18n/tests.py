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

import os, re
import pkg_resources

import zc.buildout.testing

import unittest
import zope.testing
from zope.testing import doctest, renormalizing


def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)
    zc.buildout.testing.install_develop('RestrictedPython', test)
    zc.buildout.testing.install_develop('ZConfig', test)
    zc.buildout.testing.install_develop('ZODB3', test)
    zc.buildout.testing.install_develop('pytz', test)
    zc.buildout.testing.install_develop('z3c.recipe.i18n', test)
    zc.buildout.testing.install_develop('zc.recipe.egg', test)
    zc.buildout.testing.install_develop('zdaemon', test)
    zc.buildout.testing.install_develop('docutils', test)
    zc.buildout.testing.install_develop('zope.browser', test)
    zc.buildout.testing.install_develop('zodbcode', test)
    zc.buildout.testing.install_develop('zope.annotation', test)
    zc.buildout.testing.install_develop('zc.lockfile', test)
    zc.buildout.testing.install_develop('transaction', test)
    zc.buildout.testing.install_develop('zope.app.applicationcontrol', test)
    zc.buildout.testing.install_develop('zope.app.appsetup', test)
    zc.buildout.testing.install_develop('zope.app.authentication', test)
    zc.buildout.testing.install_develop('zope.app.basicskin', test)
    zc.buildout.testing.install_develop('zope.app.broken', test)
    zc.buildout.testing.install_develop('zope.app.component', test)
    zc.buildout.testing.install_develop('zope.app.container', test)
    zc.buildout.testing.install_develop('zope.app.content', test)
    zc.buildout.testing.install_develop('zope.app.debug', test)
    zc.buildout.testing.install_develop('zope.app.dependable', test)
    zc.buildout.testing.install_develop('zope.app.error', test)
    zc.buildout.testing.install_develop('zope.app.exception', test)
    zc.buildout.testing.install_develop('zope.app.folder', test)
    zc.buildout.testing.install_develop('zope.app.form', test)
    zc.buildout.testing.install_develop('zope.app.generations', test)
    zc.buildout.testing.install_develop('zope.app.http', test)
    zc.buildout.testing.install_develop('zope.app.i18n', test)
    zc.buildout.testing.install_develop('zope.app.interface', test)
    zc.buildout.testing.install_develop('zope.app.locales', test)
    zc.buildout.testing.install_develop('zope.app.pagetemplate', test)
    zc.buildout.testing.install_develop('zope.app.principalannotation', test)
    zc.buildout.testing.install_develop('zope.app.publication', test)
    zc.buildout.testing.install_develop('zope.app.publisher', test)
    zc.buildout.testing.install_develop('zope.app.renderer', test)
    zc.buildout.testing.install_develop('zope.app.rotterdam', test)
    zc.buildout.testing.install_develop('zope.app.schema', test)
    zc.buildout.testing.install_develop('zope.app.security', test)
    zc.buildout.testing.install_develop('zope.app.testing', test)
    zc.buildout.testing.install_develop('zope.app.wsgi', test)
    zc.buildout.testing.install_develop('zope.app.zapi', test)
    zc.buildout.testing.install_develop('zope.app.zcmlfiles', test)
    zc.buildout.testing.install_develop('zope.app.zopeappgenerations', test)
    zc.buildout.testing.install_develop('zope.cachedescriptors', test)
    zc.buildout.testing.install_develop('zope.component', test)
    zc.buildout.testing.install_develop('zope.configuration', test)
    zc.buildout.testing.install_develop('zope.contenttype', test)
    zc.buildout.testing.install_develop('zope.copypastemove', test)
    zc.buildout.testing.install_develop('zope.datetime', test)
    zc.buildout.testing.install_develop('zope.deferredimport', test)
    zc.buildout.testing.install_develop('zope.deprecation', test)
    zc.buildout.testing.install_develop('zope.dottedname', test)
    zc.buildout.testing.install_develop('zope.dublincore', test)
    zc.buildout.testing.install_develop('zope.error', test)
    zc.buildout.testing.install_develop('zope.event', test)
    zc.buildout.testing.install_develop('zope.exceptions', test)
    zc.buildout.testing.install_develop('zope.filerepresentation', test)
    zc.buildout.testing.install_develop('zope.formlib', test)
    zc.buildout.testing.install_develop('zope.hookable', test)
    zc.buildout.testing.install_develop('zope.i18n', test)
    zc.buildout.testing.install_develop('zope.i18nmessageid', test)
    zc.buildout.testing.install_develop('zope.interface', test)
    zc.buildout.testing.install_develop('zope.lifecycleevent', test)
    zc.buildout.testing.install_develop('zope.location', test)
    zc.buildout.testing.install_develop('zope.minmax', test)
    zc.buildout.testing.install_develop('zope.pagetemplate', test)
    zc.buildout.testing.install_develop('zope.proxy', test)
    zc.buildout.testing.install_develop('zope.publisher', test)
    zc.buildout.testing.install_develop('zope.schema', test)
    zc.buildout.testing.install_develop('zope.security', test)
    zc.buildout.testing.install_develop('zope.session', test)
    zc.buildout.testing.install_develop('zope.size', test)
    zc.buildout.testing.install_develop('zope.structuredtext', test)
    zc.buildout.testing.install_develop('zope.tal', test)
    zc.buildout.testing.install_develop('zope.tales', test)
    zc.buildout.testing.install_develop('zope.testing', test)
    zc.buildout.testing.install_develop('zope.testing', test)
    zc.buildout.testing.install_develop('zope.thread', test)
    zc.buildout.testing.install_develop('zope.traversing', test)


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
    (re.compile('-\S+-py\d[.]\d(-\S+)?.egg'),
     '-pyN.N.egg',
    ),
    ])


def test_suite():
    return unittest.TestSuite(
        doctest.DocFileSuite('README.txt',
            setUp=setUp, tearDown=zc.buildout.testing.buildoutTearDown,
            optionflags=doctest.ELLIPSIS, checker=checker),
        )


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
