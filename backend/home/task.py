from celery import shared_task
from django.core.files.storage import default_storage
from .models import DocumentUpload, EmissionScope, EmissionData, Company
import pandas as pd
import PyPDF2
import logging
import json
from decimal import Decimal

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def process_carbon_document(self, document_id):
    """
    Task para processar documentos de pegada de carbono em background
    """
    try:
        document = DocumentUpload.objects.get(id=document_id)
        document.status = 'PROCESSING'
        document.task_id = self.request.id
        document.save()
        
        logger.info(f"Iniciando processamento do documento: {document.file_name}")
        
        # Determinar tipo de processamento baseado na extensão
        file_extension = document.file_name.lower().split('.')[-1]
        
        processed_data = {}
        
        if file_extension == 'pdf':
            processed_data = process_pdf_document(document)
        elif file_extension in ['xlsx', 'xls']:
            processed_data = process_excel_document(document)
        elif file_extension == 'csv':
            processed_data = process_csv_document(document)
        elif file_extension in ['jpg', 'jpeg', 'png']:
            processed_data = process_image_document(document)
        else:
            raise ValueError(f"Tipo de arquivo não suportado: {file_extension}")
        
        # Salvar dados processados
        document.processed_data = processed_data
        document.status = 'COMPLETED'
        document.save()
        
        # Atualizar escopos de emissão se dados foram extraídos
        if 'emissions' in processed_data:
            update_emission_scopes(document, processed_data['emissions'])
        
        logger.info(f"Documento processado com sucesso: {document.file_name}")
        
        return {
            'status': 'success',
            'document_id': str(document_id),
            'processed_data': processed_data,
            'message': f'Documento {document.file_name} processado com sucesso!'
        }
        
    except DocumentUpload.DoesNotExist:
        logger.error(f"Documento não encontrado: {document_id}")
        return {'status': 'error', 'message': 'Documento não encontrado'}
        
    except Exception as e:
        logger.error(f"Erro ao processar documento {document_id}: {str(e)}")
        
        # Atualizar status do documento para FAILED
        try:
            document = DocumentUpload.objects.get(id=document_id)
            document.status = 'FAILED'
            document.error_message = str(e)
            document.save()
        except:
            pass
            
        return {
            'status': 'error',
            'document_id': str(document_id),
            'message': f'Erro ao processar documento: {str(e)}'
        }

def process_pdf_document(document):
    """Processar documentos PDF - extração básica de texto"""
    try:
        with default_storage.open(document.file.name, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_content = ""
            
            for page in pdf_reader.pages:
                text_content += page.extract_text()
        
        # Análise básica para identificar dados de emissões
        emissions_data = extract_emissions_from_text(text_content)
        
        return {
            'type': 'pdf',
            'pages': len(pdf_reader.pages),
            'text_length': len(text_content),
            'emissions': emissions_data,
            'raw_text': text_content[:1000]  # Primeiros 1000 caracteres
        }
    except Exception as e:
        raise Exception(f"Erro ao processar PDF: {str(e)}")

def process_excel_document(document):
    """Processar planilhas Excel/XLSX"""
    try:
        with default_storage.open(document.file.name, 'rb') as file:
            df = pd.read_excel(file)
        
        # Análise da estrutura da planilha
        emissions_data = extract_emissions_from_dataframe(df)
        
        return {
            'type': 'excel',
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': df.columns.tolist(),
            'emissions': emissions_data,
            'sample_data': df.head().to_dict('records')
        }
    except Exception as e:
        raise Exception(f"Erro ao processar Excel: {str(e)}")

def process_csv_document(document):
    """Processar arquivos CSV"""
    try:
        with default_storage.open(document.file.name, 'r', encoding='utf-8') as file:
            df = pd.read_csv(file)
        
        emissions_data = extract_emissions_from_dataframe(df)
        
        return {
            'type': 'csv',
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': df.columns.tolist(),
            'emissions': emissions_data,
            'sample_data': df.head().to_dict('records')
        }
    except Exception as e:
        raise Exception(f"Erro ao processar CSV: {str(e)}")

def process_image_document(document):
    """Processar imagens - análise básica"""
    return {
        'type': 'image',
        'message': 'Imagem recebida. OCR não implementado nesta versão.',
        'emissions': []
    }

def extract_emissions_from_text(text):
    """Extrair dados de emissões de texto (implementação básica)"""
    emissions = []
    
    # Padrões simples para identificar dados de CO2
    import re
    
    # Procurar por padrões como "123.45 tCO2e" ou "123,45 toneladas CO2"
    patterns = [
        r'(\d+[.,]?\d*)\s*(?:t|toneladas?)\s*(?:CO2|CO₂)(?:e|eq)?',
        r'(?:escopo|scope)\s*(\d)\s*[:\-]?\s*(\d+[.,]?\d*)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if len(match) == 2:  # scope + value
                emissions.append({
                    'scope': int(match[0]),
                    'value': float(match[1].replace(',', '.')),
                    'unit': 'tCO₂e'
                })
            else:  # just value
                emissions.append({
                    'scope': None,
                    'value': float(match.replace(',', '.')),
                    'unit': 'tCO₂e'
                })
    
    return emissions

def extract_emissions_from_dataframe(df):
    """Extrair dados de emissões de DataFrame"""
    emissions = []
    
    # Procurar por colunas que possam conter dados de CO2
    co2_columns = []
    scope_columns = []
    
    for col in df.columns:
        col_lower = str(col).lower()
        if any(term in col_lower for term in ['co2', 'carbono', 'emiss', 'carbon']):
            co2_columns.append(col)
        if any(term in col_lower for term in ['escopo', 'scope']):
            scope_columns.append(col)
    
    # Extrair dados se encontrou colunas relevantes
    if co2_columns:
        for _, row in df.iterrows():
            for col in co2_columns:
                value = row[col]
                if pd.notna(value) and isinstance(value, (int, float)):
                    emission_data = {
                        'source_column': col,
                        'value': float(value),
                        'unit': 'tCO₂e'
                    }
                    
                    # Tentar identificar o escopo
                    if scope_columns:
                        for scope_col in scope_columns:
                            scope_val = row[scope_col]
                            if pd.notna(scope_val):
                                emission_data['scope'] = scope_val
                                break
                    
                    emissions.append(emission_data)
    
    return emissions

def update_emission_scopes(document, emissions_data):
    """Atualizar escopos de emissão com base nos dados processados"""
    try:
        # Assumir empresa padrão ou criar se não existir
        company, created = Company.objects.get_or_create(
            name="Empresa Padrão",
            defaults={'cnpj': None}
        )
        
        current_year = 2024
        
        for emission in emissions_data:
            if 'scope' in emission and emission['scope']:
                scope_number = emission['scope']
                value = Decimal(str(emission['value']))
                
                # Criar ou atualizar escopo
                scope, created = EmissionScope.objects.get_or_create(
                    company=company,
                    scope_number=scope_number,
                    year=current_year,
                    defaults={'co2_equivalent': value, 'progress_percentage': 100}
                )
                
                if not created:
                    scope.co2_equivalent += value
                    scope.save()
                
                # Criar entrada de dados detalhados
                EmissionData.objects.create(
                    document=document,
                    scope=scope,
                    source_category=emission.get('source_column', 'Dados do Documento'),
                    co2_value=value,
                    unit=emission.get('unit', 'tCO₂e'),
                    raw_data=emission
                )
        
    except Exception as e:
        logger.error(f"Erro ao atualizar escopos: {str(e)}")