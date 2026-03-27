from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class TextSplitter:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    def split_data(self, extracted_data):
        """
        Splits extracted text data into LangChain Document objects with metadata.
        """
        documents = []
        for item in extracted_data:
            chunks = self.splitter.split_text(item["text"])
            for chunk in chunks:
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "page_number": item["page_number"],
                        "source": item["source"],
                        "images": item["images"]
                    }
                )
                documents.append(doc)
        
        # Debug print
        print(f"[DEBUG] Split extracted data into {len(documents)} text chunks.")
        
        return documents

if __name__ == "__main__":
    splitter = TextSplitter()
