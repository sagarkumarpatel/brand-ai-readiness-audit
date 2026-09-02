import unittest
from unittest.mock import patch, MagicMock
from src.renderer.renderer import SafeRenderer

class TestRenderer(unittest.TestCase):
    @patch('src.renderer.renderer.time.time')
    def test_successful_render(self, mock_time):
        mock_time.side_effect = [0, 1] # start and end time
        
        # We need to mock the import of playwright in renderer.py
        with patch('sys.modules', new={}):
            mock_playwright = MagicMock()
            mock_sync = MagicMock()
            mock_context = MagicMock()
            mock_browser = MagicMock()
            mock_page = MagicMock()
            
            mock_sync.return_value.start.return_value = mock_context
            mock_context.chromium.launch.return_value = mock_browser
            mock_browser.new_page.return_value = mock_page
            mock_page.content.return_value = "<html><body>JS Loaded</body></html>"
            mock_page.url = "http://example.com/final"
            mock_response = MagicMock()
            mock_response.status = 200
            mock_page.goto.return_value = mock_response
            
            def evaluate_mock(script):
                if "document.body.innerText" in script:
                    return "JS Loaded"
                return [{"href": "http://example.com/js-link", "text": "JS Link"}]
                
            mock_page.evaluate.side_effect = evaluate_mock
            
            # Use patch.dict to mock sys.modules without affecting others
            with patch.dict('sys.modules', {'playwright.sync_api': MagicMock(sync_playwright=mock_sync)}):
                renderer = SafeRenderer()
                renderer.start()
                result = renderer.render("http://example.com")
                
                self.assertTrue(result.rendered_successfully)
                self.assertEqual(result.status_code, 200)
                self.assertEqual(result.final_url, "http://example.com/final")
                self.assertEqual(result.visible_text, "JS Loaded")
                self.assertEqual(len(result.links), 1)
                self.assertEqual(result.links[0].url, "http://example.com/js-link")

    def test_import_error(self):
        # if playwright is missing, it should raise RuntimeError
        renderer = SafeRenderer()
        with patch.dict('sys.modules', {'playwright.sync_api': None}):
            with self.assertRaises(RuntimeError):
                renderer.start()

if __name__ == '__main__':
    unittest.main()
