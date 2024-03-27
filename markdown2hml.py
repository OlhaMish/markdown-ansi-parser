import sys
import argparse
from markdown_to_html.text_processing import process_text


def convert_markdown_to_html(input_file, output_file=None):
    try:
        with open(input_file, 'r') as f:
            markdown_text = f.read()
            html_result = process_text(markdown_text)
            if output_file:
                with open(output_file, 'w') as f_out:
                    f_out.write(html_result)
            else:
                print(html_result)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to HTML.")
    parser.add_argument("input_file", help="Path to the input Markdown file")
    parser.add_argument("--output", "-o", help="Path to the output HTML file")

    args = parser.parse_args()

    convert_markdown_to_html(args.input_file, args.output)


if __name__ == "__main__":
    main()
