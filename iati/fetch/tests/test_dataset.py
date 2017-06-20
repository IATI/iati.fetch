"""A module containing tests for the library functionality to fetch datasets."""
import iati.fetch
import pkg_resources
import requests_mock


@requests_mock.Mocker(kw='mock')
class TestDataset(object):
    """Container for tests relating fetch.Dataset."""

    def test_fetch_by_dataset_id(self, **kwargs):
        """Given a dataset_id, metadata for this dataset will be populated.

        Todo:
          Remove use of live dataset_id.
        """
        sample_dataset = iati.fetch.Dataset(dataset_id='43aa0616-58a4-4d16-b0a9-1181e3871827')
        sample_dataset.set_dataset()
        assert isinstance(sample_dataset.dataset, iati.core.data.Dataset)

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

    def test_registry_metadata_bad_id(self, **kwargs):
        """Given an invalid registry ID, an Exception is raised."""
        pass

    def test_get_dataset(self, **kwargs):
        """Given an expected dataset URL, utf-8 encoded text is returned."""
        mock_dataset = pkg_resources.resource_stream(__name__, 'activity-standard-example-annotated.xml').read().decode()
        mock_dataset_url = 'mock://test.com/{0}'
        kwargs['mock'].get(mock_dataset_url, text=mock_dataset)

        dataset_bytes = iati.fetch.get_dataset(dataset_url=mock_dataset_url)
        dataset_str = dataset_bytes.decode()

        assert dataset_bytes
        assert len(dataset_str.split('\n')) == 353  # File has 353 lines.
        assert 'iati-activities' in dataset_str
        assert 'iati-activity' in dataset_str

    def test_get_dataset_correctly_encoded(self, **kwargs):
        """Given an execpted dataset URL with non-utf-8 data, utf-8 encoded text is returned."""
        pass

    def test_get_dataset_bad_url(self, **kwargs):
        """Given an invalid dataset URL, an Exception is raised."""
        pass
