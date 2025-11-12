from django.contrib import admin
from .models import Architect


@admin.register(Architect)
class ArchitectAdmin(admin.ModelAdmin):
	"""Configuración del admin para facilitar revisión/aprobación."""
	list_display = ('full_name', 'get_email', 'qualification', 'status', 'created_at')
	list_filter = ('status', 'qualification', 'created_at')
	search_fields = ('full_name', 'user__email', 'registration_number')
	readonly_fields = ('created_at',)
	list_editable = ('status',)
	actions = ['approve_selected', 'reject_selected']

	def get_email(self, obj):
		return obj.user.email
	get_email.short_description = 'Correo'

	# Acciones para el panel de administración
	def approve_selected(self, request, queryset):
		updated = queryset.update(status=Architect.STATUS_APPROVED)
		self.message_user(request, f"{updated} registro(s) marcados como Aprobado.")
	approve_selected.short_description = 'Marcar seleccionados como Aprobado'

	def reject_selected(self, request, queryset):
		updated = queryset.update(status=Architect.STATUS_REJECTED)
		self.message_user(request, f"{updated} registro(s) marcados como Rechazado.")
	reject_selected.short_description = 'Marcar seleccionados como Rechazado'
