from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import OffreForm
from .models import Offre
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Candidature
from .forms import CandidatureForm
from .models import Notification
# from django.contrib import messages
from .forms import NotificationForm


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': "Nom d'utilisateur déjà pris."})

        # Créer l'utilisateur
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=prenom,
            last_name=nom
        )

        # Ajouter l'utilisateur au groupe 'Candidat'
        candidat_group = Group.objects.get(name='Candidat')
        user.groups.add(candidat_group)

        login(request, user)  # connexion automatique
        return redirect('login')  # ou une page spécifique selon son rôle

    return render(request, 'signup.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            
            # Redirection selon le groupe
            if user.groups.filter(name='Administrateur').exists():
                return redirect('admin_dashboard')  # à toi de créer cette vue
            elif user.groups.filter(name='Candidat').exists():
                return redirect('candidat_dashboard')  # à toi aussi de le créer

            return redirect('home')  # fallback
        else:
            return render(request, 'login.html', {'error': "Nom d'utilisateur ou mot de passe incorrect."})

    return render(request, 'login.html')



@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')





@login_required
def candidat_dashboard(request):
    return render(request, 'candidat_dashboard.html')




@login_required
def admin_offres(request):
    if request.method == 'POST':
        offre_id = request.POST.get('offre_id')

        if offre_id:  #  on vérifie si l'id n'est pas vide
            offre = get_object_or_404(Offre, id=offre_id)
            form = OffreForm(request.POST, instance=offre)
        else:
            form = OffreForm(request.POST)

        if form.is_valid():
            offre = form.save(commit=False)
            offre.Administrateur = request.user  # --------------------
            offre.save()
            return redirect('admin_offres')
    else:
        form = OffreForm()

    offres = Offre.objects.all()
    return render(request, 'admin_offres.html', {'form': form, 'offres': offres})
   

@login_required
def supprimer_offre(request, id):
    offre = get_object_or_404(Offre, id=id)
    offre.delete()
    return redirect('admin_offres')







@login_required
def admin_candidatures(request):
    if request.method == 'POST':
        candidature_id = request.POST.get('candidature_id')
        candidature = get_object_or_404(Candidature, id=candidature_id)

        # Mise à jour du statut si modifié
        new_statut = request.POST.get('statut')
        if new_statut:
            candidature.statut = new_statut
        
        # Mise à jour du commentaire si ajouté
        new_commentaire = request.POST.get('commentaire')
        if new_commentaire is not None:
            candidature.commentaire = new_commentaire

        candidature.save()
        return redirect('admin_candidatures')

    candidatures = Candidature.objects.all()
    return render(request, 'admin_candidatures.html', {'candidatures': candidatures})







@login_required
def admin_commentaires(request):
    return render(request, 'admin_commentaires.html')








def admin_dashboard2(request):
    candidatures = Candidature.objects.all()
    offres = Offre.objects.all()
    utilisateurs = User.objects.all()
    notifications = Notification.objects.all()
    
    candidatures_acceptées = candidatures.filter(statut="Acceptée").count()
    candidatures_refusées = candidatures.filter(statut="Refusée").count()
    candidatures_en_attente = candidatures.filter(statut="En attente").count()





    context = {
        'candidatures': candidatures,
        'offres': offres,
        'utilisateurs': utilisateurs,
        'notifications' : notifications,
        'candidatures_acceptées': candidatures_acceptées,
        'candidatures_refusées': candidatures_refusées,
        'candidatures_en_attente': candidatures_en_attente,

        
    }
    return render(request, 'admin_dashboard2.html', context)

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models.functions import TruncMonth
from django.db.models import Count

def user_chart_data(request):
    users_by_month = (
        User.objects.annotate(month=TruncMonth('date_joined'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    labels = [u['month'].strftime('%B %Y') for u in users_by_month]
    data = [u['count'] for u in users_by_month]

    return JsonResponse({'labels': labels, 'data': data})






from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncDate
from .models import Notification

def notification_chart_data(request):
    # Regrouper les notifications par jour
    data = (
        Notification.objects
        .annotate(day=TruncDate('date_envoi'))  # Remplacez 'date_envoi' si nécessaire
        .values('day')
        .annotate(total=Count('id'))
        .order_by('day')
    )

    labels = [entry['day'].strftime('%Y-%m-%d') for entry in data]
    values = [entry['total'] for entry in data]

    return JsonResponse({
        'labels': labels,
        'data': values
    })




from django.db.models.functions import TruncDate
from django.db.models import Count
from django.http import JsonResponse
from .models import Offre

def offres_chart_data(request):
    data = (
        Offre.objects
        .annotate(day=TruncDate('date_publication'))  # Champ corrigé ici
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    labels = [entry['day'].strftime('%Y-%m-%d') for entry in data]
    counts = [entry['count'] for entry in data]

    return JsonResponse({
        'labels': labels,
        'data': counts
    })


@login_required
def admin_notifications(request):
    notifications = Notification.objects.all()  # Récupérer toutes les notifications

    # Si l'administrateur veut modifier une notification, récupérer l'objet à modifier
    notification_to_edit = None
    if request.GET.get('edit_id'):
        notification_to_edit = get_object_or_404(Notification, id=request.GET.get('edit_id'))

    if request.method == 'POST':
        form = NotificationForm(request.POST, instance=notification_to_edit) if notification_to_edit else NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_notifications')

    else:
        form = NotificationForm(instance=notification_to_edit) if notification_to_edit else NotificationForm()

    return render(request, 'admin_notifications.html', {
        'form': form,
        'notifications': notifications,
        'notification_to_edit': notification_to_edit  # Passer l'objet à modifier pour que le formulaire se remplisse
    })

@login_required
def supprimer_notification(request, id):
    notification = get_object_or_404(Notification, id=id)
    notification.delete()
    return redirect('admin_notifications')

@login_required
def ajouter_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_notifications')
    else:
        form = NotificationForm()

    return render(request, 'admin_notifications.html', {'form': form})
# @login_required
# def modifier_notification(request, id):
#     notification = get_object_or_404(Notification, id=id)

#     if request.method == 'POST':
#         form = NotificationForm(request.POST, instance=notification)
#         if form.is_valid():
#             form.save()
#             return redirect('admin_notifications')
#     else:
#         form = NotificationForm(instance=notification)

#     return render(request, 'admin_notifications.html', {'form': form, 'notification_to_edit': notification})





def logout_view(request):
    logout(request)
    return redirect('login')
















def logout_view(request):
    logout(request)
    return redirect('login')





def page_candidat(request):
    notifications = Notification.objects.filter(utilisateur=request.user).order_by('-date_envoi')
    return render(request, 'candidat_dashboard.html', {'notifications': notifications})







#candidat

from .models import OffreEmploi





def offres(request):
    # Filtrer les offres publiées pour les candidats uniquement
    offres = OffreEmploi.objects.filter(est_publiee=True)  # 'est_publiee' : champ pour les offres visibles par les candidats
    
    return render(request, 'offres.html', {'offres': offres})

def candidature(request):
    return render(request, 'candidature.html')






def candidat_offre_list(request):
    return render(request, 'candidat/offres.html')  # ou autre template

def candidat_candidature(request):
    return render(request, 'candidat/candidature.html')


# def candidat_offre(request):
#     offres = Offre.objects.all().order_by('-date_publication')  # Trie les plus récentes
#     return render(request, 'candidat_dashboard.html', {'offres': offres})


def candidat_offre(request):
    offres = Offre.objects.all()
    print("Nombre d'offres récupérées :", offres.count())  # ← À regarder dans la console
    return render(request, 'candidat_offre.html', {'offres': offres})




def candidat_dashboard(request):
    offres = Offre.objects.all()
    print("Nombre d'offres récupérées :", offres.count())  # ← À regarder dans la console
    return render(request, 'candidat_dashboard.html', {'offres': offres})





#notif icon
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification

# @login_required
# def notifications_api(request):
#     notifications = Notification.objects.filter(utilisateur=request.user).order_by('-date_envoi')
#     data = [
#         {
#             'message': n.message,
#             'date_envoi': n.date_envoi.strftime('%d/%m/%Y %H:%M'),
#             'est_lu': n.est_lu,
#         }
#         for n in notifications
#     ]
#     return JsonResponse(data, safe=False)


# #searchbar
# from .forms import OffreSearchForm  # importer le formulaire
# from django.db.models import Q
# def candidat_offre(request):
#     form = OffreSearchForm(request.GET or None)
#     offres = Offre.objects.all()

#     if form.is_valid():
#         query = form.cleaned_data.get('q')
#         if query:
#             offres = offres.filter(
#                 Q(titre__icontains=query) |
#                 Q(description__icontains=query) |
#                 Q(profil__icontains=query) |
#                 Q(lieu__icontains=query)
#             ).order_by('-date_publication')

#     return render(request, 'candidat_offre.html', {'form': form, 'offres': offres})



# postuler

from django.shortcuts import render, get_object_or_404, redirect
from .models import Offre, Candidature
from .forms import CandidatureForms
from django.contrib.auth.decorators import login_required

@login_required
def postuler_offre(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id)

    if request.method == 'POST':
        form = CandidatureForms(request.POST, request.FILES)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.candidat = request.user
            candidature.offre = offre
            candidature.save()
            return redirect('candidat_offre')  # redirige vers la liste des offres ou autre
    else:
        form = CandidatureForm()

    return render(request, 'postuler_modal.html', {'form': form, 'offre': offre})


# page candidature

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Candidature

@login_required
def candidat_candidature(request):
    # Récupérer les candidatures du candidat connecté
    candidatures = Candidature.objects.filter(candidat=request.user).order_by('-date_postulation')
    return render(request, 'candidat_candidature.html', {'candidatures': candidatures})




# profil


@login_required
def candidat_profile(request):
    return render(request, 'candidat_profile.html')




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import UserUpdateForm

@login_required
def profil_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            update_session_auth_hash(request, password_form.user)  # Garde la session active
            messages.success(request, 'Votre profil a été mis à jour.')
            return redirect('candidat_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'candidat_profil.html', {
        'user_form': user_form,
        'password_form': password_form
    })


#save_option


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Offre, SavedOffer

@login_required
def save_offer(request, offre_id):
    offre = Offre.objects.get(id=offre_id)
    saved_offer, created = SavedOffer.objects.get_or_create(candidat=request.user, offre=offre)
    return redirect('candidat_profile')  # Redirige vers la page du profil candidat


#recuperer les offres sauvegardées dans le profil candidat


@login_required
def candidat_profile(request):
    saved_offers = request.user.saved_offers.all()  # Récupérer les offres sauvegardées
    return render(request, 'candidat_profile.html', {
        'saved_offers': saved_offers
    })



# # recuperer les offres sauvegardées 15/05

from django.http import JsonResponse
from .models import Offre

def offre_detail(request, id):
    try:
        offre = Offre.objects.get(pk=id)
        data = {
            "titre": offre.titre,
            "lieu": offre.lieu,
            "contrat": offre.contrat,
            "description": offre.description,
            "profil": offre.profil,
            "debut": offre.debut.strftime("%d/%m/%Y"),
            "candidature": offre.candidature,
            "date_publication": offre.date_publication.strftime("%d/%m/%Y"),
        }
        return JsonResponse(data)
    except Offre.DoesNotExist:
        return JsonResponse({"error": "Offre non trouvée"}, status=404)
    










    
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notification

@login_required
def mes_notifications(request):
    # Seules les notifications du candidat connecté
    notifications = Notification.objects.filter(utilisateur=request.user).order_by('-date_envoi')
    return render(request, 'mes_notifications.html', {'notifications': notifications})







@login_required
def admin_offres(request):
    if request.method == 'POST':
        offre_id = request.POST.get('offre_id')

        if offre_id:  #  on vérifie si l'id n'est pas vide
            offre = get_object_or_404(Offre, id=offre_id)
            form = OffreForm(request.POST, instance=offre)
        else:
            form = OffreForm(request.POST)

        if form.is_valid():
            offre = form.save(commit=False)
            offre.Administrateur = request.user  # --------------------
            offre.save()
            return redirect('admin_offres')
    else:
        form = OffreForm()

    offres = Offre.objects.all()
    return render(request, 'admin_offres.html', {'form': form, 'offres': offres})

@login_required
def supprimer_offre(request, id):
    offre = get_object_or_404(Offre, id=id)
    offre.delete()
    return redirect('admin_offres')



def ton_vue(request):
    nb_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'candidat_dashboard.html', {'nb_notifications': nb_notifications})


from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def admin_utilisateurs(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'modifier':
            user_id = request.POST.get('user_id')
            nouveau_role = request.POST.get('role')
            user = get_object_or_404(User, id=user_id)

            # Supprimer tous les groupes puis ajouter le nouveau
            user.groups.clear()
            group = Group.objects.get(name=nouveau_role)
            user.groups.add(group)

        elif action == 'supprimer':
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)
            user.delete()

        elif action == 'ajouter':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            role = request.POST.get('role')

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=prenom,
                    last_name=nom
                )
                group = Group.objects.get(name=role)
                user.groups.add(group)

        return redirect('admin_utilisateurs')

    utilisateurs = User.objects.all()
    groupes = Group.objects.all()
    return render(request, 'admin_utilisateurs.html', {
        'utilisateurs': utilisateurs,
        'groupes': groupes
    })