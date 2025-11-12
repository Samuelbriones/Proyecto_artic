from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Payment
from .forms import PaymentForm


@login_required
def payment_list(request):
    """Lista todos los pagos del arquitecto."""
    try:
        # Verificar si el usuario tiene un perfil de arquitecto
        if not hasattr(request.user, 'architect'):
            messages.error(request, 'No tienes un perfil de arquitecto.')
            return redirect('dashboard')
        
        architect = request.user.architect
        # Obtener todos los pagos del arquitecto
        payments = Payment.objects.filter(architect=architect).order_by('-created_at')
        
        # Si no hay pagos pero el arquitecto está pendiente de pago, crear uno
        if not payments.exists() and architect.status == 'pending_payment':
            payment = Payment.objects.create(
                architect=architect,
                amount=500.00,
                description='Pago de certificación profesional',
                status=Payment.STATUS_PENDING
            )
            payments = [payment]
            messages.info(request, 'Se ha generado tu pago pendiente.')
        
        return render(request, 'payments/payment_list.html', {
            'payments': payments,
            'architect_status': architect.status  # Agregar estado para depuración
        })
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('dashboard')


@login_required
def payment_detail(request, payment_id):
    """Muestra los detalles de un pago y permite procesarlo."""
    payment = get_object_or_404(Payment, id=payment_id, architect__user=request.user)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        # Establecer el monto en el formulario
        if form.is_valid():
            return process_payment_with_form(request, payment, form.cleaned_data)
    else:
        # Inicializar el formulario con el monto del pago
        form = PaymentForm(initial={'amount': payment.amount})
    
    return render(request, 'payments/payment_detail.html', {
        'payment': payment,
        'form': form
    })


def process_payment_with_form(request, payment, form_data):
    """Procesa un pago con los datos del formulario."""
    if payment.status != Payment.STATUS_PENDING:
        messages.error(request, 'Este pago ya ha sido procesado.')
        return redirect('payments:list')
    
    # Validar que el monto coincida
    if float(form_data['amount']) != float(payment.amount):
        messages.error(request, 'El monto del pago no coincide.')
        return redirect('payments:detail', payment_id=payment.id)
    
    try:
        # Simular procesamiento de pago exitoso
        payment.status = Payment.STATUS_COMPLETED
        payment.transaction_id = f"TXN-{timezone.now().timestamp():.0f}"
        payment.paid_at = timezone.now()
        payment.save()
        
        # Actualizar estado del arquitecto a certificado
        architect = payment.architect
        architect.status = 'certified'
        architect.is_certified = True
        architect.certification_date = timezone.now().date()
        architect.certificate_number = f"CERT-{timezone.now().year}-{payment.transaction_id[-6:]}"
        architect.save()
        
        # Notificar cambio de estado
        architect.notify_status_change()
        
        messages.success(request, '¡Pago procesado exitosamente! Tu certificación está lista.')
        return redirect('payments:list')
        
    except Exception as e:
        messages.error(request, f'Error al procesar el pago: {str(e)}')
        return redirect('payments:detail', payment_id=payment.id)


@login_required
def process_payment(request, payment_id):
    """Procesa un pago pendiente - método alternativo."""
    payment = get_object_or_404(Payment, id=payment_id, architect__user=request.user)
    
    if request.method == 'POST':
        if payment.status != Payment.STATUS_PENDING:
            messages.error(request, 'Este pago ya ha sido procesado.')
            return redirect('payments:list')
        
        # Simular pago exitoso
        try:
            payment.status = Payment.STATUS_COMPLETED
            payment.transaction_id = f"DEMO-{timezone.now().timestamp():.0f}"
            payment.paid_at = timezone.now()
            payment.save()
            
            # Actualizar estado del arquitecto
            architect = payment.architect
            architect.status = 'certified'
            architect.is_certified = True
            architect.certification_date = timezone.now().date()
            architect.certificate_number = f"CERT-{timezone.now().year}-{payment.transaction_id[-6:]}"
            architect.save()
            
            messages.success(request, '¡Pago procesado exitosamente! Redirigiendo a la descarga de su certificado...')
            return redirect('architects:generate_certificate')
            
        except Exception as e:
            messages.error(request, f'Error al procesar el pago: {str(e)}')
            return redirect('payments:list')
    
    return render(request, 'payments/payment_process.html', {
        'payment': payment
    })


