from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .models import Group, Message
from .forms import GroupForm
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

@login_required
@require_GET
def fetch_chat_history(request):
    sender = request.user
    receiver_username = request.GET.get('receiver', None)
    group_name = request.GET.get('group', None)

    if receiver_username:
        try:
            receiver = CustomUser.objects.get(username=receiver_username)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Receiver does not exist'}, status=400)
        messages = Message.get_user_messages(sender, receiver)
    elif group_name:
        messages = Message.get_group_messages(group_name)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    serialized_messages = [{'author': msg.author.username, 'content': msg.content, 'timestamp': msg.timestamp} for msg in messages]
    return JsonResponse({'messages': serialized_messages})
