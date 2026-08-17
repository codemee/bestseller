"""天瓏網站的節流與暫時性錯誤重試工具。"""

from __future__ import annotations

import random
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import requests


class RateLimitedSession:
    """限制請求頻率，並對 429、5xx 與連線錯誤進行退避重試。"""

    def __init__(self, session=None, *, min_delay=3.0, max_delay=5.0,
                 max_retries=5, timeout=30, sleep=time.sleep,
                 uniform=random.uniform, monotonic=time.monotonic):
        self.session = session or requests.Session()
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.max_retries = max_retries
        self.timeout = timeout
        self.sleep = sleep
        self.uniform = uniform
        self.monotonic = monotonic
        self.last_request_at = None

    def _throttle(self):
        if self.last_request_at is None:
            return
        target_delay = self.uniform(self.min_delay, self.max_delay)
        remaining = target_delay - (self.monotonic() - self.last_request_at)
        if remaining > 0:
            self.sleep(remaining)

    @staticmethod
    def _retry_after(response, attempt):
        value = response.headers.get("Retry-After", "").strip()
        if value.isdigit():
            return max(1, int(value))
        if value:
            try:
                retry_at = parsedate_to_datetime(value)
                if retry_at.tzinfo is None:
                    retry_at = retry_at.replace(tzinfo=timezone.utc)
                return max(1, int((retry_at - datetime.now(timezone.utc)).total_seconds()))
            except (TypeError, ValueError, OverflowError):
                pass
        return 30 * (2 ** attempt)

    def get(self, url, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        for attempt in range(self.max_retries + 1):
            self._throttle()
            try:
                response = self.session.get(url, **kwargs)
                self.last_request_at = self.monotonic()
                retryable = response.status_code == 429 or 500 <= response.status_code < 600
                if not retryable:
                    response.raise_for_status()
                    return response
                if attempt == self.max_retries:
                    response.raise_for_status()
                delay = min(self._retry_after(response, attempt), 900)
                self._log_retry(f"HTTP {response.status_code}", delay, attempt, url)
                self.sleep(delay)
            except requests.RequestException as error:
                self.last_request_at = self.monotonic()
                status = getattr(getattr(error, "response", None), "status_code", None)
                if status is not None and 400 <= status < 500 and status != 429:
                    raise
                if attempt == self.max_retries:
                    raise
                delay = min(30 * (2 ** attempt), 900)
                self._log_retry(str(error), delay, attempt, url)
                self.sleep(delay)
        raise RuntimeError("請求重試流程異常結束")

    def _log_retry(self, reason, delay, attempt, url):
        timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
        print(
            f"[{timestamp}] {reason}；{delay} 秒後重試 "
            f"({attempt + 1}/{self.max_retries})：{url}", flush=True,
        )
