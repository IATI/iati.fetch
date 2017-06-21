"""A module containing tests for the library functionality to fetch datasets."""
import iati.fetch
import pytest
import pkg_resources
import requests_mock


class TestDataset(object):
    """Container for tests relating fetch.Dataset."""

    def test_fetch_by_dataset_id(self):
        """Given a dataset_id, metadata for this dataset will be populated.

        Todo:
          Remove use of live dataset_id.
        """
        sample_dataset = iati.fetch.Dataset(dataset_id='43aa0616-58a4-4d16-b0a9-1181e3871827')
        sample_dataset.set_dataset()
        assert isinstance(sample_dataset.dataset, iati.core.data.Dataset)

    @requests_mock.mock(kw='mock')
    def test_get_metadata(self, **kwargs):
        """Given a mock registry ID, metadata will be returned.

        Todo:
          Remove use of live URL in mock metadata.
        """
        mock_metadata = pkg_resources.resource_stream(__name__, 'mock-registry-metadata.json').read().decode()
        mock_registry_url = 'mock://test.com/{0}'
        kwargs['mock'].get(mock_registry_url.format('sample'), text=mock_metadata)
        assert iati.fetch.get_metadata(dataset_id='sample',
                                       registry_api_endpoint=mock_registry_url
                                       ) == {'result': {
                                            'resources': [
                                                {'url': 'https://www.vsointernational.org/sites/default/files/aasaman_gec.xml'}
                                                ]
                                            }
                                        }

    @requests_mock.mock(kw='mock')
    def test_registry_metadata_bad_id(self, **kwargs):
        """Given an invalid registry ID, an Exception is raised."""
        mock_registry_url = 'mock://test.com/{0}'
        kwargs['mock'].get(mock_registry_url.format('invalid_id'), status_code=404)

        with pytest.raises(Exception)as excinfo:
            iati.fetch.get_metadata(dataset_id='invalid_id',
                                    registry_api_endpoint=mock_registry_url)
        assert '' in str(excinfo.value)

    def test_get_dataset(self):
        """Given an execpted dataset URL, utf-8 encoded text is returned."""
        pass

    def test_get_dataset_correctly_encoded(self):
        """Given an accepted dataset URL with non-utf-8 data, utf-8 encoded text is returned."""
        # assert iati.fetch.get_dataset()
        pass

    def test_get_dataset_bad_url(self):
        """Given an invalid dataset URL, an Exception is raised."""
        pass
