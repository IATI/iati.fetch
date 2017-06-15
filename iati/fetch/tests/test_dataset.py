"""A module containing tests for the library functionality to fetch datasets."""
import iati.core
import iati.fetch
import requests_mock


class TestDatset(object):
    """Container for tests relating fetch.Dataset."""

    def test_fetch_by_dataset_id(self):
        """Given a dataset_id, metadata for this dataset will be populated."""
        sample_dataset = iati.fetch.Dataset(dataset_id='43aa0616-58a4-4d16-b0a9-1181e3871827')

        assert isinstance(sample_dataset.dataset, iati.core.data.Dataset)
