import os
import pickle
from support.settings import dest_dir


class ConfigManager:
    """Manages persistent configuration storage for user settings using 
    pickle"""
    
    def __init__(self):
        self.config_dir = f"{dest_dir}/config"
        self.config_file = f"{self.config_dir}/user_config.pkl"
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        """Create config directory if it doesn't exist"""
        os.makedirs(self.config_dir, exist_ok=True)
    
    def save_config(self, config_data):
        """Save configuration to pickle file"""
        try:
            with open(self.config_file, 'wb') as f:
                pickle.dump(config_data, f)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def load_config(self):
        """Load configuration from pickle file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'rb') as f:
                    return pickle.load(f)
            return {}
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
    
    def get_config_value(self, key, default=None):
        """Get a specific configuration value"""
        config = self.load_config()
        return config.get(key, default)
    
    def set_config_value(self, key, value):
        """Set a specific configuration value"""
        config = self.load_config()
        config[key] = value
        return self.save_config(config)
    
    def has_config(self):
        """Check if configuration file exists"""
        return os.path.exists(self.config_file)
    
    def clear_config(self):
        """Clear all configuration data"""
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            return True
        except Exception as e:
            print(f"Error clearing config: {e}")
            return False
