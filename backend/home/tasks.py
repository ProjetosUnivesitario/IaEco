from celery import shared_task
from home.models import DocumentUpload, EmissionData, EmissionScope
from django.core.files.storage import default_storage
import pandas as pd
import json

@shared_task
def process_document(document_id, file_path, file_type):
    try:
        document = DocumentUpload.objects.get(id=document_id)
        document.status = 'PROCESSING'
        document.save()

        # Simulate document processing (replace with actual logic)
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
        elif file_type == 'PDF':
            processed_data = {'message': 'PDF processing not implemented'}
            co2_value = 0.0
        else:
            processed_data = {'message': f'Unsupported file type: {file_type}'}
            co2_value = 0.0

        # Update document
        document.processed_data = processed_data
        document.status = 'COMPLETED'
        document.save()

        # Create EmissionData entry (assuming scope exists)
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

    except Exception as e:
        document.status = 'FAILED'
        document.error_message = str(e)
        document.save()