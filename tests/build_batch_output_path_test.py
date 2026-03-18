import unittest
from app.unreal_loc_tool import build_batch_output_path

class TestBuildBatchOutputPath(unittest.TestCase):
    def test_csv_output(self):
        out = build_batch_output_path('file.csv', 'output')
        self.assertEqual(out, 'output')

    def test_po_output(self):
        out = build_batch_output_path('file.po', 'output')
        self.assertEqual(out, 'output/file.csv')

    def test_unsupported(self):
        with self.assertRaises(ValueError):
            build_batch_output_path('file.txt', 'output')

if __name__ == '__main__':
    unittest.main()
