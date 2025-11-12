from django.db import models
from django.conf import settings


class Architect(models.Model):
    """Modelo que representa el registro profesional del arquitecto.

    Asociado a un usuario (settings.AUTH_USER_MODEL). Incluye documento PDF
    subido por el usuario y un estado que deberá gestionar el administrador.
    """

    STATUS_REVIEW = 'review'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_PENDING_PAYMENT = 'pending_payment'
    STATUS_CERTIFIED = 'certified'

    STATUS_CHOICES = [
        (STATUS_REVIEW, 'En revisión'),
        (STATUS_APPROVED, 'Aprobado'),
        (STATUS_REJECTED, 'Rechazado'),
        (STATUS_PENDING_PAYMENT, 'Pendiente de pago'),
        (STATUS_CERTIFIED, 'Certificado'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='architect'
    )
    full_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    qualification = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    graduation_year = models.PositiveIntegerField()
    document = models.FileField(upload_to='documents/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_REVIEW)
    created_at = models.DateTimeField(auto_now_add=True)

    # Certification fields
    is_certified = models.BooleanField(default=False)
    certificate_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    certification_date = models.DateField(blank=True, null=True)
    renewal_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} ({self.user.email})"
    
    def create_notification(self, title, message):
        """Helper method to create notifications."""
        from app.notifications.models import Notification
        Notification.objects.create(
            user=self.user,
            title=title,
            message=message,
            is_read=False  # Aseguramos que la notificación esté marcada como no leída
        )
    
    def notify_status_change(self):
        """Send notifications based on current status."""
        status_messages = {
            self.STATUS_REVIEW: (
                "Solicitud en Revisión",
                "Su solicitud está siendo revisada por nuestro equipo. Le notificaremos cuando haya una actualización."
            ),
            self.STATUS_APPROVED: (
                "¡Solicitud Aprobada!",
                "Su solicitud ha sido aprobada. Por favor, proceda a realizar el pago para completar su certificación."
            ),
            self.STATUS_REJECTED: (
                "Solicitud Rechazada",
                f"Lo sentimos, su solicitud ha sido rechazada. Motivo: {self.applicationreview.comments if hasattr(self, 'applicationreview') else 'No especificado'}."
            ),
            self.STATUS_PENDING_PAYMENT: (
                "Pago Pendiente",
                "Su solicitud está aprobada pero requiere pago. Por favor, realice el pago para obtener su certificación."
            ),
            self.STATUS_CERTIFIED: (
                "¡Certificación Completada!",
                f"¡Felicitaciones! Su certificación ha sido completada. Su número de certificado es: {self.certificate_number}"
            )
        }
        
        if self.status in status_messages:
            title, message = status_messages[self.status]
            self.create_notification(title, message)
            
    def save(self, *args, **kwargs):
        """Override save to handle status notifications."""
        status_changed = False
        if self.pk:  # If this is an update
            old_instance = Architect.objects.get(pk=self.pk)
            status_changed = old_instance.status != self.status
        else:  # If this is a new instance
            status_changed = True
            
        super().save(*args, **kwargs)
        
        if status_changed:
            self.notify_status_change()


class ApplicationReview(models.Model):
    """Manages the multi-step review process for an architect's application."""
    
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_APPROVED, 'Aprobado'),
        (STATUS_REJECTED, 'Rechazado'),
    ]
    
    architect = models.OneToOneField(
        Architect,
        on_delete=models.CASCADE,
        related_name='review'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    comments = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.architect.full_name} - {self.get_status_display()}"
