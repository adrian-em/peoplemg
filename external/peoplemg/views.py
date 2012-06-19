from django.template import RequestContext
#from django.template.loader import get_template
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
#from django.contrib.auth.views import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
#from django.contrib.auth.decorators import login_required
from datetime import datetime
from peoplemg.models import Guardia, Jornada, Vacaciones, Rol, Grupo, Intervencion, UserProfile
from peoplemg.forms import *
#from django import forms


#@login_required(login_url='/')
def main_page(request):

    '''
    Main page (index) function.
    We have to check if the user is authenticated.
    If the user is NOT authenticated, redirect to login page
    If the user IS authenticated, redirect to the first page, jornadas.
    '''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/jornadas/')
    return render_to_response(
        'index.html',
        {'user': request.user
        }
    )


def jornadas_page(request):

    '''
    Jornadas page.

    If the user who has just logged in is the admin, redirect to admin page
    In my database, team leader was rol with id 2. You may change it.

    Once we have the profiles of team leaders, we have to obtain all the
    usernames which are team leaders.

    If the user is a team leader, redirect to console.


    Within the page, we obtain all the jornadas (days worked) by the user,
    ordered desc by id.
    Show the form.
    '''
    if request.user.username == 'admin':
        return HttpResponseRedirect('/admin/')

    # if user's rol is Team Leader redirect to console
    objteamleaders = UserProfile.objects.filter(rol=2)
    teamleaders = []
    # get team leaders' usernames
    for t in range(objteamleaders.count()):
        teamleaders.append(objteamleaders[t].user.username)
        #if request.user.username == teamleaders[t]
            #return HttpResponseRedirect('/consola/')

    if request.user.username in teamleaders:
        return HttpResponseRedirect('/consola/')

    ###################################################

    j = Jornada.objects.filter(user=request.user.id).order_by('-id')
    if request.method == 'POST':
        form = JornadasForm(request.POST)
        if form.is_valid():
            nommes = form.cleaned_data['mes']
            ndias = form.cleaned_data['numdias']
            jornada = Jornada(mes=nommes, numdias=ndias, user=request.user, v_n1=0, v_n2=0)
            jornada.save()
            return HttpResponseRedirect('/jornadas/')
    else:
        form = JornadasForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response(
        'jornadas.html',
        {'user': request.user,
        'time': datetime.now(),
        'jornadas': j,
        },
        variables
    )


def intervenciones_page(request):

    '''
    Intervenciones page. (Interventions)

    Obtain all intervenciones from the user, ordered desc by id.
    Show the form.
    '''
    i = Intervencion.objects.filter(user=request.user.id).order_by('-id')
    if request.method == 'POST':
        form = IntervencionesForm(request.POST)
        if form.is_valid():
            formfini = form.cleaned_data['fini']
            formffin = form.cleaned_data['ffin']
            formobs = form.cleaned_data['obs']
            intervencion = Intervencion(fini=formfini, ffin=formffin, observaciones=formobs, user=request.user, v_n1=0, v_n2=0)
            intervencion.save()
            return HttpResponseRedirect('/intervenciones/')
    else:
        form = IntervencionesForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response(
        'intervenciones.html',
        {'user': request.user,
        'intervenciones': i},
        variables
    )


def guardias_page(request):

    '''
    Guardias page.

    Obtain all guardias from the user, ordered desc by id.
    Show the form.
    '''
    g = Guardia.objects.filter(user=request.user.id).order_by('-id')
    if request.method == 'POST':
        form = GuardiasForm(request.POST)
        if form.is_valid():
            formfini = form.cleaned_data['fini']
            formffin = form.cleaned_data['ffin']
            guardia = Guardia(fini=formfini, ffin=formffin, user=request.user, v_n1=0, v_n2=0)
            guardia.save()
            return HttpResponseRedirect('/guardias/')
    else:
        form = GuardiasForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response(
        'guardias.html',
        {'user': request.user,
         'guardias': g},
         variables
    )


def vacaciones_page(request):

    '''
    Vacaciones page.

    Obtain all vacaciones from the user, ordered desc by id.
    Show the form.
    '''
    v = Vacaciones.objects.filter(user=request.user.id).order_by('-id')
    if request.method == 'POST':
        form = VacacionesForm(request.POST)
        if form.is_valid():
            formfini = form.cleaned_data['fini']
            formffin = form.cleaned_data['ffin']
            vacaciones = Vacaciones(fini=formfini, ffin=formffin, user=request.user, v_n1=0, v_n2=0)
            vacaciones.save()
            return HttpResponseRedirect('/vacaciones/')
    else:
        form = VacacionesForm()

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response(
        'vacaciones.html',
        {'user': request.user,
        'vacaciones': v},
        variables
    )


