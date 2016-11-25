#!/usr/bin/python3

import json
import sys
import csv
from checker.models import Task
from checker.models import Flag
from cabinet.models import Team
from cabinet.models import User
from cabinet.models import Region


RATED_TEAMS_FILE = 'rated_teams.csv'
UNRATED_TEAMS_FILE = 'unrated_teams.csv'

flag_files = [
    ('Git', 'git_flags.json'),
    ('Optimization', 'optimization_flags.json'),
    ('Weather', 'weather_flags.json'),
    ('Hard Reverse', 'hard_reverse_flags.json'),
    ('Easy Reverse', 'easy_reverse_flags.json')
]

replace_info_files = [
    'git_replacements.json',
    'optimization_replacements.json',
    'weather_replacements.json',
    'hard_reverse_replacements.json',
    'easy_reverse_replacements.json',
    ]

class AggregatedTeam:
    def __init__(self, *, region, region_name, start_time, team_name, login, password):
        self.region = region
        self.region_name = region_name
        self.start_time = start_time
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
            region='',
            region_name='spare-' + start_time,
            start_time=start_time,
            team_name='spare-team-' + str(len(teams) + 1),
            login=row[3],
            password=row[4]))
    return teams

def get_or_add_region(name, title, start_time):
    try:
        return Region.objects.get(name)
    except Region.DoesNotExist:
        region = Region(name=name, title=title, start_time=start_time)
        region.save()
        return region

def create_teams(teams, replace_info_provider, flag_provider):
    for i, team in enumerate(teams):
        index = i + 1
        replace_info = replace_info_provider.build_replace_info_for_index(index)
        user = User(username=team.login, password=team.password)
        user.save()
        region = get_or_add_region(team.region, team.region_name, team.start_time)
        dbteam = Team(
            name=team.team_name,
            user=user,
            replace_info=replace_info,
            region=region,
            is_visible=True)
        dbteam.save()
        for task_name, flag in flag_provider.get_flags_for_index(index):
            dbflag = Flag(
                team=dbteam,
                task=Task.objects.get(title=task_name),
                flag=flag)
            dbflag.save()


class ReplaceInfoProvider:
    def __init__(self):
        self.replacement_sets = []

    def add_from_file(self, filename):
        with open(filename) as f:
            self.replacement_sets.append(json.load(f))

    def build_replace_info_for_index(self, index):
        result = []
        for replacement_set in self.replacement_sets:
            pattern = replacement_set['pattern']
            replacement = replacement_set['replacement'][str(index)]
            result.append([pattern, replacement])
        return result

class FlagProvider:
    def __init__(self):
        self.flag_sets = []

    def add_from_file(self, filename, taskname):
        with open(filename) as f:
            flags = json.load(f)
        self.flag_sets.append([taskname, flags])

    def get_flags_for_index(self, index):
        result = []
        for task_name, flag_set in self.flag_sets:
            result.append((task_name, flag_set[str(index)]))
        return result

def main():
    replace_info_provider = ReplaceInfoProvider()
    for filename in replace_info_files:
        replace_info_provider.add_from_file(filename)

    flag_provider = FlagProvider()
    for task, filename in flag_files:
        flag_provider.add_from_file(filename, task)
    
    teams = get_rated_teams() + get_unrated_teams()

    create_teams(teams, replace_info_provider, flag_provider)

if __name__ == '__main__':
    main()
