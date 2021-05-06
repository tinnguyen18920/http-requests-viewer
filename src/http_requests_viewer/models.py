from django.db import models
from django.urls import reverse
from user_agents import parse


class Agent(models.Model):
    string = models.CharField(max_length=200, unique=True, help_text="Agent string")
    device = models.CharField(blank=True, max_length=100)
    os = models.CharField(blank=True, max_length=100)
    browser = models.CharField(blank=True, max_length=100)
    is_bot = models.CharField(blank=True, max_length=100)

    def __str__(self):
        bot = "bot" if self.is_bot == True else "human"
        return f"{self.device} - {bot} - {self.browser} - {self.os}"

    def save(self, **kwargs):
        agent_data = parse(self.string)
        self.device = agent_data.get_device()
        self.os = agent_data.get_os()
        self.isBot = agent_data.is_bot
        self.browser = agent_data.get_browser()
        super(Agent, self).save(**kwargs)

    class Meta:
        ordering = ['-device']


class ExcludeHost(models.Model):
    """
        Disable capture http_requests from this host
    """
    host = models.CharField(max_length=200, unique=True, help_text="Example: *googleapis.com")

    def __str__(self):
        return self.host

class Target(models.Model):
    """
       Target to crawl http_requests, ... 
    """
    url = models.URLField(help_text="URL to capture http requests")

    # Agent is used
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True)

    #
    exclude_hosts = models.ManyToManyField(ExcludeHost, blank=True)

    # All http_requests
    http_requests = models.JSONField(null=True, blank=True)

    note = models.CharField(max_length=200, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def list_exclude_hosts(self):
        if self.exclude_hosts:
            return [host.host for host in self.exclude_hosts.all()]
        else:
            return []
    

    def __str__(self):
        return f"{self.url} - {self.note}"

    def get_absolute_url(self):
        return reverse("http_requests_viewer:target_detail", args=[self.id])

    class Meta:
        ordering = ['-created_at']