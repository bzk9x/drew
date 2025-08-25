#!/usr/bin/env python3
"""
Mass File Renamer Script
Renames files in a folder to camel case or lowercase while preserving extensions.
Supports removing specific words from filenames and relative paths.
"""

import os
import re
import argparse
from pathlib import Path

def to_camel_case(text):
    """Convert text to camelCase"""
    # Split by common delimiters and spaces
    words = re.split(r'[\s\-_\.]+', text)
    # Filter out empty strings
    words = [word for word in words if word]
    if not words:
        return text
    
    # First word lowercase, rest title case
    camel_case = words[0].lower()
    for word in words[1:]:
        camel_case += word.capitalize()
    
    return camel_case

def remove_words_from_filename(filename, words_to_remove):
    """Remove specified words from filename (case-insensitive)"""
    for word in words_to_remove:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(word) + r'\b'
        filename = re.sub(pattern, '', filename, flags=re.IGNORECASE)
    
    # Clean up multiple spaces/delimiters
    filename = re.sub(r'[\s\-_\.]+', ' ', filename)
    filename = filename.strip(' -_.')
    
    return filename

def rename_files(folder_path, mode='camel', words_to_remove=None, dry_run=False):
    """
    Rename files in the specified folder
    
    Args:
        folder_path (str): Path to the folder
        mode (str): 'camel' for camelCase, 'lower' for lowercase
        words_to_remove (list): List of words to remove from filenames
        dry_run (bool): If True, only show what would be renamed
    """
    if words_to_remove is None:
        words_to_remove = []
    
    # Convert to Path object and resolve
    folder = Path(folder_path).resolve()
    
    if not folder.exists():
        print(f"Error: Folder '{folder}' does not exist.")
        return
    
    if not folder.is_dir():
        print(f"Error: '{folder}' is not a directory.")
        return
    
    print(f"Processing files in: {folder}")
    print(f"Mode: {'camel' if mode == 'camel' else 'lowercase'}")
    if words_to_remove:
        print(f"Removing words: {', '.join(words_to_remove)}")
    print(f"Dry run: {'Yes' if dry_run else 'No'}")
    print("-" * 50)
    
    renamed_count = 0
    
    # Get all files in the directory (not subdirectories)
    files = [f for f in folder.iterdir() if f.is_file()]
    
    if not files:
        print("No files found in the directory.")
        return
    
    for file_path in files:
        # Get filename without extension
        name_without_ext = file_path.stem
        extension = file_path.suffix
        
        # Remove specified words
        cleaned_name = remove_words_from_filename(name_without_ext, words_to_remove)
        
        # Skip if name becomes empty after cleaning
        if not cleaned_name or cleaned_name.isspace():
            print(f"Skipping '{file_path.name}' - name would be empty after cleaning")
            continue
        
        # Apply case conversion
        if mode == 'camel':
            new_name = to_camel_case(cleaned_name)
        else:  # lowercase
            new_name = cleaned_name.lower().replace(' ', '_').replace('-', '_')
            # Clean up multiple underscores
            new_name = re.sub(r'_+', '_', new_name)
            new_name = new_name.strip('_')
        
        # Create new filename with extension
        new_filename = new_name + extension
        new_file_path = folder / new_filename
        
        # Check if rename is needed
        if file_path.name == new_filename:
            print(f"No change needed: {file_path.name}")
            continue
        
        # Check for conflicts
        if new_file_path.exists() and new_file_path != file_path:
            print(f"Conflict: '{new_filename}' already exists - skipping '{file_path.name}'")
            continue
        
        print(f"{'Would rename' if dry_run else 'Renaming'}: '{file_path.name}' -> '{new_filename}'")
        
        if not dry_run:
            try:
                file_path.rename(new_file_path)
                renamed_count += 1
            except OSError as e:
                print(f"Error renaming '{file_path.name}': {e}")
        else:
            renamed_count += 1
    
    print("-" * 50)
    print(f"{'Would rename' if dry_run else 'Renamed'} {renamed_count} file(s)")

def main():
    parser = argparse.ArgumentParser(description="Mass rename files to camelCase or lowercase")
    parser.add_argument("path", nargs="?", default=".", 
                       help="Path to folder (default: current directory, supports '../' for parent)")
    parser.add_argument("-m", "--mode", choices=["camel", "lower"], default="camel",
                       help="Naming mode: 'camel' for camel, 'lower' for lowercase (default: camel)")
    parser.add_argument("-r", "--remove", nargs="*", 
                       default=["Regular", "Outline"],
                       help="Words to remove from filenames (default: Regular, Outline)")
    parser.add_argument("-d", "--dry-run", action="store_true",
                       help="Show what would be renamed without actually renaming")
    parser.add_argument("--add-remove", nargs="*",
                       help="Additional words to remove (added to default list)")
    
    args = parser.parse_args()
    
    # Combine default and additional words to remove
    words_to_remove = args.remove if args.remove is not None else []
    if args.add_remove:
        words_to_remove.extend(args.add_remove)
    
    print("Mass File Renamer")
    print("=" * 50)
    
    try:
        rename_files(args.path, args.mode, words_to_remove, args.dry_run)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()

# Example usage:
# python rename_files.py                                    # Rename files in current dir to camel, remove "Regular" and "Outline"
# python rename_files.py ../fonts                          # Rename files in parent/fonts directory
# python rename_files.py -m lower                          # Use lowercase with underscores
# python rename_files.py -r Regular Outline Bold Italic    # Remove specific words
# python rename_files.py --add-remove Bold Italic          # Add words to default removal list
# python rename_files.py -d                                # Dry run - show what would be renamed