from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
from .views import user_chart_data


urlpatterns = [
    path('login/', views.login_view, name='login'), 
    path('signup/', views.signup_view, name='signup'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('candidat-dashboard/', views.candidat_dashboard, name='candidat_dashboard'),
    path('offres-candidat/', views.candidat_offre, name='candidat_offre'),
    path('candidature-candidat/', views.candidat_candidature, name='candidat_candidature'),
    path('candidature-profile/', views.candidat_profile, name='candidat_profile'),
    path('profil/', views.profil_view, name='profil'),
    
    
    #  Partie administrateur
    path('dashboard2/', views.admin_dashboard2, name='admin_dashboard2'),
    path('offres/', views.admin_offres, name='admin_offres'),
    path('candidatures/', views.admin_candidatures, name='admin_candidatures'),
    path('commentaires/', views.admin_commentaires, name='admin_commentaires'),
    # path('notifications/', views.admin_notifications, name='admin_notifications'),
    path('logout/', views.logout_view, name='logout'),
    
    

    # sprm offre
    path('offres/supprimer/<int:id>/', views.supprimer_offre, name='supprimer_offre'),




    path('notifications/', views.admin_notifications, name='admin_notifications'),  # Afficher la liste des notifications et gérer l'ajout/modification
    path('notifications/ajouter/', views.ajouter_notification, name='ajouter_notification'),  # Ajouter une nouvelle notification
    path('notifications/supprimer/<int:id>/', views.supprimer_notification, name='supprimer_notification'),  # Supprimer une notification
    #path('notifications/modifier/<int:id>/', views.modifier_notification, name='modifier_notification'),  # Modifier une notification

    path('mes_notifications/', views.mes_notifications, name='mes_notifications'),



    path('chart/data/', user_chart_data, name='user_chart_data'),
    path("chart/notifications/", views.notification_chart_data, name="notification_chart_data"),
    path('chart/offres/', views.offres_chart_data, name='offres_chart_data'),




    path('offres/', views.offres, name='offres'),
    path('candidature/', views.candidature, name='candidature'),
    path('postuler/<int:offre_id>/', views.postuler_offre, name='postuler_offre'),

    path('offres/', views.admin_offres, name='admin_offres'),

    # save


    path('offres-candidat/', views.candidat_offre, name='candidat_offre'),  # Page des offres
    path('profile/', views.candidat_profile, name='candidat_profile'),  # Page du profil
    path('save_offer/<int:offre_id>/', views.save_offer, name='save_offer'),  # Sauvegarder une offre
    path('utilisateurs/', views.admin_utilisateurs, name='admin_utilisateurs')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



