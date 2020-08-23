from django.contrib import admin
from django.utils.html import mark_safe


from cricket.models import Team, Player, Match, Performance

# Register your models here.


class TeamAdmin(admin.ModelAdmin):

    class Meta:
        model = Team
    list_display = ('name', 'slug', 'preview_image')
    prepopulated_fields = {'slug': ('name', ), }
    readonly_fields = ('preview_image',)

    def preview_image(self, instance):
        if instance.logo:
            url = instance.logo.url
            if url:
                return mark_safe(u'<img src="%s" style="height:auto;" width="250px" />' % (url,))
        return ''
    preview_image.short_description = 'Preview'
    preview_image.allow_tags = True


class PlayerAdmin(admin.ModelAdmin):

    class Meta:
        model = Player

    list_display = ('first_name', 'last_name', 'team', 'preview_image')
    prepopulated_fields = {'slug': ('first_name', 'last_name'), }

    readonly_fields = ('preview_image',)

    def preview_image(self, instance):
        if instance.avatar:
            url = instance.avatar.url
            if url:
                return mark_safe(u'<img src="%s" style="height:auto;" width="250px" />' % (url,))
        return ''
    preview_image.short_description = 'Preview'
    preview_image.allow_tags = True


class MatchAdmin(admin.ModelAdmin):

    class Meta:
        model = Match

    list_display = ('home_team', 'away_team', 'winner_team')


class PerformanceAdmin(admin.ModelAdmin):

    class Meta:
        model = Performance


admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Performance, PerformanceAdmin)