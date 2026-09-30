from __future__ import annotations

import html

from document_utils.sanitize import (
    sanitize_text
)


def format_html_preview(
    text: str,
    title: str = "Document Preview"
) -> str:

    safe_text = html.escape(
        sanitize_text(text)
    )


    safe_text = safe_text.replace(
        "\n",
        "<br>"
    )


    return f"""
    <div class="legal-preview">

        <div class="preview-title">
            {html.escape(title)}
        </div>

        <div class="preview-body">
            {safe_text}
        </div>

    </div>
    """