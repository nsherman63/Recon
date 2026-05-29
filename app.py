import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

# Phrase that identifies pages to remove
TEXT_TO_REMOVE = "THERE HAS NOT BEEN ANY ACTIVITY FOR THIS ACCOUNT DURING THIS FISCAL YEAR"

st.title("PDF Page Filter")

st.write(
    "Upload a PDF. Pages containing the target phrase will be removed automatically."
)

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf"
)

# User chooses output filename
output_name = st.text_input(
    "Name for filtered PDF",
    value="filtered_file"
)

if uploaded_file is not None and output_name:

    reader = PdfReader(uploaded_file)

    kept_writer = PdfWriter()
    deleted_writer = PdfWriter()

    kept_count = 0
    deleted_count = 0

    for page_num, page in enumerate(reader.pages):

        text = page.extract_text()

        # Keep pages with no text
        if text is None:
            kept_writer.add_page(page)
            kept_count += 1
            continue

        # Remove matching pages
        if TEXT_TO_REMOVE.lower() in text.lower():
            deleted_writer.add_page(page)
            deleted_count += 1
        else:
            kept_writer.add_page(page)
            kept_count += 1

    # Save PDFs into memory
    kept_buffer = io.BytesIO()
    deleted_buffer = io.BytesIO()

    kept_writer.write(kept_buffer)
    deleted_writer.write(deleted_buffer)

    st.success("Processing complete!")

    st.write(f"Pages kept: {kept_count}")
    st.write(f"Pages removed: {deleted_count}")

    # Download filtered PDF
    st.download_button(
        label="Download Filtered PDF",
        data=kept_buffer.getvalue(),
        file_name=f"{output_name}.pdf",
        mime="application/pdf"
    )

    # Download removed pages PDF
    st.download_button(
        label="Download Deleted Pages PDF",
        data=deleted_buffer.getvalue(),
        file_name="deleted_pages.pdf",
        mime="application/pdf"
    )
