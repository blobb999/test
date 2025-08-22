import subprocess
import requests
import json
import time
import logging
import os
import platform
from pathlib import Path

class OllamaInstaller:
    """Automatic Ollama installation and model setup"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ollama_url = "http://localhost:11434"
        self.system = platform.system().lower()
        
    def check_ollama_installed(self):
        """Check if Ollama is installed and running"""
        try:
            # Check if ollama command exists
            result = subprocess.run(['which', 'ollama'], capture_output=True, text=True)
            if result.returncode != 0:
                return False
                
            # Check if Ollama service is running
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def install_ollama(self):
        """Install Ollama on the system"""
        try:
            self.logger.info("Installing Ollama...")
            
            if self.system == "linux":
                # Download and install Ollama for Linux
                install_cmd = "curl -fsSL https://ollama.ai/install.sh | sh"
                result = subprocess.run(install_cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode != 0:
                    self.logger.error(f"Ollama installation failed: {result.stderr}")
                    return False
                    
                # Start Ollama service
                subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(10)  # Wait for service to start
                
            elif self.system == "darwin":  # macOS
                # For macOS, we'll try to install via Homebrew
                try:
                    subprocess.run(['brew', 'install', 'ollama'], check=True)
                    subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    time.sleep(10)
                except subprocess.CalledProcessError:
                    self.logger.error("Failed to install Ollama via Homebrew")
                    return False
                    
            else:
                self.logger.error(f"Unsupported system: {self.system}")
                return False
                
            # Verify installation
            return self.check_ollama_installed()
            
        except Exception as e:
            self.logger.error(f"Ollama installation failed: {str(e)}")
            return False
    
    def pull_model(self, model_name="llama3.2"):
        """Pull a specific model"""
        try:
            self.logger.info(f"Pulling model: {model_name}")
            
            # Use ollama pull command
            result = subprocess.run(['ollama', 'pull', model_name], 
                                  capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                self.logger.info(f"Successfully pulled model: {model_name}")
                return True
            else:
                self.logger.error(f"Failed to pull model {model_name}: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"Timeout while pulling model: {model_name}")
            return False
        except Exception as e:
            self.logger.error(f"Error pulling model {model_name}: {str(e)}")
            return False
    
    def get_available_models(self):
        """Get list of available models"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except:
            return []
    
    def test_model(self, model_name="llama3.2"):
        """Test if a model is working"""
        try:
            test_payload = {
                "model": model_name,
                "prompt": "Hello, how are you?",
                "stream": False
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", 
                                   json=test_payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return 'response' in data and len(data['response']) > 0
            return False
            
        except Exception as e:
            self.logger.error(f"Model test failed: {str(e)}")
            return False
    
    def setup_ollama_complete(self):
        """Complete Ollama setup process"""
        try:
            self.logger.info("Starting complete Ollama setup...")
            
            # Step 1: Check if already installed
            if self.check_ollama_installed():
                self.logger.info("Ollama is already installed and running")
                
                # Check if we have any models
                models = self.get_available_models()
                if models:
                    self.logger.info(f"Found existing models: {models}")
                    # Test the first available model
                    if self.test_model(models[0]):
                        return {
                            "status": "success",
                            "message": "Ollama is already set up and working",
                            "models": models
                        }
                
                # If no working models, continue to install one
                self.logger.info("No working models found, installing default model...")
            else:
                # Step 2: Install Ollama
                self.logger.info("Ollama not found, installing...")
                if not self.install_ollama():
                    return {
                        "status": "error",
                        "message": "Failed to install Ollama"
                    }
                
                # Wait a bit more for service to be ready
                time.sleep(5)
            
            # Step 3: Pull default model
            default_models = ["llama3.2", "llama3", "phi3", "gemma2"]
            model_installed = False
            
            for model in default_models:
                self.logger.info(f"Attempting to install model: {model}")
                if self.pull_model(model):
                    if self.test_model(model):
                        model_installed = True
                        installed_model = model
                        break
                    else:
                        self.logger.warning(f"Model {model} pulled but not working properly")
                else:
                    self.logger.warning(f"Failed to pull model: {model}")
            
            if not model_installed:
                return {
                    "status": "error",
                    "message": "Failed to install any working model"
                }
            
            # Step 4: Final verification
            final_models = self.get_available_models()
            
            return {
                "status": "success",
                "message": "Ollama setup completed successfully",
                "models": final_models,
                "default_model": installed_model,
                "ollama_url": self.ollama_url
            }
            
        except Exception as e:
            self.logger.error(f"Complete Ollama setup failed: {str(e)}")
            return {
                "status": "error",
                "message": f"Setup failed: {str(e)}"
            }
    
    def check_system_requirements(self):
        """Check if system meets requirements for Ollama"""
        try:
            import psutil
            
            # Check available memory (Ollama needs at least 2GB for testing)
            memory = psutil.virtual_memory()
            available_gb = memory.available / (1024**3)
            
            # Check disk space (need at least 5GB for models)
            disk = psutil.disk_usage('/')
            free_gb = disk.free / (1024**3)
            
            requirements = {
                "memory_available_gb": round(available_gb, 2),
                "disk_free_gb": round(free_gb, 2),
                "memory_sufficient": available_gb >= 2,
                "disk_sufficient": free_gb >= 5,
                "system": self.system,
                "meets_requirements": available_gb >= 2 and free_gb >= 5
            }
            
            return requirements
            
        except ImportError:
            # psutil not available, assume requirements are met
            return {
                "memory_available_gb": "unknown",
                "disk_free_gb": "unknown", 
                "memory_sufficient": True,
                "disk_sufficient": True,
                "system": self.system,
                "meets_requirements": True
            }
        except Exception as e:
            self.logger.error(f"Failed to check system requirements: {str(e)}")
            return {
                "meets_requirements": False,
                "error": str(e)
            }
    
    def create_systemd_service(self):
        """Create systemd service for Ollama (Linux only)"""
        if self.system != "linux":
            return False
            
        try:
            service_content = """[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Environment="OLLAMA_HOST=0.0.0.0"

[Install]
WantedBy=default.target
"""
            
            # Write service file
            service_path = "/etc/systemd/system/ollama.service"
            with open(service_path, 'w') as f:
                f.write(service_content)
            
            # Create ollama user
            subprocess.run(['useradd', '-r', '-s', '/bin/false', '-m', '-d', '/usr/share/ollama', 'ollama'], 
                         capture_output=True)
            
            # Enable and start service
            subprocess.run(['systemctl', 'daemon-reload'], check=True)
            subprocess.run(['systemctl', 'enable', 'ollama'], check=True)
            subprocess.run(['systemctl', 'start', 'ollama'], check=True)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create systemd service: {str(e)}")
            return False

