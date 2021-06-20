from typing import List, Tuple
from bs4 import BeautifulSoup
import weather_exceptions
import requests
import re

# TODO: Documentation


class SWO(object):
    def __init__(self) -> None:
        self.__otlk_type = None
        self.valid_time = None
        self.hail_otlks = None
        self.wind_otlks = None
        self.tornado_otlks = None
        self.categorical_otlks = None
        self.probabilistic_otlks = None

    def set_otlk_type(self, otlk_type) -> None:
        if otlk_type not in (1, 2, 3):
            raise weather_exceptions.InvalidOutlookTypeError(otlk_type)
        self.__otlk_type = {1: 'day_1_otlk', 2: 'day_2_otlk', 3: 'day_3_otlk'}[otlk_type]

    def get_otlk_type(self) -> str:
        return self.__otlk_type

    def __parse_points(self, raw_text: str, raw_otlks: dict) -> dict:
        multispace_re = '[ ]{2,}'
        for area, otlk in raw_otlks.items():
            if area == len(raw_otlks):
                otlk['points'] = re.sub(multispace_re, ' ',
                                        raw_text[otlk['end'] + 1:]
                                        .replace("\\n", " ").replace("\\", " ")
                                        .strip(' ')).split(' ')
            elif area != len(raw_otlks):
                otlk['points'] = re.sub(multispace_re, ' ',
                                        raw_text[otlk['end'] + 1:raw_otlks[area + 1]['start'] - 1]
                                        .replace("\\n", " ").replace("\\", " ")
                                        .strip(' ')).split(' ')
            otlk['points'] = self.__format_points(otlk['points'])
        return raw_otlks

    def __format_points(self, points: List[str]) -> List[Tuple[float, float]]:
        formatted_points = []
        for coord in points:
            north = coord[:4]
            west = coord[4:]
            north = north[:2] + '.' + north[2:]
            west = west[:2] + '.' + west[2:]
            if west[0] in ('0', '1', '2'):
                west = '1' + west
            west = '-' + west
            north = float(north)
            west = float(west)
            formatted_points.append((west, north))
        return formatted_points

    # noinspection PyTypeChecker
    def get_otlk(self) -> None:
        if self.__otlk_type is None:
            raise weather_exceptions.OutlookTypeNotSetError()
        # get archive page
        url = "https://www.spc.noaa.gov/products/outlook/{}.html".format({'day_1_otlk': 'day1otlk',
                                                                          'day_2_otlk': 'day2otlk',
                                                                          'day_3_otlk': 'day3otlk'}[self.__otlk_type])
        otlk_page = requests.get(url)
        if str(otlk_page) != '<Response [200]>':
            raise weather_exceptions.UnableToRetrieveSWOError(otlk_page)
        soup = BeautifulSoup(otlk_page.content, 'html.parser')
        results = soup.find_all("a")

        index = 54
        while 'archive' not in str(results[index].get('href')):  # this is stupid, maybe will fix
            index += 1
        archive_url = 'https://www.spc.noaa.gov' + str(results[index].get('href'))

        archive_page = requests.get(archive_url)
        archive_content = str(archive_page.content)
        non_cat_re = '[0-1][.][0-9]{2}|[S][IG]{2}'  # re for tornado hail and wind
        cat_re = '[TMSEH]{1}[A-Z]{2,3}'  # re for categorical

        # get spcswo data
        # general data
        valid_time = re.findall('[0-9]{6}[Z].{3}[0-9]{6}[Z]', archive_content)[0]

        # empty otlks_raw means less than 2% all areas (other than categorical)
        # tornado outlook
        if self.__otlk_type != 'day_3_otlk':
            tornado_raw = archive_content.split('... TORNADO ...')[1]
            tornado_raw = tornado_raw.split('&&')[0]
            tornado_otlks = {}
            tornado_area = 1
            for match in re.finditer(non_cat_re, tornado_raw):
                tornado_otlks[tornado_area] = {'probability': match[0],
                                               'start': match.start(),
                                               'end': match.end(),
                                               'points': None}
                tornado_area += 1

            self.tornado_otlks = self.__parse_points(tornado_raw, tornado_otlks)

        # hail outlook
        if self.__otlk_type != 'day_3_otlk':
            hail_raw = archive_content.split('... HAIL ...')[1]
            hail_raw = hail_raw.split('&&')[0]
            hail_otlks = {}
            hail_area = 0
            for match in re.finditer(non_cat_re, hail_raw):
                hail_area += 1
                hail_otlks[hail_area] = {'probability': match[0],
                                         'start': match.start(),
                                         'end': match.end(),
                                         'points': None}

            self.hail_otlks = self.__parse_points(hail_raw, hail_otlks)

        # wind outlook
        if self.__otlk_type != 'day_3_otlk':
            wind_raw = archive_content.split('... WIND ...')[1]
            wind_raw = wind_raw.split('&&')[0]
            wind_otlks = {}
            wind_area = 1
            for match in re.finditer(non_cat_re, wind_raw):
                wind_otlks[wind_area] = {'probability': match[0],
                                         'start': match.start(),
                                         'end': match.end(),
                                         'points': None}
                wind_area += 1

            self.wind_otlks = self.__parse_points(wind_raw, wind_otlks)

        # categorical outlook
        categorical_raw = archive_content.split('... CATEGORICAL ...')[1]
        categorical_raw = categorical_raw.split('&&')[0]
        categorical_otlks = {}
        categorical_area = 1
        for match in re.finditer(cat_re, categorical_raw):
            categorical_otlks[categorical_area] = {'severity': match[0],
                                                   'start': match.start(),
                                                   'end': match.end(),
                                                   'points': None}
            categorical_area += 1

        self.categorical_otlks = self.__parse_points(categorical_raw, categorical_otlks)

        if self.__otlk_type == 'day_3_otlk':
            probabilistic_raw = archive_content.split('... ANY SEVERE ...')[1]
            probabilistic_raw = probabilistic_raw.split('&&')[0]
            probabilistic_otlks = {}
            probabilistic_area = 1
            for match in re.finditer(non_cat_re, probabilistic_raw):
                probabilistic_otlks[probabilistic_area] = {'probability': match[0],
                                                           'start': match.start(),
                                                           'end': match.end(),
                                                           'points': None}
                probabilistic_area += 1
            self.probabilistic_otlks = self.__parse_points(probabilistic_raw, probabilistic_otlks)
        self.valid_time = valid_time
