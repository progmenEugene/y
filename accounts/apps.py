from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = 'Учетные записи'

    def ready(self):
        import accounts.signals
