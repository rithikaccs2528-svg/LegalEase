import sys
from pathlib import Path

# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS
# ============================================================

import requests
import streamlit as st

from backend.config import BACKEND_URL
from document_utils.docx_formatter import format_docx
from document_utils.pdf_formatter import format_pdf
from document_utils.html_preview import format_html_preview
from document_utils.sanitize import sanitize_text


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #f5f7fb;
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .brand-box {
        background: #111827;
        color: white;
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        margin-bottom: 25px;
    }

    .brand-icon {
        font-size: 48px;
    }

    .brand-name {
        font-size: 34px;
        font-weight: 800;
        margin-top: 5px;
    }

    .brand-tagline {
        color: #d1d5db;
        font-size: 15px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    .preview-box {
        background: white;
        border: 1px solid #d9dee8;
        border-radius: 15px;
        padding: 25px;
        min-height: 350px;
        max-height: 650px;
        overflow-y: auto;
        box-shadow: 0 4px 18px rgba(0,0,0,0.05);
    }

    .notice {
        background: #fff7ed;
        border-left: 5px solid #f97316;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        color: #7c2d12;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="brand-box">
        <div class="brand-icon">⚖️</div>
        <div class="brand-name">LegalEase</div>
        <div class="brand-tagline">
            AI-Powered Legal Document Generator
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "generated_document" not in st.session_state:
    st.session_state.generated_document = ""

if "document_type" not in st.session_state:
    st.session_state.document_type = "Freelance Work Contract"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📄 Document Type")

    document_types = [
        "Employment Contract",
        "Non-Disclosure Agreement",
        "Lease Agreement",
        "Freelance Work Contract",
        "Employment Offer Letter",
        "Service Agreement",
        "Consulting Agreement",
        "Partnership Agreement",
        "Custom Agreement",
    ]

    selected_type = st.selectbox(
        "Select document type",
        document_types,
        index=document_types.index(st.session_state.document_type)
        if st.session_state.document_type in document_types
        else 3,
    )

    st.session_state.document_type = selected_type

    st.divider()

    st.subheader("🔗 Backend")

    st.code(BACKEND_URL)

    st.divider()

    st.info(
        "LegalEase creates document drafts using the information "
        "you provide. Review the document for your applicable "
        "jurisdiction before using it."
    )


# ============================================================
# MAIN INPUT AREA
# ============================================================

st.markdown(
    '<div class="section-title">📝 Enter Legal Document Details</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)


with col1:

    parties = st.text_area(
        "👥 Parties Involved",
        placeholder=(
            "Example:\n"
            "Jane Doe (Service Provider)\n"
            "TechNova Inc. (Client)"
        ),
        height=150,
    )


with col2:

    dates = st.text_input(
        "📅 Effective Date",
        placeholder="Example: September 29, 2026",
    )


terms = st.text_area(
    "📌 Terms & Conditions",
    placeholder=(
        "Enter terms separated by semicolons.\n\n"
        "Example:\n"
        "Payment within 30 days; "
        "Confidentiality must be maintained; "
        "Either party may terminate with 15 days notice"
    ),
    height=180,
)


st.markdown("---")


# ============================================================
# GENERATE DOCUMENT
# ============================================================

generate_button = st.button(
    "✨ Generate Legal Document",
    type="primary",
    use_container_width=True,
)


if generate_button:

    if not parties.strip():
        st.error("Please enter the parties involved.")

    elif not terms.strip():
        st.error("Please enter the terms and conditions.")

    elif not dates.strip():
        st.error("Please enter the effective date.")

    else:

        payload = {
            "document_type": selected_type,
            "parties": parties,
            "terms": terms,
            "dates": dates,
        }

        with st.spinner("Generating your legal document..."):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120,
                )

                if response.status_code == 200:

                    data = response.json()

                    document_text = data.get("text", "").strip()

                    if document_text:

                        st.session_state.generated_document = document_text

                        st.success(
                            "✅ Legal document generated successfully!"
                        )

                    else:

                        st.error(
                            "The backend returned an empty document."
                        )

                else:

                    try:
                        error_data = response.json()
                        error_message = error_data.get(
                            "detail",
                            response.text,
                        )
                    except Exception:
                        error_message = response.text

                    st.error(
                        f"Backend error ({response.status_code}): "
                        f"{error_message}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Cannot connect to the FastAPI backend.\n\n"
                    "Make sure this is running:\n"
                    "python -m uvicorn backend.main:app "
                    "--reload --host 127.0.0.1 --port 8000"
                )

            except requests.exceptions.Timeout:

                st.error(
                    "❌ Backend request timed out. "
                    "Please try again."
                )

            except Exception as exc:

                st.error(
                    f"Unexpected error: {exc}"
                )


# ============================================================
# DOCUMENT PREVIEW
# ============================================================

if st.session_state.generated_document:

    st.markdown("---")

    st.markdown(
        '<div class="section-title">📄 Generated Document</div>',
        unsafe_allow_html=True,
    )

    preview_col, edit_col = st.columns([1, 1])

    with preview_col:

        st.subheader("👁️ Preview")

        preview_html = format_html_preview(
            st.session_state.generated_document,
            selected_type,
        )

        st.markdown(
            preview_html,
            unsafe_allow_html=True,
        )

    with edit_col:

        st.subheader("✏️ Edit Document")

        edited_document = st.text_area(
            "Edit your document here",
            value=st.session_state.generated_document,
            height=500,
            label_visibility="collapsed",
        )

        if st.button(
            "💾 Save Changes",
            use_container_width=True,
        ):

            st.session_state.generated_document = sanitize_text(
                edited_document
            )

            st.success("Changes saved.")


    # ========================================================
    # DOWNLOAD SECTION
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">⬇️ Download Document</div>',
        unsafe_allow_html=True,
    )

    final_document = st.session_state.generated_document

    download_col1, download_col2, download_col3 = st.columns(3)


    # TXT
    with download_col1:

        st.download_button(
            label="📄 Download TXT",
            data=final_document,
            file_name="LegalEase_Document.txt",
            mime="text/plain",
            use_container_width=True,
        )


    # DOCX
    with download_col2:

        try:

            docx_data = format_docx(
                final_document,
                selected_type,
            )

            st.download_button(
                label="📝 Download DOCX",
                data=docx_data,
                file_name="LegalEase_Document.docx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
                use_container_width=True,
            )

        except Exception as exc:

            st.error(
                f"DOCX generation error: {exc}"
            )


    # PDF
    with download_col3:

        try:

            pdf_data = format_pdf(
                final_document,
                selected_type,
            )

            st.download_button(
                label="📕 Download PDF",
                data=pdf_data,
                file_name="LegalEase_Document.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        except Exception as exc:

            st.error(
                f"PDF generation error: {exc}"
            )


# ============================================================
# REVIEW NOTICE
# ============================================================

st.markdown(
    """
    <div class="notice">
        <strong>⚠️ Legal Review Notice</strong><br><br>
        LegalEase is a document drafting tool. Generated content
        should be reviewed and adapted for the applicable jurisdiction
        before use. This application is not a substitute for qualified
        legal advice.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <br>
    <center>
        <small>
            ⚖️ LegalEase • AI-Powered Legal Document Generator
        </small>
    </center>
    """,
    unsafe_allow_html=True,
)