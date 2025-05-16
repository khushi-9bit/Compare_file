import fitz  # PyMuPDF
import json

def extract_text_from_pdf_to_json(pdf_path, output_json_path):
    doc = fitz.open(pdf_path)
    text_pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        text_pages.append({
            "page_number": page_num + 1,
            "text": text.strip()
        })

    doc.close()

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(text_pages, f, ensure_ascii=False, indent=4)

    print(f"✅ Extracted text from {len(text_pages)} pages and saved to {output_json_path}")

# Example usage
pdf_path = "BOFA-CC-Elite.pdf"
output_json_path = "Elite_text.json"
extract_text_from_pdf_to_json(pdf_path, output_json_path)
