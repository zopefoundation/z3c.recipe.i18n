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
  The contents of configuration used for extraction. Normaly used for load 
  meta configuration.

excludeDefaultDomain (optional, default=False)
  Exclude all messages found as part of the default domain. Messages are in
  this domain, if their domain could not be determined. This usually happens
  in page template snippets. (False if not used)

pythonOnly (optional, default=False)
  Only extract message ids from Python (False if not used)

exludeDirectoryName (optional, default=[])
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
  ...
    ]
  <BLANKLINE>
  import os
  sys.argv[0] = os.path.abspath(sys.argv[0])
  os.chdir('...src')
  <BLANKLINE>
  <BLANKLINE>
  import z3c.recipe.i18n.i18nextract
  <BLANKLINE>
  if __name__ == '__main__':
      z3c.recipe.i18n.i18nextract.main(['i18nextract', '-d', 'recipe', '-s', '/sample-buildout/parts/i18n/configure.zcml', '-o', '/sample-buildout/outputDir', '-p', 'demo1'])

i18nmergeall
------------

The i18nmergeall.py contains the following code:

  >>> cat('bin', 'i18nmergeall')
  #!C:\Python24\python.exe
  <BLANKLINE>
  import sys
  sys.path[0:0] = [
    ...
    ]
  <BLANKLINE>
  import z3c.recipe.i18n.i18nmergeall
  <BLANKLINE>
  if __name__ == '__main__':
      z3c.recipe.i18n.i18nmergeall.main(['i18nmergeall', '-l', '...outputDir'])

i18nstats
---------

The i18nstats.py contains the following code:

  >>> cat('bin', 'i18nstats')
  #!C:\Python24\python.exe
  <BLANKLINE>
  import sys
  sys.path[0:0] = [
    ...
    ]
  <BLANKLINE>
  import z3c.recipe.i18n.i18nstats
  <BLANKLINE>
  if __name__ == '__main__':
      z3c.recipe.i18n.i18nstats.main(['i18nstats', '-l', '...outputDir'])


i18ncompile
-----------

The i18ncompile.py contains the following code:

  >>> cat('bin', 'i18ncompile')
  #!C:\Python24\python.exe
  <BLANKLINE>
  import sys
  sys.path[0:0] = [
    ...
    ]
  <BLANKLINE>
  import z3c.recipe.i18n.i18ncompile
  <BLANKLINE>
  if __name__ == '__main__':
      z3c.recipe.i18n.i18ncompile.main(['i18ncompile', '-l', '...outputDir'])


Full Sample
-----------

Lets create a `buildout.cfg` file using all available arguments:

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
  ... exludeDirectoryName = foo
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
      ...
      '/sample-buildout/extra/path/1',
      '/sample-buildout/extra/path/2',
    ]
  <BLANKLINE>
  import os
  sys.argv[0] = os.path.abspath(sys.argv[0])
  os.chdir('...src')
  os.environ['fooDir'] = '/sample-buildout/parts/foo'
  <BLANKLINE>
  <BLANKLINE>
  import z3c.recipe.i18n.i18nextract
  <BLANKLINE>
  if __name__ == '__main__':
      z3c.recipe.i18n.i18nextract.main(['i18nextract', '-d', 'recipe', '-s', '/sample-buildout/parts/i18n/configure.zcml', '-o', '/sample-buildout/outputDir', '--exclude-default-domain', '--python-only', '-m', 'z3c.csvvocabulary.csvStrings', '-p', 'demo1', '-x', 'foo', '-x', 'bar', '-t', '/sample-buildout/pot_header.txt'])

i18nmergeall
------------

The i18nmergeall.py contains the following code:

  >>> cat('bin', 'i18nmergeall')
  #!C:\Python24\python.exe
  <BLANKLINE>
  import sys
  sys.path[0:0] = [
      ...
      '/sample-buildout/extra/path/1',
      '/sample-buildout/extra/path/2',
    ]
  <BLANKLINE>
  import z3c.recipe.i18n.i18nmergeall
  <BLANKLINE>
  if __name__ == '__main__':
      z3c.recipe.i18n.i18nmergeall.main(['i18nmergeall', '-l', '...outputDir'])

i18nstats
---------

The i18nstats.py contains the following code:

  >>> cat('bin', 'i18nstats')
  #!C:\Python24\python.exe
  <BLANKLINE>
  import sys
  sys.path[0:0] = [
      ...
      '/sample-buildout/extra/path/1',
      '/sample-buildout/extra/path/2',
    ]
  <BLANKLINE>
  import z3c.recipe.i18n.i18nstats
  <BLANKLINE>
  if __name__ == '__main__':
      z3c.recipe.i18n.i18nstats.main(['i18nstats', '-l', '...outputDir'])
