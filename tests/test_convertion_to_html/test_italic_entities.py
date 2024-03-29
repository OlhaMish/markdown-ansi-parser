import unittest
from markdown_convertor.text_processing import process_text


class TestTextProcessing(unittest.TestCase):
    def test_primitive(self):
        expected_result = "<p><i>italic</i></p>"
        input_markdown = "_italic_"
        result = process_text(input_markdown, "html")

        self.assertEqual(expected_result, result)

    def test_one_entity(self):
        text = "Some _italic_ text."
        self.assertEqual(process_text(text, "html"), "<p>Some <i>italic</i> text.</p>")

    def test_text_with_underline(self):
        text = "Some _ita_lic_ text."
        self.assertEqual(process_text(text, "html"), "<p>Some <i>ita_lic</i> text.</p>")

    def test_non_closed_tag(self):
        text = "Some _italic text."
        with self.assertRaises(ValueError) as context:
            process_text(text, "html")
        self.assertEqual(str(context.exception), "Non-closed tag found")

    def test_nested_tag(self):
        text = "Some _bold **and** italic_ text."
        with self.assertRaises(ValueError) as context:
            process_text(text, "html")
        self.assertEqual(str(context.exception), "Nested tags found")

    def test_non_separated_tag(self):
        text = "Someita_lic_text."
        self.assertEqual(process_text(text, "html"), "<p>Someita_lic_text.</p>")

    def test_separated_tag(self):
        text = "Some _ bold _ text."
        self.assertEqual(process_text(text, "html"), "<p>Some _ bold _ text.</p>")

    def test_multiple_italic_tags(self):
        text = "Some _italic_ text with _very italic_ and _italic_ characters."
        expected_result = "<p>Some <i>italic</i> text with <i>very italic</i> and <i>italic</i> characters.</p>"
        self.assertEqual(process_text(text, "html"), expected_result)

    def test_different_styles(self):
        text = "**Bold** text with _italic_ and `monospaced`."
        expected_result = "<p><b>Bold</b> text with <i>italic</i> and <tt>monospaced</tt>.</p>"
        self.assertEqual(process_text(text, "html"), expected_result)


if __name__ == '__main__':
    unittest.main()
