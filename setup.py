# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def get_deps():
  import re

  deps_raw = [ line.strip() for line in open("deps.txt")]
  deps = []
  for dep in deps_raw:
    if not dep or dep.startswith("#"):
      continue
    m = re.search("#egg=(.*)", dep)
    if m:
      dep = m.group(1)
    deps.append(dep)
  return deps


metadata = dict(
  name='Yaka Core',
  version='0.1dev',
  url='http://www.yaka.biz/',
  license='LGPL',
  author='Stefane Fermigier',
  author_email='sf@fermigier.com',
  description='Enterprise social networking meets CRM',
  long_description=__doc__,
  packages=['yaka'],
  platforms='any',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    ],
  # Setuptools specific
  install_requires=get_deps(),
  include_package_data=True,
  zip_safe=False,
)

setup(**metadata)
