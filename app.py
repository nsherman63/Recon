import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

TEXT_TO_REMOVE = "THERE HAS NOT BEEN ANY ACTIVITY FOR THIS ACCOUNT DURING THIS FISCAL YEAR"

st.title("Reconciliation Page Sorter")

st.write("Upload a reconciliation report, name the output file, then click Start.")

# Upload PDF
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

# Output name
output_name = st.text_input("Name for new file", value="filtered_file")

# START BUTTON
start = st.button("Start Processing")

# Only run AFTER button press
if start:

    if uploaded_file is None:
        st.error("Please upload a PDF first.")
        st.stop()

    if not output_name:
        st.error("Please enter a file name.")
        st.stop()

    reader = PdfReader(uploaded_file)

    kept_writer = PdfWriter()
    deleted_writer = PdfWriter()

    kept_count = 0
    deleted_count = 0

    for page_num, page in enumerate(reader.pages):

        text = page.extract_text()

        if text is None:
            kept_writer.add_page(page)
            kept_count += 1
            continue

        if TEXT_TO_REMOVE.lower() in text.lower():
            deleted_writer.add_page(page)
            deleted_count += 1
        else:
            kept_writer.add_page(page)
            kept_count += 1

    kept_buffer = io.BytesIO()
    deleted_buffer = io.BytesIO()

    kept_writer.write(kept_buffer)
    deleted_writer.write(deleted_buffer)

    st.success("Processing complete!")

    st.write(f"Pages kept: {kept_count}")
    st.write(f"Pages removed: {deleted_count}")

    st.download_button(
        label="Download Sorted PDF",
        data=kept_buffer.getvalue(),
        file_name=f"{output_name}.pdf",
        mime="application/pdf"
    )

    st.download_button(
        label="Download Deleted Pages PDF",
        data=deleted_buffer.getvalue(),
        file_name="deleted_pages.pdf",
        mime="application/pdf"
    )
