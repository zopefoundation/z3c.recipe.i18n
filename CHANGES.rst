=======
CHANGES
=======

1.2 (2019-06-25)
----------------

- Fix extraction on Python 3 by requiring a more recent version of
  `zope.app.locales`.

- Add support for Python 3.8.

- Drop support for Python 3.4.


1.1 (2019-01-27)
----------------

- Require zope.app.locales >= 4.0 to get rid of code copied from there.

- Add support for Python 3.7.


1.0.0 (2018-01-10)
------------------

- Python 3 compatibility.

0.9.0 (2013-11-02)
------------------

- Depend on zc.buildout 2.0+. Features introduced with zc.buildout 1.5 are removed (don't work with the 2.x branch).

- Update trove classifiers to show that this package is currently only
  compatible with Python 2.7.

0.8.1 (2012-01-06)
------------------

- Exit with a non-zero status code when one or more msgmerge calls fail.

- Use subprocess instead of os.system.


0.8.0 (2010-10-07)
------------------

- Depend on and use the new features of the zc.buildout 1.5 line. At the same
  time support for zc.buildout <= 1.5.1 has been dropped.

- Fixed test setup to run with current zopetoolkit packages.
  Made sure tests still run on older platforms, particularly Zope 2.12.

- Using python's `doctest` module instead of deprecated
  `zope.testing.doctest`.

- Typo change in configuration: exludeDirNames becomes excludeDirNames (old
  name is still supported for backward compatibility).

0.7.0 (2010-02-18)
------------------

- Fixed test setup to run with current packages.

- Added buildout option `verify_domain`. When set to ``true``
  i18nextract only retrives the message ids of specified domain from
  python files. Otherwise (default and previous behavior) all messages
  ids in all domains in python files are retrieved.


0.6.0 (2009-12-02)
------------------

- Feature: Added new 'headerTemplate' option that allows to specify the path
  of a customized pot header template.

- Feature: Added new 'extraPaths` option that is included in the PYTHONPATH.
  This allows for instance the use with Zope 2.11.

- Makers are now called with additional keyword arguments.

- Fixed dependencies: The 'extract' extra of zope.app.locales is required.

0.5.4 (2009-06-08)
------------------

- Fix bug where zcml_strings collect the same path more then once because it
  follows the configuration zcml for each package.

- Fix bug where i18ncompile miscalculated domains containing ".", everything
  after the "." was ignored.

- The ``excludeDefaultDomain`` option actually works now.

0.5.3 (2009-03-12)
------------------

- Fix bug where i18nmerge miscalculated domains containing ".", everything
  after the "." was ignored.


0.5.2 (2009-03-10)
------------------

- Feature: Generate ``*.po`` file based on ``*.pot`` file if non exists in
  i18nmerge script

- Feature: Implemented i18ncompile script which uses ``msgfmt -o moPath poPath``


0.5.1 (2009-02-22)
------------------

- fix tests

- Updated docs to render nicely when fed to docutils. [ulif]

- Added `zip_safe` flag in `setup.py` to avoid meaningless warnings
  when used with buildout. [ulif]


0.5.0 (2009-09-09)
------------------

- Implemented environment section argument support for i18nextract.py script.
  This is a name of a section which defines a set of environment variables that
  should be exported before starting the extraction.

- Initial Release
