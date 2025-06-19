import unittest
import yaml
import requests
from pathlib import Path

TOOLS_FILE = Path('tools.yaml')

class TestLinks(unittest.TestCase):
    def test_links_accessible(self):
        with TOOLS_FILE.open() as f:
            tools = yaml.safe_load(f)
        for group, items in tools.items():
            for tool in items:
                url = tool['url']
                try:
                    r = requests.head(url, timeout=5, allow_redirects=True)
                    self.assertTrue(r.status_code < 400, f"{url} returned {r.status_code}")
                except Exception as e:
                    self.fail(f"Error accessing {url}: {e}")

if __name__ == '__main__':
    unittest.main()
