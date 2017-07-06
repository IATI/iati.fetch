"""A module containing tests for the library functionality to fetch datasets."""
import iati.fetch
import pytest
import pkg_resources
import responses


class TestDataset(object):
    """Container for tests relating fetch.Dataset."""

    @pytest.mark.withoutresponses
    def test_fetch_by_dataset_id(self):
        """Given a dataset_id, metadata for this dataset will be populated.

        Todo:
          Remove use of live dataset_id.
        """
        sample_dataset = iati.fetch.Dataset(dataset_id='43aa0616-58a4-4d16-b0a9-1181e3871827')
        assert isinstance(sample_dataset.dataset, iati.core.data.Dataset)

    def test_get_metadata(self):
        """Given a mock registry ID, metadata will be returned.

        Todo:
          Remove use of live URL in mock metadata.
        """
        mock_metadata = pkg_resources.resource_stream(__name__, 'mock-registry-metadata.json').read().decode()
        mock_registry_url = 'http://test.com/sample'
        responses.add(responses.GET, mock_registry_url, body=mock_metadata)
        assert iati.fetch.get_metadata(dataset_id='sample',
                                       registry_api_endpoint='http://test.com/{0}'
                                       ) == {'result': {
                                            'resources': [
                                                {'url': 'https://www.vsointernational.org/sites/default/files/aasaman_gec.xml'}
                                                ]
                                            }
                                        }

    def test_registry_metadata_bad_id(self):
        """Given an invalid registry ID, an Exception is raised.

        Todo:
            Refactor to incorporate pending changes to status code exception.
        """
        mock_registry_url = 'mock://test.com/{0}'
        responses.add(responses.GET, mock_registry_url.format('invalid_id'), status=404)

        with pytest.raises(Exception) as excinfo:
            iati.fetch.get_metadata(dataset_id='invalid_id',
                                    registry_api_endpoint=mock_registry_url)
        assert '' in str(excinfo.value)

    def test_get_dataset(self):
        """Given an expected dataset URL, utf-8 encoded text is returned."""
        mock_dataset = pkg_resources.resource_stream(__name__, 'activity-standard-example-annotated.xml').read().decode('utf-8')
        mock_dataset_url = 'http://test.com/dataset'
        responses.add(responses.GET, mock_dataset_url, body=mock_dataset)

        dataset = iati.fetch.get_dataset(dataset_url=mock_dataset_url)

        assert dataset
        assert len(dataset.split('\n')) == 353  # File has 353 lines.
        assert 'iati-activities' in dataset
        assert 'iati-activity' in dataset

    def test_get_dataset_correctly_encoded(self):
        """Given an accepted dataset URL with non-utf-8 data, utf-8 encoded text is returned."""
        # assert iati.fetch.get_dataset()
        pass

    def test_get_dataset_bad_url(self):
        """Given an invalid dataset URL, an Exception is raised."""
        pass
