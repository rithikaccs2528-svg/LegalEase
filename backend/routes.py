from fastapi import APIRouter, HTTPException

from ai_core.gemini_generator import (
    GeminiDocumentGenerator
)

from backend.schemas import (
    DocumentRequest,
    DocumentResponse
)


router = APIRouter()


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_document(
    payload: DocumentRequest
) -> DocumentResponse:

    generator = GeminiDocumentGenerator()

    try:

        result = generator.generate_document(
            document_type=payload.document_type,
            parties=payload.parties,
            terms=payload.terms,
            dates=payload.dates,
        )

    except RuntimeError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc

    return DocumentResponse(

        document_type=payload.document_type,

        text=result.text,

        source=result.source,

        model=result.model
    )