import unittest
from markdown_convertor.text_processing import process_text


class TestTextProcessing(unittest.TestCase):
    def test_primitive(self):
        expected_result = "<p><tt>monospaced</tt></p>"
        input_markdown = "`monospaced`"
        result = process_text(input_markdown, "html")
        self.assertEqual(expected_result, result)

    def test_one_entity(self):
        text = "Some `monospaced` text."
        self.assertEqual(process_text(text, "html"), "<p>Some <tt>monospaced</tt> text.</p>")

    def test_non_closed_tag(self):
        text = "Some `monospaced text."
        with self.assertRaises(ValueError) as context:
            process_text(text, "html")
        self.assertEqual(str(context.exception), "Non-closed tag found")

    def test_nested_tag(self):
        text = "Some `bold **and** monospaced` text."
        with self.assertRaises(ValueError) as context:
            process_text(text, "html")
        self.assertEqual(str(context.exception), "Nested tags found")

    def test_non_separated_tag(self):
        text = "Some`mono`spaced`text."
        self.assertEqual(process_text(text, "html"), "<p>Some`mono`spaced`text.</p>")

    def test_separated_tag(self):
        text = "Some ` monospaced ` text."
        self.assertEqual(process_text(text, "html"), "<p>Some ` monospaced ` text.</p>")

    def test_multiple_monospaced_tags(self):
        text = "Some `monospaced` text with `very monospaced` and `monospaced` characters."
        expected_result = "<p>Some <tt>monospaced</tt> text with <tt>very monospaced</tt> and <tt>monospaced</tt> characters.</p>"
        self.assertEqual(process_text(text, "html"), expected_result)

    def test_different_styles(self):
        text = "**Bold** text with _italic_ and `monospaced`."
        expected_result = "<p><b>Bold</b> text with <i>italic</i> and <tt>monospaced</tt>.</p>"
        self.assertEqual(process_text(text, "html"), expected_result)


if __name__ == '__main__':
    unittest.main()
