import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2, AlertTriangle, CheckCircle, Brain, Zap } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { ScrollArea } from './ui/scroll-area';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'system',
      content: 'KI Self Sustain System initialisiert. Ich bin bereit für Ihre Anweisungen zur Selbstverbesserung und Systemkontrolle.',
      timestamp: new Date(),
      status: 'success'
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [systemStatus, setSystemStatus] = useState('active');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date(),
      status: 'sent'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // First check if AI is available and auto-setup if needed
      const setupResponse = await fetch('http://localhost:5000/api/ai/check-and-setup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      const setupData = await setupResponse.json();
      
      // If setup was attempted, inform user
      if (setupData.status === 'setup_attempted') {
        const setupMessage = {
          id: Date.now() + 0.5,
          type: 'system',
          content: `AI-System wird automatisch eingerichtet... Status: ${setupData.setup_result?.status || 'In Bearbeitung'}`,
          timestamp: new Date(),
          status: setupData.setup_result?.status === 'success' ? 'success' : 'warning'
        };
        setMessages(prev => [...prev, setupMessage]);
      }

      // Determine the type of request based on content
      let endpoint = '/api/learning/llm-feedback';
      let requestData = {
        message: inputValue,
        type: 'user_interaction',
        timestamp: new Date().toISOString()
      };

      // Check for specific commands
      if (inputValue.toLowerCase().includes('improve') || inputValue.toLowerCase().includes('optimize')) {
        endpoint = '/api/learning/autonomous-improvement';
        requestData = {
          trigger: 'user_request',
          context: inputValue,
          timestamp: new Date().toISOString()
        };
      } else if (inputValue.toLowerCase().includes('status') || inputValue.toLowerCase().includes('health')) {
        endpoint = '/api/ai/status';
        requestData = {};
      } else if (inputValue.toLowerCase().includes('flowise') || inputValue.toLowerCase().includes('workflow')) {
        endpoint = '/api/flowise/chatflows';
        requestData = {};
      }

      const response = await fetch(`http://localhost:5000${endpoint}`, {
        method: endpoint.includes('status') || endpoint.includes('chatflows') ? 'GET' : 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: endpoint.includes('status') || endpoint.includes('chatflows') ? undefined : JSON.stringify(requestData)
      });

      const data = await response.json();

      let botResponse = {
        id: Date.now() + 1,
        type: 'bot',
        timestamp: new Date(),
        status: response.ok ? 'success' : 'error'
      };

      if (response.ok) {
        // Format response based on endpoint
        if (endpoint.includes('status')) {
          botResponse.content = `Systemstatus: ${data.status || 'Aktiv'}
Version: ${data.version || 'Unbekannt'}
Komponenten: ${data.components ? data.components.join(', ') : 'Alle aktiv'}
Letzte Aktivität: ${data.timestamp || 'Gerade eben'}`;
        } else if (endpoint.includes('chatflows')) {
          botResponse.content = `Flowise Status: ${data.length ? `${data.length} Chatflows gefunden` : 'Keine Chatflows verfügbar'}
${data.length ? 'Chatflows können über das Flowise-Panel verwaltet werden.' : 'Erstellen Sie neue Chatflows über das Flowise-Interface.'}`;
        } else if (endpoint.includes('autonomous-improvement')) {
          botResponse.content = `Selbstverbesserung ${data.status === 'success' ? 'erfolgreich' : 'fehlgeschlagen'}:
${data.status === 'success' ? 
  `Version: ${data.version || 'Aktualisiert'}
Verbesserungen: ${data.improvement_plan ? Object.keys(data.improvement_plan).length : 0} Schritte` :
  `Grund: ${data.message || data.error || 'Unbekannter Fehler'}`}`;
        } else {
          botResponse.content = `Feedback verarbeitet: ${data.status === 'success' ? 'Erfolgreich' : 'Fehler'}
${data.message || data.analysis?.analysis || 'Verarbeitung abgeschlossen'}`;
        }
      } else {
        // Check if it's the specific endpoint error
        if (data.message && data.message.includes('No valid chat completion endpoints found')) {
          botResponse.content = `KI-System nicht verfügbar. Automatische Einrichtung wird versucht...
Fehler: ${data.message}
Bitte warten Sie einen Moment und versuchen Sie es erneut.`;
        } else {
          botResponse.content = `Fehler: ${data.error || data.message || 'Unbekannter Fehler'}`;
        }
      }

      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: `Verbindungsfehler: ${error.message}. Überprüfen Sie, ob das Backend läuft.`,
        timestamp: new Date(),
        status: 'error'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const getMessageIcon = (type, status) => {
    if (type === 'user') return <User className="w-4 h-4" />;
    if (type === 'system') return <Brain className="w-4 h-4" />;
    if (status === 'error') return <AlertTriangle className="w-4 h-4" />;
    if (status === 'success') return <CheckCircle className="w-4 h-4" />;
    return <Bot className="w-4 h-4" />;
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'success': return 'text-green-600';
      case 'error': return 'text-red-600';
      case 'warning': return 'text-yellow-600';
      default: return 'text-blue-600';
    }
  };

  const quickActions = [
    { label: 'System Status', command: 'Zeige mir den aktuellen Systemstatus' },
    { label: 'Selbstverbesserung', command: 'Starte eine autonome Selbstverbesserung' },
    { label: 'Flowise Status', command: 'Überprüfe Flowise Workflows' },
    { label: 'Lernfortschritt', command: 'Zeige mir den aktuellen Lernfortschritt' }
  ];

  return (
    <Card className="h-full flex flex-col">
      <CardHeader className="pb-3">
        <CardTitle className="flex items-center gap-2">
          <Brain className="w-5 h-5" />
          KI Interaktions-Interface
          <Badge variant={systemStatus === 'active' ? 'default' : 'destructive'} className="ml-auto">
            {systemStatus === 'active' ? 'Aktiv' : 'Inaktiv'}
          </Badge>
        </CardTitle>
      </CardHeader>
      
      <CardContent className="flex-1 flex flex-col p-0">
        {/* Messages Area */}
        <ScrollArea className="flex-1 px-4">
          <div className="space-y-4 pb-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {message.type !== 'user' && (
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    message.type === 'system' ? 'bg-purple-100 text-purple-600' :
                    message.status === 'error' ? 'bg-red-100 text-red-600' :
                    'bg-blue-100 text-blue-600'
                  }`}>
                    {getMessageIcon(message.type, message.status)}
                  </div>
                )}
                
                <div className={`max-w-[80%] ${message.type === 'user' ? 'order-first' : ''}`}>
                  <div className={`rounded-lg p-3 ${
                    message.type === 'user' 
                      ? 'bg-blue-600 text-white' 
                      : message.status === 'error'
                      ? 'bg-red-50 border border-red-200'
                      : 'bg-gray-50 border border-gray-200'
                  }`}>
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  </div>
                  <div className="flex items-center gap-2 mt-1 px-1">
                    <span className="text-xs text-gray-500">
                      {message.timestamp.toLocaleTimeString()}
                    </span>
                    {message.status && (
                      <Badge variant="outline" className={`text-xs ${getStatusColor(message.status)}`}>
                        {message.status}
                      </Badge>
                    )}
                  </div>
                </div>

                {message.type === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </div>
            ))}
            
            {isLoading && (
              <div className="flex gap-3 justify-start">
                <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center">
                  <Loader2 className="w-4 h-4 animate-spin" />
                </div>
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-3">
                  <p className="text-sm text-gray-600">KI verarbeitet Ihre Anfrage...</p>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </ScrollArea>

        {/* Quick Actions */}
        <div className="px-4 py-2 border-t border-gray-200">
          <div className="flex flex-wrap gap-2 mb-3">
            {quickActions.map((action, index) => (
              <Button
                key={index}
                variant="outline"
                size="sm"
                onClick={() => setInputValue(action.command)}
                className="text-xs"
              >
                <Zap className="w-3 h-3 mr-1" />
                {action.label}
              </Button>
            ))}
          </div>
        </div>

        {/* Input Area */}
        <div className="px-4 pb-4">
          <div className="flex gap-2">
            <Input
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Geben Sie Ihre Anweisungen für das KI-System ein..."
              disabled={isLoading}
              className="flex-1"
            />
            <Button 
              onClick={handleSendMessage} 
              disabled={!inputValue.trim() || isLoading}
              size="icon"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
            </Button>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Verwenden Sie Befehle wie "improve", "status", "flowise" für spezifische Aktionen
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default ChatInterface;

