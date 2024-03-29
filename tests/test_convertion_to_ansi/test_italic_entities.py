import unittest
from markdown_convertor.text_processing import process_text


class TestTextProcessing(unittest.TestCase):
    def test_primitive(self):
        expected_result = "\x1b[3mitalic\x1b[23m"
        input_markdown = "_italic_"
        result = process_text(input_markdown, "ansi")

        self.assertEqual(expected_result, result)

    def test_one_entity(self):
        text = "Some _italic_ text."
        self.assertEqual(process_text(text, "ansi"), "Some \x1b[3mitalic\x1b[23m text.")

    def test_text_with_underline(self):
        text = "Some _ita_lic_ text."
        self.assertEqual(process_text(text, "ansi"), "Some \x1b[3mita_lic\x1b[23m text.")

    def test_non_closed_tag(self):
        text = "Some _italic text."
        with self.assertRaises(ValueError) as context:
            process_text(text, "ansi")
        self.assertEqual(str(context.exception), "Non-closed tag found")

    def test_nested_tag(self):
        text = "Some _bold **and** italic_ text."
        with self.assertRaises(ValueError) as context:
            process_text(text, "ansi")
        self.assertEqual(str(context.exception), "Nested tags found")

    def test_non_separated_tag(self):
        text = "Someita_lic_text."
        self.assertEqual(process_text(text, "ansi"), "Someita_lic_text.")

    def test_separated_tag(self):
        text = "Some _ bold _ text."
        self.assertEqual(process_text(text, "ansi"), "Some _ bold _ text.")

    def test_multiple_italic_tags(self):
        text = "Some _italic_ text with _very italic_ and _italic_ characters."
        expected_result = "Some \x1b[3mitalic\x1b[23m text with \x1b[3mvery italic\x1b[23m and \x1b[3mitalic\x1b[23m characters."
        self.assertEqual(process_text(text, "ansi"), expected_result)

    def test_different_styles(self):
        text = "**Bold** text with _italic_ and `monospaced`."
        expected_result = "\x1b[1mBold\x1b[22m text with \x1b[3mitalic\x1b[23m and \x1b[7mmonospaced\x1b[27m."
        self.assertEqual(process_text(text, "ansi"), expected_result)


if __name__ == '__main__':
    unittest.main()
