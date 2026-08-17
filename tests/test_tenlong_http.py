import unittest

import requests

from tenlong_http import RateLimitedSession


class FakeResponse:
    def __init__(self, status, headers=None):
        self.status_code = status
        self.headers = headers or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            error = requests.HTTPError(f"HTTP {self.status_code}")
            error.response = self
            raise error


class FakeSession:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = 0

    def get(self, _url, **_kwargs):
        self.calls += 1
        return next(self.responses)


class RateLimitedSessionTests(unittest.TestCase):
    def test_retries_429_and_honors_retry_after(self):
        session = FakeSession([
            FakeResponse(429, {"Retry-After": "7"}),
            FakeResponse(200),
        ])
        sleeps = []
        client = RateLimitedSession(
            session, min_delay=0, max_delay=0,
            sleep=sleeps.append, monotonic=lambda: 0,
        )
        result = client.get("https://example.test")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(session.calls, 2)
        self.assertIn(7, sleeps)

    def test_retries_server_error_with_exponential_backoff(self):
        session = FakeSession([FakeResponse(503), FakeResponse(200)])
        sleeps = []
        client = RateLimitedSession(
            session, min_delay=0, max_delay=0,
            sleep=sleeps.append, monotonic=lambda: 0,
        )
        self.assertEqual(client.get("https://example.test").status_code, 200)
        self.assertIn(30, sleeps)

    def test_raises_after_retry_limit(self):
        session = FakeSession([FakeResponse(503), FakeResponse(503)])
        client = RateLimitedSession(
            session, min_delay=0, max_delay=0, max_retries=1,
            sleep=lambda _seconds: None, monotonic=lambda: 0,
        )
        with self.assertRaises(requests.HTTPError):
            client.get("https://example.test")

    def test_does_not_retry_non_retryable_client_error(self):
        session = FakeSession([FakeResponse(404), FakeResponse(200)])
        client = RateLimitedSession(
            session, min_delay=0, max_delay=0,
            sleep=lambda _seconds: None, monotonic=lambda: 0,
        )
        with self.assertRaises(requests.HTTPError):
            client.get("https://example.test")
        self.assertEqual(session.calls, 1)

    def test_throttles_consecutive_requests(self):
        session = FakeSession([FakeResponse(200), FakeResponse(200)])
        sleeps = []
        client = RateLimitedSession(
            session, min_delay=3, max_delay=5,
            sleep=sleeps.append, uniform=lambda _a, _b: 4,
            monotonic=lambda: 10,
        )
        client.get("https://example.test/1")
        client.get("https://example.test/2")
        self.assertEqual(sleeps, [4])


if __name__ == "__main__":
    unittest.main()
