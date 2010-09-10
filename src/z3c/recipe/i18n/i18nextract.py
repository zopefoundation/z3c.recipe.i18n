#!/usr/bin/env python2.4
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
"""Program to extract internationalization markup from Python Code,
Page Templates and ZCML located in egg packages.

This tool will extract all findable message strings from all
internationalizable files in your defined eggs product. It only extracts
message ids of the specified domain. It defaults to the 'z3c' domain and the
z3c packages which use the shared 'z3c' i18n namespace.

Note: The Python Code extraction tool does not support domain
      registration, so that all message strings are returned for
      Python code.

Note: The script expects to be executed as a buildout installed script.

Usage: i18nextract.py [options]
Options:
    -h / --help
        Print this message and exit.
    -d / --domain <domain>
        Specifies the domain that is supposed to be extracted (i.e. 'z3c')
    -p / --package <egg>
        Specifies the egg package that is supposed to be searched
        (i.e. 'z3c.form')
    -s / --site_zcml <path>
        Specify the location of the 'site.zcml' file. By default the regular
        Zope 3 one is used.
    -e / --exclude-default-domain
        Exclude all messages found as part of the default domain. Messages are
        in this domain, if their domain could not be determined. This usually
        happens in page template snippets.
    -m python-function
        Specify a python function which is added as a maker to the POTMaker.
    -o dir
        Specifies the directory path in which to put the output translation
        template.
    -x dir
        Specifies a directory, relative to the package, to exclude. Note this
        is only a directory name an not a path
        May be used more than once.
    --python-only
        Only extract message ids from Python
    --verify-domain
        Only retrieve the messages of the specified domains in the python files.
    -t <path>
        Specifies the file path of the header template.

$Id$
"""

import os, sys, getopt
import time

from zope.app.locales.extract import DEFAULT_CHARSET
from zope.app.locales.extract import DEFAULT_ENCODING
from zope.app.locales.extract import pot_header as _DEFAULT_POT_HEADER
from zope.app.locales.extract import POTMaker
from zope.app.locales.extract import py_strings
from zope.app.locales.extract import tal_strings
from zope.configuration.name import resolve


class POTMaker(POTMaker):
    """This class inserts sets of strings into a POT file.
    """

    def __init__ (self, output_fn, path, header_template=None):
        self._output_filename = output_fn
        self.path = path
        if header_template is not None and os.path.exists(header_template):
            file = open(header_template, 'r')
            try:
                self._pot_header = file.read()
            finally:
                file.close()
        else:
            self._pot_header = _DEFAULT_POT_HEADER
        self.catalog = {}

    def write(self):
        pot_header = self._pot_header

        file = open(self._output_filename, 'w')
        file.write(pot_header % {'time':     time.ctime(),
                                 'version':  self._getProductVersion(),
                                 'charset':  DEFAULT_CHARSET,
                                 'encoding': DEFAULT_ENCODING})

        # Sort the catalog entries by filename
        catalog = self.catalog.values()
        catalog.sort()

        # Write each entry to the file
        for entry in catalog:
            entry.write(file)

        file.close()


def usage(code, msg=''):
    # Python 2.1 required
    print >> sys.stderr, __doc__
    if msg:
        print >> sys.stderr, msg
    sys.exit(code)


def zcml_strings(path, domain="zope", site_zcml=None):
    """Retrieve all ZCML messages from `dir` that are in the `domain`.

    Note, the pot maker runs in a loop for each package and the maker collects
    only the given messages from such a package by the given path. This allows
    us to collect messages from eggs and external packages. This also prevents
    to collect the same message more then one time since we use the same zcml
    configuration for each package path.
    """
    from zope.app.appsetup import config
    context = config(site_zcml, features=("devmode",), execute=False)
    catalog = context.i18n_strings.get(domain, {})
    res = {}
    duplicated = []
    append = duplicated.append
    for msg, locations  in catalog.items():
        for filename, lineno in locations:
            # only collect locations based on the given path
            if filename.startswith(path):
                id = '%s-%s-%s' % (msg, filename, lineno)
                # skip duplicated entries
                if id not in duplicated:
                    append(id)
                    l = res.get(msg, [])
                    l.append((filename, lineno))
                    res[msg] = l
    return res


def main(argv=sys.argv):
    try:
        opts, args = getopt.getopt(
            argv[1:],
            'hed:s:i:m:p:o:x:t:',
            ['help', 'domain=', 'site_zcml=', 'path=', 'python-only',
             'verify-domain', 'exclude-default-domain'])
    except getopt.error, msg:
        usage(1, msg)

    domain = 'z3c'
    include_default_domain = True
    output_dir = None
    exclude_dirs = []
    python_only = False
    verify_domain = False
    site_zcml = None
    makers = []
    eggPaths = []
    header_template = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage(0)
        elif opt in ('-d', '--domain'):
            domain = arg
        elif opt in ('-s', '--site_zcml'):
            site_zcml = arg
        elif opt in ('-e', '--exclude-default-domain'):
            include_default_domain = False
        elif opt in ('-m', ):
            makers.append(resolve(arg))
        elif opt in ('-o', ):
            output_dir = arg
        elif opt in ('-x', ):
            exclude_dirs.append(arg)
        elif opt in ('--python-only',):
            python_only = True
        elif opt in ('--verify-domain'):
            verify_domain = True
        elif opt in ('-p', '--package'):
            package = resolve(arg)
            path = os.path.dirname(package.__file__)
            if not os.path.exists(path):
                usage(1, 'The specified path does not exist.')
            eggPaths.append((arg, path))
        elif opt in ('-t', ):
            if not os.path.exists(arg):
                usage(1, 'The specified header template does not exist.')
            header_template = arg

    # setup output file
    output_file = domain+'.pot'
    if output_dir:
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        output_file = os.path.join(output_dir, output_file)

    print "domain:                 %r\n" \
          "configuration:          %s\n" \
          "exclude dirs:           %r\n" \
          "include default domain: %r\n" \
          "python only:            %r\n" \
          "verify domain:          %r\n" \
          "header template:        %r\n" \
          % (domain, site_zcml, exclude_dirs, include_default_domain,
             python_only, verify_domain, header_template)

    # setup pot maker
    maker = POTMaker(output_file, '', header_template)

    # add maker for each given path
    for pkgName, path in eggPaths:
        basePath = path
        moduleNames = pkgName.split('.')
        moduleNames.reverse()
        for mName in moduleNames:
            mIdx = path.rfind(mName)
            basePath = basePath[:mIdx]
        pkgPath = path[len(basePath):]

        print "package: %r\n" \
              "base:    %r\n" \
              "path:    %r\n" \
              % (pkgPath, basePath, path)

        maker.add(py_strings(path, domain, exclude=exclude_dirs,
                             verify_domain=verify_domain),
                  basePath)
        if not python_only:
            maker.add(zcml_strings(path, domain, site_zcml), basePath)
            maker.add(tal_strings(path, domain, include_default_domain,
                                  exclude=exclude_dirs), basePath)
        for maker_func in makers:
            try:
                maker.add(
                    maker_func(
                        path=path,
                        base_path=basePath,
                        exclude_dirs=exclude_dirs,
                        domain=domain,
                        include_default_domain=include_default_domain,
                        site_zcml=site_zcml,
                        ), basePath)
            except TypeError:
                # BBB: old arguments
                maker.add(maker_func(path, basePath, exclude_dirs), basePath)

    maker.write()
    print "output: %r\n" % output_file


if __name__ == '__main__':
    main()
