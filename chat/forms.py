from django import forms
from .models import Group,Message
from django.contrib.auth import get_user_model

CustomUser = get_user_model()
        
class GroupForm(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        creator = kwargs.pop('creator', None)
        super(GroupForm, self).__init__(*args, **kwargs)

        if creator:
            self.creator = creator
            self.fields['members'].queryset = CustomUser.objects.exclude(pk=creator.pk).exclude(is_superuser=True)

    class Meta:
        model = Group
        fields = ['name', 'members', 'grp_image'] 
        widgets = {
            'members': forms.CheckboxSelectMultiple
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['author', 'receiver', 'is_grp_msg', 'group', 'content']