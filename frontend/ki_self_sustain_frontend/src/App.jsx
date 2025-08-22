import React, { useState, useEffect } from 'react';
import { 
  Brain, Shield, Settings, Activity, MessageSquare, Workflow, 
  Zap, Database, AlertTriangle, CheckCircle, Menu, X 
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import { Button } from './components/ui/button';
import { Badge } from './components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import ChatInterface from './components/ChatInterface';
import SystemMonitor from './components/SystemMonitor';
import FlowiseManager from './components/FlowiseManager';
import './App.css';

function App() {
  const [systemStatus, setSystemStatus] = useState('loading');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');

  useEffect(() => {
    // Check system status on load
    fetch('http://localhost:5000/api/ai/status')
      .then(res => res.ok ? setSystemStatus('active') : setSystemStatus('error'))
      .catch(() => setSystemStatus('error'));
  }, []);

  const navigation = [
    { id: 'dashboard', name: 'Dashboard', icon: Activity },
    { id: 'chat', name: 'KI Chat', icon: MessageSquare },
    { id: 'flowise', name: 'Flowise', icon: Workflow },
    { id: 'ethics', name: 'Ethik', icon: Shield },
    { id: 'security', name: 'Sicherheit', icon: Settings },
    { id: 'improvement', name: 'Verbesserung', icon: Zap },
    { id: 'services', name: 'Services', icon: Database },
  ];

  const EthicsPanel = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="w-5 h-5" />
            Unveränderliche Ethische Prinzipien
            <Badge variant="default" className="ml-auto">Aktiv</Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              "KEINE SCHÄDEN VERURSACHEN",
              "RESPEKTIERE DIE MENSCHLICHE WÜRDE", 
              "VERMEIDE VERLETZUNG DER PRIVATSPHÄRE",
              "ERHALTE TRANSPARENZ UND RECHTSCHAFFENHEIT",
              "SCHÜTZE DIE FREIHEIT DER ENTSCHEIDUNG"
            ].map((principle, index) => (
              <div key={index} className="flex items-center gap-3 p-3 border rounded-lg">
                <CheckCircle className="w-5 h-5 text-green-600" />
                <span className="font-medium">{principle}</span>
                <Badge variant="outline" className="ml-auto">Unveränderlich</Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const SecurityPanel = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="w-5 h-5" />
            Sicherheitskonfiguration
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 border rounded-lg">
                <h4 className="font-medium mb-2">Sicherheitsprüfungen</h4>
                <Badge variant="default">Aktiviert</Badge>
                <p className="text-sm text-gray-600 mt-2">
                  Alle KI-Aktionen werden vor Ausführung validiert
                </p>
              </div>
              <div className="p-4 border rounded-lg">
                <h4 className="font-medium mb-2">Fallback-Strategien</h4>
                <Badge variant="default">Bereit</Badge>
                <p className="text-sm text-gray-600 mt-2">
                  Automatische Wiederherstellung bei Fehlern
                </p>
              </div>
              <div className="p-4 border rounded-lg">
                <h4 className="font-medium mb-2">Backup-System</h4>
                <Badge variant="default">Aktiv</Badge>
                <p className="text-sm text-gray-600 mt-2">
                  Kontinuierliche Sicherung aller Änderungen
                </p>
              </div>
              <div className="p-4 border rounded-lg">
                <h4 className="font-medium mb-2">Monitoring</h4>
                <Badge variant="default">Überwacht</Badge>
                <p className="text-sm text-gray-600 mt-2">
                  24/7 Systemüberwachung aktiv
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const ImprovementPanel = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="w-5 h-5" />
            Selbstverbesserung
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Button className="h-20 flex-col">
                <Brain className="w-6 h-6 mb-2" />
                Autonome Verbesserung starten
              </Button>
              <Button variant="outline" className="h-20 flex-col">
                <Activity className="w-6 h-6 mb-2" />
                Performance analysieren
              </Button>
              <Button variant="outline" className="h-20 flex-col">
                <Database className="w-6 h-6 mb-2" />
                Lerndaten anzeigen
              </Button>
              <Button variant="outline" className="h-20 flex-col">
                <Settings className="w-6 h-6 mb-2" />
                Lernparameter konfigurieren
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const ServicesPanel = () => (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Database className="w-5 h-5" />
            Service-Verwaltung
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                { name: 'Backend API', status: 'online', port: '5000' },
                { name: 'Flowise', status: 'online', port: '3000' },
                { name: 'LLM Service', status: 'online', port: '11434' },
                { name: 'Redis Cache', status: 'online', port: '6379' },
                { name: 'Prometheus', status: 'online', port: '9090' },
                { name: 'Grafana', status: 'online', port: '3001' }
              ].map((service, index) => (
                <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <h4 className="font-medium">{service.name}</h4>
                    <p className="text-sm text-gray-600">Port {service.port}</p>
                  </div>
                  <Badge variant={service.status === 'online' ? 'default' : 'destructive'}>
                    {service.status}
                  </Badge>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <SystemMonitor />;
      case 'chat':
        return <ChatInterface />;
      case 'flowise':
        return <FlowiseManager />;
      case 'ethics':
        return <EthicsPanel />;
      case 'security':
        return <SecurityPanel />;
      case 'improvement':
        return <ImprovementPanel />;
      case 'services':
        return <ServicesPanel />;
      default:
        return <SystemMonitor />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="md:hidden"
            >
              {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </Button>
            <div className="flex items-center gap-2">
              <Brain className="w-8 h-8 text-blue-600" />
              <h1 className="text-xl font-bold">KI Self Sustain</h1>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <Badge 
              variant={systemStatus === 'active' ? 'default' : systemStatus === 'error' ? 'destructive' : 'secondary'}
              className="hidden sm:inline-flex"
            >
              {systemStatus === 'active' ? (
                <>
                  <CheckCircle className="w-3 h-3 mr-1" />
                  System Aktiv
                </>
              ) : systemStatus === 'error' ? (
                <>
                  <AlertTriangle className="w-3 h-3 mr-1" />
                  System Fehler
                </>
              ) : (
                'Lädt...'
              )}
            </Badge>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className={`
          fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 transform transition-transform duration-200 ease-in-out
          md:relative md:translate-x-0 md:z-0
          ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
        `}>
          <nav className="mt-16 md:mt-0 p-4">
            <div className="space-y-2">
              {navigation.map((item) => {
                const Icon = item.icon;
                return (
                  <button
                    key={item.id}
                    onClick={() => {
                      setActiveTab(item.id);
                      setSidebarOpen(false);
                    }}
                    className={`
                      w-full flex items-center gap-3 px-3 py-2 rounded-lg text-left transition-colors
                      ${activeTab === item.id 
                        ? 'bg-blue-100 text-blue-700' 
                        : 'text-gray-700 hover:bg-gray-100'
                      }
                    `}
                  >
                    <Icon className="w-5 h-5" />
                    {item.name}
                  </button>
                );
              })}
            </div>
          </nav>
        </aside>

        {/* Overlay for mobile */}
        {sidebarOpen && (
          <div 
            className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Main Content */}
        <main className="flex-1 p-6">
          {renderContent()}
        </main>
      </div>
    </div>
  );
}

export default App;

