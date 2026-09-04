import os
from pypdf import PdfReader, PdfWriter

THIS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

def split_pdf_pages(input_pdf_path, output_dir="."):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    base_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)
    
    for index, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        
        page_num = str(index + 1).zfill(len(str(total_pages)))
        output_filename = f"{base_name}_page_{page_num}.pdf"
        output_path = os.path.join(output_dir, output_filename)
        
        with open(output_path, "wb") as f:
            writer.write(f)

def rotate_pdf_pages(input_pdf_path, output_pdf_path, rotation_angle=90):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        page.rotate(rotation_angle)
        writer.add_page(page)
        
    with open(output_pdf_path, "wb") as f:
        writer.write(f)

def merge_pdfs(pdf_list, output_pdf_path):
    writer = PdfWriter()
    
    for pdf_path in pdf_list:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            writer.add_page(page)
            
    with open(output_pdf_path, "wb") as f:
        writer.write(f)

# split_pdf_pages(os.path.join(THIS_FILE_PATH, "0587_001.pdf"), os.path.join(THIS_FILE_PATH, "output"))

# rotate_pdf_pages(os.path.join(THIS_FILE_PATH, "output", "0588_001_page_1.pdf"), os.path.join(THIS_FILE_PATH, "output", "0588_001_rotated.pdf"), -90)

merge_pdfs([os.path.join(THIS_FILE_PATH, "input", i) for i in os.listdir(os.path.join(THIS_FILE_PATH, "input")) if i.endswith(".pdf")], os.path.join(THIS_FILE_PATH, "output", "merged.pdf"))