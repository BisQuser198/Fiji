# dates/utils.py
import string
from io import BytesIO
import pandas as pd

def col_letter_to_index(letter: str) -> int:
    letter = letter.strip().upper()
    idx = 0
    for ch in letter:
        if ch in string.ascii_uppercase:
            idx = idx*26 + (ord(ch)-ord('A')+1)
        else:
            raise ValueError(f"Invalid column letter: {letter}")
    return idx - 1

def extract_earliest_dates(
    excel_bytes: bytes,
    skip_rows: int,
    crit_col_letter: str,
    date_col_letter: str
) -> dict:
    # Load into DataFrame
    stream = BytesIO(excel_bytes)
    df = pd.read_excel(stream, header=None, skiprows=skip_rows)

    # Convert column letters to indices
    crit_idx = col_letter_to_index(crit_col_letter)
    date_idx = col_letter_to_index(date_col_letter)

    # Extract series
    criteria = df.iloc[:, crit_idx].astype(str)
    dates = pd.to_datetime(df.iloc[:, date_idx], dayfirst=True, errors='coerce')
    if dates.isna().all():
        raise ValueError("No valid dates found in the specified column.")

    # Group & pick earliest
    grouped = pd.DataFrame({'crit': criteria, 'date': dates})
    earliest = grouped.groupby('crit', as_index=True)['date'].min()

    # Format output
    return {k: v.strftime("%d.%m.%Y") for k, v in earliest.items()}
