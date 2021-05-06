from http_requests_viewer.models import Agent, Target, ExcludeHost
from http_requests_viewer.extractor import Wire
from django import forms


class AgentCreationForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['string']

class ExcludeHostCreationForm(forms.ModelForm):
    class Meta:
        model = ExcludeHost
        fields = '__all__'

class TargetCreationForm(forms.ModelForm):
    debug = forms.BooleanField(required=False, help_text="Manual perform actions on the driver then run `continue` command on terminal to finish")

    class Meta:
        model = Target
        fields = ['url', 'debug','note', 'agent', 'exclude_hosts']
        widgets = {
            "exclude_hosts": forms.CheckboxSelectMultiple()
        }

    def save(self, *args, **kwargs): 
        target = super().save(*args, **kwargs)
        debug = self.cleaned_data['debug']
        wire = Wire(target.url, target.agent.string)
        exclude_hosts = target.list_exclude_hosts
        target.http_requests = wire.get_http_requests(debug=debug, exclude_hosts=exclude_hosts)
        target.save()
        return target