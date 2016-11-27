from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cabinet.models import Team, Region
from django.conf import settings
from django.utils import timezone
import datetime

def get_regions_in_interval(left, right):
    regions = (Region
        .objects
        .filter(start_time__lt=right - settings.CONTEST_DURATION)
        .filter(start_time__gt=left - settings.CONTEST_DURATION))
    return regions

def get_team_infos_in_region(region, amount):
    teams = (Team
        .objects
        .filter(region=region)
        .order_by('-balance', 'submit_time', 'pk')[:amount])
    return [{'name': team.name, 'balance': team.balance} for team in teams]

def get_near_regions(l_offset, r_offset):
    now = timezone.now()
    left = now - datetime.timedelta(0, l_offset)
    right = now + datetime.timedelta(0, r_offset)
    return get_regions_in_interval(left, right)

def get_tour_info(l_offset, r_offset, amount):
    regions = get_near_regions(l_offset, r_offset)
    result = {}
    for region in regions:
        result[region.name] = get_team_infos_in_region(region, amount)
    return result

def print_tour_info(tour_info):
    for region, teams in tour_info.items():
        for team in teams:
            print(region, team['name'], team['balance'], sep="~")

class Command(BaseCommand):
    help = 'Creates default categories from file'

    def add_arguments(self, parser):
        parser.add_argument('left_offset', type=int, nargs='?', default=0)
        parser.add_argument('right_offset', type=int, nargs='?', default=3600)
        parser.add_argument('top_n', type=int, nargs='?', default=6)

    def handle(self, *args, **options):
        l_offset = options['left_offset']
        r_offset = options['right_offset']
        top_n = options['top_n']
        tour_info = get_tour_info(l_offset, r_offset, top_n)
        print_tour_info(tour_info)
