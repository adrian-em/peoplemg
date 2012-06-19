from peoplemg.models import Rol, Grupo, Guardia, Intervencion, Jornada, Vacaciones, UserProfile
from django.contrib import admin


#admin.site.register(Rol)
#admin.site.register(Grupo)
#admin.site.register(Guardia)
#admin.site.register(Intervencion)
#admin.site.register(Jornada)
#admin.site.register(Vacaciones)
#admin.site.register(UserProfile)


class RolAdmin(admin.ModelAdmin):
    search_fields = ['nombrerol', 'id']

admin.site.register(Rol, RolAdmin)


class GrupoAdmin(admin.ModelAdmin):
    search_fields = ['nombregrupo', 'id']

admin.site.register(Grupo, GrupoAdmin)


class GuardiaAdmin(admin.ModelAdmin):
    search_fields = ['id', 'fini', 'ffin', 'user__username']
    list_filter = ['fini', 'ffin']
    list_display = ('user', 'fini', 'ffin')

admin.site.register(Guardia, GuardiaAdmin)


class IntervencionAdmin(admin.ModelAdmin):
    search_fields = ['id', 'fini', 'ffin', 'observaciones', 'user__username']
    list_filter = ['fini', 'ffin']
    list_display = ('user', 'fini', 'ffin', 'observaciones')

admin.site.register(Intervencion, IntervencionAdmin)


class JornadaAdmin(admin.ModelAdmin):
    search_fields = ['id', 'numdias', 'mes', 'user__username']
    list_filter = ['mes']
    list_display = ('user', 'mes', 'numdias')
admin.site.register(Jornada, JornadaAdmin)


class VacacionesAdmin(admin.ModelAdmin):
    search_fields = ['id', 'fini', 'ffin', 'user__username']
    list_filter = ['fini', 'ffin']
    list_display = ('user', 'fini', 'ffin')
admin.site.register(Vacaciones, VacacionesAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'id', 'rol__nombrerol', 'grupo__nombregrupo']
    list_filter = ['rol__nombrerol', 'grupo__nombregrupo']
    list_display = ('user', 'grupo', 'rol')
admin.site.register(UserProfile, UserProfileAdmin)
