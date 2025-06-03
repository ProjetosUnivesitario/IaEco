import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
from django.db import connections
from django.db.utils import OperationalError


def aplicar_migracoes():
    try:

        db_conn = connections['default']
        db_conn.ensure_connection()

        call_command('migrate')
        print('Migrações aplicadas com sucesso!')
    except OperationalError:
        print('O banco de dados não está acessível.')
    except Exception as e:
        print(f'Ocorreu um erro ao aplicar as migrações: {e}')


aplicar_migracoes()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
