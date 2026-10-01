"""
Definition of urls for wald.
"""

from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
import django.contrib.auth.views
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt

# Enable the admin:
from wald.settings import APP_PREFIX, STATIC_ROOT

# Imports for the app 'dictionary'
import wald.dictionary.forms
from wald.dictionary.views import *
from wald.dictionary.adminviews import EntryListView, InfoListView

# Other Django stuff
# from django.core import urlresolvers
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy, path, re_path
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView

admin.autodiscover()

# set admin site names
admin.site.site_header = 'e-WALD Admin'
admin.site.site_title = 'e-WALD Site Admin'

pfx = APP_PREFIX

# ================ Custom error handling when debugging =============
def custom_page_not_found(request, exception=None):
    return wald.dictionary.views.view_404(request)

handler404 = custom_page_not_found

urlpatterns = [
    # Examples:
    re_path(r'^$', wald.dictionary.views.home, name='home'),
    path("404/", custom_page_not_found),
    re_path(r'^contact$', wald.dictionary.views.contact, name='contact'),
    re_path(r'^about', wald.dictionary.views.about, name='about'),
    re_path(r'^guide', wald.dictionary.views.guide, name='guide'),
    re_path(r'^robots.txt', TemplateView.as_view(template_name='dictionary/robots.txt', content_type='text/plain')),
    re_path(r'^delen', DeelListView.as_view(), name='delen'),
    re_path(r'^definitions$', RedirectView.as_view(url='/'+pfx+'admin/'), name='definitions'),
    re_path(r'^entries$', RedirectView.as_view(url='/'+pfx+'admin/dictionary/entry/'), name='entries'),
    re_path(r'^entries/import/$', permission_required('dictionary.search_gloss')(InfoListView.as_view()), name='admin_import_list'),
    re_path(r'^lemmas$', LemmaListView.as_view(), name='lemmas'),
    re_path(r'^lemma/search/$', LemmaListView.as_view(), name='lemmasearch'),
    re_path(r'^lemma/search/ajax/$', LemmaListView.as_view(), name='lemmasearch_ajax'),
    re_path(r'^lemma/map/(?P<pk>\d+)/$', csrf_exempt(LemmaMapView.as_view()), name='lemmamap'),
    re_path(r'^trefwoord/search/$', TrefwoordListView.as_view(), name='trefwoordsearch'),
    re_path(r'^dialects', DialectListView.as_view(), name='dialects'),
    re_path(r'^dialect/search/$', DialectListView.as_view(), name='dialectsearch'),
    re_path(r'^dialect/check/$', DialectCheckView.as_view(), name='dialectcheck'),
    re_path(r'^dialect/map/$', csrf_exempt(DialectMapView.as_view()), name='dialectmap'),
    re_path(r'^locations', LocationListView.as_view(), name='locations'),
    re_path(r'^location/search/$', LocationListView.as_view(), name='locationsearch'),
    re_path(r'^mines', MijnListView.as_view(), name='mines'),
    re_path(r'^mine/search/$', MijnListView.as_view(), name='minesearch'),
    re_path(r'^list/$', permission_required('dictionary.search_gloss')(EntryListView.as_view()), name='admin_entry_list'), 
    re_path(r'^dictionary/search/$', permission_required('dictionary.search_gloss')(EntryListView.as_view())),
    re_path(r'^entry/(?P<pk>\d+)', DictionaryDetailView.as_view(), name='output'),

    re_path(r'^import/start/$', wald.dictionary.views.import_csv_start, name='import_start'),
    re_path(r'^import/progress/$', wald.dictionary.views.import_csv_progress, name='import_progress'),

    re_path(r'^import/update(?:/(?P<pk>\d+))?/start/$', wald.dictionary.views.import_update_start, name='import_update_start'),
    re_path(r'^import/update(?:/(?P<pk>\d+))?/progress/$', wald.dictionary.views.import_update_progress, name='import_update_progress'),

    re_path(r'^repair/$', permission_required('dictionary.search_gloss')(wald.dictionary.views.do_repair), name='repair'),
    re_path(r'^repair/start/$', wald.dictionary.views.do_repair_start, name='repair_start'),
    re_path(r'^repair/progress/$', wald.dictionary.views.do_repair_progress, name='repair_progress'),
    re_path(r'^static/(?P<path>.*)$',django.views.static.serve, {'document_root': STATIC_ROOT}),

    re_path(r'^signup/$', wald.dictionary.views.signup, name='signup'),

    re_path(r'^login/user/(?P<user_id>\w[\w\d_]+)$', wald.dictionary.views.login_as_user, name='login_as'),

    re_path(r'^login/$', LoginView.as_view
        (
            template_name= 'dictionary/login.html',
            authentication_form= wald.dictionary.forms.BootstrapAuthenticationForm,
            extra_context= {'title': 'Log in','year': datetime.now().year,}
        ),
        name='login'),
    re_path(r'^logout$',  LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    #re_path(r'^login/$',
    #    django.contrib.auth.views.login,
    #    {
    #        'template_name': 'dictionary/login.html',
    #        'authentication_form': wald.dictionary.forms.BootstrapAuthenticationForm,
    #        'extra_context':
    #        {
    #            'title': 'Log in',
    #            'year': datetime.now().year,
    #        }
    #    },
    #    name='login'),
    #re_path(r'^logout$',
    #    django.contrib.auth.views.logout,
    #    {
    #        'next_page': reverse_lazy('home'),
    #    },
    #    name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    re_path(r'^admin/', admin.site.urls, name='admin_base'),
]
