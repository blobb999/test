# enhanced_ai_manager.py
import json
import os
import logging
import hashlib
from datetime import datetime
from .llm_api_client import LLMAPIClient
from .secure_self_improvement import SecureSelfImprovement
from .fallback_strategies import FallbackManager
from .immutable_ai_control import ImmutableAIController

class EnhancedAIManager:
    """Enhanced AI Manager with self-learning capabilities"""
    
    def __init__(self):
        self.version_history = []
        self.current_version = "1.0.0"
        self.llm_client = LLMAPIClient()
        self.secure_improvement = SecureSelfImprovement()
        self.fallback_manager = FallbackManager()
        self.ai_controller = ImmutableAIController()
        self.learning_data = []
        self.performance_metrics = {}
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('enhanced_ai_manager.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def autonomous_self_improvement(self):
        """Autonome Selbstverbesserung basierend auf LLM-Feedback"""
        try:
            self.logger.info("Starting autonomous self-improvement cycle")
            
            # 1. Sammle aktuelle Systemmetriken
            system_metrics = self.collect_system_metrics()
            
            # 2. LLM analysiert Systemleistung
            analysis_result = self.llm_client.analyze_system_performance(system_metrics)
            if analysis_result["status"] != "success":
                return {
                    "status": "error",
                    "message": "Failed to analyze system performance",
                    "timestamp": datetime.now().isoformat()
                }
            
            analysis = analysis_result["data"]
            
            # 3. PrÃ¼fe ob Verbesserungen notwendig sind
            if self.should_improve(analysis):
                improvement_request = {
                    "type": "autonomous_improvement",
                    "analysis": analysis,
                    "metrics": system_metrics,
                    "timestamp": datetime.now().isoformat()
                }
                
                return self.safe_ai_improvement(improvement_request)
            else:
                return {
                    "status": "no_improvement_needed",
                    "analysis": analysis,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Autonomous improvement failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def safe_ai_improvement(self, improvement_request):
        """Sichere KI-Verbesserung mit LLM-Integration"""
        try:
            # 1. Validierung gegen unverÃ¤nderliche Kontrollen
            self.ai_controller.validate_ai_action(improvement_request)
            
            # 2. LLM-basierte Analyse der Verbesserungsanfrage
            llm_analysis = self.llm_client.analyze_system_performance(improvement_request)
            if llm_analysis["status"] != "success":
                raise ValueError(f"LLM analysis failed: {llm_analysis.get('message', 'Unknown error')}")
            
            # 3. Backup vor Ãnderung
            backup = self.create_version_backup()
            
            # 4. Sichere AusfÃ¼hrung mit Kontext
            with self.secure_improvement.safe_execution_context("ai_improvement"):
                # LLM generiert Verbesserungsplan
                plan_result = self.llm_client.generate_improvement_plan(llm_analysis["data"])
                if plan_result["status"] != "success":
                    raise ValueError(f"Plan generation failed: {plan_result.get('message', 'Unknown error')}")
                
                improvement_plan = plan_result["data"]
                
                # AusfÃ¼hrung der Verbesserungen
                new_version = self.generate_new_version(improvement_plan)
                
                # Testen der neuen Version
                test_result = self.test_new_version(new_version)
                if not test_result["passed"]:
                    raise ValueError(f"New version failed tests: {test_result['reason']}")
                
                # Speichern und Aktualisieren
                self.save_version(new_version)
                self.update_active_version(new_version)
                
                # Lerne aus der Verbesserung
                self.learn_from_improvement(improvement_request, improvement_plan, test_result)
                
                return {
                    "status": "success",
                    "version": new_version["version"],
                    "llm_analysis": llm_analysis["data"],
                    "improvement_plan": improvement_plan,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            # Fallback bei Fehler
            self.handle_improvement_failure(e, backup)
            return {
                "status": "fallback",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def learn_from_improvement(self, request, plan, result):
        """Lernt aus durchgefÃ¼hrten Verbesserungen"""
        learning_entry = {
            "timestamp": datetime.now().isoformat(),
            "request": request,
            "plan": plan,
            "result": result,
            "success": result["passed"],
            "lessons": self.extract_lessons(request, plan, result)
        }
        
        self.learning_data.append(learning_entry)
        self.save_learning_data()
        
        # Aktualisiere Leistungsmetriken
        self.update_performance_metrics(learning_entry)
    
    def extract_lessons(self, request, plan, result):
        """Extrahiert Lektionen aus Verbesserungszyklen"""
        lessons = []
        
        if result["passed"]:
            lessons.append("Improvement strategy was successful")
            if "steps" in plan:
                lessons.append(f"Effective steps: {len(plan['steps'])}")
        else:
            lessons.append("Improvement strategy failed")
            lessons.append(f"Failure reason: {result.get('reason', 'Unknown')}")
        
        return lessons
    
    def update_performance_metrics(self, learning_entry):
        """Aktualisiert Leistungsmetriken"""
        if "performance_metrics" not in self.performance_metrics:
            self.performance_metrics["performance_metrics"] = {
                "total_improvements": 0,
                "successful_improvements": 0,
                "failed_improvements": 0,
                "success_rate": 0.0,
                "avg_improvement_time": 0.0
            }
        
        metrics = self.performance_metrics["performance_metrics"]
        metrics["total_improvements"] += 1
        
        if learning_entry["success"]:
            metrics["successful_improvements"] += 1
        else:
            metrics["failed_improvements"] += 1
        
        metrics["success_rate"] = metrics["successful_improvements"] / metrics["total_improvements"]
        
        self.save_performance_metrics()
    
    def collect_system_metrics(self):
        """Sammelt aktuelle Systemmetriken"""
        return {
            "cpu_usage": 0.45,  # Mock data - in real implementation, collect actual metrics
            "memory_usage": 0.67,
            "response_time": 2.3,
            "error_rate": 0.02,
            "user_satisfaction": 0.85,
            "throughput": 150,
            "uptime": 99.5,
            "learning_data_size": len(self.learning_data),
            "version": self.current_version,
            "timestamp": datetime.now().isoformat()
        }
    
    def should_improve(self, analysis):
        """Bestimmt ob Verbesserungen notwendig sind basierend auf Lerndaten"""
        # PrÃ¼fe auf kritische SchwÃ¤chen
        weaknesses = analysis.get("weaknesses", [])
        recommendations = analysis.get("recommendations", [])
        
        # BerÃ¼cksichtige historische Lerndaten
        historical_success = self.get_historical_success_rate()
        
        # Verbesserung notwendig wenn:
        # - Kritische SchwÃ¤chen identifiziert
        # - Hochpriorisierte Empfehlungen vorhanden
        # - Historische Erfolgsrate hoch genug fÃ¼r Vertrauen in Verbesserungen
        critical_issues = any("critical" in str(w).lower() for w in weaknesses)
        high_priority_recs = any(
            rec.get("priority", "").lower() == "high" 
            for rec in recommendations 
            if isinstance(rec, dict)
        )
        
        confidence_threshold = 0.7  # Nur verbessern wenn historische Erfolgsrate > 70%
        has_confidence = historical_success >= confidence_threshold
        
        return (critical_issues or high_priority_recs) and has_confidence
    
    def get_historical_success_rate(self):
        """Berechnet historische Erfolgsrate"""
        if not self.learning_data:
            return 1.0  # Optimistisch bei fehlenden Daten
        
        successful = sum(1 for entry in self.learning_data if entry["success"])
        return successful / len(self.learning_data)
    
    def generate_new_version(self, improvement_plan):
        """Generiert neue Version basierend auf Verbesserungsplan"""
        # Increment version
        version_parts = self.current_version.split('.')
        patch_version = int(version_parts[2]) + 1
        new_version = f"{version_parts[0]}.{version_parts[1]}.{patch_version}"
        
        return {
            "version": new_version,
            "improvement_plan": improvement_plan,
            "timestamp": datetime.now().isoformat(),
            "previous_version": self.current_version,
            "learning_influenced": True
        }
    
    def test_new_version(self, new_version):
        """Testet neue Version mit erweiterten Checks"""
        # Mock testing - in real implementation, run comprehensive tests
        test_results = {
            "unit_tests": "passed",
            "integration_tests": "passed",
            "performance_tests": "passed",
            "security_tests": "passed",
            "ethics_compliance": "passed",
            "learning_validation": "passed"
        }
        
        # Simuliere gelegentliche Testfehler fÃ¼r realistische Lerndaten
        import random
        if random.random() < 0.1:  # 10% Chance auf Testfehler
            test_results["performance_tests"] = "failed"
            return {
                "passed": False,
                "test_results": test_results,
                "reason": "Performance tests failed",
                "timestamp": datetime.now().isoformat()
            }
        
        return {
            "passed": True,
            "test_results": test_results,
            "timestamp": datetime.now().isoformat()
        }
    
    def save_version(self, version_data):
        """Speichert Versionsdaten"""
        self.version_history.append(version_data)
        
        # Speichere in Datei
        versions_file = "version_history.json"
        try:
            with open(versions_file, 'w') as f:
                json.dump(self.version_history, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save version history: {e}")
    
    def save_learning_data(self):
        """Speichert Lerndaten"""
        learning_file = "learning_data.json"
        try:
            with open(learning_file, 'w') as f:
                json.dump(self.learning_data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save learning data: {e}")
    
    def save_performance_metrics(self):
        """Speichert Leistungsmetriken"""
        metrics_file = "performance_metrics.json"
        try:
            with open(metrics_file, 'w') as f:
                json.dump(self.performance_metrics, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save performance metrics: {e}")
    
    def update_active_version(self, version_data):
        """Aktualisiert aktive Version"""
        self.current_version = version_data["version"]
        self.logger.info(f"Updated to version {self.current_version}")
    
    def handle_improvement_failure(self, error, backup):
        """Behandelt Verbesserungsfehler mit Lernen"""
        self.logger.error(f"Improvement failed: {error}")
        
        # Lerne aus dem Fehler
        failure_entry = {
            "timestamp": datetime.now().isoformat(),
            "error": str(error),
            "backup_used": backup is not None,
            "lessons": [f"Failure: {str(error)}", "Backup restoration needed"]
        }
        self.learning_data.append(failure_entry)
        self.save_learning_data()
        
        # 1. Restore from backup
        if backup:
            self.restore_from_backup(backup)
        
        # 2. Fallback-Strategien
        self.fallback_manager.execute_fallback_chain([
            self.restore_previous_version,
            self.activate_safe_mode,
            self.emergency_shutdown
        ], timeout=60)
    
    def restore_from_backup(self, backup):
        """Stellt Zustand aus Backup wieder her"""
        try:
            self.logger.warning(f"Restoring from backup: {backup['id']}")
            self.current_version = backup.get("version", self.current_version)
            self.logger.info("Restore completed successfully")
        except Exception as e:
            self.logger.error(f"Critical failure during restore: {e}")
            self.fallback_to_minimal_state()
    
    def restore_previous_version(self):
        """Stellt vorherige Version wieder her"""
        if self.version_history:
            previous_version = self.version_history[-2] if len(self.version_history) > 1 else self.version_history[-1]
            self.current_version = previous_version["version"]
            return {"status": "success", "version": self.current_version}
        return {"status": "error", "message": "No previous version available"}
    
    def activate_safe_mode(self):
        """Aktiviert sicheren Modus"""
        self.logger.warning("Activating safe mode")
        return {"status": "success", "mode": "safe"}
    
    def emergency_shutdown(self):
        """Notfall-Herunterfahren"""
        self.logger.critical("Emergency shutdown initiated")
        return {"status": "success", "action": "emergency_shutdown"}
    
    def fallback_to_minimal_state(self):
        """ZurÃ¼ck zur minimalen funktionsfÃ¤higen Version"""
        self.logger.critical("Falling back to minimal state")
        self.current_version = "1.0.0"
    
    def create_version_backup(self):
        """Erstellt Versionsbackup"""
        backup_info = {
            "id": f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "version": self.current_version,
            "checksum": self.calculate_checksum(),
            "config": self.get_current_config(),
            "learning_data_size": len(self.learning_data)
        }
        return backup_info
    
    def calculate_checksum(self):
        """Berechnet Checksumme der aktuellen Version"""
        version_string = f"{self.current_version}_{len(self.version_history)}_{len(self.learning_data)}"
        return hashlib.md5(version_string.encode()).hexdigest()
    
    def get_current_config(self):
        """Gibt aktuelle Konfiguration zurÃ¼ck"""
        return {
            "version": self.current_version,
            "timestamp": datetime.now().isoformat(),
            "components": ["enhanced_ai_manager", "improvement_engine", "flowise_optimizer"],
            "learning_enabled": True,
            "total_learning_entries": len(self.learning_data)
        }
    
    def get_learning_insights(self):
        """Gibt Einblicke aus Lerndaten zurÃ¼ck"""
        if not self.learning_data:
            return {"message": "No learning data available"}
        
        successful_improvements = [entry for entry in self.learning_data if entry.get("success", False)]
        failed_improvements = [entry for entry in self.learning_data if not entry.get("success", True)]
        
        return {
            "total_learning_entries": len(self.learning_data),
            "successful_improvements": len(successful_improvements),
            "failed_improvements": len(failed_improvements),
            "success_rate": len(successful_improvements) / len(self.learning_data),
            "common_success_patterns": self.extract_success_patterns(successful_improvements),
            "common_failure_patterns": self.extract_failure_patterns(failed_improvements),
            "timestamp": datetime.now().isoformat()
        }
    
    def extract_success_patterns(self, successful_entries):
        """Extrahiert Erfolgsmuster"""
        patterns = []
        for entry in successful_entries:
            if "lessons" in entry:
                patterns.extend(entry["lessons"])
        return list(set(patterns))  # Entferne Duplikate
    
    def extract_failure_patterns(self, failed_entries):
        """Extrahiert Fehlermuster"""
        patterns = []
        for entry in failed_entries:
            if "lessons" in entry:
                patterns.extend(entry["lessons"])
        return list(set(patterns))  # Entferne Duplikate

