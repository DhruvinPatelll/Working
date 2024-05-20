from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import GroupForm
from .models import Group
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


@login_required
def room(request):
    user = request.user
    users = CustomUser.objects.filter(is_superuser=False).exclude(id=user.id)
    groups = Group.objects.filter(members=user)
    combined_list = sorted(list(users) + list(groups), key=lambda x: getattr(x, 'create_timestamp', None), reverse=True)
    return render(request, 'chat/room.html', {'user': user, 'combined_list': combined_list})


@login_required
def chat(request):
    form = GroupForm()  
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, creator=request.user)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()
            form.save_m2m()
            group.members.add(request.user)
            group_name = group.name
            return redirect('room') 
    else:
        initial_data = {'members': [request.user.pk]}
        form = GroupForm(initial=initial_data, creator=request.user)
    return render(request, 'chat/chat.html', {'form': form})


