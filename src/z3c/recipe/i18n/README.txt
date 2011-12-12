=============================
Translation domain extraction
=============================

z3c.recipe.i18n
---------------

This Zope 3 recipes offers different tools which allows to extract i18n
translation messages from egg based packages.

The 'i18n' recipe can be used to generate the required scripts for extract
message ids from egg based packages. The i18nmerge allows to merge them into
a .po file. And the i18nstats script gives you an overview about the state
of the translated files.

Note
----

This i18nextract.py file uses different semantic for the arguments. The script
offers to define egg packages instead of one package path. This makes it easy
to define eggs as source where we extract the messages from.


Options
*******

The i18n recipe accepts the following options:

eggs
  The names of one or more eggs, with their dependencies that should
  be included in the Python path of the generated scripts.

packages
  The names of one or more eggs which the messages should get extracted from.
  Note, this is different to the original zope.app.locales implementation.
  The original implementation uses one path as -d argument which assumes a
  specific zope.* package structure with an old style trunk setup.

domain
  The translation domain.

output
  The path of the output file relative to the package root.

maker
  One or more module name which can get used as additional maker. This module
  must be located in the python path because it get resolved by
  zope.configuration.name.resolve. For a sample maker see
  z3c.csvvocabulary.csvStrings.
  Makers are called with these arguments: 'path', 'base_path', 'exclude_dirs',
  'domain', 'include_default_domain' and 'site_zcml'. The return value has to
  be a catalog dictionary.

zcml (required)
  The contents of configuration used for extraction.  Normaly used for load meta
  configuration.  Note: To include a ZCML file outside package, you can use,
  ``include`` directive with ``file`` option.  For example: ``<include
  file="${buildout:directory}/etc/site.zcml" />``

excludeDefaultDomain (optional, default=False)
  Exclude all messages found as part of the default domain. Messages are in
  this domain, if their domain could not be determined. This usually happens
  in page template snippets. (False if not used)

pythonOnly (optional, default=False)
  Only extract message ids from Python (False if not used)

verify_domain (optional, default=False)
  Retrieve all the messages in all the domains in python files when
  verify_domain is False otherwise only retrive the messages of the
  specified domain. (False if not used)

excludeDirectoryName (optional, default=[])
  Allows to specify one or more directory name, relative to the package, to
  exclude. (None if not used)

headerTemplate (optional, default=None)
  The path of the pot header template relative to the buildout directory.

environment
  A section name defining a set of environment variables that should be
  exported before starting the tests. Can be used for set product
  configuration enviroment.

extraPaths
   A new line separated list of directories which are added to the PYTHONPATH.

relative-paths
    Use egg, test, and working-directory paths relative to the test script.

include-site-packages
    You can choose to have the site-packages of the underlying Python
    available to your script or interpreter, in addition to the packages
    from your eggs.  See `the z3c.recipe.scripts documentation`_ for
    motivations and warnings.  You can just set this in your [buildout]
    section or override it in the recipe's section.

allowed-eggs-from-site-packages
    Sometimes you need or want to control what eggs from site-packages are
    used. The allowed-eggs-from-site-packages option allows you to specify a
    whitelist of project names that may be included from site-packages.  You
    can use globs to specify the value.  It defaults to a single value of '*',
    indicating that any package may come from site-packages.

    Here's a usage example::

        [buildout]
        ...

        allowed-eggs-from-site-packages =
            demo
            bigdemo
            zope.*

    This option interacts with the ``include-site-packages`` option in the
    following ways.

    If ``include-site-packages`` is true, then
    ``allowed-eggs-from-site-packages`` filters what eggs from site-packages
    may be chosen.  Therefore, if ``allowed-eggs-from-site-packages`` is an
    empty list, then no eggs from site-packages are chosen, but site-packages
    will still be included at the end of path lists.

    If ``include-site-packages`` is false, the value of
    ``allowed-eggs-from-site-packages`` is irrelevant.

    You can just set this in your [buildout] section or override it in
    the recipe's section.

extends
    You can extend another section using this value.  It is intended to help
    you avoid repeating yourself.

exec-sitecustomize
    Normally the Python's real sitecustomize module is not processed.
    If you want it to be processed, set this value to 'true'.  This will
    be honored irrespective of the setting for include-site-packages.

    You can just set this in your [buildout] section or override it in
    the recipe's section.

.. _`the z3c.recipe.scripts documentation`:
    http://pypi.python.org/pypi/z3c.recipe.scripts#including-site-packages-and-sitecustomize

Test
****

