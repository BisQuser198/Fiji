# docx_utils.py
import os
import re
import shutil

def parse_filename(filename):
    """
    Given a filename (like 'TS1.docx'), split it into:
      - prefix (e.g., 'TS')
      - a numeric portion (e.g., 1)
      - extension (e.g., '.docx')
    If no trailing number is found, simply return (base, None, ext)
    """
    base, ext = os.path.splitext(filename)
    match = re.search(r'(\d+)$', base)
    if match:
        number = int(match.group(1))
        prefix = base[:match.start()]
        return prefix, number, ext
    else:
        return base, None, ext

def clone_docx(source_path, target_start, target_end):
    """
    Clones the source DOCX file into new files with target numbers from target_start to target_end.
    If the source filename ends with a number (e.g., TS1.docx), that numeric part is replaced
    with the new number; otherwise, the new number is appended.
    Returns a list of the new filenames created.
    """
    prefix, source_number, ext = parse_filename(source_path)
    # Determine default number if none found.
    if source_number is None:
        source_number = 0
    created_files = []
    for i in range(target_start, target_end + 1):
        if source_number:
            new_filename = f"{prefix}{i}{ext}"
        else:
            base = os.path.splitext(source_path)[0]
            new_filename = f"{base}{i}{ext}"
        shutil.copy2(source_path, new_filename)
        created_files.append(new_filename)
    return created_files
