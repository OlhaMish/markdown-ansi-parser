import unittest
from markdown_convertor.text_processing import process_text


class TestTextProcessing(unittest.TestCase):
    def test_primitive(self):
        expected_result = "\x1b[7mpreformatted\x1b[27m"
        input_markdown = "```preformatted```"
        result = process_text(input_markdown, "ansi")

        self.assertEqual(expected_result, result)

    def test_one_entity(self):
        text = """
Some ```preformatted **bold** or _italic_```
text.
"""
        expected_result = ('\n'
                           'Some \x1b[7mpreformatted **bold** or _italic_\x1b[27m\n'
                           'text.\n')
        self.assertEqual(process_text(text, "ansi"), expected_result)

    def test_non_closed_tag(self):
        text = "```preformatted **bold or italic_```"
        expected_result = "\x1b[7mpreformatted **bold or italic_\x1b[27m"
        self.assertEqual(process_text(text, "ansi"), expected_result)

    def test_nested_tag(self):
        text = "```Some `bold **and** monospaced` text.```"
        expected_result = "\x1b[7mSome `bold **and** monospaced` text.\x1b[27m"
        self.assertEqual(process_text(text, "ansi"), expected_result)


if __name__ == '__main__':
    unittest.main()
