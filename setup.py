from setuptools import setup

setup(
  name='Wilson-CLI',
  version='1.0',
  packages=['cli', 'cli.commands'],
  include_package_date=True,
  install_requires=[
    'click',
  ],
  entry_points="""
    [console_scripts]
    wilson=cli.cli:cli
  """,
)