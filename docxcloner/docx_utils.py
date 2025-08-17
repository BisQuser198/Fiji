


## version 2 

# open dialogue to change, pick a range of files

# docx_utils.py
import os
import shutil

def parse_filename(filename):
    """
    Given a filename (like 'TS1.docx'), split it into:
      - prefix (e.g., 'TS')
      - a numeric portion (e.g., 1)
      - extension (e.g., '.docx')
    """
    # Split the filename into the base part and the extension.
    base, ext = os.path.splitext(filename)

    # Initialize an index at the very end of the base string.
    index = len(base) - 1

    # Move backwards through the base string as long as we find numeric characters.
    while index >= 0 and base[index].isdigit():
        index -= 1

    # After the loop, 'index' points to the last non-digit character.
    # If index is at the very end, it means no digits were found at the end.
    if index == len(base) - 1:
        # No trailing digits: return the whole base as the prefix,
        # None as the numeric portion, and the extension.
        return base, None, ext
    else:
        # Trailing digits were found.
        # The numeric part is the substring from index+1 to the end of the base string.
        numeric_part = base[index + 1:]
        # The prefix is the substring up to index+1.
        prefix = base[:index + 1]
        # Convert the numeric part to an integer.
        number = int(numeric_part)
        return prefix, number, ext

def clone_docx(source_path, target_start, target_end):
    """
    Clones the source DOCX file into new files with target numbers from target_start to target_end.
    
    - If the source filename ends with a number (e.g., 'TS1.docx'), this trailing number is replaced
      with each new target number.
    - If there is no trailing number, the new number is simply appended.

    Returns a list of the new filenames created.
    """
    # ------------------------------------------------------------------------
    # Expanded extraction of components from the source filename:
    #
    # We call the parse_filename function to break the filename into three parts:
    #  1. The prefix (non-digit part of the basename)
    #  2. The source number (the numeric portion at the end, if any)
    #  3. The file extension (e.g., '.docx')
    # ------------------------------------------------------------------------
    parsed_components = parse_filename(source_path)  # Result is a tuple of (prefix, source_number, ext)
    prefix = parsed_components[0]         # e.g., 'TS' from 'TS1.docx'
    source_number = parsed_components[1]    # e.g., 1 from 'TS1.docx'; could be None if no number was found
    ext = parsed_components[2]            # e.g., '.docx'
    
    # If the filename did not have a numeric section, we default source_number to 0.
    if source_number is None:
        source_number = 0

    created_files = []
    for i in range(target_start, target_end + 1):
        if source_number:
            # When the original filename contains a numeric part, we form the new filename by replacing
            # the old number with the new target number 'i'. For example, 'TS1.docx' becomes 'TS2.docx'.
            new_filename = f"{prefix}{i}{ext}"
        else:
            # If no trailing number was present in the original filename, we append the number 'i'
            # to the base part of the filename. For example, 'Document.docx' becomes 'Document2.docx'.
            base_name = os.path.splitext(source_path)[0]
            new_filename = f"{base_name}{i}{ext}"
#os.path.splitext() method is used to split the pathname into a pair (root, ext), where root is the part of the path before the file extension and ext is the file extension itself. It is particularly useful when you need to extract the file extension or handle files dynamically based on their type. Ex: Path Name /home/User/Desktop/file.txt ; 
# Root -- /home/User/Desktop/file ; Extension -- .txt



        # The next step copies the source file to the newly constructed filename.
        #
        # Explanation of the copy step:
        # 'shutil.copy2(source_path, new_filename)' copies the file from 'source_path' to 'new_filename'
        # while preserving the file’s metadata (like creation and modification times). This is similar to
        # a standard file copy but ensures that more attributes of the file, aside from its content, are maintained.
        shutil.copy2(source_path, new_filename)
        
        # Storing the new file name into our list of created files.
        created_files.append(new_filename)
        
    return created_files



# # docx_utils.py
# import os
# import re
# import shutil

# def parse_filename(filename):
#     """
#     Given a filename (like 'TS1.docx'), split it into:
#       - prefix (e.g., 'TS')
#       - a numeric portion (e.g., 1)
#       - extension (e.g., '.docx')
#     If no trailing number is found, simply return (base, None, ext)
#     """
#     base, ext = os.path.splitext(filename)
#     match = re.search(r'(\d+)$', base)
#     if match:
#         number = int(match.group(1))
#         prefix = base[:match.start()]
#         return prefix, number, ext
#     else:
#         return base, None, ext

# def clone_docx(source_path, target_start, target_end):
#     """
#     Clones the source DOCX file into new files with target numbers from target_start to target_end.
#     If the source filename ends with a number (e.g., TS1.docx), that numeric part is replaced
#     with the new number; otherwise, the new number is appended.
#     Returns a list of the new filenames created.
#     """
#     prefix, source_number, ext = parse_filename(source_path)
#     # Determine default number if none found.
#     if source_number is None:
#         source_number = 0
#     created_files = []
#     for i in range(target_start, target_end + 1):
#         if source_number:
#             new_filename = f"{prefix}{i}{ext}"
#         else:
#             base = os.path.splitext(source_path)[0]
#             new_filename = f"{base}{i}{ext}"
#         shutil.copy2(source_path, new_filename)
#         created_files.append(new_filename)
#     return created_files
