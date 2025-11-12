from .models import Payment

def payment_processor(request):
    """Adds pending payment information to template context."""
    context = {'pending_payment': None}
    if request.user.is_authenticated:
        try:
            context['pending_payment'] = Payment.objects.filter(
                architect=request.user.architect,
                status='pending'
            ).first()
        except:
            pass
    return context