import os
import shutil
import tempfile

import pytest
from flask import Flask
from invenio_base.signals import app_loaded
from invenio_db import InvenioDB
from invenio_indexer import InvenioIndexer
from invenio_jsonschemas import InvenioJSONSchemas
from invenio_pidstore import InvenioPIDStore
from invenio_records import InvenioRecords
from invenio_search import InvenioSearch

from oarepo_mapping_includes.ext import InvenioOARepoMappingIncludesExt


@pytest.yield_fixture(scope="function")
def app(request):
    instance_path = tempfile.mkdtemp()
    app = Flask('testapp', instance_path=instance_path)

    app.config.update(
        ACCOUNTS_JWT_ENABLE=False,
        INDEXER_DEFAULT_DOC_TYPE='record-v1.0.0',
        RECORDS_REST_ENDPOINTS={},
        RECORDS_REST_DEFAULT_CREATE_PERMISSION_FACTORY=None,
        RECORDS_REST_DEFAULT_DELETE_PERMISSION_FACTORY=None,
        RECORDS_REST_DEFAULT_READ_PERMISSION_FACTORY=None,
        RECORDS_REST_DEFAULT_UPDATE_PERMISSION_FACTORY=None,
        SERVER_NAME='localhost:5000',
        CELERY_ALWAYS_EAGER=True,
        CELERY_RESULT_BACKEND='cache',
        CELERY_CACHE_BACKEND='memory',
        CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI', 'sqlite:///test.db'
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        TESTING=True,
    )

    app.secret_key = 'changeme'

    InvenioDB(app)
    InvenioRecords(app)
    InvenioJSONSchemas(app)
    InvenioPIDStore(app)
    InvenioSearch(app)
    InvenioIndexer(app)
    InvenioOARepoMappingIncludesExt(app)

    app_loaded.send(app, app=app)

    with app.app_context():
        yield app

    # Teardown instance path.
    shutil.rmtree(instance_path)
