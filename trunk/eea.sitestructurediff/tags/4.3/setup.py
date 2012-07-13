""" Setup package
"""
from setuptools import setup, find_packages
import os

name = 'eea.sitestructurediff'
path = name.split('.') + ['version.txt']
version = open(os.path.join(*path)).read().strip()

setup(name='eea.sitestructurediff',
      version=version,
      description="jsTree to create multilingual structure diff",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='eea plone jstree multilingual',
      author='Sasha Vincic, Valentine Web Systems',
      author_email='eea at valentinewebsystems dot com',
      url='https://svn.eionet.europa.eu/projects/Zope/browser/trunk/'
                                                'eea.sitestructurediff',
      license='MPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.jstree',
          'lovely.memcached',
          #'Products.EEAPloneAdmin',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
