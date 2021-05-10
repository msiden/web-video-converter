import unittest
from video_converter.main import *


SCOPE = {
    'type': 'http', 'asgi': {'version': '3.0', 'spec_version': '2.1'}, 'http_version': '1.1',
    'server': ('127.0.0.1', 8000), 'client': ('127.0.0.1', 55381), 'scheme': 'http', 'method': 'GET', 'root_path': '',
    'path': '/', 'raw_path': b'/', 'query_string': b'', 'headers': [
        (b'host', b'127.0.0.1:8000'), (b'connection', b'keep-alive'), (b'cache-control', b'max-age=0'),
        (b'sec-ch-ua', b'" Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"'),
        (b'sec-ch-ua-mobile', b'?0'), (b'upgrade-insecure-requests', b'1'),
        (b'user-agent',
         b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
         b'(KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56'),
        (b'accept', b'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                    b'application/signed-exchange;v=b3;q=0.9')]}


class VideoConverterTests(unittest.TestCase):

    def test_index(self):
        request = Request(scope=SCOPE)
        result = index(request)
        self.assertIsInstance(result.body, bytes)
        self.assertTrue("<title>Video Converter</title>" in str(result.body))

    def test_get_token(self):
        result = get_token()
        self.assertIsInstance(result, str)
