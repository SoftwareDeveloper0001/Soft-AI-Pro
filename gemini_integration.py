"""
🤖 GEMINI API INTEGRATION - Modern Google Gemini Integration
============================================================

Integrasi lengkap dengan Google Gemini API untuk Soft AI Pro
- Secure API key management
- Conversation history
- Streaming responses
- Error handling
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Use the supported Google GenAI SDK.
google_genai: Any = None
google_genai_types: Any = None
try:
    from google import genai as _google_genai
    from google.genai import types as _google_genai_types

    google_genai = _google_genai
    google_genai_types = _google_genai_types
except ImportError:
    pass

GEMINI_AVAILABLE = google_genai is not None
if not GEMINI_AVAILABLE:
    logger.warning("Google Gemini SDK not installed. Install with: pip install google-genai")


class GeminiIntegration:
    """
    Modern Gemini API Integration Manager
    Mengelola konfigurasi, koneksi, dan interaksi dengan Gemini API
    """
    
    def __init__(self):
        self.api_key: Optional[str] = None
        self.config_path = Path.home() / ".soft_ai_pro" / "gemini_config.json"
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.model: Optional[str] = None
        self.client: Any = None
        self.chat: Any = None
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
        self.chat_history: List[Dict[str, str]] = []
        self.is_configured = False
        
        # Load saved configuration
        self._load_config()
    
    def _load_config(self):
        """Load saved Gemini configuration from disk"""
        try:
            from dotenv import load_dotenv

            load_dotenv()
            config: Dict[str, Any] = {}
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
            self.model_name = os.getenv(
                'GEMINI_MODEL', config.get('model', 'gemini-2.0-flash')
            )
            api_key = os.getenv('GEMINI_API_KEY') or config.get('api_key')
            if api_key and GEMINI_AVAILABLE and self.initialize_gemini(api_key):
                logger.info("Gemini configuration loaded")
        except Exception as e:
            logger.error("Error loading Gemini config: %s", e)
    
    def save_config(self, api_key: str) -> bool:
        """
        Save Gemini API key securely
        
        Args:
            api_key: { "workspaceRoot": "c:\\Users\\zyrex\\Soft-AI-Pro", "workingDirectory": "c:\\Users\\zyrex\\Soft-AI-Pro", "codeSnippet": "try:\n    import app\n    print('APP_IMPORT_OK')\nexcept Exception as exc:\n    print(f'{type(exc).__name__}: {exc}')", "timeout": 30000 }
            
        Returns:
            bool: True if saved successfully
        """
        try:
            if not self.is_api_key_valid(api_key):
                return False
            if not self.initialize_gemini(api_key):
                return False

            config: Dict[str, Any] = {
                'api_key': api_key,
                'saved_at': datetime.now().isoformat(),
                'model': self.model_name
            }
            
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            # Change file permissions to readable only by owner (Unix-like systems)
            try:
                os.chmod(self.config_path, 0o600)
            except:
                pass
            
            self.api_key = api_key
            logger.info("Gemini API key saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving Gemini config: {e}")
            return False
    
    def initialize_gemini(self, api_key: str) -> bool:
        """
        Initialize Gemini API with provided key
        
        Args:
            api_key: AQ.Ab8RN6JcaYmQNBVm_qaGh7KbWq4Tqw4I-D4zRoykGtyN0EM5vg
            
        Returns:
            bool: True if initialization successful
        """
        if not GEMINI_AVAILABLE:
            logger.error("❌ Google Gemini SDK not available")
            return False

        self.api_key = api_key
        self.model_name = os.getenv('GEMINI_MODEL', self.model_name)

        try:
            self.client = google_genai.Client(api_key=api_key)
            self.model = self.model_name
            self.is_configured = True
            return True
        except Exception as e:
            self.client = None
            self.model = None
            self.is_configured = False
            logger.error("Error initializing Gemini: %s", e)
            return False
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test Gemini API connection
        
        Returns:
            Dict with connection status and details
        """
        if not self.is_configured:
            return {
                'success': False,
                'message': '❌ Gemini not configured',
                'error': 'API key not set'
            }

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents="Reply with a short greeting.",
            )
            text = getattr(response, 'text', '') or ''

            if text:
                return {
                    'success': True,
                    'message': '✅ Connection successful',
                    'model': self.model_name,
                    'response': text[:100]
                }
            return {
                'success': False,
                'message': 'Gemini returned an empty response',
                'error': 'Empty response',
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'❌ Connection failed: {str(e)}',
                'error': str(e)
            }
    
    def generate_text(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Generate text using Gemini
        
        Args:
            prompt: User prompt
            **kwargs: Additional parameters like temperature, max_tokens
            
        Returns:
            Dict with generated text or error
        """
        if not self.is_configured:
            return {
                'success': False,
                'message': 'Gemini not configured',
                'text': None
            }
        
        try:
            config = google_genai_types.GenerateContentConfig(
                    temperature=kwargs.get('temperature', 0.7),
                    max_output_tokens=kwargs.get('max_tokens', 2048),
                    top_p=kwargs.get('top_p', 0.95),
                    top_k=kwargs.get('top_k', 40)
            )
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config,
            )
            text = getattr(response, 'text', None)
            if not text:
                raise ValueError('Gemini returned an empty response')
            
            return {
                'success': True,
                'text': text,
                'message': 'Text generated successfully'
            }
        except Exception as e:
            logger.error(f"Generate text error: {e}")
            return {
                'success': False,
                'message': f'Error: {str(e)}',
                'text': None
            }
    
    def start_chat(self) -> bool:
        """Initialize chat session"""
        if not self.is_configured:
            return False
        
        try:
            self.chat = self.client.chats.create(model=self.model_name)
            self.chat_history = []
            return True
        except Exception as e:
            logger.error(f"Error starting chat: {e}")
            return False
    
    def send_message(self, message: str) -> Dict[str, Any]:
        """
        Send message in chat
        
        Args:
            message: User message
            
        Returns:
            Dict with response or error
        """
        if not self.is_configured:
            return {'success': False, 'response': 'Gemini not configured'}
        
        try:
            chat: Any = self.chat
            if chat is None:
                if not self.start_chat():
                    return {'success': False, 'response': 'Unable to start Gemini chat'}
                chat = self.chat
            response = chat.send_message(message)
            
            # Store in history
            self.chat_history.append({
                'role': 'user',
                'content': message,
                'timestamp': datetime.now().isoformat()
            })
            
            response_text = getattr(response, 'text', '') or ''
            self.chat_history.append({
                'role': 'assistant',
                'content': response_text,
                'timestamp': datetime.now().isoformat()
            })
            
            return {
                'success': True,
                'response': response_text,
                'message': '✅ Response received'
            }
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return {
                'success': False,
                'response': f'Error: {str(e)}',
                'message': '❌ Chat failed'
            }
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get chat history"""
        return self.chat_history
    
    def clear_chat_history(self):
        """Clear chat history"""
        self.chat_history = []
        self.chat = None
    
    def is_api_key_valid(self, api_key: str) -> bool:
        """Check if API key format is valid"""
        # Gemini API keys are typically long strings
        return len(api_key) > 30 and api_key.strip() == api_key
    
    def remove_api_key(self) -> bool:
        """Remove saved API key"""
        try:
            if self.config_path.exists():
                self.config_path.unlink()
            self.api_key = None
            self.model = None
            self.client = None
            self.chat = None
            self.is_configured = False
            logger.info("✅ API key removed successfully")
            return True
        except Exception as e:
            logger.error(f"Error removing API key: {e}")
            return False


# Global instance
gemini_manager = GeminiIntegration()


def get_gemini_manager() -> GeminiIntegration:
    """Get global Gemini manager instance"""
    return gemini_manager
