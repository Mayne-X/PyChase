"""Completely unique code — no duplicates anywhere. Tests false positive rate."""

import json
import hashlib


class ConfigParser:
    def __init__(self, path):
        self.path = path
        self.data = {}

    def load(self):
        with open(self.path) as f:
            self.data = json.load(f)

    def get(self, key, default=None):
        keys = key.split(".")
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default


def compute_checksum(filepath, algorithm="sha256"):
    h = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


class RateLimiter:
    def __init__(self, max_calls, window):
        self.max_calls = max_calls
        self.window = window
        self.calls = []

    def allow(self):
        now = __import__("time").time()
        self.calls = [t for t in self.calls if now - t < self.window]
        if len(self.calls) >= self.max_calls:
            return False
        self.calls.append(now)
        return True
