from django.db import models
from django.conf import settings
from app.architects.models import Architect


class Payment(models.Model):
    """Modelo para registrar transacciones de pago."""

    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_PROCESSING, 'Procesando'),
        (STATUS_COMPLETED, 'Completado'),
        (STATUS_FAILED, 'Fallido'),
    ]

    architect = models.ForeignKey(
        Architect,
        on_delete=models.CASCADE,
        related_name='payments',
        null=True,
        blank=True
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    description = models.CharField(max_length=255, default='Pago de certificación')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Pago de {self.architect.full_name} - {self.get_status_display()}"

    def mark_as_paid(self, transaction_id=None):
        """Marca el pago como completado y actualiza el estado del arquitecto."""
        from django.utils import timezone
        
        self.status = self.STATUS_COMPLETED
        self.paid_at = timezone.now()
        if transaction_id:
            self.transaction_id = transaction_id
        self.save()
        
        # Actualizar el estado del arquitecto
        architect = self.architect
        architect.status = 'certified'
        architect.certification_date = timezone.now()
        architect.save()
