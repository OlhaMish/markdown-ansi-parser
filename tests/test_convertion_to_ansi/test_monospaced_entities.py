import unittest
from markdown_convertor.text_processing import process_text


class TestTextProcessing(unittest.TestCase):
    def test_primitive(self):
        expected_result = "\x1b[7mmonospaced\x1b[27m"
        input_markdown = "`monospaced`"
        result = process_text(input_markdown, "ansi")

        self.assertEqual(expected_result, result)

    def test_one_entity(self):
        text = "Some `monospaced` text."
        self.assertEqual(process_text(text, "ansi"), "Some \x1b[7mmonospaced\x1b[27m text.")

    def test_non_closed_tag(self):
        text = "Some `monospaced text."
        with self.assertRaises(ValueError) as context:
            process_text(text, "ansi")
        self.assertEqual(str(context.exception), "Non-closed tag found")

    def test_nested_tag(self):
        text = "Some `bold **and** monospaced` text."
        with self.assertRaises(ValueError) as context:
            process_text(text, "ansi")
        self.assertEqual(str(context.exception), "Nested tags found")

    def test_non_separated_tag(self):
        text = "Some`mono`spaced`text."
        self.assertEqual(process_text(text, "ansi"), "Some`mono`spaced`text.")

    def test_separated_tag(self):
        text = "Some ` monospaced ` text."
        self.assertEqual(process_text(text, "ansi"), "Some ` monospaced ` text.")

    def test_multiple_monospaced_tags(self):
        text = "Some `monospaced` text with `very monospaced` and `monospaced` characters."
        expected_result = "Some \x1b[7mmonos paced\x1b[27m text with \x1b[7mvery monospaced\x1b[27m and \x1b[7mmonospaced\x1b[27m characters."
        self.assertEqual(process_text(text, "ansi"), expected_result)

    def test_different_styles(self):
        text = "**Bold** text with _italic_ and `monospaced`."
        expected_result = "\x1b[1mBold\x1b[22m text with \x1b[3mitalic\x1b[23m and \x1b[7mmonospaced\x1b[27m."
        self.assertEqual(process_text(text, "ansi"), expected_result)


if __name__ == '__main__':
    unittest.main()
