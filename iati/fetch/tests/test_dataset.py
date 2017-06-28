"""A module containing tests for the library functionality to fetch datasets."""
import iati.fetch
import json
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
        sample_dataset.set_dataset()
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

    def test_get_publishers(self):
        """Result of iati.fetch.get_publishers() will be a list and contain expected results."""
        mock_publishers_response = pkg_resources.resource_stream(__name__, 'organization_list.json').read().decode('utf-8')
        mock_publishers_url = 'http://test.com/publishers'
        responses.add(responses.GET, mock_publishers_url, body=mock_publishers_response)

        publishers = iati.fetch.get_publishers(mock_publishers_url)

        assert isinstance(publishers, list)
        assert publishers == ['mock_iati_publisher_name', 'another_mock_publisher']

    def test_get_publishers_bad_url(self):
        """Given a bad URL is passed into iati.fetch.get_publishers(), an Exception is raised."""
        mock_publishers_bad_url = 'http://test.com/bad_publishers_url'
        responses.add(responses.GET, mock_publishers_bad_url, status=404)

        with pytest.raises(Exception) as excinfo:
            iati.fetch.get_publishers(registry_api_endpoint=mock_publishers_bad_url)

        assert '' in str(excinfo.value)

    def test_get_publishers_not_json(self):
        """Given a non-JSON response, an exception is raised.
        Note that the exception type will vary between Python versions (ValueError < v3.5; json.decoder.JSONDecodeError >= v3.5).
        """
        mock_publishers_not_json = 'http://test.com/publishers/not_json'
        responses.add(responses.GET, mock_publishers_not_json, body='This is not a JSON string.')

        with pytest.raises(Exception) as excinfo:
            iati.fetch.get_publishers(registry_api_endpoint=mock_publishers_not_json)

        assert ((excinfo.typename == 'ValueError' and str(excinfo.value) == 'No JSON object could be decoded')  # Python version < 3.5
                or (excinfo.typename == 'JSONDecodeError' and str(excinfo.value) == 'Expecting value: line 1 column 1 (char 0)'))  # Python version >= 3.5