Lets define some (bogus) eggs that we can use in our application:

  >>> mkdir('outputDir')
  >>> mkdir('demo1')
  >>> write('demo1', 'setup.py',
  ... '''
  ... from setuptools import setup
  ... setup(name = 'demo1')
  ... ''')

  >>> mkdir('demo2')
  >>> write('demo2', 'setup.py',
  ... '''
  ... from setuptools import setup
  ... setup(name = 'demo2', install_requires='demo1')
  ... ''')

Now check if the setup was correct:

  >>> ls('bin')
  -  buildout

Lets create a minimal `buildout.cfg` file:

  >>> write('buildout.cfg',
  ... '''
  ... [buildout]
  ... parts = i18n
  ... offline = true
  ...
  ... [i18n]
  ... recipe = z3c.recipe.i18n:i18n
  ... eggs = z3c.recipe.i18n
  ... packages = demo1
  ... domain = recipe
  ... output = outputDir
  ... zcml = <include package="z3c.recipe.tests" file="extract.zcml" />"
  ... ''' % globals())

Now, Let's run the buildout and see what we get:

  >>> print system(join('bin', 'buildout')),
  Installing i18n.
  i18n: setting up i18n tools
  Generated script '/sample-buildout/bin/i18nextract'.
  Generated script '/sample-buildout/bin/i18nmergeall'.
  Generated script '/sample-buildout/bin/i18nstats'.
  Generated script '/sample-buildout/bin/i18ncompile'.

After running buildout, the bin folder contains the different i18n script:

  >>> ls('bin')
  -  buildout
  -  i18ncompile
  -  i18nextract
  -  i18nmergeall
  -  i18nstats

i18nextract
-----------

The i18nextract.py contains the following code:

  >>> cat('bin', 'i18nextract')
  <BLANKLINE>
  import sys
  sys.path[0:0] = [
      '/sample-buildout/parts/i18n',
      ]
  <BLANKLINE>
  <BLANKLINE>
  import os
  path = sys.path[0]
  if os.environ.get('PYTHONPATH'):
      path = os.pathsep.join([path, os.environ['PYTHONPATH']])
  os.environ['BUILDOUT_ORIGINAL_PYTHONPATH'] = os.environ.get('PYTHONPATH', '')
  os.environ['PYTHONPATH'] = path
  import site # imports custom buildout-generated site.py
  import os
  sys.argv[0] = os.path.abspath(sys.argv[0])
  os.chdir('...src')
  <BLANKLINE>
  import z3c.recipe.i18n.i18nextract
  <BLANKLINE>
  if __name__ == '__main__':
      z3c.recipe.i18n.i18nextract.main(
          [sys.argv[0],
           '-d', 'recipe',
           '-s', '/sample-buildout/parts/i18n/configure.zcml',
           '-o', '/sample-buildout/outputDir',
           '-p', 'demo1'
          ])

i18nmergeall
------------

The i18nmergeall.py contains the following code:

  >>> cat('bin', 'i18nmergeall')
  <BLANKLINE>
  import sys
  sys.path[0:0] = [
      '/sample-buildout/parts/i18n',
      ]
  <BLANKLINE>
  <BLANKLINE>
  import os
  path = sys.path[0]
  if os.environ.get('PYTHONPATH'):
      path = os.pathsep.join([path, os.environ['PYTHONPATH']])
  os.environ['BUILDOUT_ORIGINAL_PYTHONPATH'] = os.environ.get('PYTHONPATH', '')
  os.environ['PYTHONPATH'] = path
  import site # imports custom buildout-generated site.py
  <BLANKLINE>
  import z3c.recipe.i18n.i18nmergeall
  <BLANKLINE>
  if __name__ == '__main__':
      z3c.recipe.i18n.i18nmergeall.main([sys.argv[0], '-l', '...outputDir'])

i18nstats
---------

The i18nstats.py contains the following code:

  >>> cat('bin', 'i18nstats')
  <BLANKLINE>
  import sys
  sys.path[0:0] = [
      '/sample-buildout/parts/i18n',
      ]
  <BLANKLINE>
  <BLANKLINE>
  import os
  path = sys.path[0]
  if os.environ.get('PYTHONPATH'):
      path = os.pathsep.join([path, os.environ['PYTHONPATH']])
  os.environ['BUILDOUT_ORIGINAL_PYTHONPATH'] = os.environ.get('PYTHONPATH', '')
  os.environ['PYTHONPATH'] = path
  import site # imports custom buildout-generated site.py
  <BLANKLINE>
  import z3c.recipe.i18n.i18nstats
  <BLANKLINE>
  if __name__ == '__main__':
      z3c.recipe.i18n.i18nstats.main([sys.argv[0], '-l', '...outputDir'])

