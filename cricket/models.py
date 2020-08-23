from django.db import models
from django.template.defaultfilters import slugify
from django.utils.timezone import now
from django.db.models import Sum, F, Max, Q

# Create your models here.

COUNTRIES = (
        (1, 'India'),
        (2, 'South Africa'),
        (3, 'Pakistan'),
        (4, 'Nepal'),
    )


class Team(models.Model):
    name = models.CharField(max_length=255)
    club = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='team.logo', max_length=255, blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Team, self).save(*args, **kwargs)

    def get_match_played(self):
        ''' Gets match played by team '''
        return Match.objects.filter(Q(home_team=self) | Q(away_team=self)).count()

    def get_match_wins_count(self):
        ''' Gets match wins by team '''
        return Match.objects.filter(winner_team=self).count()

    def get_match_loss_count(self):
        ''' Gets match loss by team '''
        return self.get_match_played() - self.get_match_wins_count()


class Player(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to='player.avatar', max_length=255, blank=True, null=True)
    jersey_number = models.IntegerField(default=0)
    team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE)
    country = models.IntegerField(choices=COUNTRIES, default=1)

    objects = models.Manager()

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.first_name + '-' + self.last_name)
        super(Player, self).save(*args, **kwargs)

    def full_name(self):
        ''' Gets full name of player '''
        return self.first_name + ' ' + self.last_name

    def get_match_played(self):
        ''' Gets match played count by player '''
        return Performance.objects.filter(player=self).count()

    def get_runs_count(self):
        ''' Gets total runs by player '''
        return Performance.objects.filter(player=self).aggregate(Sum('runs'))['runs__sum']

    def get_50s_count(self):
        ''' Gets number of times 50 to 99 runs scored by player'''
        return Performance.objects.filter(player=self, runs__range=[50, 99]).count()

    def get_100s_count(self):
        ''' Gets number of times 100+ runs scored by player'''
        return Performance.objects.filter(player=self, runs__gte=100).count()

    def get_highest_score(self):
        ''' Gets players highest score '''
        return Performance.objects.filter(player=self).aggregate(Max('runs'))['runs__max']


class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')
    winner_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='winner_team')
    match_date = models.DateField(blank=True, default=now, help_text='The date when this match will be play.')

    class Meta:
        verbose_name_plural = "Matches"

    def __str__(self):
        return self.home_team.name + ' v/s ' + self.away_team.name

    objects = models.Manager()


class Performance(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    runs = models.IntegerField(default=0)
    balls_faced = models.IntegerField(default=0)

    objects = models.Manager()

    class Meta:
        unique_together = ('match', 'player')