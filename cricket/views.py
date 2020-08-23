from django.shortcuts import render
from django.views.generic import View
from django.http import Http404
# Create your views here.
from cricket.models import Team, Player, Match


def index(request):
    """
    :param request:
    :return:

    this function will returns home page data in context
    """

    context = {}
    context['teams_count'] = Team.objects.count()
    context['players_count'] = Player.objects.count()
    context['match_count'] = Match.objects.count()

    return render(request, 'index.html', context=context)


def teams(request, slug=None):
    """

    :param request:
    :param slug:
    :return:

    This views return all teams and team's players data on base of team_slug argument.
    """

    context = {}

    if slug:
        try:
            context['team'] = Team.objects.prefetch_related('players').get(slug=slug)

        except Team.DoesNotExist:
            raise Http404

        return render(request, 'team.html', context=context)

    else:
        context['teams'] = Team.objects.prefetch_related('players').all()

        return render(request, 'team.html', context)


def players(request, slug=None):
    """

    :param request:
    :param slug:
    :return:

    This view return all players and single player data on base of player_slug.
    """
    context = {}
    if not slug:
        context['players'] = Player.objects.select_related('team').all()

    else:
        try:
            context['player'] = Player.objects.select_related('team').get(slug=slug)

        except Team.DoesNotExist:
            raise Http404

    return render(request, 'player.html', context)


