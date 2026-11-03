"""Offline tests for the Agent-ai-backend Flask app.

The OpenRouter API and DuckDuckGo calls are mocked; no network or API key is
required.
"""
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import app as agent_app


def _fake_ai_reply(text):
    resp = mock.Mock()
    resp.json.return_value = {"choices": [{"message": {"content": text}}]}
    return resp


class TestChatBodyValidation(unittest.TestCase):
    def setUp(self):
        agent_app.app.testing = True
        self.client = agent_app.app.test_client()

    def test_non_object_json_body_returns_400(self):
        for payload in ("null", "[]", '"text"', "42"):
            resp = self.client.post(
                "/api/chat", data=payload, content_type="application/json"
            )
            self.assertEqual(resp.status_code, 400, f"payload {payload!r}")
            self.assertIn("error", resp.get_json())


class TestOutboundTimeouts(unittest.TestCase):
    def test_web_search_uses_a_timeout(self):
        fake = mock.Mock()
        fake.json.return_value = {"AbstractText": "answer", "RelatedTopics": []}
        with mock.patch.object(
            agent_app.requests, "get", return_value=fake
        ) as get:
            self.assertEqual(agent_app.web_search("test"), "answer")
        self.assertEqual(get.call_args.kwargs.get("timeout"), 10)

    def test_chat_api_call_uses_a_timeout(self):
        agent_app.user_sessions.clear()
        agent_app.app.testing = True
        client = agent_app.app.test_client()
        with mock.patch.object(
            agent_app.requests, "post", return_value=_fake_ai_reply("hi")
        ) as post:
            resp = client.post("/api/chat", json={"message": "hello"})
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.get_json()["response"], "hi")
        self.assertEqual(post.call_args.kwargs.get("timeout"), 30)


class TestIndexRoute(unittest.TestCase):
    def test_index_serves_the_chat_page(self):
        agent_app.app.testing = True
        client = agent_app.app.test_client()
        resp = client.get("/")
        self.assertEqual(resp.status_code, 200)
        body = resp.get_data(as_text=True)
        self.assertIn("/api/chat", body)
        self.assertIn("<form", body)


if __name__ == "__main__":
    unittest.main()
