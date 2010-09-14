from django.shortcuts import get_list_or_404, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.contrib.auth.decorators import login_required
from vendors.models import Vendor
from vendors.forms import VendorForm, MarketSignUpForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from tagging.models import Tag, TaggedItem
from django.conf import settings

import datetime

def vendor_index(request):
    vendors=Vendor.public_objects.all()
    return render_to_response('vendors/vendor_index.html', locals(),
                              context_instance=RequestContext(request))

def vendor_detail(request, slug):
    if request.user.is_authenticated():
	try:
       	    vendor=Vendor.objects.get(slug__exact=slug)
        except:
 	    raise Http404
    else:
        try:
            vendor=Vendor.public_objects.get(slug__exact=slug)
        except:
            raise Http404

    if request.META['SERVER_NAME']=='castinefarmersmarket.org':
        google_api_key=settings.GOOGLE_API_KEY_CFM
    elif request.META['SERVER_NAME']=='castinefm.org':
        google_api_key=settings.GOOGLE_API_KEY_FM
    else:
        google_api_key=''

    return render_to_response('vendors/vendor_detail.html', locals(),
                              context_instance=RequestContext(request))

#def vendor_tags(request):
#    return render_to_response('vendors/vendor_tag_list.html', locals(),
#                              context_instance=RequestContext(request))

#def vendors_with_tag(request, tag, object_id=None, page=1):
#    query_tag = Tag.objects.get(name=tag)
#    vendors = TaggedItem.objects.get_by_model(Vendor, tag)
#    vendors = vendors.order_by('name')
#    return render_to_response('vendors/vendors_with_tag.html', locals(),
#                              context_instance=RequestContext(request))



@login_required
def vendor_create(request):
    form=VendorForm(request.POST or None)
    if form.is_valid():
        vendor=form.save(commit=False)
        vendor.owner=request.user
        vendor.slug=slugify(vendor.name)
        vendor.save()
        return HttpResponseRedirect(reverse('vendor_detail', args=[vendor.slug]))
        
    return render_to_response('vendors/vendor_create.html', locals(),
                              context_instance=RequestContext(request))

@login_required
def vendor_edit(request, slug):
    instance = None
    if slug is not None:
        instance = Vendor.objects.get(slug__exact=slug)
        
    if request.method == 'POST':
        form=VendorForm(request.POST, instance=instance)
        if form.is_valid():
            vendor=form.save(commit=False)
            vendor.slug=slugify(vendor.name)
            vendor.save()
            return HttpResponseRedirect(reverse('vendor_detail', args=[vendor.slug]))
    else:
        form = VendorForm(instance=instance)
        
    return render_to_response('vendors/vendor_edit.html', locals(),
                              context_instance=RequestContext(request))

@login_required
def vendor_signup(request, slug):
    if slug is not None:
        instance = Vendor.objects.get(slug__exact=slug)
        
    if request.method == 'POST':
        form=MarketSignUpForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('vendor_detail', args=[instance.slug]))
    else:
        form = MarketSignUpForm(instance=instance)
        
    return render_to_response('vendors/vendor_signup.html', locals(),
                              context_instance=RequestContext(request))

@login_required
def app_index(request):
    apps = Application.objects.all()
	return render_to_response('vendors/app_index.html', locals(),
								context_instance=RequestContext(request))
@login_required
def vendor_app_create(request):
	form=VendorAppForm(request.POST or None)
	if form.is_valid():
	    app=form.save(commit=False)
	    # Create a new application status object and set it to Pending
        status=ApplicationStatus.objects.create(application=app, status='P')
        status.save()
		app.save()
		return HttpResponseRedirect(reverse('vendor_app_detail', args=[app.vendor.slug, app.submission_date.year]))

	return render_to_response('vendors/vendor_app_create.html', locals(),
								context_instance=RequestContext(request))
								
@login_required
def vendor_app_edit(request, slug, year):
    instance = None
    if slug is not None:
        if year is not None:
            instance = Application.objects.get(slug__exact=slug, submission_date__year=year)
        
    if request.method == 'POST':
        form=VendorAppForm(request.POST, instance=instance)
        if form.is_valid():
            app=form.save()
            return HttpResponseRedirect(reverse('vendor_app_detail', args=[app.vendor.slug, app.submission_date.year]))
    else:
        form = VendorAppForm(instance=instance)
        
    return render_to_response('vendors/vendor_app_edit.html', locals(),
                              context_instance=RequestContext(request))
    