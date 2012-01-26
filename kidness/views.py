# coding: utf-8
from kidness.forms import KidnessContactForm
from django.shortcuts import render_to_response, HttpResponse
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.template.loader import get_template

def post_feedback(request):
    if request.method=="POST":
        print 'post request', request.POST
        form = KidnessContactForm(data=request.POST, files=request.FILES, request=request)
        
        if form.is_valid():
            form.save()#fail_silently=True)
            return HttpResponse()
        else:
            t = get_template('lfc/lfc_form.html')

            context = RequestContext(request, {'form':form})

            response = HttpResponse(t.render(context), status = 400)
            return response
            
#            return render_to_response('lfc/lfc_form.html', 
#                              {'form':form},
#                              context_instance=RequestContext(request),
#                              status_code=404
#                              )        


