import unittest
from unittest.mock import patch, MagicMock
from autosearch.api.search_manager import SearchManager
from autosearch.data.paper import Paper

class TestSearchManager(unittest.TestCase):

    @patch('autosearch.api.search_manager.ArxivAPI')
    @patch('autosearch.api.search_manager.GoogleScholarAPI')
    @patch('autosearch.database.paper_database.PaperDatabase')
    def setUp(self, MockPaperDatabase, MockGoogleScholarAPI, MockArxivAPI):
        self.mock_arxiv_api = MockArxivAPI.return_value
        self.mock_google_scholar_api = MockGoogleScholarAPI.return_value
        self.mock_paper_db = MockPaperDatabase.return_value
        self.search_manager = SearchManager(project_dir='/fake/dir')

    def test_search_all(self):
        self.mock_arxiv_api.search.return_value = [Paper(title="Arxiv Paper", url="http://arxiv.org/abs/1234")]
        self.mock_google_scholar_api.search.return_value = [Paper(title="Google Scholar Paper", url="http://scholar.google.com/abs/5678")]

        results = self.search_manager.search_all("quantum computing", 5)

        self.assertIn('arxiv', results)
        self.assertIn('google_scholar', results)
        self.assertEqual(len(results['arxiv']), 1)
        self.assertEqual(len(results['google_scholar']), 1)

    def test_download_pdf(self):
        paper = Paper(title="Test Paper", url="http://arxiv.org/abs/1234", source="arxiv")
        self.mock_arxiv_api.download_pdf.return_value = "/fake/dir/1234.pdf"

        pdf_path = self.search_manager.download_pdf(paper, "/fake/dir")

        self.assertEqual(pdf_path, "/fake/dir/1234.pdf")
        self.mock_arxiv_api.download_pdf.assert_called_once_with("http://arxiv.org/abs/1234", "/fake/dir/1234.pdf")

    def test_search_and_download(self):
        self.mock_arxiv_api.search.return_value = [Paper(title="Arxiv Paper", url="http://arxiv.org/abs/1234", source="arxiv")]
        self.mock_google_scholar_api.search.return_value = [Paper(title="Google Scholar Paper", url="http://scholar.google.com/abs/5678", source="google_scholar")]
        self.mock_arxiv_api.download_pdf.return_value = "/fake/dir/1234.pdf"
        self.mock_google_scholar_api.download_pdf.return_value = "/fake/dir/5678.pdf"

        results = self.search_manager.search_and_download("quantum computing", 5, "/fake/dir")

        self.assertIn('arxiv', results)
        self.assertIn('google_scholar', results)
        self.assertEqual(len(results['arxiv']), 1)
        self.assertEqual(len(results['google_scholar']), 1)
        self.assertEqual(results['arxiv'][0].local_path, "/fake/dir/1234.pdf")
        self.assertEqual(results['google_scholar'][0].local_path, "/fake/dir/5678.pdf")

if __name__ == '__main__':
    unittest.main()
