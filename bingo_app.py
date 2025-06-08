import streamlit as st
import pandas as pd
import random
import re
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER


# Function to generate a 4x4 bingo card
def generate_bingo_card(words):
    return random.sample(words, 16)


# Function to create a PDF of the bingo card
def create_pdf(filename, bingo_card, bg_color):
    # Define page size and orientation (landscape)
    pdf = SimpleDocTemplate(filename, pagesize=landscape(letter))

    # Calculate optimal font size based on word length
    max_word_length = max(len(word) for word in bingo_card)

    # Adjust font size dynamically
    if max_word_length > 20:
        font_size = 12
    elif max_word_length > 15:
        font_size = 16
    else:
        font_size = 20

    # Create table data for the Bingo card
    table_data = [[Paragraph(word, getSampleStyleSheet()['Normal']) for word in bingo_card[i:i + 4]] for i in
                  range(0, len(bingo_card), 4)]

    # Set text alignment for paragraphs
    for row in table_data:
        for cell in row:
            cell.style.alignment = TA_CENTER
            cell.style.fontName = 'Helvetica-Bold'
            cell.style.fontSize = font_size
            cell.style.leading = font_size * 1.2  # Line spacing

    table = Table(table_data)

    # Styling the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_color),  # Background color for entire table
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # Text color for entire table
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align content
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertically align content
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),  # Bottom padding (adjust as needed)
        ('TOPPADDING', (0, 0), (-1, -1), 10),  # Top padding (adjust as needed)
        ('GRID', (0, 0), (-1, -1), 2, colors.black),  # Grid lines (2 pixels thick)
    ])
    table.setStyle(style)

    # Calculate column width dynamically to ensure text fits
    col_width = (landscape(letter)[0] - 2 * 72) / 4  # Total width - margins / 4 columns (assuming 1 inch margin)
    table._argW = [col_width] * 4  # Set all column widths to be equal

    # Title
    styles = getSampleStyleSheet()
    title = Paragraph("<font size=40>CSLS 2024</font>", styles['Title'])
    title.style.alignment = TA_CENTER

    # Add spacing
    space = Spacer(1, 48)

    # Build PDF document with the title and styled table
    elements = [title, space, table]
    pdf.build(elements)


# Read words from CSV
words_df = pd.read_csv("word_list.csv")
words = words_df['word'].tolist()
words = [re.sub(r"-\\n", "", word) for word in words]
words = [re.sub(r"\\n", "", word) for word in words]

# Streamlit app
st.set_page_config(page_title="CSLS 2024: Bingo Card Generator", layout="centered")
st.title("CSLS 2024: Bingo Card Generator")

# Option to regenerate the bingo card
if st.button("Generate New Bingo Card"):
    bingo_card = generate_bingo_card(words)
else:
    bingo_card = generate_bingo_card(words)

bingo_card_matrix = [bingo_card[i:i + 4] for i in range(0, len(bingo_card), 4)]

# Display Bingo card
st.write("Your Bingo Card:")
st.table(bingo_card_matrix)

# Background color options
bg_color_option = st.selectbox(
    "Select background color for the Bingo card:",
    ["Light Purple", "Light Blue", "Light Green", "Light Yellow", "Light Gray"]
)

# Map color option to actual color
color_map = {
    "Light Purple": colors.lavender,
    "Light Blue": colors.lightblue,
    "Light Green": colors.lightgreen,
    "Light Yellow": colors.lightyellow,
    "Light Gray": colors.lightgrey,
}
bg_color = color_map[bg_color_option]

# Center the download button
st.markdown(
    """
    <style>
    .stButton {text-align: center;}
    </style>
    """, unsafe_allow_html=True
)

filename = "Bingo_Card_CSLS_2024.pdf"
create_pdf(filename, bingo_card, bg_color)
with open(filename, "rb") as pdf_file:
    st.download_button(label="Download PDF", data=pdf_file, file_name=filename, mime="application/pdf")