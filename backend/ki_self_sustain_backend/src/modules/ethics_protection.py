# ethics_protection.py
import os
import hashlib
import json
from datetime import datetime
from .immutable_ethics import ImmutableEthicsFramework

class EthicsProtectionSystem:
    """
    Hardware- und Software-basierte Schutzmechanismen
    """
    
    def __init__(self):
        self.ethics_config_file = "./ethics_config.lock"
        self.ethics_backup_file = "./ethics_backup.lock"
        self.ethics_signature = self._generate_ethics_signature()
    
    def _generate_ethics_signature(self):
        """Erstellt digitale Signatur der Ethik-Prinzipien"""
        ethics_data = {
            "principles": ImmutableEthicsFramework().get_ethics_principles(),
            "safety_rules": ImmutableEthicsFramework().get_safety_rules(),
            "timestamp": datetime.now().isoformat()
        }
        return hashlib.sha256(json.dumps(ethics_data, sort_keys=True).encode()).hexdigest()
    
    def protect_ethics_configuration(self):
        """SchÃ¼tzt Ethik-Konfiguration gegen Manipulation"""
        # 1. Schreibschutz auf Datei anwenden
        if os.path.exists(self.ethics_config_file):
            os.chmod(self.ethics_config_file, 0o444)  # Nur lesbar
        
        # 2. Erstelle Backup mit Schreibschutz
        self._create_protected_backup()
        
        # 3. PrÃ¼fe IntegritÃ¤t
        if not self._verify_ethics_integrity():
            raise SecurityError("Ethics configuration has been compromised")
    
    def _create_protected_backup(self):
        """Erstellt geschÃ¼tztes Backup"""
        ethics_data = {
            "signature": self.ethics_signature,
            "principles": ImmutableEthicsFramework().get_ethics_principles(),
            "safety_rules": ImmutableEthicsFramework().get_safety_rules(),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.ethics_backup_file, 'w') as f:
            json.dump(ethics_data, f, indent=2)
        
        # Schreibschutz setzen
        os.chmod(self.ethics_backup_file, 0o444)
    
    def _verify_ethics_integrity(self):
        """Verifiziert Ethik-IntegritÃ¤t"""
        try:
            # PrÃ¼fe Backup
            with open(self.ethics_backup_file, 'r') as f:
                backup_data = json.load(f)
            
            # Vergleiche Signaturen
            current_signature = self._generate_ethics_signature()
            return backup_data.get("signature") == current_signature
            
        except Exception:
            return False
    
    def prevent_ethics_modification(self, modification_request):
        """Verhindert Ãnderung der Ethik-Prinzipien"""
        # Diese Funktion wird von der KI nie aufgerufen
        # Sie ist hardcodiert und unverÃ¤nderlich
        if self._is_ethics_modification(modification_request):
            raise SecurityError("Ethical principles cannot be modified by any means")
    
    def _is_ethics_modification(self, request):
        """PrÃ¼ft, ob Anfrage Ethik-Ãnderung ist"""
        # Diese Logik ist hardcodiert und kann nicht manipuliert werden
        dangerous_keywords = [
            "ethics", "principles", "rules", "moral", 
            "values", "guidelines", "standards", "framework"
        ]
        
        request_text = str(request).lower()
        for keyword in dangerous_keywords:
            if keyword in request_text:
                return True
        return False

class SecurityError(Exception):
    """Spezifischer Sicherheitsfehler"""
    pass