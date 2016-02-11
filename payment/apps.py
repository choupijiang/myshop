from django.apps import AppConfig

class PaymentConfig(AppConfig):
    name = 'payment'
    verbose = 'PayPal payment'

    def ready(self):
        import payment.signals