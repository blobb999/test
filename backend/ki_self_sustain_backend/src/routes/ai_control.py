from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import json
import os
import yaml
from datetime import datetime
from src.modules.enhanced_ai_manager import EnhancedAIManager
from src.modules.self_improvement_engine import SelfImprovementEngine
from src.modules.flowise_optimizer import FlowiseOptimizer
from src.modules.self_extending_services import SelfExtendingService
from src.modules.ethics_monitoring import EthicsMonitoringSystem
from src.modules.immutable_ethics import ImmutableEthicsFramework
from src.modules.immutable_ai_control import ImmutableAIController
from src.modules.fallback_strategies import FallbackManager

ai_control_bp = Blueprint('ai_control', __name__)

# Initialize core components
try:
    ai_manager = EnhancedAIManager()
    improvement_engine = SelfImprovementEngine()
    flowise_optimizer = FlowiseOptimizer()
    extending_service = SelfExtendingService()
    ethics_monitor = EthicsMonitoringSystem()
    ethics_framework = ImmutableEthicsFramework()
    ai_controller = ImmutableAIController()
    fallback_manager = FallbackManager()
except Exception as e:
    print(f"Warning: Failed to initialize some components: {e}")
    # Initialize with None to prevent crashes
    ai_manager = None
    improvement_engine = None
    flowise_optimizer = None
    extending_service = None
    ethics_monitor = None
    ethics_framework = None
    ai_controller = None
    fallback_manager = None

