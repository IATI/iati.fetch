"""A module containing tests for the library functionality to fetch datasets."""
import pkg_resources
import pytest
import requests_mock
import iati.fetch


class TestDataset(object):
    """Container for tests relating fetch.Dataset."""

    @pytest.fixture
    @requests_mock.Mocker(kw='mock')
    def mock_registry_metadata(self, **kwargs):  # Needs to be generisised.
        """Mock for registry metadata and returns specific dataset_url.

        Todo:
          Remove use of live URL in mock metadata.
        """
        mock_metadata = pkg_resources.resource_stream(__name__, 'mock-registry-metadata.json').read().decode()
        mock_registry_url = iati.fetch.REGISTRY_API_METADATA_BY_DATASET_ID.format('sample')
        kwargs['mock'].get(mock_registry_url, text=mock_metadata)
        mock_registry_metadata = iati.fetch.get_metadata(dataset_id='sample')
        return mock_registry_metadata

    def test_fetch_by_dataset_id(self):
        """Given a dataset_id, metadata for this dataset will be populated.

        Todo:
          Remove use of live dataset_id.
        """
        sample_dataset = iati.fetch.Dataset(dataset_id='43aa0616-58a4-4d16-b0a9-1181e3871827')
        sample_dataset.set_dataset()
        assert isinstance(sample_dataset.dataset, iati.core.data.Dataset)

    def test_get_metadata(self, mock_registry_metadata):
        """Given a mock registry ID, metadata will be returned."""
        assert mock_registry_metadata == {'result': {
            'resources': [
                {'url': 'https://www.vsointernational.org/sites/default/files/aasaman_gec.xml'}
                ]
            }
        }
