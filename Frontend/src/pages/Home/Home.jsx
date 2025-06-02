import { Factory, Zap, Globe, Upload, FileText, Table, Image, File, TrendingUp, Leaf } from 'lucide-react';
import CardBody from '../../Components/CardBody/CardBody';
import Header from '../../Components/Header/Header'

import Logomarca from "../../assets/img/Logomarca.png"

import { useState, useEffect } from 'react';

const Home = () => {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [dashboardData, setDashboardData] = useState(null);
  const [uploadStatus, setUploadStatus] = useState([]);

  const API_BASE_URL = '/api/carbon';

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/dashboard/`);
      if (response.ok) {
        const data = await response.json();
        setDashboardData(data);
      }
    } catch (error) {
      console.error('Erro ao carregar dados do dashboard:', error);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
  };

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    handleFiles(files);
  };

  const handleFiles = async (files) => {
    if (files.length === 0) return;

    setUploading(true);
    
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await fetch(`${API_BASE_URL}/upload/`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        
        // Atualizar status dos uploads
        setUploadStatus(prev => [...prev, ...result.documents.map(doc => ({
          ...doc,
          timestamp: new Date().toLocaleTimeString()
        }))]);

        // Mostrar mensagem de sucesso
        alert(result.message);
        
        // Recarregar dados do dashboard após alguns segundos
        setTimeout(fetchDashboardData, 3000);
        
      } else {
        const error = await response.json();
        alert(`Erro no upload: ${error.error || 'Erro desconhecido'}`);
      }
    } catch (error) {
      console.error('Erro no upload:', error);
      alert('Erro de conexão com o servidor');
    } finally {
      setUploading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'COMPLETED':
        return <CheckCircle className="text-green-500" size={16} />;
      case 'PROCESSING':
        return <Clock className="text-blue-500" size={16} />;
      case 'FAILED':
        return <AlertCircle className="text-red-500" size={16} />;
      default:
        return <Clock className="text-gray-500" size={16} />;
    }
  };

  const getStatusText = (status) => {
    const statusMap = {
      'PENDING': 'Pendente',
      'PROCESSING': 'Processando',
      'COMPLETED': 'Concluído',
      'FAILED': 'Falhou'
    };
    return statusMap[status] || status;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center space-x-3">
            <Header title="Gestão de Pegada de Carbono" subtitle="Faça upload de documentos para análise e cálculo de emissões"></Header>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <CardBody
            icon={Factory}
            title="Escopo 1"
            value={dashboardData?.scopes?.find(s => s.scope_number === 1)?.co2_equivalent || "735.0"}
            unit="toneladas CO₂e"
            bgColor="bg-gradient-to-br from-green-600 to-green-700"
            progress={dashboardData?.scopes?.find(s => s.scope_number === 1)?.progress_percentage || 100}
            description="Emissões Diretas"
            subdescription="Fontes que são de propriedade ou controladas pela organização."
            items={[
              "Combustão Estacionária",
              "Combustão Móvel", 
              "Emissões Fugitivas",
              "Processos Industriais"
            ]}
          />

          <CardBody
            icon={Zap}
            title="Escopo 2"
            value={dashboardData?.scopes?.find(s => s.scope_number === 2)?.co2_equivalent || "625.0"}
            unit="toneladas CO₂e"
            bgColor="bg-gradient-to-br from-blue-600 to-blue-700"
            progress={dashboardData?.scopes?.find(s => s.scope_number === 2)?.progress_percentage || 100}
            description="Emissões Indiretas"
            subdescription="Geração de eletricidade, vapor, aquecimento e refrigeração adquiridos."
            items={[
              "Eletricidade Adquirida",
              "Vapor Adquirido",
              "Refrigeração Adquirida", 
              "Aquecimento Adquirido"
            ]}
          />

          <CardBody
            icon={Globe}
            title="Escopo 3"
            value={dashboardData?.scopes?.find(s => s.scope_number === 3)?.co2_equivalent || "1.285,0"}
            unit="toneladas CO₂e"
            bgColor="bg-gradient-to-br from-purple-600 to-purple-700"
            progress={dashboardData?.scopes?.find(s => s.scope_number === 3)?.progress_percentage || 92}
            description="Outras Emissões Indiretas"
            subdescription="Ocorrências na cadeia de valor da empresa (upstream e downstream)."
            items={[
              "Bens e Serviços Adquiridos",
              "Transporte e Distribuição",
              "Viagens de Negócios"
            ]}
            pendingItem="Uso de Produtos Vendidos"
          />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="lg:col-span-2 bg-white rounded-2xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">Resumo de Emissões</h2>
              <div className="flex items-center space-x-2 text-green-600">
                <TrendingUp size={16} />
                <span className="text-sm font-medium">97% Completo</span>
              </div>
            </div>
            <div className="mb-8">
              <p className="text-sm font-medium text-gray-700 mb-2">PROGRESSO TOTAL</p>
              <div className="w-full h-4 bg-gray-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-green-500 to-green-600 rounded-full transition-all duration-700"
                  style={{ width: "97%" }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">97% dos dados coletados</p>
            </div>

            {/* Scope Distribution */}
            <div className="space-y-4">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Distribuição por Escopo</h3>
              
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-4 h-4 bg-green-500 rounded"></div>
                    <span className="text-sm font-medium text-gray-700">Escopo 1</span>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="w-32 bg-gray-200 rounded-full h-2">
                      <div className="bg-green-500 h-2 rounded-full" style={{ width: "27.8%" }}></div>
                    </div>
                    <span className="text-sm font-medium text-gray-900 w-12">27.8%</span>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-4 h-4 bg-blue-500 rounded"></div>
                    <span className="text-sm font-medium text-gray-700">Escopo 2</span>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="w-32 bg-gray-200 rounded-full h-2">
                      <div className="bg-blue-500 h-2 rounded-full" style={{ width: "23.6%" }}></div>
                    </div>
                    <span className="text-sm font-medium text-gray-900 w-12">23.6%</span>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-4 h-4 bg-purple-500 rounded"></div>
                    <span className="text-sm font-medium text-gray-700">Escopo 3</span>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="w-32 bg-gray-200 rounded-full h-2">
                      <div className="bg-purple-500 h-2 rounded-full" style={{ width: "48.6%" }}></div>
                    </div>
                    <span className="text-sm font-medium text-gray-900 w-12">48.6%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Total Emissions */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Emissões Totais</h2>
            
            <div className="text-center mb-6">
              <div className="text-4xl font-bold text-gray-900 mb-2">
                {dashboardData?.total_emissions?.toFixed(1) || "2.645,0"}
              </div>
              <div className="text-gray-600 text-lg">tCO₂e</div>
            </div>

            <div className="space-y-3 mb-6">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Escopo 1:</span>
                <span className="text-sm font-medium">
                  {dashboardData?.scopes?.find(s => s.scope_number === 1)?.co2_equivalent || "735.0"} tCO₂e
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Escopo 2:</span>
                <span className="text-sm font-medium">
                  {dashboardData?.scopes?.find(s => s.scope_number === 2)?.co2_equivalent || "625.0"} tCO₂e
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Escopo 3:</span>
                <span className="text-sm font-medium">
                  {dashboardData?.scopes?.find(s => s.scope_number === 3)?.co2_equivalent || "1.285,0"} tCO₂e
                </span>
              </div>
            </div>

            <div className="pt-4 border-t border-gray-200">
              <div className="flex items-center justify-center space-x-2">
                <TrendingUp className="text-green-600" size={16} />
                <span className="text-green-600 font-semibold text-sm">+12% vs. ano anterior</span>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Upload de Documentos</h2>

          <div className="flex flex-wrap gap-2 mb-6">
            {[
              { name: "PDF", icon: FileText, color: "bg-red-100 text-red-700" },
              { name: "Csv", icon: Table, color: "bg-green-100 text-green-700" },
              { name: "Imagens", icon: Image, color: "bg-blue-100 text-blue-700" },
              { name: "Outros", icon: File, color: "bg-gray-100 text-gray-700" }
            ].map(({ name, icon: Icon, color }, i) => (
              <span key={i} className={`px-4 py-2 ${color} text-sm rounded-full font-medium flex items-center space-x-2`}>
                <Icon size={14} />
                <span>{name}</span>
              </span>
            ))}
          </div>

          <div 
            className={`border-2 border-dashed rounded-2xl p-8 transition-all duration-300 ${
              dragActive 
                ? 'border-blue-400 bg-blue-50' 
                : 'border-gray-300 hover:border-gray-400'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <div className="text-center">
              <div className="mb-4">
                {uploading ? (
                  <div className="mx-auto animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
                ) : (
                  <Upload className="mx-auto text-gray-400" size={48} />
                )}
              </div>
              <p className="text-gray-600 mb-4">
                {uploading ? 'Enviando arquivos...' : 'Arraste e solte arquivos aqui'}<br />
                <span className="text-sm">Suporte para PDF, CSV, JPG, PNG</span>
              </p>
              <input
                type="file"
                multiple
                onChange={handleFileSelect}
                accept=".pdf,.xlsx,.xls,.csv,.jpg,.jpeg,.png"
                className="hidden"
                id="file-upload"
                disabled={uploading}
              />
              <label
                htmlFor="file-upload"
                className={`inline-block px-8 py-3 rounded-xl font-medium shadow-lg cursor-pointer transition-all duration-300 ${
                  uploading 
                    ? 'bg-gray-400 text-white cursor-not-allowed' 
                    : 'bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white hover:shadow-xl'
                }`}
              >
                {uploading ? 'Enviando...' : 'Selecionar Arquivos'}
              </label>
            </div>
          </div>

          {uploadStatus.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Status dos Uploads</h3>
              <div className="space-y-2">
                {uploadStatus.slice(-5).map((upload, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      {getStatusIcon(upload.status)}
                      <span className="text-sm font-medium">{upload.file_name}</span>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-gray-600">{getStatusText(upload.status)}</div>
                      <div className="text-xs text-gray-400">{upload.timestamp}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;
