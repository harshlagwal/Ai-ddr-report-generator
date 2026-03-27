class Retriever:
    def __init__(self, vector_db):
        self.vector_db = vector_db

    def retrieve_relevant_chunks(self, query, k=5):
        """
        Retrieves the top k relevant chunks for a given query.
        """
        results = self.vector_db.similarity_search(query, k=k)
        return results

    def get_context_for_ddr(self, query):
        """
        Retrieves relevant context and associated images.
        """
        chunks = self.retrieve_relevant_chunks(query, k=10)
        context_text = ""
        associated_images = []

        import os
        for chunk in chunks:
            source = chunk.metadata.get('source', 'unknown')
            page = chunk.metadata.get('page_number', 'unknown')
            context_text += f"\n[SOURCE: {source}, PAGE: {page}]\n"
            
            # Embed image names directly in the context for the LLM
            if chunk.metadata.get("images"):
                img_names = [os.path.basename(img) for img in chunk.metadata["images"]]
                context_text += f"[AVAILABLE EVIDENCE IMAGES: {', '.join(img_names)}]\n"
            
            context_text += chunk.page_content + "\n"
            
            # Map images from metadata for the gallery
            if chunk.metadata.get("images"):
                associated_images.extend(chunk.metadata["images"])

        # Deduplicate images
        associated_images = list(set(associated_images))
        
        # Debug print requested
        print(f"[DEBUG] Retrieved {len(chunks)} relevant chunks from vector store.")
        print(f"[DEBUG] Total context characters: {len(context_text)}")
        print(f"[DEBUG] Unique evidence images found: {len(associated_images)}")
        
        return context_text, associated_images

if __name__ == "__main__":
    pass
