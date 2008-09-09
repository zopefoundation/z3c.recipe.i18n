#!/usr/bin/env python2.4
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
"""Program to extract internationalization markup from Python Code,
Page Templates and ZCML located in egg packages.

This tool will extract all findable message strings from all
internationalizable files in your defined eggs product. It only extracts 
message ids of the specified domain. It defaults to the 'z3c' domain and the 
z3c package whihc use the shared 'z3c' i18n namespace.

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

$Id:$
"""

from zope.configuration.name import resolve

import os, sys, getopt
def usage(code, msg=''):
    # Python 2.1 required
    print >> sys.stderr, __doc__
    if msg:
        print >> sys.stderr, msg
    sys.exit(code)


def main(argv=sys.argv):
    try:
        opts, args = getopt.getopt(
            argv[1:],
            'hed:s:i:m:p:o:x:',
            ['help', 'domain=', 'site_zcml=', 'path=', 'python-only'])
    except getopt.error, msg:
        usage(1, msg)

    domain = 'z3c'
    include_default_domain = True
    output_dir = None
    exclude_dirs = []
    python_only = False
    site_zcml = None
    makers = []
    eggPaths = []
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
            makers.append(arg)
        elif opt in ('-o', ):
            output_dir = arg
        elif opt in ('-x', ):
            exclude_dirs.append(arg)
        elif opt in ('--python-only',):
            python_only = True
        elif opt in ('-p', '--package'):
            package = resolve(arg)
            path = os.path.dirname(package.__file__)
            if not os.path.exists(path):
                usage(1, 'The specified path does not exist.')
            eggPaths.append((arg, path))

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
          % (domain, site_zcml, exclude_dirs, include_default_domain,
             python_only)

    from zope.app.locales.extract import POTMaker
    from zope.app.locales.extract import py_strings
    from zope.app.locales.extract import tal_strings
    from zope.app.locales.extract import zcml_strings

    # setup pot maker
    maker = POTMaker(output_file, '')

    # add maker for each given path
    for pkgName, path in eggPaths:
        srcIdx = path.rfind('src')
        if srcIdx == -1:
            # this is an egg package, strip down base path
            basePath = path
            moduleNames = pkgName.split('.')
            moduleNames.reverse()
            for mName in moduleNames:
                mIdx = path.rfind(mName)
                basePath = basePath[:mIdx]
            pkgPath = path[len(basePath):]
        else:
            # this is a package linked in as externals
            basePath = path[:srcIdx]
            pkgPath = path[len(basePath):]

        print "package: %r\n" \
              "base:    %r\n" \
              "path:    %r\n" \
              % (pkgPath, basePath, path)

        maker.add(py_strings(path, domain, exclude=exclude_dirs), basePath)
        if not python_only:
            maker.add(zcml_strings(path, domain, site_zcml), basePath)
            maker.add(tal_strings(path, domain, include_default_domain,
                                  exclude=exclude_dirs), basePath)
        for m in makers:
            poMaker = resolve(m)
            maker.add(poMaker(path, basePath, exclude_dirs))
    maker.write()
    print "output: %r\n" % output_file


if __name__ == '__main__':
    main()
