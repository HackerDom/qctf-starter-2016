#!/usr/bin/python3

import json
import sys
import csv
import datetime
import os

from django.core.management.base import BaseCommand
from django.utils import timezone
from checker.models import Task
from checker.models import Flag
from cabinet.models import Team
from cabinet.models import User
from cabinet.models import Region


RATED_TEAMS_FILE = 'rated_teams.csv'
UNRATED_TEAMS_FILE = 'unrated_teams.csv'

class AggregatedTeam:
    def __init__(self, *, region, region_name, start_time, team_name, login, password):
        self.region = region
        self.region_name = region_name
        self.team_name = team_name
        self.login = login
        self.password = password

    @staticmethod
    def from_row(row):
        assert len(row) == 7
        return AggregatedTeam(
            region = row[1],
            region_name = row[2],
            start_time = row[3],
            team_name = row[4],
            login = row[5],
            password = row[6])

def get_csv_rows(filename):
    with open(filename, newline='') as f:
        return list(csv.reader(f))[1:]

def get_rated_teams():
    rows = get_csv_rows(RATED_TEAMS_FILE)
    return list(map(AggregatedTeam.from_row, rows))

def get_unrated_teams():
    rows = get_csv_rows(UNRATED_TEAMS_FILE)
    teams = []
    for row in rows:
        assert len(row) == 5
        start_time = row[1]
        teams.append(AggregatedTeam(
            region='Spare region MSK' + start_time,
            region_name='spare-' + start_time,
            start_time=start_time,
            team_name='spare-team-' + str(len(teams) + 1),
            login=row[3],
            password=row[4]))
    return teams

def fix_teams(teams):
    for team in teams:
        user = User(username=team.login)
        user.set_password(team.password)
        user.save()

def main():
    teams = get_rated_teams() + get_unrated_teams()
    fix_teams(teams)

class Command(BaseCommand):
    help = 'Fix users'

    def add_arguments(self, parser):
        parser.add_argument('configs_path', type=str)

    def handle(self, *args, **options):
        initial_path = os.path.abspath(os.path.curdir)
        os.chdir(options['configs_path'])
        try:
            self.stdout.write('Going to fix users, ' +
            'using csv data from {}'.format(os.path.abspath(os.path.curdir)))
            main()
            self.stdout.write(self.style.SUCCESS('Done'))
        finally:
            os.chdir(initial_path)

if __name__ == '__main__':
    main()
