import os
import requests
import json
from datetime import datetime
import logging
from typing import List, Optional, Dict, Any


class LLMAPIClient:
    """Client zum Interagieren mit LLM-APIs (unterstützt Ollama und OpenAI-kompatible Endpunkte)

    Ziele:
    - Automatische Erkennung von Ollama (Standardport 11434)
    - Docker-Netzwerk-bewusste Fallback-URLs (llm_service, localhost, etc.)
    - Bevorzugt Ollama /api/chat, fällt bei Bedarf auf OpenAI /v1/chat/completions zurück
    - Einheitliches Rückgabeformat analog OpenAI: { choices: [ { message: { content } } ] }
    - Automatische Modellerkennung und Fallback auf verfügbare Modelle
    """

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        # Basis-URL aus Parametern oder Umgebungsvariablen bestimmen
        env_base = (
            base_url
            or os.getenv("LLM_API_BASE_URL")
            or os.getenv("OLLAMA_HOST")
            or os.getenv("OLLAMA_BASE_URL")
        )

        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.api_key = api_key
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})

        # Liste möglicher Base-URLs erstellen (Docker-bewusst)
        self.base_urls: List[str] = self._build_candidate_base_urls(env_base)
        
        # Cache für verfügbare Modelle
        self._available_models_cache = None
        self._cache_timestamp = None
        self._cache_ttl = 300  # 5 Minuten Cache

    def _build_candidate_base_urls(self, primary: Optional[str]) -> List[str]:
        candidates = []
        
        # Primäre URL falls angegeben
        if primary:
            candidates.append(primary)
        
        # Docker-Compose Service-Namen (höchste Priorität in Container-Umgebung)
        candidates.extend([
            "http://llm_service:11434",  # Service-Name aus docker-compose.yaml
            "http://ki_self_sustain_llm:11434",  # Container-Name
            "http://ollama:11434",  # Generischer Service-Name
        ])
        
        # Lokale Varianten (für lokale Entwicklung)
        candidates.extend([
            "http://localhost:11434",
            "http://127.0.0.1:11434",
        ])
        
        # Docker Desktop Host-Zugriff (Mac/Windows)
        candidates.extend([
            "http://host.docker.internal:11434",
        ])
        
        # Trimmen & deduplizieren
        seen = set()
        result = []
        for u in candidates:
            u = (u or "").strip().rstrip("/")
            if u and u not in seen:
                seen.add(u)
                result.append(u)
        return result

    def set_base_url(self, url: str):
        """Manuelles Überschreiben der Base-URL (setzt auch Kandidatenliste neu)."""
        self.base_urls = self._build_candidate_base_urls(url)
        # Cache invalidieren
        self._available_models_cache = None

    def set_api_key(self, api_key: Optional[str]):
        """API-Key setzen/löschen."""
        self.api_key = api_key
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
        elif "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]

    # -----------------------------
    # Hilfsfunktionen
    # -----------------------------
    def _is_ollama(self, base: str) -> bool:
        """Erkennen, ob unter base eine Ollama-API erreichbar ist."""
        try:
            r = self.session.get(f"{base}/api/version", timeout=5)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        try:
            r = self.session.get(f"{base}/api/tags", timeout=5)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        return False

    def _post_json(self, url: str, payload: Dict[str, Any], timeout: int = 60) -> Optional[requests.Response]:
        """POST-Request mit JSON-Payload. Längerer Timeout für LLM-Anfragen."""
        try:
            return self.session.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=timeout)
        except Exception as e:
            self.logger.debug(f"POST {url} failed: {e}")
            return None

    def _get(self, url: str, timeout: int = 10) -> Optional[requests.Response]:
        try:
            return self.session.get(url, timeout=timeout)
        except Exception as e:
            self.logger.debug(f"GET {url} failed: {e}")
            return None

    def _get_available_models(self) -> List[str]:
        """Holt verfügbare Modelle und cached sie."""
        now = datetime.now().timestamp()
        
        # Cache prüfen
        if (self._available_models_cache is not None and 
            self._cache_timestamp is not None and 
            now - self._cache_timestamp < self._cache_ttl):
            return self._available_models_cache
        
        models = []
        for base in self.base_urls:
            # Ollama-spezifisch
            r = self._get(f"{base}/api/tags")
            if r and r.status_code == 200:
                try:
                    data = r.json()
                    for model in data.get("models", []):
                        model_name = model.get("name", "")
                        if model_name:
                            models.append(model_name)
                    self.logger.info(f"Found {len(models)} models on {base}: {models}")
                    break  # Erfolgreich, keine weiteren URLs probieren
                except Exception as e:
                    self.logger.warning(f"Failed to parse Ollama models from {base}: {e}")
        
        # Cache aktualisieren
        self._available_models_cache = models
        self._cache_timestamp = now
        
        return models

    def _find_best_model(self, preferred_model: str) -> str:
        """Findet das beste verfügbare Modell basierend auf Präferenz."""
        available_models = self._get_available_models()
        
        if not available_models:
            self.logger.warning("No models available, using preferred model anyway")
            return preferred_model
        
        # Exakte Übereinstimmung
        if preferred_model in available_models:
            return preferred_model
        
        # Fallback-Reihenfolge für kleine, schnelle Modelle
        fallback_models = [
            "phi3:mini",
            "tinyllama",
            "tinyllama:latest", 
            "phi3:3.8b",
            "llama3.2:1b",
            "llama3.2:3b",
            "gemma2:2b",
            "qwen2:0.5b",
            "qwen2:1.5b"
        ]
        
        # Prüfe Fallback-Modelle
        for fallback in fallback_models:
            if fallback in available_models:
                self.logger.info(f"Using fallback model {fallback} instead of {preferred_model}")
                return fallback
        
        # Wenn kein kleines Modell verfügbar ist, nimm das erste verfügbare
        if available_models:
            selected = available_models[0]
            self.logger.info(f"Using first available model {selected} instead of {preferred_model}")
            return selected
        
        # Als letzter Ausweg das ursprünglich gewünschte Modell verwenden
        self.logger.warning(f"No suitable model found, using {preferred_model} anyway")
        return preferred_model

    # -----------------------------
    # Verbindungs- und Modellabfrage
    # -----------------------------
    def test_connection(self) -> Dict[str, Any]:
        """Verbindung testen: prüft mehrere Base-URLs und typische Endpunkte inkl. Ollama."""
        for base in self.base_urls:
            self.logger.info(f"Testing connection to {base}")
            # Bevorzugt Ollama-Checks
            for ep in ["/api/version", "/api/tags"]:
                r = self._get(f"{base}{ep}")
                if r and r.status_code == 200:
                    self.logger.info(f"Successfully connected to {base}{ep}")
                    return {"status": "success", "endpoint": ep, "base_url": base, "message": "Connection successful"}
            # Fallback auf generische Endpunkte
            for ep in ["/v1/models", "/api/v1/models", "/models", "/health", "/api/health"]:
                r = self._get(f"{base}{ep}")
                if r and r.status_code == 200:
                    self.logger.info(f"Successfully connected to {base}{ep}")
                    return {"status": "success", "endpoint": ep, "base_url": base, "message": "Connection successful"}
        
        self.logger.error(f"No valid endpoints found. Tried URLs: {self.base_urls}")
        return {"status": "error", "message": f"No valid endpoints found. Tried: {self.base_urls}"}

    def get_models(self) -> Dict[str, Any]:
        """Verfügbare Modelle abrufen: versucht Ollama /api/tags und OpenAI-kompatible Endpunkte."""
        for base in self.base_urls:
            # Ollama-spezifisch
            r = self._get(f"{base}/api/tags")
            if r and r.status_code == 200:
                try:
                    data = r.json()
                    models = [{
                        "id": m["name"],
                        "object": "model",
                        "created": datetime.now().timestamp(),
                        "owned_by": "ollama",
                        "permission": [],
                        "root": m["name"],
                        "parent": None,
                    } for m in data.get("models", [])]
                    return {"status": "success", "data": {"data": models}}
                except Exception as e:
                    self.logger.warning(f"Failed to parse Ollama models from {base}: {e}")

            # OpenAI-kompatibel
            for ep in ["/v1/models", "/api/v1/models", "/models"]:
                r = self._get(f"{base}{ep}")
                if r and r.status_code == 200:
                    try:
                        return {"status": "success", "data": r.json()}
                    except Exception as e:
                        self.logger.warning(f"Failed to parse OpenAI-compatible models from {base}{ep}: {e}")

        return {"status": "error", "message": "Could not retrieve models"}

    # -----------------------------
    # Chat Completion
    # -----------------------------
    def chat_completion(self, messages: List[Dict[str, str]], model: str = "phi3:mini", temperature: float = 0.7, max_tokens: int = 1000) -> Dict[str, Any]:
        """Sende Chat-Completion-Anfrage an LLM.

        Versucht zuerst Ollama /api/chat, dann OpenAI-kompatible Endpunkte.
        Gibt ein OpenAI-ähnliches Antwortformat zurück.
        """
        # Bestes verfügbares Modell finden
        actual_model = self._find_best_model(model)
        self.logger.info(f"Using model: {actual_model} (requested: {model})")
        
        for base in self.base_urls:
            self.logger.info(f"Trying chat completion with {base}")
            
            # 1. Versuch: Ollama /api/chat
            ollama_payload = {
                "model": actual_model,
                "messages": messages,
                "stream": False,
                "options": {"temperature": temperature, "num_predict": max_tokens},
            }
            r = self._post_json(f"{base}/api/chat", ollama_payload, timeout=120)
            if r and r.status_code == 200:
                try:
                    ollama_response = r.json()
                    if "message" in ollama_response:
                        self.logger.info(f"Successful chat completion from {base}")
                        return {
                            "status": "success",
                            "data": {
                                "choices": [
                                    {"message": {"content": ollama_response["message"]["content"]}}
                                ]
                            },
                        }
                    else:
                        self.logger.warning(f"Ollama response from {base} missing \"message\" field: {ollama_response}")
                except Exception as e:
                    self.logger.warning(f"Failed to parse Ollama chat response from {base}: {e}")
            elif r and r.status_code == 404:
                # Modell nicht gefunden, Cache invalidieren und erneut versuchen
                self.logger.warning(f"Model {actual_model} not found on {base}, invalidating cache")
                self._available_models_cache = None
                # Erneut bestes Modell finden
                actual_model = self._find_best_model(model)
                if actual_model != ollama_payload["model"]:
                    # Neues Modell probieren
                    ollama_payload["model"] = actual_model
                    r = self._post_json(f"{base}/api/chat", ollama_payload, timeout=120)
                    if r and r.status_code == 200:
                        try:
                            ollama_response = r.json()
                            if "message" in ollama_response:
                                self.logger.info(f"Successful chat completion from {base} (retry with {actual_model})")
                                return {
                                    "status": "success",
                                    "data": {
                                        "choices": [
                                            {"message": {"content": ollama_response["message"]["content"]}}
                                        ]
                                    },
                                }
                        except Exception as e:
                            self.logger.warning(f"Failed to parse Ollama chat response from {base} (retry): {e}")
            elif r:
                self.logger.warning(f"Ollama chat request to {base} failed with status {r.status_code}: {r.text}")
            else:
                self.logger.warning(f"Ollama chat request to {base} failed (no response)")

            # 2. Versuch: OpenAI-kompatible Endpunkte
            openai_payload = {
                "model": actual_model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            for ep in ["/v1/chat/completions", "/api/v1/chat/completions", "/chat/completions"]:
                try:
                    r = self._post_json(f"{base}{ep}", openai_payload, timeout=120)
                    if r and r.status_code == 200:
                        try:
                            self.logger.info(f"Successful OpenAI-compatible chat completion from {base}{ep}")
                            return {"status": "success", "data": r.json()}
                        except Exception as e:
                            self.logger.warning(f"Failed to parse OpenAI-compatible chat response from {base}{ep}: {e}")
                except Exception as e:
                    self.logger.warning(f"Request to {base}{ep} failed: {e}")
                    continue

        error_msg = f"No valid chat completion endpoints found. Tried model: {actual_model}, URLs: {self.base_urls}"
        self.logger.error(error_msg)
        return {"status": "error", "message": error_msg}

    def simple_completion(self, prompt: str, model: str = "phi3:mini", temperature: float = 0.7, max_tokens: int = 1000) -> Dict[str, Any]:
        """Sende einfache Text-Completion-Anfrage (konvertiert zu Chat-Format)."""
        messages = [{"role": "user", "content": prompt}]
        return self.chat_completion(messages, model, temperature, max_tokens)

    # -----------------------------
    # Zusätzliche Funktionen (unverändert)
    # -----------------------------
    def analyze_system_performance(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
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
                json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                    return {"status": "success", "data": analysis}
                else:
                    return {
                        "status": "success",
                        "data": {
                            "analysis": response_text,
                            "weaknesses": [],
                            "recommendations": [],
                        },
                    }
            except Exception:
                return {
                    "status": "success",
                    "data": {
                        "analysis": result["data"]["choices"][0]["message"]["content"],
                        "weaknesses": [],
                        "recommendations": [],
                    },
                }

        return result

    def generate_improvement_plan(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
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
                    "success_metric": "...",
                }}
            ],
            "risks": ["...", "..."],
            "expected_outcomes": ["...", "..."],
        }}
        """

        result = self.simple_completion(prompt, temperature=0.3)

        if result["status"] == "success":
            try:
                response_text = result["data"]["choices"][0]["message"]["content"]
                import re
                json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
                if json_match:
                    plan = json.loads(json_match.group())
                    return {"status": "success", "data": plan}
            except Exception:
                pass

            return {
                "status": "success",
                "data": {
                    "plan_name": "Generated Improvement Plan",
                    "steps": [],
                    "risks": [],
                    "expected_outcomes": [],
                    "raw_response": result["data"]["choices"][0]["message"]["content"],
                },
            }

        return result

    def generate_service_code(self, service_type: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
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
                    "timestamp": datetime.now().isoformat(),
                },
            }

        return result

    def optimize_flowise_configuration(self, current_config: Dict[str, Any]) -> Dict[str, Any]:
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
                json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
                if json_match:
                    optimized_config = json.loads(json_match.group())
                    return {"status": "success", "data": optimized_config}
            except Exception:
                pass

            return {
                "status": "success",
                "data": {
                    "optimized_config": current_config,
                    "suggestions": result["data"]["choices"][0]["message"]["content"],
                },
            }

        return result

