import re


from markdown_to_html.patterns import ITALIC_PATTERN, BOLD_PATTERN, CODE_PATTERN
from markdown_to_html.syntax_validation import nested_tags_check, check_opened_tags, remove_empty_paragraphs


def split_by_code_entities(text):
    result = []
    open_backticks_position = text.find("```")
    closed_backticks_position = text.find("```", open_backticks_position + 3)

    if closed_backticks_position == -1:
        return [text]

    result.append(text[:open_backticks_position])
    text_from_backticks_to_backticks = (text[open_backticks_position: closed_backticks_position + 3]
                                        .replace("```", "<p><pre>", 1)
                                        .replace("```", "</pre></p>")
                                        )
    result.append(text_from_backticks_to_backticks)

    new_parts = split_by_code_entities(text[closed_backticks_position + 3:])
    result.extend(new_parts)

    return result


def split_by_paragraph_entities(text):
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
        text = (text[:start] + f"<{tag}>" + text[start + number_of_symbols:end - number_of_symbols] +
                               f"</{tag}>" + text[end:])
        offset += len(f"<{tag}></{tag}>") - number_of_symbols*2
    return text


def split_by_entities(text_array, pattern, tag, number_of_symbols):
    new_text_array = []
    for paragraph in text_array:
        if paragraph[3:8] == "<pre>":
            new_text_array += [paragraph]
            continue
        new_text_array += [wrap_with_tag(paragraph, pattern, tag, number_of_symbols)]
    return new_text_array


def process_text(text):
    array_with_code_parts = split_by_code_entities(text)
    array_with_paragraphs = []
    for part_of_array in array_with_code_parts:
        if part_of_array[3:8] == "<pre>":
            array_with_paragraphs += [part_of_array]
            continue
        array_with_paragraphs += split_by_paragraph_entities(part_of_array)
        nested_tags_check(part_of_array)

    code_parts = split_by_entities(array_with_paragraphs, CODE_PATTERN, "tt", 1)
    bold_parts = split_by_entities(code_parts, BOLD_PATTERN, "b", 2)
    italic_parts = split_by_entities(bold_parts, ITALIC_PATTERN, "i", 1)
    check_opened_tags(italic_parts)
    html_text = remove_empty_paragraphs(italic_parts)
    html_string = '\n'.join(html_text)
    return html_string