def vacaciones_edit_page(request, idvacaciones):

    '''
    Edit page for vacaciones.

    Obtain profile.
    Request the id of the element.
    If sended with GET, get data.
    If it is POST, save the values
    Else, show the form with the given values.
    '''
    # Queries to get the user rol. Must be Team Leader.
    # We send it to the template
    u = User.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=u.id)
    # Problem here. It seems that GET parameters aren't sent correctly
    # Don't why. So I request also the id from the database, and use it instead of GET.
    if request.method == 'GET':
        v = Vacaciones.objects.get(id=idvacaciones)
    if request.method == 'POST':
        form = VacacionesEditarForm(request.POST)
        if form.is_valid():
            formfini = form.cleaned_data['fini']
            formffin = form.cleaned_data['ffin']
            formfid = form.cleaned_data['fid']
            v = Vacaciones.objects.get(id=formfid)
            v.fini = formfini
            v.ffin = formffin
            v.save()
            return HttpResponseRedirect('/consola/')
    else:
        form = VacacionesEditarForm(initial={'fini': v.fini, 'ffin': v.ffin, 'fid': v.id})

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response(
        'vacaciones_edit_page.html',
        {'user': request.user,
        'userrol': profile.rol.nombrerol},
        variables
    )


def vacaciones_approve_page(request, idvacaciones):

    '''
    Approve page for vacaciones.

    Obtain profile.
    Request the id of the element.
    Change the value of v_n1
    '''
    # Queries to get the user rol. Must be Team Leader.
    # We send it to the template
    u = User.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=u.id)
    v = Vacaciones.objects.get(id=idvacaciones)
    v.v_n1 = 1
    v.save()
    return HttpResponseRedirect('/consola/')
    return render_to_response(
        'vacaciones_edit_page.html',
        {'user': request.user,
        'userrol': profile.rol.nombrerol},
    )


def vacaciones_reject_page(request, idvacaciones):

    '''
    Reject page for vacaciones.

    Obtain profile.
    Request the id of the element.
    Change the value of v_n1
    '''
    # Queries to get the user rol. Must be Team Leader.
    # We send it to the template
    u = User.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=u.id)
    v = Vacaciones.objects.get(id=idvacaciones)
    v.v_n1 = 2
    v.save()
    return HttpResponseRedirect('/consola/')

    return render_to_response(
        'vacaciones_reject_page.html',
        {'user': request.user,
        'userrol': profile.rol.nombrerol},
    )


##########################################


def jornadas_edit_page(request, idjornadas):

    '''
    Edit page for jornadas.

    Obtain profile.
    Request the id of the element.
    If sended with GET, get data.
    If it is POST, save the values
    Else, show the form with the given values.
    '''
    # Queries to get the user rol. Must be Team Leader.
    # We send it to the template
    u = User.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=u.id)
    # Problem here. It seems that GET parameters aren't sent correctly
    # Don't why. So I request also the id from the database, and use it instead of GET.
    if request.method == 'GET':
        j = Jornada.objects.get(id=idjornadas)

    if request.method == 'POST':
        form = JornadaEditarForm(request.POST)
        if form.is_valid():
            formmes = form.cleaned_data['mes']
            formdias = form.cleaned_data['numdias']
            formfid = form.cleaned_data['fid']
            j = Jornada.objects.get(id=formfid)
            j.mes = formmes
            j.numdias = formdias
            j.save()
            return HttpResponseRedirect('/consola/')
    else:
        form = JornadaEditarForm(initial={'mes': j.mes, 'numdias': j.numdias, 'fid': j.id})

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response(
        'jornada_edit_page.html',
        {'user': request.user,
        'userrol': profile.rol.nombrerol},
        variables
    )


def jornadas_approve_page(request, idjornadas):

    '''
    Approve page for jornadas.

    Obtain profile.
    Request the id of the element.
    Change value of v_n1
    '''
    # Queries to get the user rol. Must be Team Leader.
    # We send it to the template
    u = User.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=u.id)
    j = Jornada.objects.get(id=idjornadas)
    j.v_n1 = 1
    j.save()
    return HttpResponseRedirect('/consola/')

    return render_to_response(
        'vacaciones_edit_page.html',
        {'user': request.user,
        'userrol': profile.rol.nombrerol},
    )


