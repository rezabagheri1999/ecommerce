from django.apps import AppConfig
from django.db.backends.signals import connection_created
from django.dispatch import receiver

class ProductsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products_app'

    def ready(self):
        @receiver(connection_created)
        def enforce_foreign_keys(sender, connection, **kwargs):
            if 'sqlite3' in connection.vendor:
                cursor = connection.cursor()
                cursor.execute('PRAGMA foreign_keys = ON;')