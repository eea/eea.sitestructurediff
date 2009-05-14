from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='eea.sitestructurediff',
      version=version,
      description="jsTree to create multilingual structure diff",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='eea plone jstree multilingual',
      author='Sasha Vincic, Valentine Web Systems',
      author_email='eea at valentinewebsystems dot com',
      url='https://svn.eionet.europa.eu/projects/Zope/browser/trunk/eea.sitestructurediff',
      license='MPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
