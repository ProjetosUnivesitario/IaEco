import os
import django
import pika
from home.models import DocumentUpload, EmissionData, EmissionScope
import json
import pandas as pd
# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()
def callback(ch, method, properties, body):
    message = json.loads(body)
    document_id = message['document_id']
    file_path = message['file_path']
    file_type = message['file_type']
    try:
        document = DocumentUpload.objects.get(id=document_id)
        document.status = 'PROCESSING'
        document.save()
        # Simular processamento do documento
        processed_data = {}
        co2_value = 0.0
        if file_type == 'CSV':
            df = pd.read_csv(file_path)
            processed_data = df.to_dict(orient='records')
            co2_value = df.get('co2_value', pd.Series([0.0])).sum()
        elif file_type == 'EXCEL':
            df = pd.read_excel(file_path)
            processed_data = df.to_dict(orient='records')
            co2_value = df.get('co2_value', pd.Series([0.0])).sum()
        else:
            processed_data = {'message': f'Tipo de arquivo não suportado: {file_type}'}
        document.processed_data = processed_data
        document.status = 'COMPLETED'
        document.save()
        # Criar entrada em EmissionData
        scope = EmissionScope.objects.filter(company=document.company, scope_number=1, year=2025).first()
        if scope:
            EmissionData.objects.create(
                document=document,
                scope=scope,
                source_category='Uploaded Document',
                co2_value=co2_value,
                unit='tCO₂e',
                calculation_method='Automated Extraction',
                raw_data=processed_data
            )
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        document.status = 'FAILED'
        document.error_message = str(e)
        document.save()
        ch.basic_ack(delivery_tag=method.delivery_tag)
# Conectar ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='document_processing', durable=True)
channel.basic_consume(queue='document_processing', on_message_callback=callback)
print('Aguardando mensagens na fila document_processing. Pressione CTRL+C para sair.')
channel.start_consuming()