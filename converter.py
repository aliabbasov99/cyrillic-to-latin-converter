"""
Azerbaijani Cyrillic → Latin transliteration engine.

Handles the standard Azerbaijani Cyrillic alphabet mappings.
"""

# ── Mapping tables ──────────────────────────────────────────────

# Strictly 1-to-1 character replacements based on standard alphabet
SIMPLE_MAP = {
    # Lowercase
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "q",
    "ғ": "ğ",
    "д": "d",
    "е": "e",
    "ә": "ə",
    "ж": "j",
    "з": "z",
    "и": "i",
    "ы": "ı",
    "ј": "y",
    "к": "k",
    "ҝ": "g",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "ө": "ö",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ү": "ü",
    "ф": "f",
    "х": "x",
    "һ": "h",
    "ч": "ç",
    "ш": "ş",
    "ҹ": "c",

    
    # Uppercase
    "А": "A",
    "Б": "B",
    "В": "V",
    "Г": "Q",
    "Ғ": "Ğ",
    "Д": "D",
    "Е": "E",
    "Ә": "Ə",
    "Ж": "J",
    "З": "Z",
    "И": "İ",
    "Ы": "I",
    "Ј": "Y",
    "К": "K",
    "Ҝ": "G",
    "Л": "L",
    "М": "M",
    "Н": "N",
    "О": "O",
    "Ө": "Ö",
    "П": "P",
    "Р": "R",
    "С": "S",
    "Т": "T",
    "У": "U",
    "Ү": "Ü",
    "Ф": "F",
    "Х": "X",
    "Һ": "H",
    "Ч": "Ç",
    "Ш": "Ş",
    "Ҹ": "C",
}

def convert_text(text: str, replace_quotes: bool = False) -> str:
    """
    Convert Azerbaijani Cyrillic text to Latin script using strict 1-to-1 mapping.

    Args:
        text: Input string (may contain mixed Cyrillic/Latin/other).
        replace_quotes: If True, replaces « and » with ".

    Returns:
        Transliterated string.
    """
    result = []
    
    for ch in text:
        if ch in SIMPLE_MAP:
            result.append(SIMPLE_MAP[ch])
        elif replace_quotes and ch in ('«', '»'):
            result.append('"')
        else:
            result.append(ch)

    return "".join(result)
