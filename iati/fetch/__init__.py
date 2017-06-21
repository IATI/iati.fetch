"""A module containing functionality for iati.fetch."""
import iati.core.data
import json
import requests

REGISTRY_API_METADATA_BY_DATASET_ID = "https://iatiregistry.org/api/3/action/package_show?id={0}"


class Dataset(object):
    """Container class to fetch a dataset."""

    def __init__(self, dataset_id):
        """Fetch a dataset by registry dataset ID.

        Args:
            dataset_id (str): The Registry UUID for the dataset.
        """
        self.dataset_id = dataset_id
        self.dataset = None

    def set_dataset(self):
        """Set dataset from the dataset ID."""
        registry_metadata = get_metadata(self.dataset_id)
        dataset_url = registry_metadata['result']['resources'][0]['url']
        dataset = get_dataset(dataset_url)
        self.dataset = iati.core.data.Dataset(dataset)


def get_metadata(dataset_id, registry_api_endpoint=REGISTRY_API_METADATA_BY_DATASET_ID):
    """Get registry metadata for given dataset ID.

    Args:
        dataset_id (str): The Registry UUID for the dataset metadata to be returned.
        registry_api_endpoint (str): The API endpoint URL for obtaining dataset metadata for a given Registry dataset UUID.

    Raises:
        Exception: When a HTTP 200 response code is not received.

    Returns:
        dict: A dictionary containing the data returned by the Registry API.

    """
    req = requests.get(registry_api_endpoint.format(dataset_id))

    if not is_response_okay(req):
        raise Exception()
    else:
        registry_metadata = json.loads(req.text)
        return registry_metadata


def get_dataset(dataset_url):
    """Get dataset from dataset URL.

    Raises:
        Exception: When a HTTP 200 response code is not received.

    Args:
        dataset_url (str): The URL of the dataset to be returned.

    Returns:
        str: The data contained at the dataset_url.

    """
    dataset = requests.get(dataset_url)
    if not is_response_okay(dataset):
        raise Exception()
    else:
        if dataset.encoding == 'utf-8':
            dataset_text = dataset.text
        else:
            dataset_text = dataset.text.encode('utf-8')
        return dataset_text


def is_response_okay(request):
    """Check for network failure.

    Args:
        request (requests.Response): A Response object, generated from a request.

    Returns:
        bool: True is the HTTP status code is 200, or False otherwise.

    Todo:
        Delete this function and use builtin requests.status.ok instead.

    """
    if request.status_code != 200:
        return False
    else:
        return True
