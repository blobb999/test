from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import json
import os
from datetime import datetime
from src.modules.flowise_api_client import FlowiseAPIClient
from src.modules.llm_api_client import LLMAPIClient

flowise_control_bp = Blueprint('flowise_control', __name__)

# Initialize clients with default endpoints
flowise_client = FlowiseAPIClient()
llm_client = LLMAPIClient()

@flowise_control_bp.route('/config', methods=['GET'])
@cross_origin()
def get_flowise_config():
    """Get current Flowise configuration"""
    try:
        return jsonify({
            "flowise_endpoint": flowise_client.base_url,
            "llm_endpoint": llm_client.base_url,
            "status": "active"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flowise_control_bp.route('/config', methods=['POST'])
@cross_origin()
def update_flowise_config():
    """Update Flowise and LLM endpoints"""
    try:
        config = request.json
        
        if 'flowise_endpoint' in config:
            flowise_client.set_base_url(config['flowise_endpoint'])
        
        if 'llm_endpoint' in config:
            llm_client.set_base_url(config['llm_endpoint'])
        
        if 'llm_api_key' in config:
            llm_client.set_api_key(config['llm_api_key'])
        
        return jsonify({
            "message": "Configuration updated successfully",
            "flowise_endpoint": flowise_client.base_url,
            "llm_endpoint": llm_client.base_url
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flowise_control_bp.route('/test-connection', methods=['POST'])
@cross_origin()
def test_connections():
    """Test connections to Flowise and LLM APIs"""
    try:
        flowise_test = flowise_client.test_connection()
        llm_test = llm_client.test_connection()
        
        return jsonify({
            "flowise": flowise_test,
            "llm": llm_test,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flowise_control_bp.route('/chatflows', methods=['GET'])
@cross_origin()
def get_chatflows():
    """Get all chatflows from Flowise"""
    try:
        result = flowise_client.get_chatflows()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flowise_control_bp.route('/chatflows/<chatflow_id>', methods=['GET'])
@cross_origin()
def get_chatflow(chatflow_id):
    """Get specific chatflow by ID"""
    try:
        result = flowise_client.get_chatflow(chatflow_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flowise_control_bp.route('/chatflows', methods=['POST'])
@cross_origin()
def create_chatflow():
    """Create new chatflow"""
    try:
        chatflow_data = request.json
        result = flowise_client.create_chatflow(chatflow_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flowise_control_bp.route('/chatflows/<chatflow_id>', methods=['PUT'])
@cross_origin()
def update_chatflow(chatflow_id):
    """Update existing chatflow"""
    try:
        chatflow_data = request.json
        result = flowise_client.update_chatflow(chatflow_id, chatflow_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flowise_control_bp.route('/chatflows/<chatflow_id>', methods=['DELETE'])
@cross_origin()
def delete_chatflow(chatflow_id):
    """Delete chatflow"""
    try:
        result = flowise_client.delete_chatflow(chatflow_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flowise_control_bp.route('/chatflows/<chatflow_id>/predict', methods=['POST'])
@cross_origin()
def predict_chatflow(chatflow_id):
    """Send message to chatflow and get prediction"""
    try:
        data = request.json
        message = data.get('message', '')
        session_id = data.get('session_id')
        
        result = flowise_client.predict_chatflow(chatflow_id, message, session_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flowise_control_bp.route('/chatflows/<chatflow_id>/stats', methods=['GET'])
@cross_origin()
def get_chatflow_stats(chatflow_id):
    """Get chatflow statistics"""
    try:
        result = flowise_client.get_chatflow_stats(chatflow_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flowise_control_bp.route('/chatflows/<chatflow_id>/optimize', methods=['POST'])
@cross_origin()
def optimize_chatflow(chatflow_id):
    """Analyze and optimize chatflow performance"""
    try:
        # Get current chatflow
        chatflow_result = flowise_client.get_chatflow(chatflow_id)
        if chatflow_result["status"] != "success":
            return jsonify(chatflow_result), 400
        
        # Use LLM to analyze and optimize
        optimization_result = llm_client.optimize_flowise_configuration(
            chatflow_result["data"]
        )
        
        if optimization_result["status"] == "success":
            # Get performance analysis from Flowise client
            performance_result = flowise_client.optimize_chatflow_performance(chatflow_id)
            
            return jsonify({
                "status": "success",
                "optimization": optimization_result["data"],
                "performance_analysis": performance_result.get("data", {}),
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify(optimization_result), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flowise_control_bp.route('/chatflows/<chatflow_id>/create-optimized', methods=['POST'])
@cross_origin()
def create_optimized_chatflow(chatflow_id):
    """Create optimized version of existing chatflow"""
    try:
        optimization_params = request.json
        
        result = flowise_client.create_optimized_chatflow(
            chatflow_id, 
            optimization_params
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flowise_control_bp.route('/llm/models', methods=['GET'])
@cross_origin()
def get_llm_models():
    """Get available LLM models"""
    try:
        result = llm_client.get_models()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flowise_control_bp.route('/llm/chat', methods=['POST'])
@cross_origin()
def llm_chat():
    """Send chat message to LLM"""
    try:
        data = request.json
        messages = data.get('messages', [])
        model = data.get('model', 'gpt-3.5-turbo')
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 1000)
        
        result = llm_client.chat_completion(
            messages, model, temperature, max_tokens
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flowise_control_bp.route('/llm/analyze-performance', methods=['POST'])
@cross_origin()
def llm_analyze_performance():
    """Use LLM to analyze system performance"""
    try:
        performance_data = request.json
        
        result = llm_client.analyze_system_performance(performance_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flowise_control_bp.route('/llm/generate-improvement-plan', methods=['POST'])
@cross_origin()
def llm_generate_improvement_plan():
    """Use LLM to generate improvement plan"""
    try:
        analysis_data = request.json
        
        result = llm_client.generate_improvement_plan(analysis_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flowise_control_bp.route('/llm/generate-service', methods=['POST'])
@cross_origin()
def llm_generate_service():
    """Use LLM to generate service code"""
    try:
        data = request.json
        service_type = data.get('service_type', 'generic')
        requirements = data.get('requirements', {})
        
        result = llm_client.generate_service_code(service_type, requirements)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@flowise_control_bp.route('/auto-optimize', methods=['POST'])
@cross_origin()
def auto_optimize_system():
    """Automatically optimize the entire system using AI"""
    try:
        # Get all chatflows
        chatflows_result = flowise_client.get_chatflows()
        if chatflows_result["status"] != "success":
            return jsonify(chatflows_result), 400
        
        chatflows = chatflows_result["data"]
        optimization_results = []
        
        # Optimize each chatflow
        for chatflow in chatflows:
            chatflow_id = chatflow.get("id")
            if chatflow_id:
                try:
                    # Get performance stats
                    stats_result = flowise_client.get_chatflow_stats(chatflow_id)
                    
                    # Use LLM to analyze performance
                    if stats_result["status"] == "success":
                        analysis_result = llm_client.analyze_system_performance(
                            stats_result["data"]
                        )
                        
                        if analysis_result["status"] == "success":
                            # Generate improvement plan
                            plan_result = llm_client.generate_improvement_plan(
                                analysis_result["data"]
                            )
                            
                            optimization_results.append({
                                "chatflow_id": chatflow_id,
                                "chatflow_name": chatflow.get("name", "Unknown"),
                                "analysis": analysis_result["data"],
                                "improvement_plan": plan_result.get("data", {}),
                                "status": "optimized"
                            })
                        else:
                            optimization_results.append({
                                "chatflow_id": chatflow_id,
                                "status": "analysis_failed",
                                "error": analysis_result.get("message", "Unknown error")
                            })
                    else:
                        optimization_results.append({
                            "chatflow_id": chatflow_id,
                            "status": "stats_failed",
                            "error": stats_result.get("message", "Unknown error")
                        })
                        
                except Exception as e:
                    optimization_results.append({
                        "chatflow_id": chatflow_id,
                        "status": "error",
                        "error": str(e)
                    })
        
        return jsonify({
            "status": "success",
            "message": "Auto-optimization completed",
            "results": optimization_results,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

