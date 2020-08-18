from setuptools import setup

setup(
    name="tests",
    version='1.0.0',
    zip_safe=False,
    packages=['test_module'],
    entry_points={
        "invenio_search.mappings": [
            "test = test_module.mappings"
        ],
        "invenio_oarepo_mapping_includes": [
            "test = test_module.mapping_includes"
        ],
        "invenio_oarepo_mapping_handlers": [
            "dynamic = test_module.mapping_handlers:dynamic"
        ]
    },
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
    ],
)