i18ncompile
-----------

The i18ncompile.py contains the following code:

  >>> cat('bin', 'i18ncompile')
  <BLANKLINE>
  import sys
  sys.path[0:0] = [
      '/sample-buildout/parts/i18n',
      ]
  <BLANKLINE>
  <BLANKLINE>
  import os
  path = sys.path[0]
  if os.environ.get('PYTHONPATH'):
      path = os.pathsep.join([path, os.environ['PYTHONPATH']])
  os.environ['BUILDOUT_ORIGINAL_PYTHONPATH'] = os.environ.get('PYTHONPATH', '')
  os.environ['PYTHONPATH'] = path
  import site # imports custom buildout-generated site.py
  <BLANKLINE>
  import z3c.recipe.i18n.i18ncompile
  <BLANKLINE>
  if __name__ == '__main__':
      z3c.recipe.i18n.i18ncompile.main([sys.argv[0], '-l', '...outputDir'])


Full Sample
-----------

Lets create a `buildout.cfg` file using all available arguments that are
implemented directly in this package:

  >>> write('buildout.cfg',
  ... '''
  ... [buildout]
  ... parts = i18n
  ... offline = true
  ...
  ... [testenv]
  ... fooDir = ${buildout:directory}/parts/foo
  ...
  ... [i18n]
  ... recipe = z3c.recipe.i18n:i18n
  ... eggs = z3c.recipe.i18n
  ... packages = demo1
  ... domain = recipe
  ... output = outputDir
  ... zcml = <include package="z3c.recipe.tests" file="extract.zcml" />"
  ... maker = z3c.csvvocabulary.csvStrings
  ... excludeDefaultDomain = true
  ... pythonOnly = true
  ... verify_domain = true
  ... excludeDirectoryName = foo
  ...                       bar
  ... headerTemplate = pot_header.txt
  ... environment = testenv
  ... extraPaths = extra/path/1
  ...              extra/path/2
  ... ''' % globals())

Now, Let's run the buildout and see what we get:

  >>> print system(join('bin', 'buildout')),
  Uninstalling i18n.
  Installing i18n.
  i18n: setting up i18n tools
  Generated script '/sample-buildout/bin/i18nextract'.
  Generated script '/sample-buildout/bin/i18nmergeall'.
  Generated script '/sample-buildout/bin/i18nstats'.
  Generated script '/sample-buildout/bin/i18ncompile'.

After running buildout, the bin folder contains the different i18n script:

  >>> ls('bin')
  -  buildout
  -  i18ncompile
  -  i18nextract
  -  i18nmergeall
  -  i18nstats

i18nextract
-----------

The i18nextract.py contains the following code:

  >>> cat('bin', 'i18nextract')
  <BLANKLINE>
  import sys
  sys.path[0:0] = [
      '/sample-buildout/parts/i18n',
      ]
  <BLANKLINE>
  <BLANKLINE>
  import os
  path = sys.path[0]
  if os.environ.get('PYTHONPATH'):
      path = os.pathsep.join([path, os.environ['PYTHONPATH']])
  os.environ['BUILDOUT_ORIGINAL_PYTHONPATH'] = os.environ.get('PYTHONPATH', '')
  os.environ['PYTHONPATH'] = path
  import site # imports custom buildout-generated site.py
  import os
  sys.argv[0] = os.path.abspath(sys.argv[0])
  os.chdir('...src')
  os.environ['fooDir'] = '/sample-buildout/parts/foo'
  <BLANKLINE>
  import z3c.recipe.i18n.i18nextract
  <BLANKLINE>
  if __name__ == '__main__':
      z3c.recipe.i18n.i18nextract.main(
          [sys.argv[0],
           '-d', 'recipe',
           '-s', '/sample-buildout/parts/i18n/configure.zcml',
           '-o', '/sample-buildout/outputDir',
           '--exclude-default-domain',
           '--python-only',
           '--verify-domain',
           '-m', 'z3c.csvvocabulary.csvStrings',
           '-p', 'demo1',
           '-x', 'foo',
           '-x', 'bar',
           '-t', '/sample-buildout/pot_header.txt'
          ])

The site.py has inserted the extraPaths.

  >>> cat('parts', 'i18n', 'site.py')
  "...
  def addsitepackages(known_paths):
      """Add site packages, as determined by zc.buildout.
  <BLANKLINE>
      See original_addsitepackages, below, for the original version."""
      ...
      buildout_paths = [
          ...
          '/sample-buildout/extra/path/1',
          '/sample-buildout/extra/path/2'
          ]
      for path in buildout_paths:
          sitedir, sitedircase = makepath(path)
          if not sitedircase in known_paths and os.path.exists(sitedir):
              sys.path.append(sitedir)
              known_paths.add(sitedircase)
      ...
      return known_paths
  <BLANKLINE>
  ...

