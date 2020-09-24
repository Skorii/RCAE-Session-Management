from django.contrib import admin
from django.utils.html import format_html
from .models import Member, Section, Session


@admin.register(Member)
class MemberDisplay(admin.ModelAdmin):
    search_fields = ['last_name', 'first_name']
    list_display = ('last_name', 'first_name', 'rcae_number', 'subscription_number', 'e_mail', 'session')


@admin.register(Section)
class SectionDisplay(admin.ModelAdmin):
    list_display = ('code', 'name', 'subscription', 'active')
    actions = ['activate_selected', 'deactivate_selected']

    def deactivate_selected(self, request, queryset):
        for section in queryset:
            tmp = Section.objects.get(code=section.code)
            tmp.active = False
            tmp.save()
    deactivate_selected.short_description = "Désactiver les Sections sélectionnés"

    def activate_selected(self, request, queryset):
        for section in queryset:
            tmp = Section.objects.get(code=section.code)
            tmp.active = True
            tmp.save()
    activate_selected.short_description = "Activer les Sections sélectionnés"


@admin.register(Session)
class SessionDisplay(admin.ModelAdmin):
    date_hierarchy = 'date_time'
    list_display = ('section', 'date_time', 'duration', 'location', 'max_members', 'list_member',)
    list_filter = ('section', 'date_time',)
    actions = ['export_as_csv']

    @staticmethod
    def list_member(session):
        if Section.objects.get(code=session.section.code).subscription:
            return format_html("<br />".join([member.__str__() + " (" + member.rcae_number + " - " + member.subscription_number + ")" for member in Member.objects.filter(session=session.id)]))
        else:
            return format_html("<br />".join([member.__str__() + " (" + member.rcae_number + ")" for member in Member.objects.filter(session=session.id)]))

    def export_as_csv(self, request, queryset):
        # Implement csv export
        pass

    export_as_csv.short_description = "Exporter la sélection en CSV"
