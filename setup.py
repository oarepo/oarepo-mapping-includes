# -*- coding: utf-8 -*-
"""Setup module for elasticsearch mapping includes."""
import os

from setuptools import setup

readme = open('README.rst').read()

DATABASE = "postgresql"

install_requires = [
    'elasticsearch',
    'requests',
    'deepmerge'
]

tests_require = [
    'invenio[base,metadata,sqlite,elasticsearch7]',
    'pytest',
    'pytest-cov',
    'pytest-pep8'
]

g = {}
with open(os.path.join('invenio_oarepo_mapping_includes', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name="invenio_oarepo_mapping_includes",
    version=version,
    url="https://github.com/oarepo/invenio-oarepo-mapping-includes",
    license="MIT",
    author="Miroslav Simek",
    author_email="miroslav.simek@vscht.cz",
    description="An inclusion mechanism for elasticsearch mappings",
    zip_safe=False,
    packages=['invenio_oarepo_mapping_includes'],
    entry_points={
        'invenio_config.module': [
            'invenio_oarepo_mapping_includes = invenio_oarepo_mapping_includes.config',
        ],
        'invenio_base.apps': [
            'invenio_oarepo_mapping_includes = invenio_oarepo_mapping_includes.ext:InvenioOARepoMappingIncludesExt'
        ],
        'invenio_base.api_apps': [
            'invenio_oarepo_mapping_includes = invenio_oarepo_mapping_includes.ext:InvenioOARepoMappingIncludesExt'
        ]
    },
    include_package_data=True,
    setup_requires=install_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 4 - Beta',
    ],
)
