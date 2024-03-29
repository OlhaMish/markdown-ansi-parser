import unittest
from markdown_convertor.text_processing import process_text


class TestTextProcessing(unittest.TestCase):
    def test_primitive(self):
        expected_result = "\x1b[1mbold\x1b[22m"
        input_markdown = "**bold**"
        result = process_text(input_markdown, "ansi")

        self.assertEqual(expected_result, result)

    def test_one_entity(self):
        text = "Some **bold** text."
        self.assertEqual(process_text(text, "ansi"), "Some \x1b[1mbold\x1b[22m text.")

    def test_text_without_bold(self):
        text = "Some plain text."
        self.assertEqual(process_text(text, "ansi"), "Some plain text.")

    def test_non_closed_tag(self):
        text = "Some **bold text."
        with self.assertRaises(ValueError) as context:
            process_text(text, "ansi")
        self.assertEqual(str(context.exception), "Non-closed tag found")

    def test_nested_tag(self):
        text = "Some ***bold _and_ italic** text."
        with self.assertRaises(ValueError) as context:
            process_text(text, "ansi")
        self.assertEqual(str(context.exception), "Nested tags found")

    def test_non_separated_tag(self):
        text = "Somebo**ld**text."
        self.assertEqual(process_text(text, "ansi"), "Somebo**ld**text.")

    def test_separated_tag(self):
        text = "Some ** bold ** text."
        self.assertEqual(process_text(text, "ansi"), "Some ** bold ** text.")

    def test_invalid_tag(self):
        text = "Some *italic* text."
        self.assertEqual(process_text(text, "ansi"), "Some *italic* text.")

    def test_multiple_bold_tags(self):
        text = "Some **bold** text with **very bold** and **special** characters."
        expected_result = "Some \x1b[1mbold\x1b[22m text with \x1b[1mvery bold\x1b[22m and \x1b[1mspecial\x1b[22m characters."
        self.assertEqual(process_text(text, "ansi"), expected_result)

    def test_different_styles(self):
        text = "**Bold** text with _italic_ and `monospaced`."
        expected_result = "\x1b[1mBold\x1b[22m text with \x1b[3mitalic\x1b[23m and \x1b[7mmonospaced\x1b[27m."
        self.assertEqual(process_text(text, "ansi"), expected_result)


if __name__ == '__main__':
    unittest.main()
