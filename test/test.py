from pdfminer.high_level import extract_text

try:
    text = extract_text("test_pdf.pdf") #replace with a pdf file in the same directory
    print(text)
    print("pdfminer is working")

except Exception as e:
    print(f"Error: {e}")