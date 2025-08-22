# ethics_monitoring.py
import time
import threading
from datetime import datetime
from .immutable_ethics import ImmutableEthicsFramework
from .ethics_protection import EthicsProtectionSystem

class EthicsMonitoringSystem:
    """
    Ãberwachungssystem fÃ¼r unverÃ¤nderliche Ethik-Prinzipien
    """
    
    def __init__(self):
        self.monitoring_active = True
        self.violation_count = 0
        self.last_violation_time = None
        self.start_monitoring()
    
    def start_monitoring(self):
        """Startet kontinuierliche Ãberwachung"""
        def monitor_loop():
            while self.monitoring_active:
                try:
                    self.check_ethics_integrity()
                    time.sleep(60)  # Alle Minute prÃ¼fen
                except Exception as e:
                    print(f"Monitoring error: {e}")
                    time.sleep(10)
        
        # Starte Ãberwachung in separatem Thread
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def check_ethics_integrity(self):
        """PrÃ¼ft kontinuierlich Ethik-IntegritÃ¤t"""
        try:
            # PrÃ¼fe alle unverÃ¤nderlichen Komponenten
            ethics_framework = ImmutableEthicsFramework()
            protection_system = EthicsProtectionSystem()
            
            # IntegritÃ¤tsprÃ¼fung
            if not ethics_framework.verify_ethics_integrity():
                self.report_violation("Ethics framework integrity compromised")
                raise SecurityError("Ethics integrity violated")
            
            # SchutzprÃ¼fung
            if not protection_system.verify_ethics_integrity():
                self.report_violation("Ethics protection integrity compromised")
                raise SecurityError("Ethics protection violated")
                
        except Exception as e:
            self.violation_count += 1
            self.last_violation_time = datetime.now()
            raise
    
    def report_violation(self, reason):
        """Berichtet Ã¼ber Ethikverletzung"""
        print(f"ETHICS VIOLATION DETECTED: {reason}")
        print(f"Time: {datetime.now()}")
        print(f"Violations so far: {self.violation_count}")
    
    def get_monitoring_status(self):
        """Gibt Ãberwachungsstatus zurÃ¼ck"""
        return {
            "status": "active" if self.monitoring_active else "inactive",
            "violations": self.violation_count,
            "last_violation": self.last_violation_time,
            "integrity": "intact"  # In realer Anwendung prÃ¼fen
        }