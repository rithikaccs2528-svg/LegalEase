from __future__ import annotations

import re

from fpdf import FPDF

from backend.config import COMPANY_NAME, COMPANY_TAGLINE
from document_utils.sanitize import sanitize_text


class LegalPDF(FPDF):

    def __init__(self):
        super().__init__()

        self.set_margins(
            left=15,
            top=20,
            right=15
        )

        self.set_auto_page_break(
            auto=True,
            margin=20
        )

    def header(self):

        self.set_font(
            "Helvetica",
            "B",
            9
        )

        self.cell(
            0,
            6,
            COMPANY_NAME,
            align="C"
        )

        self.ln(8)

    def footer(self):

        self.set_y(-15)

        self.set_font(
            "Helvetica",
            "",
            7
        )

        self.cell(
            0,
            5,
            f"{COMPANY_NAME} | AI Generated Draft | Page {self.page_no()}",
            align="C"
        )


def clean_pdf_text(text: str) -> str:
    """
    Make text safer for standard PDF fonts.
    """

    text = sanitize_text(text)

    # Remove characters that Helvetica cannot safely render.
    text = text.encode(
        "latin-1",
        errors="replace"
    ).decode("latin-1")

    # Prevent extremely long unbroken strings
    text = re.sub(
        r"(\S{70})",
        r"\1 ",
        text
    )

    return text


def format_pdf(text: str, doc_type: str) -> bytes:

    pdf = LegalPDF()

    pdf.set_title(
        f"{COMPANY_NAME} - {doc_type}"
    )

    pdf.set_author(
        COMPANY_NAME
    )

    pdf.add_page()

    # ---------------------------------------------------------
    # Document title
    # ---------------------------------------------------------

    safe_doc_type = clean_pdf_text(
        doc_type
    )

    pdf.set_font(
        "Helvetica",
        "B",
        15
    )

    pdf.multi_cell(
        w=pdf.epw,
        h=8,
        text=safe_doc_type.upper(),
        align="C"
    )

    pdf.ln(2)

    # ---------------------------------------------------------
    # Tagline
    # ---------------------------------------------------------

    safe_tagline = clean_pdf_text(
        COMPANY_TAGLINE
    )

    pdf.set_font(
        "Helvetica",
        "I",
        8
    )

    pdf.multi_cell(
        w=pdf.epw,
        h=5,
        text=safe_tagline,
        align="C"
    )

    pdf.ln(6)

    # ---------------------------------------------------------
    # Body
    # ---------------------------------------------------------

    body = clean_pdf_text(text)

    lines = body.splitlines()

    for raw_line in lines:

        line = raw_line.strip()

        # Empty line
        if not line:

            pdf.ln(3)

            continue

        # Heading detection
        is_heading = (
            line.isupper()
            or line.endswith(":")
            or (
                len(line) >= 2
                and line[0].isdigit()
                and line[1] == "."
            )
        )

        if is_heading:

            pdf.set_font(
                "Helvetica",
                "B",
                10
            )

            pdf.multi_cell(
                w=pdf.epw,
                h=6,
                text=line,
                align="L"
            )

        else:

            pdf.set_font(
                "Helvetica",
                "",
                10
            )

            pdf.multi_cell(
                w=pdf.epw,
                h=5.5,
                text=line,
                align="L"
            )

    # ---------------------------------------------------------
    # Output
    # ---------------------------------------------------------

    output = pdf.output()

    return bytes(output)