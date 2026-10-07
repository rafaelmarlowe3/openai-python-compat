import pathlib,unittest
class T(unittest.TestCase):
 def test_headers(self):
  s=pathlib.Path("examples/video_httpx.py").read_text();self.assertIn("User-Agent",s);self.assertIn("/videos/generations",s)
if __name__=='__main__':unittest.main()
