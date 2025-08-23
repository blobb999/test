from flask import Blueprint, request, jsonify
import json
import os
import logging
from datetime import datetime

initialization_bp = Blueprint('initialization', __name__)

@initialization_bp.route('/initialize', methods=['POST'])
def initialize_system():
    """Initialize the KI Self Sustain system with default configurations"""
    try:
        # Create necessary directories
        directories = [
            'data/learning',
            'data/backups',
            'data/logs',
            'data/metrics',
            'flowise_data/chatflows',
            'llm_models'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        # Initialize learning database
        learning_data = {
            "learning_entries": [],
            "successful_improvements": 0,
            "failed_improvements": 0,
            "total_learning_entries": 0,
            "success_rate": 0.0,
            "last_improvement": None,
            "learning_insights": {
                "common_patterns": [],
                "optimization_areas": [],
                "performance_trends": []
            }
        }
        
        with open('data/learning/learning_database.json', 'w') as f:
            json.dump(learning_data, f, indent=2)
        
        # Initialize system metrics
        metrics_data = {
            "system_health": "excellent",
            "uptime": "0 minutes",
            "last_check": datetime.now().isoformat(),
            "performance_metrics": {
                "cpu_usage": 0.0,
                "memory_usage": 0.0,
                "response_time": 0.0,
                "throughput": 0.0
            },
            "component_status": {
                "backend": "active",
                "frontend": "active",
                "flowise": "checking",
                "llm_service": "checking",
                "database": "active"
            }
        }
        
        with open('data/metrics/system_metrics.json', 'w') as f:
            json.dump(metrics_data, f, indent=2)
        
        # Initialize configuration
        config_data = {
            "system": {
                "name": "KI Self Sustain",
                "version": "1.0.0",
                "initialized": datetime.now().isoformat(),
                "environment": "development"
            },
            "flowise": {
                "endpoint": "http://localhost:3000",
                "api_key": None,
                "auto_optimize": True,
                "check_interval": 300
            },
            "llm": {
                "endpoint": "http://localhost:11434",
                "model": "llama3",
                "temperature": 0.7,
                "max_tokens": 1000
            },
            "learning": {
                "auto_improvement": True,
                "max_improvements_per_hour": 5,
                "safety_checks": True,
                "backup_before_changes": True
            },
            "security": {
                "enable_safety_checks": True,
                "max_execution_time": 30,
                "alert_threshold": 0.8,
                "monitoring_enabled": True
            }
        }
        
        with open('data/config.json', 'w') as f:
            json.dump(config_data, f, indent=2)
        
        # Create initial log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": "INFO",
            "component": "initialization",
            "message": "KI Self Sustain system successfully initialized",
            "details": {
                "directories_created": len(directories),
                "config_files_created": 3,
                "status": "success"
            }
        }
        
        with open('data/logs/system.log', 'w') as f:
            json.dump([log_entry], f, indent=2)
        
        # Load example chatflows if available
        example_chatflows_path = 'flowise_data/example_chatflows.json'
        if os.path.exists(example_chatflows_path):
            with open(example_chatflows_path, 'r') as f:
                example_chatflows = json.load(f)
            
            # Save to chatflows directory
            for chatflow in example_chatflows:
                chatflow_file = f"flowise_data/chatflows/{chatflow['id']}.json"
                with open(chatflow_file, 'w') as f:
                    json.dump(chatflow, f, indent=2)
        
        return jsonify({
            "status": "success",
            "message": "System successfully initialized",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "directories": directories,
                "config_files": ["learning_database.json", "system_metrics.json", "config.json"],
                "log_files": ["system.log"],
                "example_chatflows": len(example_chatflows) if 'example_chatflows' in locals() else 0
            }
        })
        
    except Exception as e:
        logging.error(f"System initialization failed: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"System initialization failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@initialization_bp.route('/status', methods=['GET'])
def get_initialization_status():
    """Check if the system is properly initialized"""
    try:
        required_files = [
            'data/learning/learning_database.json',
            'data/metrics/system_metrics.json',
            'data/config.json',
            'data/logs/system.log'
        ]
        
        required_directories = [
            'data/learning',
            'data/backups',
            'data/logs',
            'data/metrics',
            'flowise_data/chatflows',
            'llm_models'
        ]
        
        missing_files = [f for f in required_files if not os.path.exists(f)]
        missing_directories = [d for d in required_directories if not os.path.exists(d)]
        
        is_initialized = len(missing_files) == 0 and len(missing_directories) == 0
        
        # Check configuration
        config_valid = False
        if os.path.exists('data/config.json'):
            try:
                with open('data/config.json', 'r') as f:
                    config = json.load(f)
                config_valid = 'system' in config and 'initialized' in config['system']
            except:
                pass
        
        return jsonify({
            "initialized": is_initialized,
            "config_valid": config_valid,
            "missing_files": missing_files,
            "missing_directories": missing_directories,
            "timestamp": datetime.now().isoformat(),
            "ready_for_operation": is_initialized and config_valid
        })
        
    except Exception as e:
        logging.error(f"Failed to check initialization status: {str(e)}")
        return jsonify({
            "initialized": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@initialization_bp.route('/reset', methods=['POST'])
def reset_system():
    """Reset the system to initial state (use with caution)"""
    try:
        # This is a dangerous operation - require confirmation
        confirmation = request.json.get('confirmation', '')
        if confirmation != 'RESET_CONFIRMED':
            return jsonify({
                "status": "error",
                "message": "Reset requires confirmation. Send 'RESET_CONFIRMED' in request body."
            }), 400
        
        # Create backup before reset
        backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = f"data/backups/reset_backup_{backup_timestamp}"
        os.makedirs(backup_dir, exist_ok=True)
        
        # Backup existing data
        import shutil
        if os.path.exists('data/learning'):
            shutil.copytree('data/learning', f"{backup_dir}/learning")
        if os.path.exists('data/metrics'):
            shutil.copytree('data/metrics', f"{backup_dir}/metrics")
        if os.path.exists('data/config.json'):
            shutil.copy2('data/config.json', f"{backup_dir}/config.json")
        
        # Remove existing data
        import glob
        for pattern in ['data/learning/*', 'data/metrics/*', 'data/logs/*']:
            for file in glob.glob(pattern):
                if os.path.isfile(file):
                    os.remove(file)
        
        # Re-initialize
        init_response = initialize_system()
        
        if init_response[1] == 200:  # Success
            return jsonify({
                "status": "success",
                "message": "System successfully reset and re-initialized",
                "backup_location": backup_dir,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Reset completed but re-initialization failed",
                "backup_location": backup_dir,
                "timestamp": datetime.now().isoformat()
            }), 500
            
    except Exception as e:
        logging.error(f"System reset failed: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"System reset failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@initialization_bp.route('/health', methods=['GET'])
def health_check():
    """Comprehensive health check of all system components"""
    try:
        health_status = {
            "overall": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {}
        }
        
        # Check file system
        try:
            test_file = 'data/.health_check'
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            health_status["components"]["filesystem"] = "healthy"
        except:
            health_status["components"]["filesystem"] = "unhealthy"
            health_status["overall"] = "degraded"
        
        # Check configuration
        try:
            if os.path.exists('data/config.json'):
                with open('data/config.json', 'r') as f:
                    config = json.load(f)
                health_status["components"]["configuration"] = "healthy"
            else:
                health_status["components"]["configuration"] = "missing"
                health_status["overall"] = "degraded"
        except:
            health_status["components"]["configuration"] = "corrupted"
            health_status["overall"] = "degraded"
        
        # Check learning system
        try:
            if os.path.exists('data/learning/learning_database.json'):
                with open('data/learning/learning_database.json', 'r') as f:
                    learning_data = json.load(f)
                health_status["components"]["learning_system"] = "healthy"
            else:
                health_status["components"]["learning_system"] = "missing"
                health_status["overall"] = "degraded"
        except:
            health_status["components"]["learning_system"] = "corrupted"
            health_status["overall"] = "degraded"
        
        # Check metrics system
        try:
            if os.path.exists('data/metrics/system_metrics.json'):
                with open('data/metrics/system_metrics.json', 'r') as f:
                    metrics_data = json.load(f)
                health_status["components"]["metrics_system"] = "healthy"
            else:
                health_status["components"]["metrics_system"] = "missing"
                health_status["overall"] = "degraded"
        except:
            health_status["components"]["metrics_system"] = "corrupted"
            health_status["overall"] = "degraded"
        
        return jsonify(health_status)
        
    except Exception as e:
        logging.error(f"Health check failed: {str(e)}")
        return jsonify({
            "overall": "critical",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

