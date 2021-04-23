import unittest
import bitrate_converter

QUEUE_ITEMS = ["file1", "file2"]


class BRConverterTests(unittest.TestCase):

    def setUp(self):
        self.br_converter = bitrate_converter.BitRateConverter()
        self.assertIs(self.br_converter.add_to_queue(QUEUE_ITEMS), None)

    def test_get_queue(self):
        result = self.br_converter.get_queue()
        result.sort()
        self.assertEqual(result, QUEUE_ITEMS)

    def test_clear_queue(self):
        self.assertIs(self.br_converter.clear_queue(), None)
        result = self.br_converter.get_queue()
        self.assertEqual(result, [])

    def test_get_progress(self):
        self.assertEqual(self.br_converter.get_progress(), [])

    def test_get_done_items(self):
        self.assertEqual(self.br_converter.get_done_items(), [])

    def test_process_queue_and_get_failed_items(self):
        self.assertIs(self.br_converter.process_queue(), None)
        failed_items = self.br_converter.get_failed_items()
        failed_items.sort()
        self.assertEqual(failed_items, QUEUE_ITEMS)

    def test_set_and_get_bitrate(self):
        self.assertIs(self.br_converter.set_bitrate(4), None)
        self.assertEqual(self.br_converter.get_bitrate(), "4M")
