import json
import os

import pkg_resources
import requests
from invenio_base.signals import app_loaded
from jsonpointer import JsonPointer
from pkg_resources import iter_entry_points

from invenio_oarepo_mapping_includes.mapping_transformer import mapping_transformer
from elasticsearch import VERSION as ES_VERSION


class OARepoMappingIncludesState:
    def __init__(self, app):
        self.app = app
        self._includes = None
        self._handlers = None

    @property
    def included_mappings(self):
        if self._includes is None:
            self._includes = self._load_included_mappings()
        return self._includes

    @property
    def mapping_handlers(self):
        if self._handlers is None:
            self._handlers = self._load_mapping_handlers()
        return self._handlers

    def _load_included_mappings(self):
        included_mappings = {}
        for ep in iter_entry_points('invenio_oarepo_mapping_includes'):
            package_name = '{}.v{}'.format(ep.module_name, ES_VERSION[0])
            package_name = package_name.split('.', maxsplit=1)
            package_path = package_name[1].replace('.', '/')
            for filename in pkg_resources.resource_listdir(package_name[0], package_path):
                if filename.endswith('.json'):
                    file_data = pkg_resources.resource_string(
                        package_name[0],
                        os.path.join(package_path, filename))
                    included_mappings[filename] = json.loads(file_data.decode("utf-8"))
        return included_mappings

    def _load_mapping_handlers(self):
        handlers = {}
        for ep in iter_entry_points('invenio_oarepo_mapping_handlers'):
            handlers[ep.name] = ep.load()
        return handlers

    def load_resource(self, resource, json_pointer):
        mapping_handlers = self.mapping_handlers
        if resource in mapping_handlers:
            return mapping_handlers[resource](resource=resource, json_pointer=json_pointer)

        mappings = self.included_mappings
        if resource not in mappings:
            if resource.startswith('http://') or resource.startswith('https://'):
                mappings[resource] = requests.get(resource).json()
        try:
            mapping = mappings[resource]
        except KeyError:
            raise KeyError('%s not in %s' % (resource, list(sorted(mappings.keys()))))

        ptr = JsonPointer(json_pointer)
        return ptr.resolve(mapping)


class InvenioOARepoMappingIncludesExt:

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.init_config(app)
        app.extensions['oarepo-mapping-includes'] = OARepoMappingIncludesState(app)
        app_loaded.connect(mapping_transformer)

    def init_config(self, app):
        pass
