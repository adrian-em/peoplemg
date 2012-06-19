from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from peoplemg.views import *
import os.path
from django.conf.urls.defaults import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

site_media = os.path.join(
os.path.dirname(__file__), 'site_media'
)
urlpatterns = patterns('',
    (r'^$', main_page),
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    # pages 
    {'document_root': site_media}),
    (r'^jornadas/$', jornadas_page),
    #(r'^jornadas/add/$', jornadas_add),
    (r'^guardias/$', guardias_page),
    (r'^intervenciones/$', intervenciones_page),
    (r'^vacaciones/$', vacaciones_page),
    # edition
    (r'^vacaciones/editar/(?P<idvacaciones>\w{0,50})$', vacaciones_edit_page),
    (r'^vacaciones/aprobar/(?P<idvacaciones>\w{0,50})$', vacaciones_approve_page),
    (r'^vacaciones/rechazar/(?P<idvacaciones>\w{0,50})$', vacaciones_reject_page),
    (r'^jornadas/editar/(?P<idjornadas>\w{0,50})$', jornadas_edit_page),
    (r'^jornadas/aprobar/(?P<idjornadas>\w{0,50})$', jornadas_approve_page),
    (r'^jornadas/rechazar/(?P<idjornadas>\w{0,50})$', jornadas_reject_page),
    (r'^guardias/editar/(?P<idguardias>\w{0,50})$', guardias_edit_page),
    (r'^guardias/aprobar/(?P<idguardias>\w{0,50})$', guardias_approve_page),
    (r'^guardias/rechazar/(?P<idguardias>\w{0,50})$', guardias_reject_page),
    (r'^intervenciones/editar/(?P<idintervenciones>\w{0,50})$', intervenciones_edit_page),
    (r'^intervenciones/aprobar/(?P<idintervenciones>\w{0,50})$', intervenciones_approve_page),
    (r'^intervenciones/rechazar/(?P<idintervenciones>\w{0,50})$', intervenciones_reject_page),
    # others
    (r'^logout/$', logout_page),
    (r'^admin/', include(admin.site.urls)),
    (r'^consola/$', consola_tl_page),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
