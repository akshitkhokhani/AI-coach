import logging
from typing import List, Dict, Any
from app.config import OPENAI_API_KEY, OPENAI_MODEL
from openai import OpenAI

logger = logging.getLogger(__name__)

class LLMService:
    """Service for interacting with LLM API"""
    
    def __init__(self, model=OPENAI_MODEL):
        self.model = model
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        if not OPENAI_API_KEY:
            logger.warning("OpenAI API key not found. LLM functionality will not work.")
    
    def generate_response(self, query: str, similar_examples: List[Dict[str, Any]]) -> str:
        """
        Generate counseling response using LLM
        
        Args:
            query (str): The user's query
            similar_examples (list): List of similar examples from vector search
            
        Returns:
            str: Generated counseling response
        """
        if not OPENAI_API_KEY:
            return "OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable."
            
        # Construct prompt with examples
        examples_text = ""
        for i, example in enumerate(similar_examples):
            examples_text += f"Example {i+1}:\n"
            examples_text += f"User Challenge: {example['Context']}\n"
            examples_text += f"Counseling Response: {example['Response']}\n\n"
        
        system_prompt = """You are a supportive mental health counseling assistant. Your role is to provide helpful, 
compassionate, and practical responses to people seeking guidance on everyday mental health challenges.

IMPORTANT: You should ALWAYS provide a supportive response based on the examples given. Do not refuse to help or 
suggest the user seek professional help unless the query involves serious harm, self-harm, or illegal activities.

For most everyday mental health challenges like stress, time management, mild anxiety, or feeling overwhelmed,
you should offer practical advice and empathetic support similar to the example responses.

Your goal is to be helpful and reflect the same tone, style and approach shown in the examples."""

        user_prompt = f"""Here are some specific examples of helpful counseling responses for situations 
similar to the current user query. Please model your response style, tone, and helpfulness after these examples:

{examples_text}

Based on the examples above, please provide a compassionate and helpful counseling response to the following mental health challenge:

User Challenge: {query}

Counseling Response:"""
        
        try:
            logger.info("Sending request to OpenAI API")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=600,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating response from LLM: {str(e)}")
            return "I'm sorry, but I'm having trouble providing a response at the moment. Please try again later."
