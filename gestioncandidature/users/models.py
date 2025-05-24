
from django.db import models
from django.contrib.auth.models import User



class Offre(models.Model):
    titre = models.CharField(max_length=255)
    description = models.CharField(max_length=455)
    date_publication = models.DateTimeField(auto_now_add=True)
    Administrateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offres')

    # Nouveau champ pour l'offre d'emploi
    lieu = models.CharField(max_length=255)  # Ville
    contrat = models.CharField(max_length=20, choices=[('CDI', 'CDI'), ('CDD', 'CDD'), ('Stage', 'Stage')])  # Type de contrat
    profil = models.CharField(max_length=255)  # Profil recherché
    debut = models.DateField()  # Date de début
    candidature = models.EmailField()  # Email pour envoyer le CV

    def __str__(self):
        return self.titre


class Candidature(models.Model):
    STATUT_CHOICES = [
        ('En attente', 'En attente'),
        ('Acceptée', 'Acceptée'),
        ('Refusée', 'Refusée'),
    ]

    candidat = models.ForeignKey(User, on_delete=models.CASCADE, related_name='candidatures')
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE, related_name='candidatures')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='En attente')
    # cv = models.CharField(max_length=255)
    # lettre_motivation = models.CharField(max_length=255)
    cv = models.FileField(upload_to='cvs/')
    lettre_motivation = models.FileField(upload_to='lettres/')
    date_postulation = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"{self.candidat.username} - {self.offre.titre}"


class Notification(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    est_lu = models.BooleanField(default=False)
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification pour {self.utilisateur.username} : {self.message[:50]}"










class OffreEmploi(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_publication = models.DateField(auto_now_add=True)
    Administrateur = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.titre
# class OffreEmploi(models.Model):
#     titre = models.CharField(max_length=255)
#     description = models.TextField()
#     date_publication = models.DateField()
#     administrateur = models.ForeignKey(User, on_delete=models.CASCADE)  # L'administrateur qui a créé l'offre
#     est_publiee = models.BooleanField(default=True)  # champ pour savoir si l'offre est publiée pour les candidats
    
#     def __str__(self):
#         return self.titre

#save_option


class SavedOffer(models.Model):
    candidat = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_offers')
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE, related_name='saved_by')
    date_saved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidat.username} saved {self.offre.titre}"