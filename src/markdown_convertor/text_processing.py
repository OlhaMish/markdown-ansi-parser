import re
from dataclasses import dataclass

from markdown_convertor.patterns import ITALIC_PATTERN, BOLD_PATTERN, CODE_PATTERN, BOLD_PATTERN_START_OF_LINE, \
    CODE_PATTERN_START_OF_LINE, ITALIC_PATTERN_START_OF_LINE
from markdown_convertor.syntax_validation import nested_tags_check, check_opened_tags, remove_empty_paragraphs


@dataclass
class TAG:
    open_tag: str
    close_tag: str


def split_by_code_entities(text, preformatted_tag):
    result = []
    open_backticks_position = text.find("```")
    closed_backticks_position = text.find("```", open_backticks_position + 3)

    if closed_backticks_position == -1:
        return [text]

    result.append(text[:open_backticks_position])
    text_from_backticks_to_backticks = (text[open_backticks_position: closed_backticks_position + 3]
                                        .replace("```", preformatted_tag.open_tag, 1)
                                        .replace("```", preformatted_tag.close_tag)
                                        )
    result.append(text_from_backticks_to_backticks)

    new_parts = split_by_code_entities(text[closed_backticks_position + 3:], preformatted_tag)
    result.extend(new_parts)

    return result


def split_by_ansi_paragraph_entities(text):
    result = []
    paragraphs_content = text.splitlines(True)
    for paragraph in paragraphs_content:
        result.append(paragraph)

    return result


def split_by_html_paragraph_entities(text):
    result = []
    paragraphs_content = text.split("\n\n")
    for paragraph in paragraphs_content:
        paragraph = "<p>" + paragraph + "</p>"
        paragraph = paragraph.replace("\n", " ")
        result.append(paragraph)

    return result


def wrap_with_tag(text, pattern, tag, number_of_symbols):
    matches = [(match.start(), match.end()) for match in re.finditer(pattern, text)]
    offset = 0
    for start, end in matches:
        start += offset
        end += offset
        text = (text[:start] + f"{tag.open_tag}" + text[start + number_of_symbols:end - number_of_symbols] +
                               f"{tag.close_tag}" + text[end:])
        offset += len(f"{tag.open_tag}{tag.close_tag}") - number_of_symbols*2
    return text


def split_by_entities(text_array, pattern, tag, preformatted_tag, number_of_symbols):
    new_text_array = []
    for paragraph in text_array:
        if paragraph[:len(preformatted_tag.open_tag)] == preformatted_tag.open_tag:
            new_text_array += [paragraph]
            continue
        new_text_array += [wrap_with_tag(paragraph, pattern, tag, number_of_symbols)]
    return new_text_array


def initialise_tags(style):
    bold_tag = italic_tag = monospaced_tag = preformatted_tag = None
    if style == "ansi":
        bold_tag = TAG(open_tag="\x1b[1m", close_tag="\x1b[22m")
        italic_tag = TAG(open_tag="\x1b[3m", close_tag="\x1b[23m")
        monospaced_tag = TAG(open_tag="\x1b[7m", close_tag="\x1b[27m")
        preformatted_tag = TAG(open_tag="\x1b[7m", close_tag="\x1b[27m")
    if style == "html":
        bold_tag = TAG(open_tag="<b>", close_tag="</b>")
        italic_tag = TAG(open_tag="<i>", close_tag="</i>")
        monospaced_tag = TAG(open_tag="<tt>", close_tag="</tt>")
        preformatted_tag = TAG(open_tag="<p><pre>", close_tag="</pre></p>")

    return bold_tag, italic_tag, monospaced_tag, preformatted_tag


def process_text(text, style):
    bold_tag, italic_tag, monospaced_tag, preformatted_tag = initialise_tags(style)
    if style == "ansi":
        split_by_paragraph_entities = split_by_ansi_paragraph_entities
    else:
        split_by_paragraph_entities = split_by_html_paragraph_entities

    array_with_code_parts = split_by_code_entities(text, preformatted_tag)
    array_with_paragraphs = []
    for part_of_array in array_with_code_parts:
        if part_of_array[:len(preformatted_tag.open_tag)] == preformatted_tag.open_tag:
            array_with_paragraphs += [part_of_array]
            continue
        array_with_paragraphs += split_by_paragraph_entities(part_of_array)
        nested_tags_check(part_of_array)

    bold_parts = split_by_entities(array_with_paragraphs, BOLD_PATTERN, bold_tag, preformatted_tag, 2)
    bold_parts = split_by_entities(bold_parts, BOLD_PATTERN_START_OF_LINE, bold_tag, preformatted_tag, 2)
    italic_parts = split_by_entities(bold_parts, ITALIC_PATTERN, italic_tag, preformatted_tag, 1)
    italic_parts = split_by_entities(italic_parts, ITALIC_PATTERN_START_OF_LINE, italic_tag, preformatted_tag, 1)
    code_parts = split_by_entities(italic_parts, CODE_PATTERN, monospaced_tag, preformatted_tag, 1)
    code_parts = split_by_entities(code_parts, CODE_PATTERN_START_OF_LINE, monospaced_tag, preformatted_tag, 1)

    check_opened_tags(code_parts, preformatted_tag.open_tag)

    if style == "ansi":
        processed_text = ''.join(code_parts)
    else:
        processed_text = remove_empty_paragraphs(code_parts)
        processed_text = '\n'.join(processed_text)

    return processed_text
