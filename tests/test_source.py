import pathlib
import unittest

ROOT = pathlib.Path(__file__).parents[1]


class SourceTests(unittest.TestCase):
    def test_sdk_is_lazy_and_retries_are_explicit(self):
        source = (ROOT / "examples/client.py").read_text(encoding="utf-8")
        self.assertIn("max_retries=0", source)
        self.assertIn("OPENAI_API_KEY", source)
        self.assertNotIn("client = OpenAI", source)

    def test_video_contract_is_explicit_and_import_safe(self):
        source = (ROOT / "examples/video_httpx.py").read_text(encoding="utf-8")
        self.assertIn("User-Agent", source)
        self.assertIn("/videos/generations", source)
        self.assertIn("/videos/" + '" + request_id + "', source)
        self.assertIn('"done", "failed", "expired"', source)
        self.assertNotIn("/v1/" + "tasks", source)

    def test_local_validation_without_key(self):
        namespace = {}
        exec((ROOT / "examples/client.py").read_text(encoding="utf-8"), namespace)
        with self.assertRaises(ValueError):
            namespace["chat"](" ")


if __name__ == "__main__":
    unittest.main()
