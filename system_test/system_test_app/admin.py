from django.contrib import admin
from .models import User, Subject, Theme, Test, Answer, Activate
models = [User, Subject, Theme, Test, Answer, Activate]
for model in models:
    admin.site.register(model)