# core/config_validator.py

"""
✅ Configuration Validator
Validates all configuration values and provides helpful error messages.
"""

import os
from typing import Dict, Any, List
from core.config_loader import load_config

class ConfigValidator:
    """Validates configuration values and provides helpful error messages."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.errors = []
        self.warnings = []
    
    def validate(self) -> bool:
        """Validate all configuration values. Returns True if valid, False otherwise."""
        self.errors = []
        self.warnings = []
        
        # Validate required sections
        self._validate_openai_config()
        self._validate_postgres_config()
        self._validate_embedding_config()
        self._validate_paths_config()
        self._validate_settings_config()
        self._validate_llm_config()
        
        # Validate file paths exist
        self._validate_file_paths()
        
        return len(self.errors) == 0
    
    def _validate_openai_config(self):
        """Validate OpenAI configuration."""
        openai_config = self.config.get("openai", {})
        
        if not openai_config.get("api_key"):
            self.errors.append("❌ OpenAI API key is required in config.yaml")
        elif not openai_config["api_key"].startswith("sk-"):
            self.warnings.append("⚠️ OpenAI API key format looks incorrect (should start with 'sk-')")
        
        if not openai_config.get("org_id"):
            self.warnings.append("⚠️ OpenAI organization ID is missing (optional but recommended)")
    
    def _validate_postgres_config(self):
        """Validate PostgreSQL configuration."""
        postgres_config = self.config.get("postgres", {})
        
        required_fields = ["host", "database", "user", "password", "port"]
        for field in required_fields:
            if not postgres_config.get(field):
                self.errors.append(f"❌ PostgreSQL {field} is required in config.yaml")
        
        if postgres_config.get("port"):
            try:
                port = int(postgres_config["port"])
                if not (1 <= port <= 65535):
                    self.errors.append("❌ PostgreSQL port must be between 1 and 65535")
            except ValueError:
                self.errors.append("❌ PostgreSQL port must be a valid integer")
    
    def _validate_embedding_config(self):
        """Validate embedding configuration."""
        embedding_config = self.config.get("embedding", {})
        
        if not embedding_config.get("provider"):
            self.errors.append("❌ Embedding provider is required in config.yaml")
        
        if not embedding_config.get("model"):
            self.errors.append("❌ Embedding model is required in config.yaml")
    
    def _validate_paths_config(self):
        """Validate paths configuration."""
        paths_config = self.config.get("paths", {})
        
        required_paths = ["schema_json", "index_folder", "embedding_dir", "table_index_folder", "logs_dir"]
        for path_field in required_paths:
            if not paths_config.get(path_field):
                self.errors.append(f"❌ Path {path_field} is required in config.yaml")
    
    def _validate_settings_config(self):
        """Validate settings configuration."""
        settings_config = self.config.get("settings", {})
        
        # Validate embedding settings
        if not isinstance(settings_config.get("column_top_k"), int) or settings_config["column_top_k"] <= 0:
            self.errors.append("❌ column_top_k must be a positive integer")
        
        if not isinstance(settings_config.get("table_top_k"), int) or settings_config["table_top_k"] <= 0:
            self.errors.append("❌ table_top_k must be a positive integer")
        
        # Validate similarity threshold
        threshold = settings_config.get("similarity_threshold")
        if not isinstance(threshold, (int, float)) or not (0 <= threshold <= 1):
            self.errors.append("❌ similarity_threshold must be a number between 0 and 1")
        
        # Validate forbidden SQL keywords
        forbidden_keywords = settings_config.get("forbidden_sql_keywords", [])
        if not isinstance(forbidden_keywords, list) or len(forbidden_keywords) == 0:
            self.errors.append("❌ forbidden_sql_keywords must be a non-empty list")
        
        # Validate column mappings
        column_mappings = settings_config.get("column_mappings", {})
        if not isinstance(column_mappings, dict):
            self.errors.append("❌ column_mappings must be a dictionary")
        
        # Validate logging settings
        log_level = settings_config.get("log_level", "INFO")
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if log_level not in valid_log_levels:
            self.errors.append(f"❌ log_level must be one of: {', '.join(valid_log_levels)}")
        
        # Validate performance settings
        timeout = settings_config.get("max_query_timeout")
        if timeout is not None and (not isinstance(timeout, (int, float)) or timeout <= 0):
            self.errors.append("❌ max_query_timeout must be a positive number")
        
        max_rows = settings_config.get("max_result_rows")
        if max_rows is not None and (not isinstance(max_rows, int) or max_rows <= 0):
            self.errors.append("❌ max_result_rows must be a positive integer")
    
    def _validate_llm_config(self):
        """Validate LLM configuration."""
        llm_config = self.config.get("llm", {})
        
        if not llm_config.get("model"):
            self.errors.append("❌ LLM model is required in config.yaml")
        
        temperature = llm_config.get("temperature")
        if temperature is not None and (not isinstance(temperature, (int, float)) or not (0 <= temperature <= 2)):
            self.errors.append("❌ LLM temperature must be a number between 0 and 2")
        
        max_tokens = llm_config.get("max_tokens")
        if max_tokens is not None and (not isinstance(max_tokens, int) or max_tokens <= 0):
            self.errors.append("❌ LLM max_tokens must be a positive integer")
    
    def _validate_file_paths(self):
        """Validate that required files and directories exist."""
        paths_config = self.config.get("paths", {})
        
        # Check if schema file exists
        schema_path = paths_config.get("schema_json")
        if schema_path and not os.path.exists(schema_path):
            self.warnings.append(f"⚠️ Schema file not found: {schema_path}")
        
        # Check if embedding directory exists
        embedding_dir = paths_config.get("embedding_dir")
        if embedding_dir and not os.path.exists(embedding_dir):
            self.warnings.append(f"⚠️ Embedding directory not found: {embedding_dir}")
        
        # Check if logs directory exists (will be created automatically)
        logs_dir = paths_config.get("logs_dir")
        if logs_dir and not os.path.exists(logs_dir):
            self.warnings.append(f"⚠️ Logs directory not found: {logs_dir} (will be created automatically)")
    
    def get_errors(self) -> List[str]:
        """Get list of validation errors."""
        return self.errors
    
    def get_warnings(self) -> List[str]:
        """Get list of validation warnings."""
        return self.warnings
    
    def print_validation_report(self):
        """Print a comprehensive validation report."""
        print("🔍 Configuration Validation Report")
        print("=" * 50)
        
        if self.errors:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print("\n⚠️ WARNINGS:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✅ Configuration is valid!")
        elif not self.errors:
            print("\n✅ Configuration is valid (with warnings)")
        else:
            print(f"\n❌ Configuration has {len(self.errors)} error(s)")

def validate_config() -> bool:
    """Convenience function to validate the current configuration."""
    config = load_config()
    validator = ConfigValidator(config)
    is_valid = validator.validate()
    validator.print_validation_report()
    return is_valid

if __name__ == "__main__":
    validate_config() 