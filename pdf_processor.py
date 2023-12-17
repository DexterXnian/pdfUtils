import os
import logging
from PyPDF2 import PdfReader, PdfWriter


class PDFSplitter:
    def __init__(self, pdf_path, save_path):
        self.validate_file_path(pdf_path, save_path)
        self.pdf_path = pdf_path
        self.save_path = save_path
        self.ranges = []
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def validate_file_path(self, path, save_path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found at the specified path: {path}")
        if os.path.exists(save_path):
            raise FileNotFoundError(f"Output file already exists: {save_path}")

    def add_range(self, start, end):
        self.ranges.append((start, end))
        self.logger.info(f"Added page range from {start} to {end}.")

    def remove_range(self, start, end):
        try:
            self.ranges.remove((start, end))
            self.logger.info(f"Removed page range from {start} to {end}.")
        except ValueError:
            self.logger.error(f"Range from {start} to {end} not found in the list.")

    def split(self):
        self.validate_file_path(self.pdf_path, self.save_path) 
        pdf_reader = PdfReader(self.pdf_path)
        output_pdf = open(self.save_path, 'wb')
        
        try:
            pdf_writer = PdfWriter()
            total_ranges = len(self.ranges)
            for count, (start, end) in enumerate(self.ranges, 1):
                for i in range(start, end + 1):
                    pdf_writer.add_page(pdf_reader.pages[i])
                self.logger.info(f"Processing range {count}/{total_ranges}...")
            pdf_writer.write(output_pdf)
        finally:
            output_pdf.close()

        self.logger.info(f"PDF saved successfully to {self.save_path}")



class PDFMerger:
    def __init__(self):
        self.pdf_writer = PdfWriter()

    def add_pdf(self, pdf_path):
        pdf_reader = PdfReader(pdf_path)
        for page in pdf_reader.pages:
            self.pdf_writer.add_page(page)

    def merge(self, output_path):
        with open(output_path, 'wb') as output_pdf:
            self.pdf_writer.write(output_pdf)

# # 使用方法
# pdf_path = r"C:\Users\hc0\Desktop\Eng\eng.pdf"
# save_path = r"C:\Users\hc0\Desktop\Eng\eee7.pdf"
# pdf_splitter = PDFSplitter(pdf_path, save_path)
# pdf_splitter.add_range(0, 1)
# pdf_splitter.split()