@login_required
def download_certificate(request):
    """Genera y descarga el certificado PDF del arquitecto."""
    from django.http import HttpResponse
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from io import BytesIO
    import os
    from django.conf import settings
    
    try:
        architect = request.user.architect
        
        if not architect.is_certified:
            messages.error(request, 'Tu certificación aún no está completa.')
            return redirect('payments:list')
        
        # Crear el PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Configurar colores y estilos
        from reportlab.lib.colors import HexColor, black
        blue_color = HexColor('#1e40af')  # Azul corporativo
        
        # Título principal
        p.setFont("Helvetica-Bold", 28)
        p.setFillColor(blue_color)
        title = "CERTIFICADO PROFESIONAL"
        title_width = p.stringWidth(title, "Helvetica-Bold", 28)
        p.drawString((width - title_width) / 2, height - 2 * inch, title)
        
        # Subtítulo
        p.setFont("Helvetica", 16)
        p.setFillColor(black)
        subtitle = "Colegio de Arquitectos - ARCON"
        subtitle_width = p.stringWidth(subtitle, "Helvetica", 16)
        p.drawString((width - subtitle_width) / 2, height - 2.5 * inch, subtitle)
        
        # Línea decorativa
        p.setStrokeColor(blue_color)
        p.setLineWidth(3)
        p.line(100, height - 3 * inch, width - 100, height - 3 * inch)
        
        # Texto principal
        p.setFont("Helvetica", 14)
        p.setFillColor(black)
        
        text_y = height - 4 * inch
        p.drawString(100, text_y, "Por medio del presente se certifica que:")
        
        # Nombre del arquitecto
        text_y -= 0.8 * inch
        p.setFont("Helvetica-Bold", 20)
        p.setFillColor(blue_color)
        name_width = p.stringWidth(architect.full_name, "Helvetica-Bold", 20)
        p.drawString((width - name_width) / 2, text_y, architect.full_name)
        
        # Información del certificado
        p.setFont("Helvetica", 14)
        p.setFillColor(black)
        text_y -= 0.8 * inch
        p.drawString(100, text_y, f"Con título de: {architect.qualification}")
        
        text_y -= 0.4 * inch
        p.drawString(100, text_y, f"Egresado de: {architect.institution}")
        
        text_y -= 0.4 * inch
        p.drawString(100, text_y, f"Año de graduación: {architect.graduation_year}")
        
        # Información de certificación
        text_y -= 0.8 * inch
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, text_y, "Se encuentra debidamente registrado y certificado")
        p.setFont("Helvetica", 14)
        text_y -= 0.4 * inch
        p.drawString(100, text_y, "para ejercer la profesión de Arquitecto en el territorio nacional.")
        
        # Datos del certificado
        text_y -= 1 * inch
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, text_y, f"Número de certificado: {architect.certificate_number}")
        
        text_y -= 0.3 * inch
        p.drawString(100, text_y, f"Fecha de certificación: {architect.certification_date.strftime('%d de %B de %Y')}")
        
        # Firmas (simuladas)
        text_y -= 1.5 * inch
        p.setFont("Helvetica", 10)
        p.line(100, text_y, 250, text_y)
        p.line(350, text_y, 500, text_y)
        
        text_y -= 0.3 * inch
        p.drawString(140, text_y, "Director General")
        p.drawString(380, text_y, "Secretario Académico")
        
        text_y -= 0.2 * inch
        p.drawString(125, text_y, "ARCON - Colegio de Arquitectos")
        p.drawString(370, text_y, "ARCON - Colegio de Arquitectos")
        
        # Footer
        p.setFont("Helvetica", 8)
        p.setFillColor(HexColor('#666666'))
        footer_y = 50
        p.drawString(100, footer_y, f"Generado el {timezone.now().strftime('%d/%m/%Y a las %H:%M')}")
        p.drawString(100, footer_y - 15, "Este documento tiene validez oficial.")
        
        # Finalizar PDF
        p.showPage()
        p.save()
        
        # Preparar respuesta
        pdf = buffer.getvalue()
        buffer.close()
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="certificado_{architect.certificate_number}.pdf"'
        
        return response
        
    except Exception as e:
        messages.error(request, f'Error al generar el certificado: {str(e)}')
        return redirect('payments:list')