def jornadas_reject_page(request, idjornadas):

    '''
    Reject page for jornadas.

    Obtain profile.
    Request the id of the element.
    Change value v_n1
    '''
    # Queries to get the user rol. Must be Team Leader.
    # We send it to the template
    u = User.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=u.id)
    j = Jornada.objects.get(id=idjornadas)
    j.v_n1 = 2
    j.save()
    return HttpResponseRedirect('/consola/')

    return render_to_response(
        'vacaciones_reject_page.html',
        {'user': request.user,
        'userrol': profile.rol.nombrerol},
    )

#####################################################################


def guardias_edit_page(request, idguardias):

    '''
    Edit page for guardias.

    Obtain profile.
    Request the id of the element.
    If sended with GET, get data.
    If it is POST, save the values
    Else, show the form with the given values.
    '''
    # Queries to get the user rol. Must be Team Leader.
    # We send it to the template
    u = User.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=u.id)
    # Problem here. It seems that GET parameters aren't sent correctly
    # Don't why. So I request also the id from the database, and use it instead of GET.
    if request.method == 'GET':
        g = Guardia.objects.get(id=idguardias)
    if request.method == 'POST':
        form = GuardiaEditarForm(request.POST)
        if form.is_valid():
            formfini = form.cleaned_data['fini']
            formffin = form.cleaned_data['ffin']
            formfid = form.cleaned_data['fid']
            g = Guardia.objects.get(id=formfid)
            g.fini = formfini
            g.ffin = formffin
            g.save()
            return HttpResponseRedirect('/consola/')
    else:
        form = GuardiaEditarForm(initial={'fini': g.fini, 'ffin': g.ffin, 'fid': g.id})

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response(
        'guardia_edit_page.html',
        {'user': request.user,
        'userrol': profile.rol.nombrerol},
        variables
    )


def guardias_approve_page(request, idguardias):

    '''
    Approve page for guardias.

    Obtain profile.
    Request the id of the element.
    Change value of v_n1
    '''
    # Queries to get the user rol. Must be Team Leader.
    # We send it to the template
    u = User.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=u.id)
    g = Guardia.objects.get(id=idguardias)
    g.v_n1 = 1
    g.save()
    return HttpResponseRedirect('/consola/')
    return render_to_response(
        'guardias_edit_page.html',
        {'user': request.user,
        'userrol': profile.rol.nombrerol},
    )


def guardias_reject_page(request, idguardias):

    '''
    Reject page for guardias.

    Obtain profile.
    Request the id of the element.
    Change value of v_n1
    '''
    # Queries to get the user rol. Must be Team Leader.
    # We send it to the template
    u = User.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=u.id)
    g = Guardia.objects.get(id=idguardias)
    g.v_n1 = 2
    g.save()
    return HttpResponseRedirect('/consola/')

    return render_to_response(
        'vacaciones_reject_page.html',
        {'user': request.user,
        'userrol': profile.rol.nombrerol},
    )


###############################################


def intervenciones_edit_page(request, idintervenciones):

    '''
    Edit page for intervenciones.

    Obtain profile.
    Request the id of the element.
    If sended with GET, get data.
    If it is POST, save the values
    Else, show the form with the given values.
    '''
    # Queries to get the user rol. Must be Team Leader.
    # We send it to the template
    u = User.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=u.id)
    # Problem here. It seems that GET parameters aren't sent correctly
    # Don't why. So I request also the id from the database, and use it instead of GET.
    if request.method == 'GET':
        i = Intervencion.objects.get(id=idintervenciones)
    if request.method == 'POST':
        form = IntervencionEditarForm(request.POST)
        if form.is_valid():
            formfini = form.cleaned_data['fini']
            formffin = form.cleaned_data['ffin']
            formobs = form.cleaned_data['obs']
            formfid = form.cleaned_data['fid']
            i = Intervencion.objects.get(id=formfid)
            i.fini = formfini
            i.ffin = formffin
            i.observaciones = formobs
            i.save()
            return HttpResponseRedirect('/consola/')
    else:
        form = IntervencionEditarForm(initial={'fini': i.fini, 'ffin': i.ffin, 'obs': i.observaciones, 'fid': i.id})

    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response(
        'intervencion_edit_page.html',
        {'user': request.user,
        'userrol': profile.rol.nombrerol},
        variables
    )


