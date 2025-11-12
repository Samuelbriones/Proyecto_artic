from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
from .models import Architect, ApplicationReview
from io import BytesIO
from .forms import ArchitectForm, ApplicationReviewForm
from app.payments.models import Payment


@login_required
def register_architect(request):
    """Permite al usuario crear su registro profesional si no existe."""
    try:
        existing = request.user.architect
        messages.info(request, 'Ya tienes un registro profesional. Puedes editarlo.')
        return redirect('dashboard')
    except Architect.DoesNotExist:
        if request.method == 'POST':
            form = ArchitectForm(request.POST, request.FILES)
            if form.is_valid():
                arch = form.save(commit=False)
                arch.user = request.user
                arch.status = Architect.STATUS_REVIEW
                arch.save()

                # Crear ApplicationReview automáticamente
                review = ApplicationReview.objects.create(
                    architect=arch,
                    status=ApplicationReview.STATUS_PENDING
                )
                messages.success(request, 'Registro enviado. Se encuentra en revisión.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Corrige los errores del formulario.')
        else:
            form = ArchitectForm()
        return render(request, 'register_architect.html', {'form': form})


@login_required
def edit_architect(request):
    """Edición del registro profesional existente."""
    arch = get_object_or_404(Architect, user=request.user)
    if request.method == 'POST':
        form = ArchitectForm(request.POST, request.FILES, instance=arch)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos del registro actualizados.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = ArchitectForm(instance=arch)
    return render(request, 'register_architect.html', {'form': form, 'edit': True})

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def review_applications(request):
    """Vista para que los administradores revisen las solicitudes pendientes."""
    pending_reviews = ApplicationReview.objects.filter(status=ApplicationReview.STATUS_PENDING)
    return render(request, 'architects/review_applications.html', {
        'pending_reviews': pending_reviews
    })

@user_passes_test(is_admin)
def process_review(request, review_id):
    """Procesa la revisión de una solicitud."""
    review = get_object_or_404(ApplicationReview, id=review_id)
    
    if request.method == 'POST':
        form = ApplicationReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save()
            architect = review.architect
            
            # Actualizar status del arquitecto según la revisión
            if review.status == ApplicationReview.STATUS_APPROVED:
                architect.status = Architect.STATUS_PENDING_PAYMENT
                architect.save()  # Guardar el cambio de estado
                # Crear pago pendiente
                Payment.objects.create(
                    architect=architect,
                    amount=500.00,  # Monto de ejemplo
                    description='Pago de certificación profesional',
                    status=Payment.STATUS_PENDING
                )
                messages.success(request, 'Solicitud aprobada y pago creado.')
                architect.notify_status_change()  # Notificar al arquitecto
            elif review.status == ApplicationReview.STATUS_REJECTED:
                architect.status = Architect.STATUS_REJECTED
                architect.save()  # Guardar el cambio de estado
                messages.warning(request, 'Solicitud rechazada.')
                architect.notify_status_change()  # Notificar al arquitecto
            
            architect.save()
            messages.success(request, 'Revisión procesada exitosamente.')
            return redirect('review_applications')
    else:
        form = ApplicationReviewForm(instance=review)
    
    return render(request, 'architects/process_review.html', {
        'form': form,
        'review': review
    })

@login_required
def process_payment(request, payment_id):
    """Procesa el pago de la certificación."""
    # Esta vista se implementará cuando tengamos la app de pagos
    return redirect('dashboard')

@login_required
def generate_certificate(request):
    """Genera el certificado en PDF para arquitectos certificados."""
    architect = get_object_or_404(Architect, user=request.user, status=Architect.STATUS_CERTIFIED)
    
    # Crear un buffer para el PDF
    buffer = BytesIO()
    
    # Crear el PDF
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Configurar el contenido
    p.setTitle(f'Certificado ARCON - {architect.full_name}')
    
    # Dibujar borde
    p.setStrokeColorRGB(0, 0, 0)
    p.setLineWidth(2)
    p.rect(1*inch, 1*inch, width-2*inch, height-2*inch)
    
    # Título
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width/2, height-3*inch, "CERTIFICADO DE REGISTRO PROFESIONAL")
    
    # Contenido
    p.setFont("Helvetica", 12)
    y = height-4*inch
    p.drawCentredString(width/2, y, "Por medio de la presente, se certifica que:")
    
    y -= 0.5*inch
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, y, architect.full_name)
    
    y -= 0.5*inch
    p.setFont("Helvetica", 12)
    p.drawCentredString(width/2, y, f"con número de registro {architect.registration_number}")
    
    y -= 0.3*inch
    p.drawCentredString(width/2, y, f"graduado de {architect.institution}")
    
    y -= 0.5*inch
    p.drawCentredString(width/2, y, "se encuentra debidamente registrado como Arquitecto Profesional")
    y -= 0.3*inch
    p.drawCentredString(width/2, y, "en el Registro Nacional de Arquitectos.")
    
    y -= 0.5*inch
    p.drawCentredString(width/2, y, f"Número de Certificado: {architect.certificate_number}")
    y -= 0.3*inch
    if architect.certification_date:
        p.drawCentredString(width/2, y, f"Fecha de Certificación: {architect.certification_date.strftime('%d/%m/%Y')}")
    
    # Firma
    y = 3*inch
    p.line(width/2 - inch, y, width/2 + inch, y)
    y -= 0.3*inch
    p.drawCentredString(width/2, y, "Director ARCON")
    
    # Finalizar PDF
    p.showPage()
    p.save()
    
    # Preparar respuesta
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado_ARCON_{architect.certificate_number}.pdf"'
    return response

@login_required
def dashboard(request):
    """Dashboard mejorado con estado de la solicitud."""
    try:
        architect = request.user.architect
        try:
            review = ApplicationReview.objects.get(architect=architect)
        except ApplicationReview.DoesNotExist:
            # Si no existe la revisión, la creamos
            review = ApplicationReview.objects.create(architect=architect)
        
        return render(request, 'architects/dashboard.html', {
            'architect': architect,
            'review': review
        })
    except Architect.DoesNotExist:
        messages.info(request, 'Complete su registro profesional para continuar.')
        return redirect('register_architect')
