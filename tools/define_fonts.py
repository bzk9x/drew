#!/usr/bin/env python3
import os
import json
import sys
from pathlib import Path

def snake_case_to_title_case(snake_str):
    """Convert snake_case string to Title Case"""
    return snake_str.replace('_', ' ').title()

def process_fonts_folder(folder_path):
    """Process all TTF files in the given folder and create JSON structure"""
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print(f"Error: Folder '{folder_path}' does not exist")
        sys.exit(1)
    
    if not folder_path.is_dir():
        print(f"Error: '{folder_path}' is not a directory")
        sys.exit(1)
    
    fonts = []
    
    # Find all TTF files in the folder (case-insensitive)
    ttf_files = []
    for file in folder_path.iterdir():
        if file.is_file() and file.suffix.lower() == '.ttf':
            ttf_files.append(file)
    
    if not ttf_files:
        print(f"Warning: No TTF files found in '{folder_path}'")
    
    for ttf_file in sorted(ttf_files):
        # Get filename without extension
        filename_without_ext = ttf_file.stem
        
        # Convert snake_case to Title Case
        display_name = snake_case_to_title_case(filename_without_ext)
        
        # Create font object
        font_obj = {
            "name": display_name,
            "font": ttf_file.name
        }
        
        fonts.append(font_obj)
        print(f"Added: {display_name} -> {ttf_file.name}")
    
    return fonts

def generate_css(fonts_data):
    """Generate CSS @font-face definitions"""
    css_content = ""
    
    for font in fonts_data:
        css_content += f"""@font-face {{
    font-family: '{font['name']}';
    src: url(../../fonts/{font['font']});
}}

"""
    
    return css_content

def main():
    if len(sys.argv) != 2:
        print("Usage: python define_fonts.py <path_to_fonts_folder>")
        sys.exit(1)
    
    fonts_folder = sys.argv[1]
    
    try:
        fonts_data = process_fonts_folder(fonts_folder)
        
        # Create output filenames
        json_output_file = "fonts.json"
        css_output_file = "font_definitions.css"
        
        # Write JSON file
        with open(json_output_file, 'w', encoding='utf-8') as f:
            json.dump(fonts_data, f, indent=2, ensure_ascii=False)
        
        # Generate and write CSS file
        css_content = generate_css(fonts_data)
        with open(css_output_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print(f"\nFiles created:")
        print(f"  JSON: {json_output_file}")
        print(f"  CSS:  {css_output_file}")
        print(f"Total fonts processed: {len(fonts_data)}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()