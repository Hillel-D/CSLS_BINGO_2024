import streamlit as st
import pandas as pd
import random
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Function to generate a 4x4 bingo card
def generate_bingo_card(words):
    return random.sample(words, 16)

# Function to create a PDF of the bingo card
def create_pdf(filename, bingo_card, bg_color):
    # Define page size and orientation (landscape)
    pdf = SimpleDocTemplate(filename, pagesize=landscape(letter))

    # Create table data for the Bingo card
    table_data = [bingo_card[i:i+4] for i in range(0, len(bingo_card), 4)]
    table = Table(table_data)

    # Styling the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_color),  # Background color for entire table
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),      # Text color for entire table
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),              # Center align content
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),   # Font name (Helvetica-Bold)
        ('FONTSIZE', (0, 0), (-1, -1), 20),                 # Font size (24)
        ('BOTTOMPADDING', (0, 0), (-1, -1), 40),            # Bottom padding (40)
        ('GRID', (0, 0), (-1, -1), 2, colors.black),        # Grid lines (2 pixels thick)
    ])
    table.setStyle(style)

    # Title
    styles = getSampleStyleSheet()
    title = Paragraph("<font size=40>CSLS 2024</font>", styles['Title'])

    # Add spacing
    space = Spacer(1, 48)

    # Build PDF document with the title and styled table
    elements = [title, space, table]
    pdf.build(elements)

# Read words from CSV
words_df = pd.read_csv("word_list.csv")
words = words_df['word'].tolist()
words = [word.replace("-\n", "") for word in words]

# Streamlit app
st.set_page_config(page_title="CSLS 2024: Bingo Card Generator", layout="centered")
st.title("CSLS 2024: Bingo Card Generator")

# Option to regenerate the bingo card
if st.button("Generate New Bingo Card"):
    bingo_card = generate_bingo_card(words)
else:
    bingo_card = generate_bingo_card(words)

bingo_card_matrix = [bingo_card[i:i+4] for i in range(0, len(bingo_card), 4)]

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
