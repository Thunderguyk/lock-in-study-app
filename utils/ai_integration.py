"""
AI Integration utilities for Lock-In App
Handles DeepSeek and Ollama API interactions
"""

import requests
import json
from typing import Dict, List, Optional
import streamlit as st

class DeepSeekClient:
    """DeepSeek API client for document analysis"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com"
        
    def analyze_document(self, text: str) -> Dict:
        """Analyze document text and extract insights"""
        # Mock implementation - replace with actual API call
        return {
            "key_topics": ["Topic 1", "Topic 2", "Topic 3"],
            "weightage": [40, 30, 30],
            "summary": "Document analysis summary",
            "question_formats": {
                "Multiple Choice": 40,
                "Short Answer": 35,
                "Essay": 25
            }
        }
    
    def summarize_text(self, text: str, max_length: int = 500) -> str:
        """Summarize text using DeepSeek"""
        # Mock implementation
        return f"This is a summarized version of the input text (max {max_length} chars)."

class OllamaClient:
    """Ollama local LLM client"""
    
    def __init__(self, endpoint: str = "http://localhost:11434"):
        self.endpoint = endpoint
        
    def chat(self, message: str, model: str = "llama2") -> str:
        """Send chat message to Ollama"""
        try:
            response = requests.post(
                f"{self.endpoint}/api/generate",
                json={
                    "model": model,
                    "prompt": message,
                    "stream": False
                }
            )
            if response.status_code == 200:
                return response.json().get("response", "No response")
            else:
                return "Error connecting to Ollama"
        except Exception as e:
            return f"Connection error: {str(e)}"
    
    def list_models(self) -> List[str]:
        """List available Ollama models"""
        try:
            response = requests.get(f"{self.endpoint}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model["name"] for model in models]
            return []
        except Exception:
            return []

def get_ai_clients():
    """Get configured AI clients from settings"""
    settings = st.session_state.get('app_settings', {})
    ai_settings = settings.get('ai', {})
    
    deepseek_client = None
    if ai_settings.get('deepseek_api_key'):
        deepseek_client = DeepSeekClient(ai_settings['deepseek_api_key'])
    
    ollama_client = OllamaClient(
        ai_settings.get('ollama_endpoint', 'http://localhost:11434')
    )
    
    return deepseek_client, ollama_client
