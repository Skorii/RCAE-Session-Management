from django.db import models


class Section(models.Model):
    code = models.CharField(max_length=6, primary_key=True, verbose_name="Code")
    name = models.CharField(max_length=100, verbose_name="Section")
    subscription = models.BooleanField(verbose_name='Abonnement')
    active = models.BooleanField(verbose_name='Activé', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"


class Session(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name="Section")
    date_time = models.DateTimeField(verbose_name="Début")
    duration = models.TimeField(verbose_name="Durée")
    location = models.TextField(verbose_name="Emplacement")
    max_members = models.PositiveSmallIntegerField(verbose_name="Place")

    def __str__(self):
        return self.section.__str__() + " - " + self.date_time.date().__str__() + " " + self.date_time.time().__str__()

    class Meta:
        ordering = ['date_time']
        verbose_name = "Séance"
        verbose_name_plural = "Séances"


class Member(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Prénom")
    last_name = models.CharField(max_length=50, verbose_name="Nom")
    e_mail = models.CharField(max_length=100, verbose_name="Adresse e-mail")
    rcae_number = models.CharField(max_length=6, verbose_name="Numéro RCAE")
    subscription_number = models.CharField(max_length=6, blank=True, verbose_name="Abonnement")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="Séance")
    registration_date = models.DateField(auto_now=True, verbose_name="Date d'inscription")

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"
