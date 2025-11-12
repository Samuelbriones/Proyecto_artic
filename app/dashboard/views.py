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
