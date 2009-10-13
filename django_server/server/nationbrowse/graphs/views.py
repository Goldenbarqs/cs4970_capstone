# coding=utf-8
from __future__ import division
from django.http import HttpResponse
from cacheutil import safe_get_cache,safe_set_cache
from django.shortcuts import get_object_or_404
from django.http import Http404

from nationbrowse.demographics.models import PlacePopulation
from nationbrowse.places.models import County

from django.db.models.loading import get_model

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import graph_maker

def render_graph(request,place_type,slug,graph_type,size=700):
    """
    Generates a png pie graph of the given location's racial breakdown. Example
    URLs include:
    /graphs/state/missouri/race_pie/
    /graphs/zipcode/65201/race_pie/
    /graphs/county/boone-missouri/race_pie/
    
    See render_graph_county, below, for a version with nicer URL arguments.
    """
    # Check if we have a cache of this render, with the same request parameters ...
    # Set the cache based on the specific object we got (place_type + place_id)
    cache_key = "render_graph place_type=%s slug=%s graph_type=%s size=%s" % (place_type, slug, graph_type, size)
    response = safe_get_cache(cache_key)
    
    # If it wasn't cached, do all of this fancy logic and generate the image as a PNG
    if not response:
        # 404 if graph_type is invalid
        if hasattr(graph_maker, 'generate_%s' % graph_type):
            graph_generator = getattr(graph_maker, 'generate_%s' % graph_type)
        else:
            raise Http404
        
        # 404 if the PlaceType is invalid
        PlaceClass = get_model("places",place_type)
        if not PlaceClass:
            raise Http404
        
        # 404 if place slug is invalid
        if place_type.lower() == "zipcode":
            # Querying ZipCode by numeric ID is *MUCH* quicker than string
            place = get_object_or_404(PlaceClass,id=slug)
        else:
            place = get_object_or_404(PlaceClass,slug=slug)
        
        # Generate the graph & render it as a PNG to the HTTP response
        fig = graph_generator(place,size)
        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)
        
        # Save the response to cache
        safe_set_cache(cache_key,response,86400)

    # Return the response that was either cached OR generated just now.
    return response

def render_graph_county(request,state_abbr,name,graph_type,size=700):
    """
    An alternative view to above, with nicer URL structure for county browsing:
    /graphs/county/mo/boone/race_pie/
    """
    cache_key = "render_graph_county state_abbr=%s name=%s graph_type=%s size=%s" % (state_abbr, name, graph_type, size)
    response = safe_get_cache(cache_key)
    
    if not response:
        if hasattr(graph_maker, 'generate_%s' % graph_type):
            graph_generator = getattr(graph_maker, 'generate_%s' % graph_type)
        else:
            raise Http404

        place = get_object_or_404(County,state__abbr__iexact=state_abbr,name__iexact=name)

        fig = graph_generator(place,size)
        canvas=FigureCanvas(fig)
        response=HttpResponse(content_type='image/png')
        canvas.print_png(response)
        
        # Save the response to cache
        safe_set_cache(cache_key,response,86400)

    # Return the response that was either cached OR generated just now.
    return response

