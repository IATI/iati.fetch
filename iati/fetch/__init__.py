"""A module containing functionality for iati.fetch"""
import json
import requests

class Dataset(object):
    def __init__(self, dataset_id):
        req = requests.get("https://iatiregistry.org/api/3/action/package_show?id={0}".format(dataset_id))

        if req.status_code != 200:
            raise Exception()
        else:
            registry_metadata = json.loads(req.text)
        pass
