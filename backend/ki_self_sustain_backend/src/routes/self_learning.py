from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import json
import os
from datetime import datetime
from src.modules.enhanced_ai_manager import EnhancedAIManager
from src.modules.llm_api_client import LLMAPIClient

self_learning_bp = Blueprint('self_learning', __name__)

# Initialize enhanced AI manager
enhanced_ai_manager = EnhancedAIManager()
llm_client = LLMAPIClient(base_url="http://localhost:11434")

@self_learning_bp.route('/status', methods=['GET'])
@cross_origin()
def get_learning_status():
    """Get current self-learning system status"""
    try:
        learning_insights = enhanced_ai_manager.get_learning_insights()
        system_metrics = enhanced_ai_manager.collect_system_metrics()
        
        return jsonify({
            "status": "active",
            "current_version": enhanced_ai_manager.current_version,
            "learning_insights": learning_insights,
            "system_metrics": system_metrics,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@self_learning_bp.route('/autonomous-improvement', methods=['POST'])
@cross_origin()
def trigger_autonomous_improvement():
    """Trigger autonomous self-improvement cycle"""
    try:
        result = enhanced_ai_manager.autonomous_self_improvement()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@self_learning_bp.route('/manual-improvement', methods=['POST'])
@cross_origin()
def trigger_manual_improvement():
    """Trigger manual improvement with user-provided data"""
    try:
        improvement_data = request.json
        
        improvement_request = {
            "type": "manual_improvement",
            "user_data": improvement_data,
            "timestamp": datetime.now().isoformat()
        }
        
        result = enhanced_ai_manager.safe_ai_improvement(improvement_request)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@self_learning_bp.route('/learning-data', methods=['GET'])
@cross_origin()
def get_learning_data():
    """Get historical learning data"""
    try:
        learning_insights = enhanced_ai_manager.get_learning_insights()
        return jsonify(learning_insights)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@self_learning_bp.route('/performance-metrics', methods=['GET'])
@cross_origin()
def get_performance_metrics():
    """Get performance metrics"""
    try:
        metrics = enhanced_ai_manager.performance_metrics
        system_metrics = enhanced_ai_manager.collect_system_metrics()
        
        return jsonify({
            "performance_metrics": metrics,
            "current_system_metrics": system_metrics,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@self_learning_bp.route('/version-history', methods=['GET'])
@cross_origin()
def get_version_history():
    """Get version history"""
    try:
        return jsonify({
            "current_version": enhanced_ai_manager.current_version,
            "version_history": enhanced_ai_manager.version_history,
            "total_versions": len(enhanced_ai_manager.version_history),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@self_learning_bp.route('/llm-feedback', methods=['POST'])
@cross_origin()
def process_llm_feedback():
    """Process feedback from LLM for learning"""
    try:
        feedback_data = request.json
        
        # Use LLM to analyze the feedback
        analysis_result = llm_client.analyze_system_performance(feedback_data)
        
        if analysis_result["status"] == "success":
            # Create learning entry from feedback
            learning_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": "llm_feedback",
                "feedback": feedback_data,
                "analysis": analysis_result["data"],
                "processed": True
            }
            
            enhanced_ai_manager.learning_data.append(learning_entry)
            enhanced_ai_manager.save_learning_data()
            
            return jsonify({
                "status": "success",
                "message": "Feedback processed and learned from",
                "analysis": analysis_result["data"],
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to analyze feedback",
                "error": analysis_result.get("message", "Unknown error")
            }), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@self_learning_bp.route('/simulate-learning', methods=['POST'])
@cross_origin()
def simulate_learning_cycle():
    """Simulate a complete learning cycle for testing"""
    try:
        simulation_data = request.json
        cycles = simulation_data.get('cycles', 1)
        
        results = []
        
        for i in range(cycles):
            # Simulate different scenarios
            scenarios = [
                {
                    "type": "performance_improvement",
                    "metrics": {
                        "response_time": 2.5 - (i * 0.1),
                        "accuracy": 0.85 + (i * 0.02),
                        "user_satisfaction": 0.8 + (i * 0.03)
                    }
                },
                {
                    "type": "error_reduction",
                    "metrics": {
                        "error_rate": 0.05 - (i * 0.005),
                        "uptime": 99.0 + (i * 0.1),
                        "stability": 0.9 + (i * 0.01)
                    }
                }
            ]
            
            scenario = scenarios[i % len(scenarios)]
            
            # Process scenario through learning system
            improvement_request = {
                "type": "simulation",
                "scenario": scenario,
                "cycle": i + 1,
                "timestamp": datetime.now().isoformat()
            }
            
            result = enhanced_ai_manager.safe_ai_improvement(improvement_request)
            results.append({
                "cycle": i + 1,
                "scenario": scenario["type"],
                "result": result
            })
        
        return jsonify({
            "status": "success",
            "message": f"Completed {cycles} learning cycles",
            "results": results,
            "final_insights": enhanced_ai_manager.get_learning_insights(),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@self_learning_bp.route('/reset-learning', methods=['POST'])
@cross_origin()
def reset_learning_data():
    """Reset learning data (for testing purposes)"""
    try:
        confirmation = request.json.get('confirm', False)
        
        if not confirmation:
            return jsonify({
                "status": "error",
                "message": "Confirmation required to reset learning data"
            }), 400
        
        # Backup current learning data
        backup_data = {
            "timestamp": datetime.now().isoformat(),
            "learning_data": enhanced_ai_manager.learning_data.copy(),
            "performance_metrics": enhanced_ai_manager.performance_metrics.copy(),
            "version_history": enhanced_ai_manager.version_history.copy()
        }
        
        # Save backup
        backup_file = f"learning_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"Failed to create backup: {str(e)}"
            }), 500
        
        # Reset learning data
        enhanced_ai_manager.learning_data = []
        enhanced_ai_manager.performance_metrics = {}
        enhanced_ai_manager.version_history = []
        enhanced_ai_manager.current_version = "1.0.0"
        
        # Save reset state
        enhanced_ai_manager.save_learning_data()
        enhanced_ai_manager.save_performance_metrics()
        
        return jsonify({
            "status": "success",
            "message": "Learning data reset successfully",
            "backup_file": backup_file,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@self_learning_bp.route('/export-learning', methods=['GET'])
@cross_origin()
def export_learning_data():
    """Export learning data for analysis"""
    try:
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "current_version": enhanced_ai_manager.current_version,
            "learning_data": enhanced_ai_manager.learning_data,
            "performance_metrics": enhanced_ai_manager.performance_metrics,
            "version_history": enhanced_ai_manager.version_history,
            "learning_insights": enhanced_ai_manager.get_learning_insights(),
            "system_metrics": enhanced_ai_manager.collect_system_metrics()
        }
        
        return jsonify(export_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@self_learning_bp.route('/learning-recommendations', methods=['GET'])
@cross_origin()
def get_learning_recommendations():
    """Get AI-generated recommendations based on learning data"""
    try:
        learning_insights = enhanced_ai_manager.get_learning_insights()
        system_metrics = enhanced_ai_manager.collect_system_metrics()
        
        # Use LLM to generate recommendations
        recommendation_request = {
            "learning_insights": learning_insights,
            "system_metrics": system_metrics,
            "request_type": "learning_recommendations"
        }
        
        recommendations_result = llm_client.analyze_system_performance(recommendation_request)
        
        if recommendations_result["status"] == "success":
            return jsonify({
                "status": "success",
                "recommendations": recommendations_result["data"],
                "based_on": {
                    "learning_insights": learning_insights,
                    "system_metrics": system_metrics
                },
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to generate recommendations",
                "error": recommendations_result.get("message", "Unknown error")
            }), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

