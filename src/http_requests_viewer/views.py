from http_requests_viewer.models import Agent, Target, ExcludeHost
from http_requests_viewer.forms import AgentCreationForm, TargetCreationForm, ExcludeHostCreationForm

from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django import http

class AgentListAndCreateView(generic.ListView):
    template_name = "http_requests_viewer/agent_list_n_create.html"
    form_class = AgentCreationForm
    success_message = "Agent created"
    context_object_name = "objects"
    delete_viewname = "http_requests_viewer:agent_delete"
    def get_queryset(self):
        return Agent.objects.all()

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs: # GET method
            kwargs['form'] = self.get_form()
            kwargs['delete_viewname'] = self.delete_viewname

        return super().get_context_data(**kwargs)

    def get_form(self):
        """"""
        return self.form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """"""
        kwargs = {
            'initial': {},
            'prefix': None,
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_success_url(self):
        return reverse("http_requests_viewer:agent_list")

    def post(self, request, *args, **kwargs):
        """"""
        form = self.get_form()
        if form.is_valid():
            agent = form.save()
            messages.success(request, self.success_message)
            return http.HttpResponseRedirect(self.get_success_url())
        else:
            return self.get(request=request, form=form)

class ExcludeHostListAndCreateView(AgentListAndCreateView):
    form_class = ExcludeHostCreationForm
    success_message = "Exclude host created"
    delete_viewname = "http_requests_viewer:exclude_host_delete"
    def get_queryset(self):
        return ExcludeHost.objects.all()

    def get_success_url(self):
        return reverse("http_requests_viewer:exclude_host_list")


class AgentDeleteView(generic.DeleteView):
    """"""
    model = Agent

    def get_success_url(self):
        return reverse("http_requests_viewer:agent_list")

class ExcludeHostDeleteView(AgentDeleteView):
    model = ExcludeHost

    def get_success_url(self):
        return reverse("http_requests_viewer:exclude_host_list")

class TargetCreateView(generic.CreateView):
    template_name = "http_requests_viewer/target_create.html"
    form_class = TargetCreationForm

class TargetListView(generic.ListView):
    template_name = "http_requests_viewer/target_list.html"
    context_object_name = "targets"
    def get_queryset(self):
        return Target.objects.all()

class TargetDetailView(generic.DetailView):
    model = Target
    template_name = "http_requests_viewer/target_detail.html"

class TargetDeleteView(generic.DeleteView):
    model = Target

    def get_success_url(self):
        return reverse("http_requests_viewer:target_list")


class RequestDetailView(generic.DetailView):
    template_name = "http_requests_viewer/request_detail.html"
    context_object_name = "request"
    
    def get_object(self):
        target = Target.objects.get(pk=self.kwargs['pk'])
        http_request = next((r for r in target.http_requests if r["id"] == self.kwargs['request_id']), None)
        http_request['target_id'] = target.pk
        return http_request


class RequestResponseView(generic.View):

    def get_object(self):
        target = Target.objects.get(pk=self.kwargs['pk'])
        request = next((r for r in target.http_requests if r["id"] == self.kwargs['request_id']), None)
        # request['target_id'] = target.pk
        return request

    def get(self, request, *args, **kwargs):
        http_request = self.get_object()
        content_type = request.GET.get("content_type", http_request['content_type']['response'])
        try:
            content = http_request['response']['body']
        except:
            content = ""
        response = http.HttpResponse(content=content, content_type=content_type)
        return response