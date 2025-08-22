import requests
import json
from datetime import datetime
import logging

class FlowiseAPIClient:
    """Client for interacting with Flowise API"""
    
    def __init__(self, base_url="http://localhost:3000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        
    def set_base_url(self, url):
        """Update the Flowise API base URL"""
        self.base_url = url.rstrip('/')
        
    def test_connection(self):
        """Test connection to Flowise API"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/chatflows")
            return {
                "status": "success" if response.status_code == 200 else "error",
                "status_code": response.status_code,
                "message": "Connection successful" if response.status_code == 200 else f"HTTP {response.status_code}"
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Connection failed: {str(e)}"
            }
    
    def get_chatflows(self):
        """Get all chatflows from Flowise"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/chatflows")
            if response.status_code == 200:
                return {
                    "status": "success",
                    "data": response.json()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to get chatflows: HTTP {response.status_code}"
                }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Request failed: {str(e)}"
            }
    
    def get_chatflow(self, chatflow_id):
        """Get specific chatflow by ID"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/chatflows/{chatflow_id}")
            if response.status_code == 200:
                return {
                    "status": "success",
                    "data": response.json()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to get chatflow: HTTP {response.status_code}"
                }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Request failed: {str(e)}"
            }
    
    def create_chatflow(self, chatflow_data):
        """Create new chatflow"""
        try:
            headers = {'Content-Type': 'application/json'}
            response = self.session.post(
                f"{self.base_url}/api/v1/chatflows",
                json=chatflow_data,
                headers=headers
            )
            if response.status_code in [200, 201]:
                return {
                    "status": "success",
                    "data": response.json()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to create chatflow: HTTP {response.status_code}"
                }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Request failed: {str(e)}"
            }
    
    def update_chatflow(self, chatflow_id, chatflow_data):
        """Update existing chatflow"""
        try:
            headers = {'Content-Type': 'application/json'}
            response = self.session.put(
                f"{self.base_url}/api/v1/chatflows/{chatflow_id}",
                json=chatflow_data,
                headers=headers
            )
            if response.status_code == 200:
                return {
                    "status": "success",
                    "data": response.json()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to update chatflow: HTTP {response.status_code}"
                }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Request failed: {str(e)}"
            }
    
    def delete_chatflow(self, chatflow_id):
        """Delete chatflow"""
        try:
            response = self.session.delete(f"{self.base_url}/api/v1/chatflows/{chatflow_id}")
            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "Chatflow deleted successfully"
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to delete chatflow: HTTP {response.status_code}"
                }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Request failed: {str(e)}"
            }
    
    def predict_chatflow(self, chatflow_id, message, session_id=None):
        """Send message to chatflow and get prediction"""
        try:
            payload = {
                "question": message
            }
            if session_id:
                payload["sessionId"] = session_id
                
            headers = {'Content-Type': 'application/json'}
            response = self.session.post(
                f"{self.base_url}/api/v1/prediction/{chatflow_id}",
                json=payload,
                headers=headers
            )
            if response.status_code == 200:
                return {
                    "status": "success",
                    "data": response.json()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to get prediction: HTTP {response.status_code}"
                }
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Request failed: {str(e)}"
            }
    
    def get_chatflow_stats(self, chatflow_id):
        """Get statistics for a chatflow (mock implementation)"""
        # This would be implemented based on actual Flowise API capabilities
        return {
            "status": "success",
            "data": {
                "chatflow_id": chatflow_id,
                "total_messages": 0,
                "avg_response_time": 0.0,
                "success_rate": 1.0,
                "last_used": datetime.now().isoformat()
            }
        }
    
    def optimize_chatflow_performance(self, chatflow_id):
        """Analyze and optimize chatflow performance"""
        try:
            # Get current chatflow
            chatflow_result = self.get_chatflow(chatflow_id)
            if chatflow_result["status"] != "success":
                return chatflow_result
            
            chatflow = chatflow_result["data"]
            
            # Analyze performance (mock implementation)
            analysis = {
                "current_performance": {
                    "response_time": 2.5,
                    "accuracy": 0.85,
                    "user_satisfaction": 0.8
                },
                "optimization_suggestions": [
                    "Optimize node connections",
                    "Update model parameters",
                    "Improve prompt engineering"
                ],
                "estimated_improvement": {
                    "response_time": 1.8,
                    "accuracy": 0.92,
                    "user_satisfaction": 0.9
                }
            }
            
            return {
                "status": "success",
                "data": analysis
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Optimization failed: {str(e)}"
            }
    
    def create_optimized_chatflow(self, original_chatflow_id, optimization_params):
        """Create an optimized version of an existing chatflow"""
        try:
            # Get original chatflow
            original_result = self.get_chatflow(original_chatflow_id)
            if original_result["status"] != "success":
                return original_result
            
            original_chatflow = original_result["data"]
            
            # Create optimized version
            optimized_chatflow = original_chatflow.copy()
            optimized_chatflow["name"] = f"Optimized_{original_chatflow.get('name', 'Chatflow')}"
            
            # Apply optimizations (mock implementation)
            if "nodes" in optimized_chatflow:
                for node in optimized_chatflow["nodes"]:
                    if node.get("type") == "llm":
                        # Optimize LLM parameters
                        node["data"] = node.get("data", {})
                        node["data"]["temperature"] = optimization_params.get("temperature", 0.7)
                        node["data"]["maxTokens"] = optimization_params.get("maxTokens", 1000)
            
            # Create the optimized chatflow
            return self.create_chatflow(optimized_chatflow)
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create optimized chatflow: {str(e)}"
            }

