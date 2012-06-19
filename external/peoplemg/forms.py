from django import forms


class JornadasForm(forms.Form):
    mes = forms.CharField(label='Mes')
    numdias = forms.CharField(label='Numero dias')


class GuardiasForm(forms.Form):
    fini = forms.DateTimeField(label='Fecha Inicio', widget=forms.DateTimeInput)
    ffin = forms.DateTimeField(label='Fecha Fin', widget=forms.DateTimeInput)


class IntervencionesForm(forms.Form):
    fini = forms.DateTimeField(label='Fecha Inicio', widget=forms.DateTimeInput)
    ffin = forms.DateTimeField(label='Fecha Fin', widget=forms.DateTimeInput)
    obs = forms.CharField(label='Observaciones')


class VacacionesForm(forms.Form):
    fini = forms.DateField(label='Fecha Inicio', widget=forms.DateInput)
    ffin = forms.DateField(label='Fecha Fin', widget=forms.DateInput)


class VacacionesEditarForm(forms.Form):
    fini = forms.DateField(label='Fecha Inicio', widget=forms.DateInput)
    ffin = forms.DateField(label='Fecha Fin', widget=forms.DateInput)
    fid = forms.CharField(label='ID')


class JornadaEditarForm(forms.Form):
    mes = forms.CharField(label='Mes', widget=forms.TextInput)
    numdias = forms.CharField(label='Numero dias', widget=forms.TextInput)
    fid = forms.CharField(label='ID')


class GuardiaEditarForm(forms.Form):
    fini = forms.DateTimeField(label='Fecha Inicio', widget=forms.DateTimeInput)
    ffin = forms.DateTimeField(label='Fecha Fin', widget=forms.DateTimeInput)
    fid = forms.CharField(label='ID')


class IntervencionEditarForm(forms.Form):
    fini = forms.DateTimeField(label='Fecha Inicio', widget=forms.DateTimeInput)
    ffin = forms.DateTimeField(label='Fecha Fin', widget=forms.DateTimeInput)
    obs = forms.CharField(label='Observaciones')
    fid = forms.CharField(label='ID')
