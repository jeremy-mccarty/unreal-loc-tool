import unittest
from app.unreal_loc_tool import escape_po

class TestEscapePo(unittest.TestCase):
    def test_escape_quotes(self):
        self.assertEqual(escape_po('"Hello"'), '\\"Hello\\"')
        self.assertEqual(escape_po('No quotes'), 'No quotes')

if __name__ == '__main__':
    unittest.main()
