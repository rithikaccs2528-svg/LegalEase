from __future__ import annotations

from dataclasses import dataclass

from backend.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    demo_mode_enabled
)


@dataclass
class GenerationResult:

    text: str

    source: str

    model: str


class GeminiDocumentGenerator:
    """
    Generates legal document drafts.

    If GEMINI_API_KEY is available:
        Uses Gemini.

    If API key is missing and DEMO_MODE=true:
        Uses local demo generation.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None
    ):

        self.api_key = (
            api_key or GEMINI_API_KEY
        ).strip()

        self.model = (
            model or GEMINI_MODEL
        ).strip()


    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str
    ) -> GenerationResult:

        # Gemini mode
        if self.api_key:

            return self._generate_with_gemini(

                document_type,

                parties,

                terms,

                dates
            )

        # Local demo mode
        if demo_mode_enabled():

            return GenerationResult(

                text=self._demo_document(

                    document_type,

                    parties,

                    terms,

                    dates
                ),

                source="demo",

                model="local-demo"
            )

        raise RuntimeError(

            "GEMINI_API_KEY is not configured. "
            "Add it to .env or enable DEMO_MODE=true."
        )


    def _generate_with_gemini(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str
    ) -> GenerationResult:

        try:

            from google import genai

            from google.genai import types # type: ignore

        except ImportError as exc:

            raise RuntimeError(

                "google-genai package is missing. "
                "Run: pip install -r requirements.txt"

            ) from exc


        client = genai.Client(
            api_key=self.api_key
        )


        prompt = f"""
You are LegalEase, an AI legal-document drafting assistant.

Create a professional legal-document DRAFT.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

TERMS AND CONDITIONS:
{terms}

EFFECTIVE DATE:
{dates}

IMPORTANT REQUIREMENTS:

1. Create a professional legal document.

2. Do not invent names, dates, addresses,
   payment amounts, obligations, or facts.

3. Use [TO BE COMPLETED] when important
   information is missing.

4. Include an appropriate title.

5. Include an introductory section where useful.

6. Use numbered clauses.

7. Include appropriate terms and conditions.

8. Include termination provisions where appropriate.

9. Include confidentiality provisions where
   appropriate.

10. Include governing-law language only when
    sufficient information exists.

11. Include signature blocks.

12. Preserve all important user-provided terms.

13. Do not claim that the document has been
    reviewed by a lawyer.

14. Do not claim that the document is legally
    valid in a specific jurisdiction.

15. Return plain text only.

16. Do not wrap the answer in Markdown code fences.

17. End with:

REVIEW NOTICE

The document should be reviewed for the
applicable jurisdiction before use.

This is a drafting tool and not a substitute
for qualified legal advice.
""".strip()


        try:

            response = client.models.generate_content(

                model=self.model,

                contents=prompt,

                config=types.GenerateContentConfig(

                    temperature=0.2,

                    max_output_tokens=5000
                )
            )

        except Exception as exc:

            raise RuntimeError(

                f"Gemini generation failed: {exc}"

            ) from exc


        text = (
            response.text or ""
        ).strip()


        if not text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )


        return GenerationResult(

            text=text,

            source="gemini",

            model=self.model
        )


    @staticmethod
    def _demo_document(
        document_type: str,
        parties: str,
        terms: str,
        dates: str
    ) -> str:

        term_lines = [

            item.strip()

            for item in terms.replace(
                "\n",
                ";"
            ).split(";")

            if item.strip()
        ]


        clauses = "\n".join(

            f"{index}. {item}"

            for index, item
            in enumerate(
                term_lines,
                1
            )
        )


        if not clauses:

            clauses = (
                "1. [TO BE COMPLETED]"
            )


        return f"""
{document_type.upper()}

EFFECTIVE DATE

{dates}


PARTIES

{parties}


BACKGROUND

This document records the principal
terms supplied by the parties for the
above agreement.


1. PURPOSE

The parties intend to enter into the
arrangement described in this document.


2. AGREED TERMS

{clauses}


3. RESPONSIBILITIES

Each party shall perform the
responsibilities agreed between the
parties and described in this document.


4. CONFIDENTIALITY

Where confidential information is
exchanged, the parties should maintain
appropriate confidentiality protections
and should not disclose confidential
information except as permitted by the
agreement or applicable law.


5. TERMINATION

The parties should specify the events,
notice requirements, and consequences
of termination applicable to their
particular arrangement.


6. GENERAL PROVISIONS

Any additional provisions required
for the transaction should be completed
before execution.


7. SIGNATURES


PARTY 1

Signature: ___________________________

Name: ________________________________

Date: ________________________________



PARTY 2

Signature: ___________________________

Name: ________________________________

Date: ________________________________



REVIEW NOTICE

This is a locally generated
demonstration draft.

Review and adapt this document for
the applicable jurisdiction before use.
""".strip()