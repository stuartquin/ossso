from django.contrib import admin
from django.utils.html import format_html

from sso import models


class DomainInline(admin.TabularInline):
    extra = 1
    model = models.Domain
    readonly_fields = [
        "guid",
    ]


class SAMLConnectionAdmin(admin.ModelAdmin):
    inlines = [DomainInline]

    def sso_url_link(self, instance):
        url = instance.sso_url
        return format_html('<a href="{}">{}</a>', url, url)

    sso_url_link.short_description = "SSO URL"

    def acs_url_link(self, instance):
        url = instance.acs_url
        return format_html('<a href="{}">{}</a>', url, url)

    sso_url_link.short_description = "SSO URL"
    acs_url_link.short_description = "ACS URL"
    readonly_fields = ("sso_url_link", "acs_url_link")


class OrganizationAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Account)
admin.site.register(models.Organization, OrganizationAdmin)
admin.site.register(models.SAMLResponse)
admin.site.register(models.SAMLConnection, SAMLConnectionAdmin)
