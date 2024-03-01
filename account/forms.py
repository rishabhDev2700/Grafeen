
from account.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

class AccountCreationForm(UserCreationForm):
    '''Account creation form to add new users'''
    class Meta:
        '''Extra meta information'''
        model = User
        fields = ('email','full_name','is_seller')
        
class AccountChangeForm(UserChangeForm):
    '''Form for updating a user's details'''
    password=None
    class Meta:
        '''Extra meta information'''
        model = User
        fields = ('full_name','is_seller')

