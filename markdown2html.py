import sys
import argparse
from markdown_convertor.text_processing import process_text


def convert_markdown_to_format(input_file, output_file=None, output_format=None):
    try:
        with open(input_file, 'r') as f:
            markdown_text = f.read()
            if output_format is None:
                output_format = 'ansi' if output_file is None else 'html'

            processed_text = process_text(markdown_text, output_format)

            if output_file:
                with open(output_file, 'w') as f_out:
                    f_out.write(processed_text)
            else:
                if output_format == 'ansi':
                    print(processed_text)
                elif output_format == 'html':
                    print(processed_text)

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
    parser.add_argument("--format", "-f", choices=['ansi', 'html'],
                        help="Output format (ansi/html). Default is ansi.")

    args = parser.parse_args()
    convert_markdown_to_format(args.input_file, args.output, args.format)


if __name__ == "__main__":
    main()
