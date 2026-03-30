# pip install pypdf
from pypdf import PdfReader, PdfWriter

def show_metadata(input_file):
    reader = PdfReader(input_file)
    print(reader.metadata)

def change_metadata(input_file, meta_data = {}, output_file = None):
    if output_file == None:
        if input_file.endswith('.pdf'):
            extension_position = input_file.index('.pdf')
            output_file = "{0}_NEW.pdf".format(input_file[0:extension_position])
        else:
            output_file = "output.pdf"
    
    reader = PdfReader(input_file)
    writer = PdfWriter()

    writer.append_pages_from_reader(reader)
    if reader.metadata is not None:
        writer.add_metadata(reader.metadata)
        
    writer.add_metadata(meta_data)
    writer.write(output_file)

