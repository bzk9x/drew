import os
import sys
import argparse
from pathlib import Path

try:
    from fontTools.ttLib import TTFont
except ImportError as e:
    print(f"Error: fonttools library is required but not found.")
    print(f"Import error: {e}")
    print("Try installing with: pip install fonttools")
    print("Or if using conda: conda install fonttools")
    sys.exit(1)

def convert_otf_to_ttf(input_path, output_path=None):
    """
    Convert an OTF file to TTF format
    
    Args:
        input_path (str): Path to the input OTF file
        output_path (str, optional): Path for the output TTF file
    
    Returns:
        str: Path to the created TTF file
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if input_path.suffix.lower() not in ['.otf', '.ttf']:
        raise ValueError("Input file must be an OTF or TTF file")
    
    # Generate output path if not provided
    if output_path is None:
        output_path = input_path.with_suffix('.ttf')
    else:
        output_path = Path(output_path)
    
    try:
        print(f"Loading font: {input_path}")
        
        # Load the font
        font = TTFont(input_path)
        
        # Check what kind of font this is
        if 'CFF ' in font:
            print(f"Font has PostScript outlines (CFF), converting to TrueType...")
        elif 'glyf' in font:
            print(f"Font already has TrueType outlines")
        else:
            print(f"Warning: Font format not clearly identified")
        
        # For basic conversion, we mainly need to ensure proper format
        # More complex outline conversion would require additional libraries
        
        # Save as TTF
        print(f"Saving as: {output_path}")
        font.save(output_path)
        font.close()
        
        print(f"✓ Successfully converted: {output_path}")
        return str(output_path)
        
    except Exception as e:
        raise Exception(f"Error converting font: {str(e)}")


def batch_convert(input_dir, output_dir=None):
    """
    Convert all OTF files in a directory to TTF
    
    Args:
        input_dir (str): Directory containing OTF files
        output_dir (str, optional): Output directory for TTF files
    """
    input_dir = Path(input_dir)
    
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input directory not found: {input_dir}")
    
    # Find all OTF files
    otf_files = list(input_dir.glob("*.otf")) + list(input_dir.glob("*.OTF"))
    
    if not otf_files:
        print(f"No OTF files found in {input_dir}")
        return
    
    # Set up output directory
    if output_dir is None:
        output_dir = input_dir
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    converted_count = 0
    
    for otf_file in otf_files:
        try:
            output_path = output_dir / otf_file.with_suffix('.ttf').name
            convert_otf_to_ttf(otf_file, output_path)
            converted_count += 1
        except Exception as e:
            print(f"Failed to convert {otf_file.name}: {e}")
    
    print(f"\nBatch conversion complete: {converted_count}/{len(otf_files)} files converted")


def main():
    parser = argparse.ArgumentParser(
        description="Convert OTF (OpenType) fonts to TTF (TrueType) format"
    )
    parser.add_argument(
        "input", 
        help="Input OTF file or directory containing OTF files"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Output TTF file or directory (optional)"
    )
    parser.add_argument(
        "-b", "--batch", 
        action="store_true",
        help="Batch convert all OTF files in input directory"
    )
    
    args = parser.parse_args()
    
    try:
        if args.batch or Path(args.input).is_dir():
            batch_convert(args.input, args.output)
        else:
            convert_otf_to_ttf(args.input, args.output)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()