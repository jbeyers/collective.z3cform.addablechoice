from setuptools import setup, find_packages
import os

version = '1.0.1'

setup(name='collective.z3cform.keywordwidget',
      version=version,
      description="Adds a keyword widget (similar to to Archetypes.Widget:KeywordWidget) to z3cform.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='syslab keyword widget keywordwidget z3cform',
      author='JC Brand',
      author_email='brand@syslab.com',
      url='http://pypi.python.org/pypi/collective.z3cform.keywordwidget',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.z3cform'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'plone.app.z3cform',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