def intervenciones_approve_page(request, idintervenciones):

    '''
    Approve page for intervenciones.

    Obtain profile.
    Request the id of the element.
    Change value of v_n1
    '''
    # Queries to get the user rol. Must be Team Leader.
    # We send it to the template
    u = User.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=u.id)
    i = Intervencion.objects.get(id=idintervenciones)
    i.v_n1 = 1
    i.save()
    return HttpResponseRedirect('/consola/')
    return render_to_response(
        'intervencion_edit_page.html',
        {'user': request.user,
        'userrol': profile.rol.nombrerol},
    )


def intervenciones_reject_page(request, idintervenciones):

    '''
    Reject page for intervenciones.

    Obtain profile.
    Request the id of the element.
    Change value of v_n1
    '''
    # Queries to get the user rol. Must be Team Leader.
    # We send it to the template
    u = User.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=u.id)
    i = Intervencion.objects.get(id=idintervenciones)
    i.v_n1 = 2
    i.save()
    return HttpResponseRedirect('/consola/')

    return render_to_response(
        'vacaciones_reject_page.html',
        {'user': request.user,
        'userrol': profile.rol.nombrerol},
    )

#################################################################################


def logout_page(request):

    '''
    Logout page.
    '''
    logout(request)
    return HttpResponseRedirect('/')


