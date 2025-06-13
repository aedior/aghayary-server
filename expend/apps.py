from django.apps import AppConfig


class ExpendConfig(AppConfig):
    verbose_name="هزینه ها"
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'expend'

    def ready(self):
        import expend.signals