i18nmergeall
------------

The i18nmergeall.py contains the following code:

  >>> cat('bin', 'i18nmergeall')
  <BLANKLINE>
  import sys
  sys.path[0:0] = [
      '/sample-buildout/parts/i18n',
      ]
  <BLANKLINE>
  <BLANKLINE>
  import os
  path = sys.path[0]
  if os.environ.get('PYTHONPATH'):
      path = os.pathsep.join([path, os.environ['PYTHONPATH']])
  os.environ['BUILDOUT_ORIGINAL_PYTHONPATH'] = os.environ.get('PYTHONPATH', '')
  os.environ['PYTHONPATH'] = path
  import site # imports custom buildout-generated site.py
  <BLANKLINE>
  import z3c.recipe.i18n.i18nmergeall
  <BLANKLINE>
  if __name__ == '__main__':
      z3c.recipe.i18n.i18nmergeall.main([sys.argv[0], '-l', '...outputDir'])

i18nstats
---------

The i18nstats.py contains the following code:

  >>> cat('bin', 'i18nstats')
  <BLANKLINE>
  import sys
  sys.path[0:0] = [
      '/sample-buildout/parts/i18n',
      ]
  <BLANKLINE>
  <BLANKLINE>
  import os
  path = sys.path[0]
  if os.environ.get('PYTHONPATH'):
      path = os.pathsep.join([path, os.environ['PYTHONPATH']])
  os.environ['BUILDOUT_ORIGINAL_PYTHONPATH'] = os.environ.get('PYTHONPATH', '')
  os.environ['PYTHONPATH'] = path
  import site # imports custom buildout-generated site.py
  <BLANKLINE>
  import z3c.recipe.i18n.i18nstats
  <BLANKLINE>
  if __name__ == '__main__':
      z3c.recipe.i18n.i18nstats.main([sys.argv[0], '-l', '...outputDir'])

Alternate Full Sample
---------------------

Now let's do it again using all available arguments plus three delegated
delegated internally to code in z3c.recipe.filetemplate:
include-site-packages, extends, and relative-paths.

This example also uses the legacy name "exludeDirectoryName" instead of
"excludeDirectoryName," to show that it still works.

  >>> write('buildout.cfg',
  ... '''
  ... [buildout]
  ... parts = i18n
  ... offline = true
  ... include-site-packages = true
  ... relative-paths = true
  ...
  ... [testenv]
  ... fooDir = ${buildout:directory}/parts/foo
  ...
  ... [shared]
  ... eggs = z3c.recipe.i18n
  ... excludeDefaultDomain = true
  ... pythonOnly = true
  ... verify_domain = true
  ... headerTemplate = pot_header.txt
  ... environment = testenv
  ...
  ... [i18n]
  ... recipe = z3c.recipe.i18n:i18n
  ... extends = shared
  ... packages = demo1
  ... domain = recipe
  ... output = outputDir
  ... zcml = <include package="z3c.recipe.tests" file="extract.zcml" />"
  ... maker = z3c.csvvocabulary.csvStrings
  ... exludeDirectoryName = foo
  ...                       bar
  ... extraPaths = extra/path/1
  ...              extra/path/2
  ... ''' % globals())

Now, Let's run the buildout and see what we get:

  >>> print system(join('bin', 'buildout')),
  Uninstalling i18n.
  Installing i18n.
  i18n: setting up i18n tools
  Generated script '/sample-buildout/bin/i18nextract'.
  Generated script '/sample-buildout/bin/i18nmergeall'.
  Generated script '/sample-buildout/bin/i18nstats'.
  Generated script '/sample-buildout/bin/i18ncompile'.

After running buildout, the bin folder contains the different i18n script:

  >>> ls('bin')
  -  buildout
  -  i18ncompile
  -  i18nextract
  -  i18nmergeall
  -  i18nstats

i18nextract
-----------

