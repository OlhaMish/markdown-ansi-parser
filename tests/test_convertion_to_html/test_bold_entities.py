import unittest
from markdown_convertor.text_processing import process_text


class TestTextProcessing(unittest.TestCase):
    def test_primitive(self):
        expected_result = "<p><b>bold</b></p>"
        input_markdown = "**bold**"
        result = process_text(input_markdown, "html")

        self.assertEqual(expected_result, result)

    def test_one_entity(self):
        text = "Some **bold** text."
        expected_result = "<p>Some <b>bold</b> text.</p>"
        self.assertEqual(process_text(text, "html"), expected_result)

    def test_text_without_bold(self):
        text = "Some plain text."
        expected_result = "<p>Some plain text.</p>"
        self.assertEqual(process_text(text, "html"), expected_result)

    def test_non_closed_tag(self):
        text = "Some **bold text."
        with self.assertRaises(ValueError) as context:
            process_text(text, "html")
        self.assertEqual(str(context.exception), "Non-closed tag found")

    def test_nested_tag(self):
        text = "Some ***bold _and_ italic** text."
        with self.assertRaises(ValueError) as context:
            process_text(text, "html")
        self.assertEqual(str(context.exception), "Nested tags found")

    def test_non_separated_tag(self):
        text = "Somebo**ld**text."
        expected_result = "<p>Somebo**ld**text.</p>"
        self.assertEqual(process_text(text, "html"), expected_result)

    def test_separated_tag(self):
        text = "Some ** bold ** text."
        expected_result = "<p>Some ** bold ** text.</p>"
        self.assertEqual(process_text(text, "html"), expected_result)

    def test_invalid_tag(self):
        text = "Some *italic* text."
        expected_result = "<p>Some *italic* text.</p>"
        self.assertEqual(process_text(text, "html"), expected_result)

    def test_multiple_bold_tags(self):
        text = "Some **bold** text with **very bold** and **special** characters."
        expected_result = "<p>Some <b>bold</b> text with <b>very bold</b> and <b>special</b> characters.</p>"
        self.assertEqual(process_text(text, "html"), expected_result)


    def test_different_styles(self):
        text = "**Bold** text with _italic_ and `monospaced`."
        expected_result = "<p><b>Bold</b> text with <i>italic</i> and <tt>monospaced</tt>.</p>"
        self.assertEqual(process_text(text, "html"), expected_result)


if __name__ == '__main__':
    unittest.main()
