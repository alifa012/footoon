import importlib
import os
import tempfile
import unittest

from fastapi.testclient import TestClient


class FootToonAppTests(unittest.TestCase):
    def setUp(self):
        fd, path = tempfile.mkstemp()
        os.close(fd)
        self.db_path = path
        os.environ["FOOTOON_DB"] = self.db_path
        self.app_module = importlib.import_module("app")
        self.app_module = importlib.reload(self.app_module)
        self.client = TestClient(self.app_module.app)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_create_idea_persists_and_lists(self):
        self.app_module.fetch_football_context = lambda: ["Team A vs Team B (1-0)"]
        self.app_module.fetch_social_trends = lambda: {"reddit": ["Meme moment"]}
        self.app_module.fetch_song_trends = lambda: ["Top Song"]

        created = self.client.post("/api/ideas", json={"prompt": "Make it dramatic"})
        self.assertEqual(created.status_code, 200)
        created_payload = created.json()
        self.assertIn("id", created_payload)
        self.assertIn("Make it dramatic", created_payload["body"])

        listed = self.client.get("/api/ideas")
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(len(listed.json()), 1)

    def test_download_returns_attachment(self):
        self.app_module.fetch_football_context = lambda: ["Team A vs Team B (1-0)"]
        self.app_module.fetch_social_trends = lambda: {"reddit": ["Meme moment"]}
        self.app_module.fetch_song_trends = lambda: ["Top Song"]

        created = self.client.post("/api/ideas", json={})
        created_payload = created.json()
        idea_id = created_payload["id"]

        download = self.client.get(f"/api/ideas/{idea_id}/download")
        self.assertEqual(download.status_code, 200)
        self.assertIn("attachment; filename=\"footoon-idea-", download.headers["content-disposition"])
        self.assertIn(created_payload["title"], download.text)
        self.assertIn(created_payload["body"], download.text)

    def test_create_idea_accepts_form_payload(self):
        self.app_module.fetch_football_context = lambda: ["Team A vs Team B (1-0)"]
        self.app_module.fetch_social_trends = lambda: {"reddit": ["Meme moment"]}
        self.app_module.fetch_song_trends = lambda: ["Top Song"]

        created = self.client.post("/api/ideas", data={"prompt": "Form prompt"})
        self.assertEqual(created.status_code, 200)
        self.assertIn("Form prompt", created.json()["body"])


if __name__ == "__main__":
    unittest.main()
