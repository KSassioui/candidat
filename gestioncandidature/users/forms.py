from django import forms
from .models import Offre
from .models import Candidature
from .models import Notification
from django.contrib.auth.models import User





class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        fields = ['titre', 'description', 'lieu', 'contrat', 'profil', 'debut', 'candidature']





#candidature
class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['statut']  # Juste le statut





class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['utilisateur', 'message']  # Utilisateur et message sont les champs à remplir

    utilisateur = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Sélectionner un Candidat")
    message = forms.CharField(widget=forms.Textarea, label="Message")



from django import forms

class OffreSearchForm(forms.Form):
    q = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Mots-clés',
            'class': 'search-input'
        })
    )



from .models import Candidature

class CandidatureForms(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['cv', 'lettre_motivation']



# profile



from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']




