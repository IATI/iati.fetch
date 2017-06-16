"""A module containing functionality for iati.fetch."""
import iati.core.data
import json
import requests

REGISTRY_API_METADATA_BY_DATASET_ID = "https://iatiregistry.org/api/3/action/package_show?id={0}"


class Dataset(object):
    """Container class to fetch a dataset."""

    def __init__(self, dataset_id):
        """Fetch a dataset by registry dataset ID."""
        self.dataset_id = dataset_id
        self.dataset = None

    def set_dataset(self):
        """Set dataset from the dataset ID."""
        registry_metadata = get_metadata(self.dataset_id)
        dataset_url = registry_metadata['result']['resources'][0]['url']
        dataset = get_dataset(dataset_url)
        self.dataset = iati.core.data.Dataset(dataset)


def get_metadata(dataset_id):
    """Get registry metadata for given dataset ID."""
    req = requests.get(REGISTRY_API_METADATA_BY_DATASET_ID.format(dataset_id))
    if not is_response_okay(req):
        raise Exception()
    else:
        registry_metadata = json.loads(req.text)
        return registry_metadata


def get_dataset(dataset_url):
    """Get dataset from dataset URL."""
    dataset = requests.get(dataset_url)
    if not is_response_okay(dataset):
        raise Exception()
    else:
        return dataset.text.encode('utf-8')


def is_response_okay(request):
    """Check for network failure."""
    if request.status_code != 200:
        return False
    else:
        return True
