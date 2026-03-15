import hashlib

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Module, Resource
from .forms import ModuleFilterForm, ResourceUploadForm


# ─────────────────────────────────────────────
# Browse Resources
# ─────────────────────────────────────────────

def resource_list(request):
    """
    Browse page — filterable list of all resources.
    Handles: ?query=...&level=...&semester=...&resource_type=...
    """
    form      = ModuleFilterForm(request.GET or None)
    resources = Resource.objects.select_related('module', 'uploaded_by').all()

    if form.is_valid():
        query         = form.cleaned_data.get('query')
        level         = form.cleaned_data.get('level')
        semester      = form.cleaned_data.get('semester')
        resource_type = form.cleaned_data.get('resource_type')

        if query:
            resources = resources.filter(
                Q(title__icontains=query) | Q(module__name__icontains=query)
            )
        if level:
            resources = resources.filter(module__level=level)
        if semester:
            resources = resources.filter(module__semester=semester)
        if resource_type:
            resources = resources.filter(resource_type=resource_type)

    context = {
        'form':       form,
        'resources':  resources,
        'count':      resources.count(),
    }
    return render(request, 'C:\\Users\\DELL E5470\\Desktop\\estin_student\\estin_student\\froms\\templates\\list.html', context)


# ─────────────────────────────────────────────
# Upload Resource (3-step wizard)
# ─────────────────────────────────────────────
def upload_resource(request):
    """
    3-step upload form.
    Step 1 — Categorize  (level, semester, module)
    Step 2 — Content     (title, type, year)
    Step 3 — Transfer    (file)
    All steps live in one POST — the wizard is purely visual (JS-driven).
    """
    if request.method == 'POST':
        form = ResourceUploadForm(request.POST, request.FILES)

        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user

            # ── Hash the file for duplicate detection ──
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                sha256 = hashlib.sha256()
                for chunk in uploaded_file.chunks():
                    sha256.update(chunk)
                file_hash = sha256.hexdigest()

                if Resource.objects.filter(file_hash=file_hash).exists():
                    messages.error(request, 'This file has already been uploaded.')
                    return render(request, 'froms/upload.html', {'form': form})

                resource.file_hash = file_hash

            # ── TODO: Upload to Google Drive here ──
            # drive_id = upload_to_drive(uploaded_file)
            # resource.drive_id = drive_id
            # resource.file = None  # clear local temp file after Drive upload

            resource.save()
            messages.success(request, 'Resource uploaded successfully! Thank you for contributing.')
            return redirect('resources:resource_list')

    else:
        form = ResourceUploadForm()

    return render(request, 'C:\\Users\\DELL E5470\\Desktop\\estin_student\\estin_student\\froms\\templates\\upload.html', {'form': form})


# ─────────────────────────────────────────────
# Download (increment counter + redirect)
# ─────────────────────────────────────────────

def download_resource(request, pk):
    """
    Increments download counter then redirects to Google Drive download URL.
    """
    resource = get_object_or_404(Resource, pk=pk)
    resource.downloads += 1
    resource.save(update_fields=['downloads'])

    download_url = resource.get_download_url()
    if not download_url:
        messages.error(request, 'File not available for download.')
        return redirect('froms:list')

    return redirect(download_url)


# ─────────────────────────────────────────────
# AJAX — filter modules by level + semester
# ─────────────────────────────────────────────

def ajax_get_modules(request):
    """
    Called by JS when user selects level + semester in the upload form.
    Returns JSON list of matching modules.
    GET /resources/ajax/modules/?level=1CP&semester=S1
    """
    level    = request.GET.get('level', '').strip()
    semester = request.GET.get('semester', '').strip()

    if not level or not semester:
        return HttpResponseBadRequest('level and semester are required.')

    modules = (
        Module.objects
        .filter(level=level, semester=semester)
        .order_by('name')
        .values('id', 'name')
    )
    return JsonResponse(list(modules), safe=False)