def consola_tl_page(request):

    '''
    Console page for Team Leaders.

    If the user is not authenticated, redirect to login.

    Get the user profile, get the group and obtain the coworkers.

    Store coworkers objects.

    Work with the objects.

    There are so many list because of the format of the table. On the template
    I only work with two nested for
    '''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    u = User.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=u.id)

    # Retrieve data from the users of the same group
    coworkersprofile = UserProfile.objects.filter(grupo=profile.grupo.id)
    # create the lists to store all the objects
    vacacionesobj = []
    jornadasobj = []
    guardiasobj = []
    intervencionesobj = []
    # for the total of coworkers, store all respective objects by user id.
    for x in range(coworkersprofile.count()):
        vacacionesobj.append(Vacaciones.objects.filter(user=coworkersprofile[x].user.id))
        jornadasobj.append(Jornada.objects.filter(user=coworkersprofile[x].user.id))
        guardiasobj.append(Guardia.objects.filter(user=coworkersprofile[x].user.id))
        intervencionesobj.append(Intervencion.objects.filter(user=coworkersprofile[x].user.id))
    # The previous lists have empty strings, now we clean them
    vacacionesobj = filter(None, vacacionesobj)
    jornadasobj = filter(None, jornadasobj)
    guardiasobj = filter(None, guardiasobj)
    intervencionesobj = filter(None, intervencionesobj)

    # Define several lists. One for each field.
    vacacionesfini = []
    vacacionesffin = []
    vacacionesuser = []
    vacacionesid = []

    jornadasdias = []
    jornadasmes = []
    jornadasuser = []
    jornadasid = []

    guardiasfini = []
    guardiasffin = []
    guardiasuser = []
    guardiasid = []

    intervencionesfini = []
    intervencionesffin = []
    intervencionesobservaciones = []
    intervencionesuser = []
    intervencionesid = []

    # This will be temporal
    jornadas = []
    vacaciones = []
    guardias = []
    intervenciones = []

    ############################
    # for each element in the object list, append it to the temporal list.
    for x in vacacionesobj:
        for i in x:
            vacaciones.append(i)

    # By each field, store in the respective list
    for x in vacaciones:
        vacacionesfini.append(x.fini)
        vacacionesffin.append(x.ffin)
        vacacionesuser.append(x.user.username)
        vacacionesid.append(x.id)

    # Button containers
    vacacioneshtml = []
    vacacioneshtml2 = []
    vacacioneshtml3 = []

    # For each ID, three buttons separated by list.
    for x in vacacionesid:
        vacacioneshtml.append("<td><a href=\"/vacaciones/editar/" + str(x) + "\"><i class=\"icon-list-alt\"></i></td>")
        vacacioneshtml2.append("<td><a onclick=\"alert('Aprobado')\" href=\"/vacaciones/aprobar/" + str(x) + "\"><i class=\"icon-ok-circle\"></i></td>")
        vacacioneshtml3.append("<td><a  onclick=\"alert('Rechazado')\" href=\"/vacaciones/rechazar/" + str(x) + "\"><i class=\"icon-ban-circle\"></i></td>")

    # join everything in the final list
    vacacioneslist = (vacacionesfini, vacacionesffin, vacacionesuser, vacacioneshtml, vacacioneshtml2, vacacioneshtml3)
    # Change columns to rows
    vacacioneslist = zip(*vacacioneslist)

    # The following objects, use the same procedure
   ############################
    for x in jornadasobj:
        for i in x:
            jornadas.append(i)

    for x in jornadas:
        jornadasdias.append(x.numdias)
        jornadasmes.append(x.mes)
        jornadasuser.append(x.user.username)
        jornadasid.append(x.id)

    jornadashtml = []
    jornadashtml2 = []
    jornadashtml3 = []
    for x in jornadasid:
        jornadashtml.append("<td><a href=\"/jornadas/editar/" + str(x) + "\"><i class=\"icon-list-alt\"></i></td>")
        jornadashtml2.append("<td><a  onclick=\"alert('Aprobado')\" href=\"/jornadas/aprobar/" + str(x) + "\"><i class=\"icon-ok-circle\"></i></td>")
        jornadashtml3.append("<td><a  onclick=\"alert('Rechazado')\" href=\"/jornadas/rechazar/" + str(x) + "\"><i class=\"icon-ban-circle\"></i></td>")

    jornadaslist = (jornadasdias, jornadasmes, jornadasuser, jornadashtml, jornadashtml2, jornadashtml3)
    jornadaslist = zip(*jornadaslist)

    ############################
    for x in guardiasobj:
        for i in x:
            guardias.append(i)

    for x in guardias:
        guardiasfini.append(x.fini)
        guardiasffin.append(x.ffin)
        guardiasuser.append(x.user.username)
        guardiasid.append(x.id)

    guardiashtml = []
    guardiashtml2 = []
    guardiashtml3 = []
    for x in guardiasid:
        guardiashtml.append("<td><a href=\"/guardias/editar/" + str(x) + "\"><i class=\"icon-list-alt\"></i></td>")
        guardiashtml2.append("<td><a  onclick=\"alert('Aprobado')\" href=\"/guardias/aprobar/" + str(x) + "\"><i class=\"icon-ok-circle\"></i></td>")
        guardiashtml3.append("<td><a  onclick=\"alert('Rechazado')\" href=\"/guardias/rechazar/" + str(x) + "\"><i class=\"icon-ban-circle\"></i></td>")

    guardiaslist = (guardiasfini, guardiasffin, guardiasuser, guardiashtml, guardiashtml2, guardiashtml3)
    guardiaslist = zip(*guardiaslist)

    ############################
    for x in intervencionesobj:
        for i in x:
            intervenciones.append(i)

    for x in intervenciones:
        intervencionesfini.append(x.fini)
        intervencionesffin.append(x.ffin)
        intervencionesobservaciones.append(x.observaciones)
        intervencionesuser.append(x.user.username)
        intervencionesid.append(x.id)

    intervencioneshtml = []
    intervencioneshtml2 = []
    intervencioneshtml3 = []

    for x in intervencionesid:
        intervencioneshtml.append("<td><a href=\"/intervenciones/editar/" + str(x) + "\"><i class=\"icon-list-alt\"></i></td>")
        intervencioneshtml2.append("<td><a  onclick=\"alert('Aprobado')\" href=\"/intervenciones/aprobar/" + str(x) + "\"><i class=\"icon-ok-circle\"></i></td>")
        intervencioneshtml3.append("<td><a  onclick=\"alert('Rechazado')\" href=\"/intervenciones/rechazar/" + str(x) + "\"><i class=\"icon-ban-circle\"></i></td>")

    intervencioneslist = (intervencionesfini, intervencionesffin, intervencionesobservaciones, intervencionesuser, intervencioneshtml,
        intervencioneshtml2, intervencioneshtml3)
    intervencioneslist = zip(*intervencioneslist)

    return render_to_response(
        'consola.html',
        {'user': request.user,
         'usergroup': profile.grupo.nombregrupo,
         'userrol': profile.rol.nombrerol,
         'vacacioneslist': vacacioneslist,
         'guardiaslist': guardiaslist,
         'intervencioneslist': intervencioneslist,
         'jornadaslist': jornadaslist,
        }
    )
