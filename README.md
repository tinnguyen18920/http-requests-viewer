# HTTP Requests Viewer

A django app to view all http(s) from driver session using [selenium-wire](https://pypi.org/project/selenium-wire/)

## Installation

1. Using pip:

```bash
pip install http-requests-viewer
```

2. Add "bootstrap4" and "http_requests_viewer" in INSTALLED_APPS setting:

```python
INSTALLED_APPS = (
  # ...
  'bootstrap4',
  'http_requests_viewer',
  # ...
)
```

3. Include the http_requests_viewer URLconf in your project urls.py:

```python
urlpatterns = [
    # ...
    path('hr-viewer/', include('http_requests_viewer.urls')),
    # ...
]
```


4. Run `python manage.py migrate` to create the models.

5. Run `python manage.py runserver`

6. Visit http://127.0.0.1:8000/hr-viewer/agents/ to create new agent.

7. Visit http://127.0.0.1:8000/hr-viewer/targets/new/ to create new target.
