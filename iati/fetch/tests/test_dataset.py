"""A module containing tests for the library functionality to fetch datasets."""
import iati.fetch
import pkg_resources
import requests_mock


class TestDataset(object):
    """Container for tests relating fetch.Dataset."""

    def test_fetch_by_dataset_id(self):
        """Given a dataset_id, metadata for this dataset will be populated."""
        sample_dataset = iati.fetch.Dataset(dataset_id='43aa0616-58a4-4d16-b0a9-1181e3871827')
        sample_dataset.set_dataset()
        assert isinstance(sample_dataset.dataset, iati.core.data.Dataset)

    @requests_mock.Mocker(kw='mock')
    def test_get_metadata(self, **kwargs):
        """Given a mock registry ID, metadata will be returned."""
        mock_metadata = pkg_resources.resource_stream(__name__, 'mock-registry-metadata.json').read().decode()
        kwargs['mock'].get('https://iatiregistry.org/api/3/action/package_show?id=sample', text=mock_metadata)
        assert iati.fetch.get_metadata(dataset_id='sample') == {'result': {
            'resources': [
                {'url': 'https://www.vsointernational.org/sites/default/files/aasaman_gec.xml'}
                ]
            }
        }
