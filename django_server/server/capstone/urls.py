from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'django.views.generic.simple.direct_to_template', {
		'template': 'homepage.html',
	}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
        'show_indexes': True
    }),
    (r'^admin_static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.ADMIN_MEDIA_ROOT,
        'show_indexes': False
    }),
    (r'^admin/', include(admin.site.urls)),
)