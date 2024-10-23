#!/usr/bin/env python3
import re
import sys
import os
from urllib.parse import urljoin
from pathlib import Path

def convert_markdown_urls(content: str, base_url: str) -> str:
    """
    Convert relative Markdown URLs to absolute URLs using the provided base URL.
    
    Args:
        content (str): Markdown content containing URLs
        base_url (str): Base URL to prepend to relative URLs
        
    Returns:
        str: Markdown content with converted absolute URLs
    """
    # Remove trailing slash from base_url if present
    base_url = base_url.rstrip('/')
    
    # Regular expression patterns for different types of Markdown URLs
    patterns = [
        # [text](url) format
        (r'\[([^\]]+)\]\((?!http|#|mailto:)([^)]+)\)',
         lambda m: f'[{m.group(1)}]({urljoin(base_url + "/", m.group(2))})'
        ),
        # ![alt](image-url) format
        (r'!\[([^\]]*)\]\((?!http|#)([^)]+)\)',
         lambda m: f'![{m.group(1)}]({urljoin(base_url + "/", m.group(2))})'
        ),
        # Reference-style [text][ref] definitions
        (r'^\[([^\]]+)\]:\s*(?!http|#|mailto:)([^\s]+)(.*)$',
         lambda m: f'[{m.group(1)}]: {urljoin(base_url + "/", m.group(2))}{m.group(3)}',
         re.MULTILINE
        )
    ]
    
    # Apply each pattern to the content
    result = content
    for pattern, replacement, *flags in patterns:
        if flags:
            result = re.sub(pattern, replacement, result, flags=flags[0])
        else:
            result = re.sub(pattern, replacement, result)
    
    return result

def main():
    # Check if BASE_URL environment variable is set
    base_url = os.environ.get('BASE_URL')
    if not base_url:
        print("Error: BASE_URL environment variable must be set")
        print("Usage: BASE_URL='https://example.com' python convert_markdown_urls.py <input_file>")
        sys.exit(1)

    # Check if input file is provided
    if len(sys.argv) != 2:
        print("Error: Please provide an input file")
        print("Usage: BASE_URL='https://example.com' python convert_markdown_urls.py <input_file>")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    
    # Check if input file exists
    if not input_file.exists():
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)

    try:
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Convert URLs
        converted_content = convert_markdown_urls(content, base_url)

        # Create output file name
        output_file = input_file.with_stem(f"{input_file.stem}_converted")
        
        # Write converted content to new file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(converted_content)
        
        print(f"Success: Converted content written to '{output_file}'")

    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
