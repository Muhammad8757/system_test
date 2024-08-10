from django.contrib import admin
from .models import User, Subjects, Theme, Tests, Answers, Activate
models = [User, Subjects, Theme, Tests, Answers, Activate]
for model in models:
    admin.site.register(model)