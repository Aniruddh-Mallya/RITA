import json
import os

PROMPT_CONFIG_FILE = "prompts_config.json"

class ConfigManager:
    def __init__(self):
        self.llm_map = {}
        self.prompts = {}
        self.loaded = False

    def load_config(self):
        """Loads the LLM map and prompts from the JSON file."""
        if not os.path.exists(PROMPT_CONFIG_FILE):
            print(f"[CONFIG-ERROR] CRITICAL: '{PROMPT_CONFIG_FILE}' not found.")
            return False
            
        try:
            with open(PROMPT_CONFIG_FILE, 'r') as f:
                config_data = json.load(f)
                
                self.llm_map = config_data.get("llm_map", {})
                self.prompts = {
                    "FR": config_data.get("FR", {}),
                    "NFR": config_data.get("NFR", {}),
                    "SRS": config_data.get("SRS", {}),
                    "USER_STORIES": config_data.get("USER_STORIES", {})
                }

                # Validation
                if not self.llm_map:
                    raise ValueError("'llm_map' missing.")
                if not all(self.prompts.values()):
                     raise ValueError("Missing prompt categories (FR, NFR, SRS, or USER_STORIES).")
                     
            self.loaded = True
            print(f"[CONFIG] Successfully loaded configuration from '{PROMPT_CONFIG_FILE}'.")
            return True
            
        except Exception as e:
            print(f"[CONFIG-ERROR] Failed to load config: {e}")
            return False

    def get_prompt(self, category, strategy):
        return self.prompts.get(category, {}).get(strategy)

    def get_backend_llm(self, frontend_name):
        return self.llm_map.get(frontend_name)

# Create a singleton instance to be used by other files
config_manager = ConfigManager()