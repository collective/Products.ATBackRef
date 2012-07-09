from setuptools import setup, find_packages
import sys, os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '2.2'
shortdesc = "Back Reference Field/Widget for Plone/Archetypes"
longdesc = "\n\n".join([
    read('README.rst'),
    read('CHANGES.txt'),
])

setup(name='Products.ATBackRef',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Web Environment',
            'Framework :: Zope2',
            'Framework :: Plone',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
      ], # Strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Phil Auersperg, Jens Klein, et al',
      author_email='dev@bluedynamics.com',
      url='https://svn.plone.org/svn/archetypes/MoreFieldsAndWidgets/ATBackRef',
      license='GNU General Public License GPL 2.0',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Products.Archetypes',
      ],
      extras_require={
      },
      entry_points="""
      """,
      )