The i18nextract.py contains the following code:

  >>> cat('bin', 'i18nextract')
  <BLANKLINE>
  import os
  <BLANKLINE>
  join = os.path.join
  base = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
  base = os.path.dirname(base)
  <BLANKLINE>
  import sys
  sys.path[0:0] = [
      join(base, 'parts/i18n'),
      ]
  <BLANKLINE>
  <BLANKLINE>
  import os
  path = sys.path[0]
  if os.environ.get('PYTHONPATH'):
      path = os.pathsep.join([path, os.environ['PYTHONPATH']])
  os.environ['BUILDOUT_ORIGINAL_PYTHONPATH'] = os.environ.get('PYTHONPATH', '')
  os.environ['PYTHONPATH'] = path
  import site # imports custom buildout-generated site.py
  import os
  sys.argv[0] = os.path.abspath(sys.argv[0])
  os.chdir('...src')
  os.environ['fooDir'] = '/sample-buildout/parts/foo'
  <BLANKLINE>
  import z3c.recipe.i18n.i18nextract
  <BLANKLINE>
  if __name__ == '__main__':
      z3c.recipe.i18n.i18nextract.main(
          [sys.argv[0],
           '-d', 'recipe',
           '-s', join(base, 'parts/i18n/configure.zcml'),
           '-o', join(base, 'outputDir'),
           '--exclude-default-domain',
           '--python-only',
           '--verify-domain',
           '-m', 'z3c.csvvocabulary.csvStrings',
           '-p', 'demo1',
           '-x', 'foo',
           '-x', 'bar',
           '-t', join(base, 'pot_header.txt')
          ])

Notice that the environ was not relativized, because it was inserted directly
as a string.  This is a current limitation of the relative-paths support.

The site.py has inserted the extraPaths, all paths are relative, and
original_paths are included.

  >>> cat('parts', 'i18n', 'site.py')
  "...
  def addsitepackages(known_paths):
      """Add site packages, as determined by zc.buildout.
  <BLANKLINE>
      See original_addsitepackages, below, for the original version."""
      join = os.path.join
      base = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
      base = os.path.dirname(base)
      base = os.path.dirname(base)
      setuptools_path = ...
      sys.path.append(setuptools_path)
      known_paths.add(os.path.normcase(setuptools_path))
      import pkg_resources
      buildout_paths = [
          ...
          join(base, 'extra/path/1'),
          join(base, 'extra/path/2')
          ]
      for path in buildout_paths:
          sitedir, sitedircase = makepath(path)
          if not sitedircase in known_paths and os.path.exists(sitedir):
              sys.path.append(sitedir)
              known_paths.add(sitedircase)
              pkg_resources.working_set.add_entry(sitedir)
      sys.__egginsert = len(buildout_paths) # Support distribute.
      original_paths = [
          ...
          ]
      for path in original_paths:
          if path == setuptools_path or path not in known_paths:
              addsitedir(path, known_paths)
      return known_paths
  <BLANKLINE>
  ...

i18nmergeall
------------

The i18nmergeall.py contains the following code:

  >>> cat('bin', 'i18nmergeall')
  <BLANKLINE>
  import os
  <BLANKLINE>
  join = os.path.join
  base = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
  base = os.path.dirname(base)
  <BLANKLINE>
  import sys
  sys.path[0:0] = [
      join(base, 'parts/i18n'),
      ]
  <BLANKLINE>
  <BLANKLINE>
  import os
  path = sys.path[0]
  if os.environ.get('PYTHONPATH'):
      path = os.pathsep.join([path, os.environ['PYTHONPATH']])
  os.environ['BUILDOUT_ORIGINAL_PYTHONPATH'] = os.environ.get('PYTHONPATH', '')
  os.environ['PYTHONPATH'] = path
  import site # imports custom buildout-generated site.py
  <BLANKLINE>
  import z3c.recipe.i18n.i18nmergeall
  <BLANKLINE>
  if __name__ == '__main__':
      z3c.recipe.i18n.i18nmergeall.main([sys.argv[0], '-l', join(base, 'outputDir')])

i18nstats
---------

The i18nstats.py contains the following code:

  >>> cat('bin', 'i18nstats')
  <BLANKLINE>
  import os
  <BLANKLINE>
  join = os.path.join
  base = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
  base = os.path.dirname(base)
  <BLANKLINE>
  import sys
  sys.path[0:0] = [
      join(base, 'parts/i18n'),
      ]
  <BLANKLINE>
  <BLANKLINE>
  import os
  path = sys.path[0]
  if os.environ.get('PYTHONPATH'):
      path = os.pathsep.join([path, os.environ['PYTHONPATH']])
  os.environ['BUILDOUT_ORIGINAL_PYTHONPATH'] = os.environ.get('PYTHONPATH', '')
  os.environ['PYTHONPATH'] = path
  import site # imports custom buildout-generated site.py
  <BLANKLINE>
  import z3c.recipe.i18n.i18nstats
  <BLANKLINE>
  if __name__ == '__main__':
      z3c.recipe.i18n.i18nstats.main([sys.argv[0], '-l', join(base, 'outputDir')])
