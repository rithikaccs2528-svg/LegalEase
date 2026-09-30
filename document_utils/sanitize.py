from __future__ import annotations

import re
import unicodedata


def sanitize_text(text: str) -> str:

    replacements = {

        "\u2018": "'",

        "\u2019": "'",

        "\u201c": '"',

        "\u201d": '"',

        "\u2013": "-",

        "\u2014": "-",

        "\u2026": "...",

        "\u00a0": " ",

        "\ufeff": ""
    }


    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )


    text = unicodedata.normalize(
        "NFKC",
        text
    )


    text = re.sub(

        r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]",

        "",

        text
    )


    return text.strip()


def split_terms(text: str) -> list[str]:

    return [

        item.strip(
            " \t\r\n-•"
        )

        for item in re.split(
            r"[;\n]+",
            text
        )

        if item.strip(
            " \t\r\n-•"
        )
    ]