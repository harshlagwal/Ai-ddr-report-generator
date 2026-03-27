from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os

# SECURITY WARNING: DO NOT HARDCODE API KEYS.
# Always fetch keys from environment variables or constructor arguments.

class ReportGenerator:
    def __init__(self, groq_api_key=None, primary_model="llama-3.1-8b-instant", fallback_model="gemma2-9b-it", temperature=0.1):
        # Use provided key or fetch from environment
        self.api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError("Groq API Key not found. Please provide it or set GROQ_API_KEY environment variable.")

        self.primary_model = primary_model
        self.fallback_model = fallback_model
        self.temperature = temperature
        
        # Initialize primary LLM
        self.llm = ChatGroq(
            groq_api_key=self.api_key,
            model_name=self.primary_model,
            temperature=self.temperature
        )

    def generate_ddr(self, context):
        """
        Generates a Detailed Diagnostic Report (DDR) based on provided context.
        Includes automatic fallback logic for deprecated models.
        """
        # Debug print requested
        print(f"[DEBUG] Context length sent to LLM: {len(context)} characters.")

        if not context.strip():
            return "Error: No relevant context found to generate the report. Please check the source documents."

        prompt_template = """
        You are an expert Property Diagnostic Engineer. Your task is to generate a Detailed Diagnostic Report (DDR) by merging information from an Inspection Report and a Thermal Report.

        CONTEXT:
        {context}

        ---
        STRICT RULES FOR EVIDENCE IMAGES:
        1. For each observation or issue you describe, you MUST check the [AVAILABLE EVIDENCE IMAGES] tag in the context above.
        2. If an image name is available for that specific observation, write "Evidence Image: <image_name>" directly below the observation text.
        3. If no relevant image name is found in the context for an observation, write "Evidence Image: Not Available".
        4. Format example:
           Master Bedroom:
           • Dampness and Efflorescence:
             Observed dampness on the wall surface.
             Evidence Image: inspection_p3_i7.jpeg

        ---
        STRICT RULES FOR MISSING INFORMATION:
        1. Every missing or unclear detail in the final section MUST be written exactly as: "<Detail Name> → Not Available".
        2. DO NOT use phrases like "not specified", "not mentioned", or "no information".
        3. Format example:
           Missing or Unclear Information:
           • Thermal performance details → Not Available
           • Paint type and manufacturer → Not Available

        ---
        GENERAL RULES:
        1. Clean, client-friendly, non-technical language.
        2. NO HALLUCINATIONS. Only use facts from the context.
        3. If inspection and thermal reports conflict, EXPLICITLY mention the conflict.
        4. Group issues logically by area/room.
        5. Remove duplicate observations found across multiple pages.
        6. Provide reasoning for severity (Low, Medium, High).

        ---
        REPORT STRUCTURE (Mandatory):
        1. Property Issue Summary: A high-level overview.
        2. Area-wise Observations: Detailed breakdown by room/area (including Evidence Images).
        3. Probable Root Cause: Scientific reasoning.
        4. Severity Assessment: Low/Medium/High with justification.
        5. Recommended Actions: Clear remediation steps.
        6. Additional Notes.
        7. Missing or Unclear Information: (Using the strict "→ Not Available" format).

        ---
        GENERATE THE STRUCTURED DDR REPORT:
        """
        
        prompt = PromptTemplate(template=prompt_template, input_variables=["context"])
        
        try:
            # Try with primary model
            chain = prompt | self.llm
            response = chain.invoke({"context": context})
            return response.content
        except Exception as primary_error:
            print(f"[WARNING] Primary model ({self.primary_model}) failed: {primary_error}")
            print(f"[INFO] Switching to fallback model: {self.fallback_model}")
            
            try:
                # Fallback model attempt
                fallback_llm = ChatGroq(
                    groq_api_key=self.api_key,
                    model_name=self.fallback_model,
                    temperature=self.temperature
                )
                fallback_chain = prompt | fallback_llm
                response = fallback_chain.invoke({"context": context})
                return response.content
            except Exception as fallback_error:
                error_msg = f"Error during report generation. Primary ({self.primary_model}) and Fallback ({self.fallback_model}) both failed. Detail: {fallback_error}"
                print(f"[ERROR] {error_msg}")
                return error_msg

if __name__ == "__main__":
    # Test block
    try:
        gen = ReportGenerator()
        print("ReportGenerator initialized successfully.")
    except Exception as e:
        print(f"Initialization failed: {e}")
