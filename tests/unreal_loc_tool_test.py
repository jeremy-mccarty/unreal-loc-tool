import unittest
import os
from app import unreal_loc_tool

class TestUnrealLocTool(unittest.TestCase):
    def setUp(self):
        self.csv_sample = os.path.join(os.path.dirname(__file__), '../samples/sample.csv')
        self.po_sample = os.path.join(os.path.dirname(__file__), '../samples/sample.po')
        self.output_dir = os.path.join(os.path.dirname(__file__), 'test_output')
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
        # Clean up output files
        for f in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, f))
        os.rmdir(self.output_dir)

    def test_detect_language_from_filename(self):
        lang = unreal_loc_tool.detect_language_from_filename('Game.csv')
        self.assertEqual(lang, 'Game')

    def test_csv_to_po_and_po_to_csv(self):
        # Convert CSV to PO
        po_result = unreal_loc_tool.csv_to_po(self.csv_sample, self.output_dir)
        self.assertTrue('Generated' in po_result)
        po_path = os.path.join(self.output_dir, 'sample.po')
        self.assertTrue(os.path.exists(po_path))

        # Convert PO to CSV
        csv_result = unreal_loc_tool.po_to_csv(po_path, os.path.join(self.output_dir, 'roundtrip.csv'))
        self.assertTrue('Generated' in csv_result)
        csv_path = os.path.join(self.output_dir, 'roundtrip.csv')
        self.assertTrue(os.path.exists(csv_path))

    def test_batch_convert(self):
        result = unreal_loc_tool.batch_convert(os.path.join(os.path.dirname(__file__), '../samples'), self.output_dir)
        self.assertTrue('Batch convert successful' in result)

if __name__ == '__main__':
    unittest.main()
