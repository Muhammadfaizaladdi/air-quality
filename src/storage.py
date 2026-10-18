import json
from google.api_core.exceptions import PreconditionFailed
from google.cloud import storage

def to_jsonable(value):
    