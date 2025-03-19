import io
import streamlit as st
import pandas as pd
import pdfplumber

# Streamlit app layout
st.title("PDF to Excel Converter")
st.subheader("Upload a PDF file and download as Excel")

# File uploader [[2]]
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:
    # Process PDF button
    if st.button("Convert to Excel"):
        try:
            # Extract text from PDF using pdfplumber [[5]]
            with pdfplumber.open(uploaded_file) as pdf:
                text_data = []
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_data.append(text)
            
            # Convert to DataFrame (adjust parsing based on your PDF structure)
            # This example splits text by newlines - customize for table structures
            data = [line.split() for line in '\n'.join(text_data).split('\n')]
            df = pd.DataFrame(data[1:], columns=data[0])
            
            # Create Excel file in memory [[7]]
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            
            # Download button [[9]]
            st.download_button(
                label="Download Excel File",
                data=excel_buffer.getvalue(),
                file_name="converted.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            st.success("Conversion successful! Click download button above.")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.warning("Note: This basic converter works best with text-based PDFs. "
                     "For scanned/image-based PDFs, OCR is required (not implemented here).")