from django.contrib import admin

from .models import Alias, Close, Create, Delete, IndexSet, Mappings, Optimize, Settings, Snapshot

admin.site.register(Alias)
admin.site.register(Close)
admin.site.register(Create)
admin.site.register(Delete)
admin.site.register(IndexSet)
admin.site.register(Mappings)
admin.site.register(Optimize)
admin.site.register(Settings)
admin.site.register(Snapshot)
