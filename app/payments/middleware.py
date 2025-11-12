from django.shortcuts import redirect
from django.urls import reverse
from .models import Payment

class PaymentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                architect = request.user.architect
                if architect.status == 'pending_payment':
                    # Si está en la página de pagos, permitir
                    if not request.path.startswith('/payments/'):
                        # Verificar si tiene pagos pendientes
                        pending_payment = Payment.objects.filter(
                            architect=architect,
                            status='pending'
                        ).exists()
                        if pending_payment:
                            return redirect('payments:list')
            except:
                pass
                
        response = self.get_response(request)
        return response