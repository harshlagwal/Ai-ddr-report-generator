import fitz  # PyMuPDF
import os
from PIL import Image
import io

class PDFLoader:
    def __init__(self, upload_dir="data/extracted_images"):
        self.upload_dir = upload_dir
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

    def extract_text_and_images(self, pdf_path, source_type):
        """
        Extracts text and images from a PDF file.
        Returns a list of dictionaries containing page text and image paths.
        """
        doc = fitz.open(pdf_path)
        extracted_data = []
        total_images = 0

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            
            image_list = page.get_images(full=True)
            page_images = []

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                image_filename = f"{source_type}_p{page_num+1}_i{img_index+1}.{image_ext}"
                image_path = os.path.join(self.upload_dir, image_filename)
                
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                
                page_images.append(image_path)
                total_images += 1

            extracted_data.append({
                "page_number": page_num + 1,
                "text": text,
                "images": page_images,
                "source": source_type
            })

        doc.close()
        
        # Debug prints
        print(f"[DEBUG] Loaded {len(extracted_data)} pages from {source_type} report.")
        print(f"[DEBUG] Extracted {total_images} images from {source_type} report.")
        
        return extracted_data

if __name__ == "__main__":
    loader = PDFLoader()
    # data = loader.extract_text_and_images("data/inspection.pdf", "inspection")
