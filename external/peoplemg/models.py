from django.db import models
from django.contrib.auth.models import User
# Models


# v_n1, v_n2
# 0 - Not checked
# 1 - Checked, approved
# 2 - Checked, rejected


class Jornada(models.Model):
    mes = models.CharField(max_length=10, blank=True)
    numdias = models.IntegerField(blank=True)
    user = models.ForeignKey(User)
    v_n1 = models.IntegerField(blank=True)
    v_n2 = models.IntegerField(blank=True)

    def __unicode__(self):
        return str(str(self.mes) + " ----> " + str(self.user))


class Guardia(models.Model):
    fini = models.DateTimeField(blank=True)
    ffin = models.DateTimeField(blank=True)
    user = models.ForeignKey(User)
    v_n1 = models.IntegerField(blank=True)
    v_n2 = models.IntegerField(blank=True)

    def __unicode__(self):
        return str(str(self.fini) + " -- " + str(self.ffin) + " -----> " + str(self.user))


class Intervencion(models.Model):
    fini = models.DateTimeField(blank=True)
    ffin = models.DateTimeField(blank=True)
    observaciones = models.TextField(blank=True)
    user = models.ForeignKey(User)
    v_n1 = models.IntegerField(blank=True)
    v_n2 = models.IntegerField(blank=True)

    def __unicode__(self):
        return self.observaciones


class Vacaciones(models.Model):
    fini = models.DateField(blank=True)
    ffin = models.DateField(blank=True)
    user = models.ForeignKey(User)
    v_n1 = models.IntegerField(blank=True)
    v_n2 = models.IntegerField(blank=True)

    def __unicode__(self):
        return str(str(self.fini) + " -- " + str(self.ffin) + " -----> " + str(self.user))


class Rol(models.Model):
    nombrerol = models.CharField(max_length=20)
    #user = models.IntegerField()

    def __unicode__(self):
        return self.nombrerol


class Grupo(models.Model):
    nombregrupo = models.CharField(max_length=20)
    #user = models.IntegerField()

    def __unicode__(self):
        return self.nombregrupo


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    rol = models.ForeignKey(Rol)
    grupo = models.ForeignKey(Grupo)

    def __unicode__(self):
        return str(str(self.user) + " - " + str(self.rol) + " - " + str(self.grupo))
