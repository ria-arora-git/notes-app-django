from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def note_list(request):
    notes = Note.objects.all().order_by('-created_at')
    notes = Note.objects.filter(user=request.user)

    return render(request, 'notes/list.html', {'notes': notes})

@login_required
def note_create(request):
    if request.method == 'POST':
        Note.objects.create(
            title=request.POST['title'],
            content=request.POST['content'],
            user=request.user
        )
        return redirect('note_list')
    return render(request, 'notes/create.html')

@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.title = request.POST['title']
        note.content = request.POST['content']
        note.save()
        return redirect('note_list')
    return render(request, 'notes/edit.html', {'note': note})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    note.delete()
    return redirect('note_list')




