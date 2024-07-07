import streamlit as st
import pandas as pd
import random
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Function to generate a 4x4 bingo card
def generate_bingo_card(words):
    return random.sample(words, 16)

# Function to create a PDF of the bingo card
def create_pdf(filename, bingo_card):
    # Define page size and orientation (landscape)
    pdf = SimpleDocTemplate(filename, pagesize=landscape(A4))

    # Create table data for the Bingo card
    table_data = [bingo_card[i:i+4] for i in range(0, len(bingo_card), 4)]
    table = Table(table_data)

    # Styling the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightblue),  # Background color for entire table
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),      # Text color for entire table
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),              # Center align content
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),       
        ('FONTSIZE', (0, 0), (-1, -1), 28),                
        ('BOTTOMPADDING', (0, 0), (-1, -1), 40),            # Bottom padding (12)
        ('GRID', (0, 0), (-1, -1), 1, colors.black),       
    ])
    table.setStyle(style)

    # Build PDF document with the styled table
    elements = [table]
    pdf.build(elements)

# Read words from CSV
words_df = pd.read_csv("word_list.csv")
words = words_df['word'].tolist()

# Streamlit app
st.set_page_config(page_title="Bingo Card Generator", layout="centered")
st.title("Bingo Card Generator")

# Generate bingo card
bingo_card = generate_bingo_card(words)
bingo_card_matrix = [bingo_card[i:i+4] for i in range(0, len(bingo_card), 4)]

filename = "Bingo_Card_CSLS_2024.pdf"
create_pdf(filename, bingo_card)
with open(filename, "rb") as pdf_file:
    st.download_button(label="Download PDF", data=pdf_file, file_name=filename, mime="application/pdf")
