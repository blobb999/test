import React, { useState, useEffect } from 'react';
import { 
  Workflow, Plus, Play, Pause, Settings, Trash2, Edit, 
  ExternalLink, RefreshCw, Zap, Brain, AlertCircle, CheckCircle 
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Label } from './ui/label';

const FlowiseManager = () => {
  const [chatflows, setChatflows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [flowiseConfig, setFlowiseConfig] = useState({
    flowise_endpoint: 'http://localhost:3000',
    llm_endpoint: 'http://localhost:11434',
    status: 'checking'
  });
  const [newChatflow, setNewChatflow] = useState({
    name: '',
    description: '',
    type: 'conversational'
  });
  const [testMessage, setTestMessage] = useState('');
  const [testResults, setTestResults] = useState({});

  const fetchFlowiseData = async () => {
    setLoading(true);
    try {
      // Fetch configuration
      const configRes = await fetch('http://localhost:5000/api/flowise/config');
      if (configRes.ok) {
        const configData = await configRes.json();
        setFlowiseConfig(configData);
      }

      // Fetch chatflows
      const chatflowsRes = await fetch('http://localhost:5000/api/flowise/chatflows');
      if (chatflowsRes.ok) {
        const chatflowsData = await chatflowsRes.json();
        setChatflows(chatflowsData.data || []);
      } else {
        setChatflows([]);
      }

      // Test connection
      const testRes = await fetch('http://localhost:5000/api/flowise/test-connection', {
        method: 'POST'
      });
      if (testRes.ok) {
        const testData = await testRes.json();
        setFlowiseConfig(prev => ({
          ...prev,
          status: testData.flowise.status === 'success' ? 'online' : 'offline',
          llm_status: testData.llm.status === 'success' ? 'online' : 'offline'
        }));
      }
    } catch (error) {
      console.error('Failed to fetch Flowise data:', error);
      setFlowiseConfig(prev => ({ ...prev, status: 'offline' }));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFlowiseData();
    const interval = setInterval(fetchFlowiseData, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const handleCreateChatflow = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/flowise/chatflows', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newChatflow.name,
          description: newChatflow.description,
          flowData: {
            nodes: [
              {
                id: 'llm-1',
                type: 'llm',
                position: { x: 100, y: 100 },
                data: {
                  label: 'LLM Node',
                  name: 'chatOpenAI',
                  inputs: {
                    modelName: 'gpt-3.5-turbo',
                    temperature: 0.7
                  }
                }
              }
            ],
            edges: []
          }
        })
      });

      if (response.ok) {
        setNewChatflow({ name: '', description: '', type: 'conversational' });
        fetchFlowiseData();
      }
    } catch (error) {
      console.error('Failed to create chatflow:', error);
    }
  };

  const handleTestChatflow = async (chatflowId) => {
    if (!testMessage.trim()) return;

    try {
      const response = await fetch(`http://localhost:5000/api/flowise/chatflows/${chatflowId}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: testMessage,
          session_id: `test_${Date.now()}`
        })
      });

      const result = await response.json();
      setTestResults(prev => ({
        ...prev,
        [chatflowId]: {
          status: response.ok ? 'success' : 'error',
          response: result.data || result.error || 'No response',
          timestamp: new Date().toLocaleTimeString()
        }
      }));
    } catch (error) {
      setTestResults(prev => ({
        ...prev,
        [chatflowId]: {
          status: 'error',
          response: error.message,
          timestamp: new Date().toLocaleTimeString()
        }
      }));
    }
  };

  const handleOptimizeChatflow = async (chatflowId) => {
    try {
      const response = await fetch(`http://localhost:5000/api/flowise/chatflows/${chatflowId}/optimize`, {
        method: 'POST'
      });

      if (response.ok) {
        const result = await response.json();
        // Show optimization results
        alert(`Optimierung abgeschlossen: ${JSON.stringify(result.optimization, null, 2)}`);
        fetchFlowiseData();
      }
    } catch (error) {
      console.error('Failed to optimize chatflow:', error);
    }
  };

  const handleAutoOptimize = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/flowise/auto-optimize', {
        method: 'POST'
      });

      if (response.ok) {
        const result = await response.json();
        alert(`Auto-Optimierung abgeschlossen: ${result.results.length} Chatflows verarbeitet`);
        fetchFlowiseData();
      }
    } catch (error) {
      console.error('Failed to auto-optimize:', error);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'online':
      case 'success': return 'text-green-600 bg-green-100';
      case 'offline':
      case 'error': return 'text-red-600 bg-red-100';
      default: return 'text-yellow-600 bg-yellow-100';
    }
  };

  const ChatflowCard = ({ chatflow }) => (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">{chatflow.name || `Chatflow ${chatflow.id}`}</CardTitle>
          <Badge variant="outline" className={getStatusColor(chatflow.status || 'active')}>
            {chatflow.status || 'Aktiv'}
          </Badge>
        </div>
        {chatflow.description && (
          <p className="text-sm text-gray-600">{chatflow.description}</p>
        )}
      </CardHeader>
      
      <CardContent>
        <div className="space-y-3">
          {/* Test Interface */}
          <div className="border rounded-lg p-3">
            <Label className="text-sm font-medium">Chatflow testen:</Label>
            <div className="flex gap-2 mt-2">
              <Input
                placeholder="Testnachricht eingeben..."
                value={testMessage}
                onChange={(e) => setTestMessage(e.target.value)}
                className="flex-1"
              />
              <Button 
                size="sm" 
                onClick={() => handleTestChatflow(chatflow.id)}
                disabled={!testMessage.trim()}
              >
                <Play className="w-4 h-4" />
              </Button>
            </div>
            
            {testResults[chatflow.id] && (
              <div className={`mt-2 p-2 rounded text-sm ${
                testResults[chatflow.id].status === 'success' 
                  ? 'bg-green-50 text-green-800' 
                  : 'bg-red-50 text-red-800'
              }`}>
                <div className="flex items-center gap-2 mb-1">
                  {testResults[chatflow.id].status === 'success' ? (
                    <CheckCircle className="w-4 h-4" />
                  ) : (
                    <AlertCircle className="w-4 h-4" />
                  )}
                  <span className="font-medium">
                    {testResults[chatflow.id].timestamp}
                  </span>
                </div>
                <p>{testResults[chatflow.id].response}</p>
              </div>
            )}
          </div>

          {/* Actions */}
          <div className="flex gap-2">
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => handleOptimizeChatflow(chatflow.id)}
            >
              <Zap className="w-4 h-4 mr-1" />
              Optimieren
            </Button>
            
            <Button variant="outline" size="sm">
              <Edit className="w-4 h-4 mr-1" />
              Bearbeiten
            </Button>
            
            <Button 
              variant="outline" 
              size="sm"
              onClick={() => window.open(`${flowiseConfig.flowise_endpoint}/chatflow/${chatflow.id}`, '_blank')}
            >
              <ExternalLink className="w-4 h-4 mr-1" />
              Öffnen
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <Card>
        <CardContent className="flex items-center justify-center h-64">
          <RefreshCw className="w-6 h-6 animate-spin mr-2" />
          Lade Flowise-Daten...
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Flowise Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Workflow className="w-5 h-5" />
            Flowise-Status
            <Badge variant={flowiseConfig.status === 'online' ? 'default' : 'destructive'} className="ml-auto">
              {flowiseConfig.status}
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label className="text-sm font-medium">Flowise Endpoint</Label>
              <p className="text-sm text-gray-600">{flowiseConfig.flowise_endpoint}</p>
              <Badge variant="outline" className={getStatusColor(flowiseConfig.status)}>
                {flowiseConfig.status}
              </Badge>
            </div>
            <div>
              <Label className="text-sm font-medium">LLM Endpoint</Label>
              <p className="text-sm text-gray-600">{flowiseConfig.llm_endpoint}</p>
              <Badge variant="outline" className={getStatusColor(flowiseConfig.llm_status || 'checking')}>
                {flowiseConfig.llm_status || 'Prüfung...'}
              </Badge>
            </div>
          </div>
          
          <div className="flex gap-2 mt-4">
            <Button variant="outline" onClick={fetchFlowiseData}>
              <RefreshCw className="w-4 h-4 mr-2" />
              Status aktualisieren
            </Button>
            <Button variant="outline" onClick={handleAutoOptimize}>
              <Brain className="w-4 h-4 mr-2" />
              Auto-Optimierung
            </Button>
            <Button 
              variant="outline"
              onClick={() => window.open(flowiseConfig.flowise_endpoint, '_blank')}
            >
              <ExternalLink className="w-4 h-4 mr-2" />
              Flowise öffnen
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Chatflows Management */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Workflow className="w-5 h-5" />
              Chatflows ({chatflows.length})
            </CardTitle>
            
            <Dialog>
              <DialogTrigger asChild>
                <Button>
                  <Plus className="w-4 h-4 mr-2" />
                  Neuer Chatflow
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Neuen Chatflow erstellen</DialogTitle>
                </DialogHeader>
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="name">Name</Label>
                    <Input
                      id="name"
                      value={newChatflow.name}
                      onChange={(e) => setNewChatflow(prev => ({ ...prev, name: e.target.value }))}
                      placeholder="Chatflow-Name"
                    />
                  </div>
                  <div>
                    <Label htmlFor="description">Beschreibung</Label>
                    <Textarea
                      id="description"
                      value={newChatflow.description}
                      onChange={(e) => setNewChatflow(prev => ({ ...prev, description: e.target.value }))}
                      placeholder="Beschreibung des Chatflows"
                    />
                  </div>
                  <Button onClick={handleCreateChatflow} className="w-full">
                    Chatflow erstellen
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>
        </CardHeader>
        
        <CardContent>
          {chatflows.length === 0 ? (
            <div className="text-center py-8">
              <Workflow className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Keine Chatflows gefunden</h3>
              <p className="text-gray-600 mb-4">
                Erstellen Sie Ihren ersten Chatflow oder überprüfen Sie die Flowise-Verbindung.
              </p>
              <Button onClick={fetchFlowiseData} variant="outline">
                <RefreshCw className="w-4 h-4 mr-2" />
                Neu laden
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {chatflows.map((chatflow) => (
                <ChatflowCard key={chatflow.id} chatflow={chatflow} />
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Schnellaktionen</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button variant="outline" className="h-20 flex-col">
              <Brain className="w-6 h-6 mb-2" />
              KI-Assistent erstellen
            </Button>
            <Button variant="outline" className="h-20 flex-col">
              <Zap className="w-6 h-6 mb-2" />
              Workflow optimieren
            </Button>
            <Button variant="outline" className="h-20 flex-col">
              <Settings className="w-6 h-6 mb-2" />
              Erweiterte Einstellungen
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default FlowiseManager;

