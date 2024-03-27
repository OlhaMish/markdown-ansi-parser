import re
from markdown_to_html.patterns import BOLD_PATTERN, ITALIC_PATTERN, CODE_PATTERN, OPENING_STARS_PATTERN, \
    CLOSED_STARS_PATTERN, OPENING_UNDERSCORE_PATTERN, CLOSED_UNDERSCORE_PATTERN, OPENING_BACKTICK_PATTERN, \
    CLOSED_BACKTICK_PATTERN


def check_nested_tags_for_each_style(nested_style_matches, pattern_1, pattern_2):
    nested_matches = []
    for match in nested_style_matches:
        match = ' ' + match
        nested_matches += pattern_1.findall(match)
        nested_matches += pattern_2.findall(match)
    if len(nested_matches) > 0:
        raise ValueError(f"Nested tags found")


def nested_tags_check(text):
    nested_bold_matches = BOLD_PATTERN.findall(text)
    check_nested_tags_for_each_style(nested_bold_matches, ITALIC_PATTERN, CODE_PATTERN)
    nested_italic_matches = ITALIC_PATTERN.findall(text)
    check_nested_tags_for_each_style(nested_italic_matches, BOLD_PATTERN, CODE_PATTERN)
    nested_code_matches = CODE_PATTERN.findall(text)
    check_nested_tags_for_each_style(nested_code_matches, ITALIC_PATTERN, BOLD_PATTERN)


def check_opened_tags(text):
    for sentence in text:
        if sentence[3:8] == "<pre>":
            continue
        matches = OPENING_STARS_PATTERN.findall(sentence)
        matches += CLOSED_STARS_PATTERN.findall(sentence)
        matches += OPENING_UNDERSCORE_PATTERN.findall(sentence)
        matches += CLOSED_UNDERSCORE_PATTERN.findall(sentence)
        matches += OPENING_BACKTICK_PATTERN.findall(sentence)
        matches += CLOSED_BACKTICK_PATTERN.findall(sentence)
        if len(matches) != 0:
            raise ValueError("Non-closed tag found")


def remove_empty_paragraphs(paragraphs):
    final_html_text = []
    for paragraph in paragraphs:
        if paragraph == "<p></p>":
            continue
        final_html_text += [paragraph]
    return final_html_text