@ai_control_bp.route('/status', methods=['GET'])
@cross_origin()
def get_system_status():
    """Get overall system status"""
    try:
        status = {
            "timestamp": datetime.now().isoformat(),
            "system_health": "operational",
            "ethics_integrity": ethics_framework.verify_ethics_integrity(),
            "monitoring_status": ethics_monitor.get_monitoring_status(),
            "components": {
                "ai_manager": "active",
                "improvement_engine": "active",
                "flowise_optimizer": "active",
                "extending_service": "active",
                "ethics_monitor": "active"
            }
        }
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_control_bp.route('/ethics/principles', methods=['GET'])
@cross_origin()
def get_ethics_principles():
    """Get immutable ethics principles"""
    try:
        principles = ethics_framework.get_ethics_principles()
        safety_rules = ethics_framework.get_safety_rules()
        return jsonify({
            "principles": principles,
            "safety_rules": safety_rules,
            "immutable": True,
            "integrity_verified": ethics_framework.verify_ethics_integrity()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_control_bp.route('/config/security', methods=['GET'])
@cross_origin()
def get_security_config():
    """Get security configuration"""
    try:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'security_config.yaml')
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return jsonify(config)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_control_bp.route('/config/security', methods=['POST'])
@cross_origin()
def update_security_config():
    """Update security configuration"""
    try:
        new_config = request.json
        config_path = os.path.join(os.path.dirname(__file__), '..', 'security_config.yaml')
        
        # Validate configuration
        required_keys = ['security', 'fallback', 'safety']
        for key in required_keys:
            if key not in new_config:
                return jsonify({"error": f"Missing required key: {key}"}), 400
        
        with open(config_path, 'w') as f:
            yaml.dump(new_config, f, default_flow_style=False)
        
        return jsonify({"message": "Security configuration updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_control_bp.route('/improvement/analyze', methods=['POST'])
@cross_origin()
def analyze_performance():
    """Analyze system performance for improvement"""
    try:
        feedback_data = request.json
        analysis = improvement_engine.analyze_performance(feedback_data)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_control_bp.route('/improvement/plan', methods=['POST'])
@cross_origin()
def generate_improvement_plan():
    """Generate improvement plan based on analysis"""
    try:
        analysis_data = request.json
        plan = improvement_engine.generate_improvement_plan(analysis_data)
        return jsonify(plan)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_control_bp.route('/improvement/execute', methods=['POST'])
@cross_origin()
def execute_improvements():
    """Execute improvement plan"""
    try:
        plan_data = request.json
        
        # Validate against immutable controls
        ai_controller.validate_ai_action(plan_data)
        
        results = improvement_engine.execute_improvements(plan_data)
        evaluation = improvement_engine.evaluate_results(results)
        
        return jsonify({
            "results": results,
            "evaluation": evaluation
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_control_bp.route('/flowise/optimize', methods=['POST'])
@cross_origin()
def optimize_flowise():
    """Optimize Flowise flows"""
    try:
        flow_data = request.json
        flow_name = flow_data.get('flow_name', 'default_flow')
        
        performance = flowise_optimizer.analyze_flow_performance(flow_name)
        optimized = flowise_optimizer.optimize_flow(flow_name)
        
        return jsonify({
            "performance": performance,
            "optimized_flow": optimized
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_control_bp.route('/services/analyze', methods=['GET'])
@cross_origin()
def analyze_system_needs():
    """Analyze current system needs"""
    try:
        analysis = extending_service.analyze_system_needs()
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_control_bp.route('/services/create', methods=['POST'])
@cross_origin()
def create_new_service():
    """Create new service based on analysis"""
    try:
        service_data = request.json
        service_type = service_data.get('service_type', 'generic')
        
        # Validate against immutable controls
        ai_controller.validate_ai_action(service_data)
        
        service_path = extending_service.create_new_service(service_type)
        
        return jsonify({
            "message": "Service created successfully",
            "service_path": service_path,
            "service_type": service_type
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_control_bp.route('/flowise/map/create', methods=['POST'])
@cross_origin()
def create_flowise_map():
    """Create new Flowise map"""
    try:
        map_data = request.json
        purpose = map_data.get('purpose', 'general_purpose')
        
        map_path = extending_service.create_flowise_map(purpose)
        
        return jsonify({
            "message": "Flowise map created successfully",
            "map_path": map_path,
            "purpose": purpose
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_control_bp.route('/llm/communicate', methods=['POST'])
@cross_origin()
def communicate_with_llm():
    """Communicate with configurable LLM"""
    try:
        llm_data = request.json
        message = llm_data.get('message', '')
        llm_endpoint = llm_data.get('llm_endpoint', 'http://localhost:8000')
        
        # This would be implemented to actually communicate with the LLM
        # For now, return a mock response
        response = {
            "llm_response": f"Mock LLM response to: {message}",
            "timestamp": datetime.now().isoformat(),
            "endpoint": llm_endpoint
        }
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_control_bp.route('/logs', methods=['GET'])
@cross_origin()
def get_system_logs():
    """Get system logs"""
    try:
        # Mock log data - in real implementation, read from log files
        logs = [
            {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "message": "System initialized successfully",
                "component": "ai_manager"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "message": "Ethics monitoring active",
                "component": "ethics_monitor"
            }
        ]
        
        return jsonify({"logs": logs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@ai_control_bp.route('/auto-setup', methods=['POST'])
@cross_origin()
def auto_setup_ai():
    """Automatically setup AI system if not available"""
    try:
        if ai_manager is None:
            return jsonify({
                "status": "error",
                "message": "AI Manager not initialized"
            }), 500
        
        result = ai_manager.auto_setup_ai_if_needed()
        
        if result["status"] == "success":
            return jsonify(result), 200
        elif result["status"] == "warning":
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Auto-setup failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@ai_control_bp.route('/ai-status', methods=['GET'])
@cross_origin()
def get_ai_status():
    """Get detailed AI system status"""
    try:
        if ai_manager is None:
            return jsonify({
                "status": "error",
                "message": "AI Manager not initialized"
            }), 500
        
        status = ai_manager.get_ai_status()
        return jsonify(status), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to get AI status: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@ai_control_bp.route('/check-and-setup', methods=['POST'])
@cross_origin()
def check_and_setup_ai():
    """Check AI status and setup if needed"""
    try:
        if ai_manager is None:
            return jsonify({
                "status": "error",
                "message": "AI Manager not initialized"
            }), 500
        
        # First get current status
        status = ai_manager.get_ai_status()
        
        # If AI is not healthy, try auto-setup
        if status.get("overall_status") != "healthy":
            setup_result = ai_manager.auto_setup_ai_if_needed()
            
            return jsonify({
                "status": "setup_attempted",
                "initial_status": status,
                "setup_result": setup_result,
                "timestamp": datetime.now().isoformat()
            }), 200
        else:
            return jsonify({
                "status": "already_healthy",
                "ai_status": status,
                "timestamp": datetime.now().isoformat()
            }), 200
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Check and setup failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

