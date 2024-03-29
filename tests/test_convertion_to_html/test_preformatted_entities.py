import unittest
from markdown_convertor.text_processing import process_text


class TestTextProcessing(unittest.TestCase):
    def test_primitive(self):
        expected_result = "<p><pre>preformatted</pre></p>"
        input_markdown = "```preformatted```"
        result = process_text(input_markdown, "html")
        self.assertEqual(expected_result, result)

    def test_one_entity(self):
        text = """
Some ```preformatted **bold** or _italic_```
text.
"""
        expected_result = ('<p> Some </p>\n'
                           '<p><pre>preformatted **bold** or _italic_</pre></p>\n'
                           '<p> text. </p>')
        self.assertEqual(process_text(text, "html"), expected_result)

    def test_non_closed_tag(self):
        text = "```preformatted **bold or italic_```"
        expected_result = "<p><pre>preformatted **bold or italic_</pre></p>"
        self.assertEqual(process_text(text, "html"), expected_result)

    def test_nested_tag(self):
        text = "```Some `bold **and** monospaced` text.```"
        expected_result = "<p><pre>Some `bold **and** monospaced` text.</pre></p>"
        self.assertEqual(process_text(text, "html"), expected_result)


if __name__ == '__main__':
    unittest.main()
