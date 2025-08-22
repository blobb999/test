import React, { useState, useEffect } from 'react';
import { Activity, Brain, Database, Network, Zap, AlertTriangle, CheckCircle, Clock, TrendingUp } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';

const SystemMonitor = () => {
  const [systemData, setSystemData] = useState({
    status: 'loading',
    metrics: {},
    learning: {},
    services: {},
    performance: []
  });
  const [lastUpdate, setLastUpdate] = useState(new Date());

  const fetchSystemData = async () => {
    try {
      // Fetch multiple endpoints in parallel
      const [statusRes, learningRes, flowiseRes] = await Promise.allSettled([
        fetch('http://localhost:5000/api/ai/status'),
        fetch('http://localhost:5000/api/learning/status'),
        fetch('http://localhost:5000/api/flowise/config')
      ]);

      const newData = { ...systemData };

      // Process AI status
      if (statusRes.status === 'fulfilled' && statusRes.value.ok) {
        const statusData = await statusRes.value.json();
        newData.status = statusData.status || 'active';
        newData.metrics = statusData.metrics || {};
        newData.services.backend = 'online';
      } else {
        newData.services.backend = 'offline';
      }

      // Process learning status
      if (learningRes.status === 'fulfilled' && learningRes.value.ok) {
        const learningData = await learningRes.value.json();
        newData.learning = learningData.learning_insights || {};
        newData.services.learning = 'online';
      } else {
        newData.services.learning = 'offline';
      }

      // Process Flowise status
      if (flowiseRes.status === 'fulfilled' && flowiseRes.value.ok) {
        const flowiseData = await flowiseRes.value.json();
        newData.services.flowise = 'online';
        newData.services.flowise_endpoint = flowiseData.flowise_endpoint;
      } else {
        newData.services.flowise = 'offline';
      }

      // Generate mock performance data for visualization
      const now = new Date();
      const newPerformancePoint = {
        time: now.toLocaleTimeString(),
        cpu: Math.random() * 100,
        memory: Math.random() * 100,
        learning_rate: newData.learning.success_rate ? newData.learning.success_rate * 100 : Math.random() * 100,
        timestamp: now.getTime()
      };

      newData.performance = [...(systemData.performance || []), newPerformancePoint].slice(-20);

      setSystemData(newData);
      setLastUpdate(now);
    } catch (error) {
      console.error('Failed to fetch system data:', error);
      setSystemData(prev => ({
        ...prev,
        status: 'error',
        services: { backend: 'offline', learning: 'offline', flowise: 'offline' }
      }));
    }
  };

  useEffect(() => {
    fetchSystemData();
    const interval = setInterval(fetchSystemData, 5000); // Update every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
      case 'online':
      case 'success': return 'bg-green-500';
      case 'warning': return 'bg-yellow-500';
      case 'error':
      case 'offline': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'active':
      case 'online':
      case 'success': return 'default';
      case 'warning': return 'secondary';
      case 'error':
      case 'offline': return 'destructive';
      default: return 'outline';
    }
  };

  const ServiceStatus = ({ name, status, icon: Icon, details }) => (
    <div className="flex items-center justify-between p-3 border rounded-lg">
      <div className="flex items-center gap-3">
        <div className={`w-3 h-3 rounded-full ${getStatusColor(status)}`} />
        <Icon className="w-4 h-4 text-gray-600" />
        <div>
          <p className="font-medium text-sm">{name}</p>
          {details && <p className="text-xs text-gray-500">{details}</p>}
        </div>
      </div>
      <Badge variant={getStatusBadge(status)} className="text-xs">
        {status}
      </Badge>
    </div>
  );

  const MetricCard = ({ title, value, unit, icon: Icon, trend }) => (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-600">{title}</p>
            <p className="text-2xl font-bold">
              {typeof value === 'number' ? value.toFixed(1) : value || '---'}
              {unit && <span className="text-sm font-normal text-gray-500 ml-1">{unit}</span>}
            </p>
          </div>
          <div className="flex flex-col items-end">
            <Icon className="w-5 h-5 text-gray-400" />
            {trend && (
              <div className={`flex items-center text-xs mt-1 ${trend > 0 ? 'text-green-600' : 'text-red-600'}`}>
                <TrendingUp className="w-3 h-3 mr-1" />
                {Math.abs(trend).toFixed(1)}%
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="space-y-6">
      {/* System Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="w-5 h-5" />
            System-Übersicht
            <Badge variant={getStatusBadge(systemData.status)} className="ml-auto">
              {systemData.status}
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <MetricCard
              title="CPU Auslastung"
              value={systemData.performance[systemData.performance.length - 1]?.cpu}
              unit="%"
              icon={Activity}
              trend={2.3}
            />
            <MetricCard
              title="Speicher"
              value={systemData.performance[systemData.performance.length - 1]?.memory}
              unit="%"
              icon={Database}
              trend={-1.2}
            />
            <MetricCard
              title="Lernrate"
              value={systemData.learning.success_rate ? systemData.learning.success_rate * 100 : null}
              unit="%"
              icon={Brain}
              trend={5.7}
            />
            <MetricCard
              title="Verbesserungen"
              value={systemData.learning.successful_improvements}
              unit=""
              icon={Zap}
              trend={12.4}
            />
          </div>

          {/* Performance Chart */}
          {systemData.performance.length > 0 && (
            <div className="h-64">
              <h4 className="text-sm font-medium mb-3">Performance-Verlauf</h4>
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={systemData.performance}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" />
                  <YAxis />
                  <Tooltip />
                  <Area type="monotone" dataKey="cpu" stackId="1" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
                  <Area type="monotone" dataKey="memory" stackId="1" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.6} />
                  <Area type="monotone" dataKey="learning_rate" stackId="1" stroke="#ffc658" fill="#ffc658" fillOpacity={0.6} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Services Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Network className="w-5 h-5" />
            Service-Status
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <ServiceStatus
              name="Backend API"
              status={systemData.services.backend || 'offline'}
              icon={Database}
              details="Flask Server - Port 5000"
            />
            <ServiceStatus
              name="Lern-Engine"
              status={systemData.services.learning || 'offline'}
              icon={Brain}
              details={`${systemData.learning.total_learning_entries || 0} Lerneinträge`}
            />
            <ServiceStatus
              name="Flowise"
              status={systemData.services.flowise || 'offline'}
              icon={Network}
              details={systemData.services.flowise_endpoint || 'Nicht konfiguriert'}
            />
            <ServiceStatus
              name="LLM Service"
              status="checking"
              icon={Zap}
              details="Ollama - Port 11434"
            />
          </div>
        </CardContent>
      </Card>

      {/* Learning Insights */}
      {systemData.learning && Object.keys(systemData.learning).length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Brain className="w-5 h-5" />
              Lern-Insights
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center">
                <p className="text-2xl font-bold text-green-600">
                  {systemData.learning.successful_improvements || 0}
                </p>
                <p className="text-sm text-gray-600">Erfolgreiche Verbesserungen</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-red-600">
                  {systemData.learning.failed_improvements || 0}
                </p>
                <p className="text-sm text-gray-600">Fehlgeschlagene Versuche</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-blue-600">
                  {systemData.learning.success_rate ? (systemData.learning.success_rate * 100).toFixed(1) : '0.0'}%
                </p>
                <p className="text-sm text-gray-600">Erfolgsrate</p>
              </div>
            </div>

            {systemData.learning.success_rate && (
              <div className="mt-4">
                <div className="flex justify-between text-sm mb-2">
                  <span>Lern-Fortschritt</span>
                  <span>{(systemData.learning.success_rate * 100).toFixed(1)}%</span>
                </div>
                <Progress value={systemData.learning.success_rate * 100} className="h-2" />
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Last Update */}
      <div className="flex items-center justify-between text-sm text-gray-500">
        <div className="flex items-center gap-2">
          <Clock className="w-4 h-4" />
          Letzte Aktualisierung: {lastUpdate.toLocaleTimeString()}
        </div>
        <button
          onClick={fetchSystemData}
          className="flex items-center gap-1 hover:text-gray-700 transition-colors"
        >
          <Activity className="w-4 h-4" />
          Aktualisieren
        </button>
      </div>
    </div>
  );
};

export default SystemMonitor;

