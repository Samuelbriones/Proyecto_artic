from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification


@login_required
def notification_list(request):
    """Lista todas las notificaciones del usuario."""
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications
    })


@login_required
def mark_as_read(request, notification_id):
    """Marca una notificación como leída."""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.mark_as_read()
    messages.success(request, 'Notificación marcada como leída.')
    return redirect('notifications:list')
