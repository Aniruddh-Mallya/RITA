import ollama

class LLMClient:
    @staticmethod
    def call_ollama(model_name: str, prompt_text: str) -> str:
        """Generic wrapper for Ollama calls."""
        try:
            # Generation tasks can be long, so we rely on Ollama's internal queue.
            # If using requests directly, we'd set a timeout=300 here.
            response = ollama.chat(
                model=model_name,
                messages=[{'role': 'user', 'content': prompt_text}]
            )
            return response['message']['content'].strip()
        except Exception as e:
            print(f"[LLM-ERROR] Ollama call failed: {e}")
            # Return a safe error string that won't crash JSON parsers immediately
            return f"ERROR: LLM Generation Failed. Reason: {str(e)}"

    @staticmethod
    def classify_review(review_text: str, model_name: str, prompt_template: str) -> str:
        """Specialized logic for classification (Worker)."""
        try:
            formatted_prompt = prompt_template.format(review_text=review_text)
            result = LLMClient.call_ollama(model_name, formatted_prompt)

            # Basic cleaning/validation logic
            valid_classifications = [
                'Feature', 'Bug', 'Performance', 'Usability', 'Reliability', 'Security', 
                'FR_Category_1', 'FR_Category_2', 'Other'
            ]
            for valid in valid_classifications:
                if valid.lower() in result.lower():
                    return valid
            return "Other"
        except Exception as e:
            print(f"[LLM-ERROR] Classification failed: {e}")
            return "ERROR_LLM"

    @staticmethod
    def generate_text(input_text: str, model_name: str, prompt_template: str) -> str:
        """Specialized logic for SRS/User Stories (API/Worker)."""
        try:
            # Validation: Ensure template exists
            if not prompt_template:
                return "ERROR: Prompt template not found."
                
            formatted_prompt = prompt_template.format(review_text=input_text)
            return LLMClient.call_ollama(model_name, formatted_prompt)
        except Exception as e:
             print(f"[LLM-ERROR] Generation failed: {e}")
             return f"ERROR_GENERATION: {str(e)}"