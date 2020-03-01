from django.contrib import admin

from .models import Topic, Entry


class EntryAdmin(admin.ModelAdmin):
    readonly_fields = ['date_added']
    fieldsets = [
        (None, {'fields': ['topic', 'text']}),
        ('Date information', {'fields': ['date_added'], 'classes': ['collapse']}),
    ]
    list_display = ('topic', 'text', 'date_added', 'was_published_recently')
    list_filter = ['date_added']
    search_fields = ['text']


admin.site.register(Topic)
admin.site.register(Entry, EntryAdmin)
