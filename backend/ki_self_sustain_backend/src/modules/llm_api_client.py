import requests
import json
from datetime import datetime
import logging

class LLMAPIClient:
    """Client for interacting with configurable LLM APIs"""
    
    def __init__(self, base_url="http://localhost:8000", api_key=None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        
        # Set up authentication if API key is provided
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}'
            })
    
    def set_base_url(self, url):
        """Update the LLM API base URL"""
        self.base_url = url.rstrip('/')
    
    def set_api_key(self, api_key):
        """Update the API key"""
        self.api_key = api_key
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}'
            })
        elif 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
    
    def test_connection(self):
        """Test connection to LLM API"""
        try:
            # Try different common endpoints
            endpoints_to_try = [
                "/v1/models",
                "/api/v1/models", 
                "/models",
                "/health",
                "/api/health"
            ]
            
            for endpoint in endpoints_to_try:
                try:
                    response = self.session.get(f"{self.base_url}{endpoint}")
                    if response.status_code == 200:
                        return {
                            "status": "success",
                            "endpoint": endpoint,
                            "message": "Connection successful"
                        }
                except:
                    continue
            
            return {
                "status": "error",
                "message": "No valid endpoints found"
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Connection failed: {str(e)}"
            }
    
    def get_models(self):
        """Get available models from LLM API"""
        try:
            endpoints_to_try = [
                "/v1/models",
                "/api/v1/models",
                "/models"
            ]
            
            for endpoint in endpoints_to_try:
                try:
                    response = self.session.get(f"{self.base_url}{endpoint}")
                    if response.status_code == 200:
                        return {
                            "status": "success",
                            "data": response.json()
                        }
                except:
                    continue
            
            return {
                "status": "error",
                "message": "Could not retrieve models"
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Request failed: {str(e)}"
            }
    
    def chat_completion(self, messages, model="gpt-3.5-turbo", temperature=0.7, max_tokens=1000):
        """Send chat completion request to LLM"""
        try:
            # Try OpenAI-compatible endpoint first
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            endpoints_to_try = [
                "/v1/chat/completions",
                "/api/v1/chat/completions",
                "/chat/completions",
                "/api/chat"
            ]
            
            headers = {'Content-Type': 'application/json'}
            
            for endpoint in endpoints_to_try:
                try:
                    response = self.session.post(
                        f"{self.base_url}{endpoint}",
                        json=payload,
                        headers=headers
                    )
                    if response.status_code == 200:
                        return {
                            "status": "success",
                            "data": response.json()
                        }
                except:
                    continue
            
            return {
                "status": "error",
                "message": "No valid chat completion endpoints found"
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Request failed: {str(e)}"
            }
    
    def simple_completion(self, prompt, model="gpt-3.5-turbo", temperature=0.7, max_tokens=1000):
        """Send simple text completion request"""
        messages = [
            {"role": "user", "content": prompt}
        ]
        return self.chat_completion(messages, model, temperature, max_tokens)
    
    def analyze_system_performance(self, performance_data):
        """Use LLM to analyze system performance and suggest improvements"""
        prompt = f"""
        Analyze the following system performance data and provide improvement suggestions:
        
        Performance Data:
        {json.dumps(performance_data, indent=2)}
        
        Please provide:
        1. Analysis of current performance
        2. Identified weaknesses or bottlenecks
        3. Specific improvement recommendations
        4. Priority ranking of improvements
        
        Format your response as JSON with the following structure:
        {{
            "analysis": "...",
            "weaknesses": ["...", "..."],
            "recommendations": [
                {{
                    "action": "...",
                    "priority": "high|medium|low",
                    "expected_impact": "..."
                }}
            ]
        }}
        """
        
        result = self.simple_completion(prompt, temperature=0.3)
        
        if result["status"] == "success":
            try:
                # Extract JSON from response
                response_text = result["data"]["choices"][0]["message"]["content"]
                # Try to parse JSON from the response
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                    return {
                        "status": "success",
                        "data": analysis
                    }
                else:
                    return {
                        "status": "success",
                        "data": {
                            "analysis": response_text,
                            "weaknesses": [],
                            "recommendations": []
                        }
                    }
            except:
                return {
                    "status": "success",
                    "data": {
                        "analysis": result["data"]["choices"][0]["message"]["content"],
                        "weaknesses": [],
                        "recommendations": []
                    }
                }
        
        return result
    
    def generate_improvement_plan(self, analysis_data):
        """Generate detailed improvement plan based on analysis"""
        prompt = f"""
        Based on the following analysis, create a detailed improvement plan:
        
        Analysis:
        {json.dumps(analysis_data, indent=2)}
        
        Create a comprehensive improvement plan with:
        1. Specific actionable steps
        2. Implementation timeline
        3. Resource requirements
        4. Success metrics
        5. Risk assessment
        
        Format as JSON:
        {{
            "plan_name": "...",
            "steps": [
                {{
                    "step": "...",
                    "description": "...",
                    "timeline": "...",
                    "resources": "...",
                    "success_metric": "..."
                }}
            ],
            "risks": ["...", "..."],
            "expected_outcomes": ["...", "..."]
        }}
        """
        
        result = self.simple_completion(prompt, temperature=0.3)
        
        if result["status"] == "success":
            try:
                response_text = result["data"]["choices"][0]["message"]["content"]
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    plan = json.loads(json_match.group())
                    return {
                        "status": "success",
                        "data": plan
                    }
            except:
                pass
            
            return {
                "status": "success",
                "data": {
                    "plan_name": "Generated Improvement Plan",
                    "steps": [],
                    "risks": [],
                    "expected_outcomes": [],
                    "raw_response": result["data"]["choices"][0]["message"]["content"]
                }
            }
        
        return result
    
    def generate_service_code(self, service_type, requirements):
        """Generate code for new services based on requirements"""
        prompt = f"""
        Generate Python code for a {service_type} service with the following requirements:
        
        Requirements:
        {json.dumps(requirements, indent=2)}
        
        The code should:
        1. Be production-ready and well-documented
        2. Include error handling
        3. Follow Python best practices
        4. Include a simple API interface
        5. Be containerizable with Docker
        
        Provide the complete Python code.
        """
        
        result = self.simple_completion(prompt, temperature=0.2, max_tokens=2000)
        
        if result["status"] == "success":
            return {
                "status": "success",
                "data": {
                    "code": result["data"]["choices"][0]["message"]["content"],
                    "service_type": service_type,
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        return result
    
    def optimize_flowise_configuration(self, current_config):
        """Use LLM to optimize Flowise configuration"""
        prompt = f"""
        Analyze and optimize the following Flowise configuration:
        
        Current Configuration:
        {json.dumps(current_config, indent=2)}
        
        Provide optimization suggestions for:
        1. Node connections and flow efficiency
        2. Model parameters and settings
        3. Prompt engineering improvements
        4. Performance optimizations
        
        Return optimized configuration as JSON.
        """
        
        result = self.simple_completion(prompt, temperature=0.3, max_tokens=1500)
        
        if result["status"] == "success":
            try:
                response_text = result["data"]["choices"][0]["message"]["content"]
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    optimized_config = json.loads(json_match.group())
                    return {
                        "status": "success",
                        "data": optimized_config
                    }
            except:
                pass
            
            return {
                "status": "success",
                "data": {
                    "optimized_config": current_config,
                    "suggestions": result["data"]["choices"][0]["message"]["content"]
                }
            }
        
        return result

