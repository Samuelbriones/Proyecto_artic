from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.architects.models import Architect


@login_required
def dashboard_view(request):
	"""Panel principal del usuario que muestra estado del registro profesional."""
	arch = None
	try:
		arch = request.user.architect
	except Architect.DoesNotExist:
		arch = None

	context = {
		'user': request.user,
		'architect': arch,
	}
	return render(request, 'dashboard.html', context)

@login_required
def calendar_view(request):
    """Renderiza la plantilla estática del calendario."""
    return render(request, 'calendar.html')

@login_required
def exams_view(request):
    """Renderiza la plantilla estática de exámenes."""
    return render(request, 'exams.html')

@login_required
def materials_view(request):
    """Renderiza la plantilla estática de materiales."""
    return render(request, 'materials.html')

@login_required
def courses_view(request):
    """Renderiza la plantilla estática de cursos."""
    return render(request, 'courses.html')
