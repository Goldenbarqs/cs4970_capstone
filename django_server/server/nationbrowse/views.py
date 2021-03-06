# coding=utf-8
"""
Default, root-level views for the site
"""

from __future__ import division
from django.http import HttpResponse
from cacheutil import safe_get_cache,safe_set_cache,USING_DUMMY_CACHE
from django.shortcuts import get_object_or_404,render_to_response
from django.http import HttpResponseRedirect,HttpResponsePermanentRedirect,Http404
from django.core.urlresolvers import reverse
from random import choice as rand_choice
from django.template import RequestContext
from django.template.defaultfilters import urlencode
from django.views.decorators.cache import cache_control,never_cache

from nationbrowse.places.models import State,County

from threadutil import call_in_bg

@cache_control(public=True,max_age=604800)
def nation_overview(request):
    states = State.objects.exclude(poly=None)

    response=render_to_response("homepage.html",{
        'states':states,
    },context_instance=RequestContext(request))

    return response
