#!python3
import urllib.request
import re
import time
import string
from inspect import signature


class Persoon:

    def __init__(self, postcode, leeftijd, bruto_loon_mnd, vakantiegeld, bonus, uitgaven_laag, uitgaven_hoog, spaargeld,
                 verbruik_gas, verbruik_stroom, verbruik_water):
        self.postcode = postcode
        self.leeftijd = leeftijd
        self.bruto_loon_mnd = bruto_loon_mnd
        self.vakantiegeld = vakantiegeld
        self.bonus = bonus
        self.uitgaven_laag = uitgaven_laag
        self.uitgaven_hoog = uitgaven_hoog
        self.spaargeld = spaargeld
        self.verbruik_gas = verbruik_gas
        self.verbruik_stroom = verbruik_stroom
        self.verbruik_water = verbruik_water

        print('Getting location data ...')
        start = time.perf_counter()
        url = 'https://www.postcodezoekmachine.nl/' + self.postcode.upper()
        response = urllib.request.urlopen(url)
        html = response.read().decode(response.headers.get_content_charset())

        self.stad = regex_lookup("<td><a href=\"\/(\w*)\">", html)
        self.stad = string.capwords(self.stad, '-')
        self.provincie = regex_lookup("<td><a href=\"\/provincie\/(.*?)\">", html)
        self.provincie = string.capwords(self.provincie, '-')
        self.gemeente = regex_lookup("<td><a href=\"\/gemeente\/(.*?)\">", html)
        self.gemeente = string.capwords(self.gemeente, '-')
        print('Success! Data found in {} seconds'.format(round(time.perf_counter() - start, 2)))
        print('{}, {}, {}'.format(self.stad, self.provincie, self.gemeente))

    def roken(self, roken_per_week):
        self.roken = roken_per_week

    def drinken(self, alcohol_per_week):
        self.alcohol = alcohol_per_week

    def check_input(

class Voertuig:

    def __init__(self, kenteken, prijs, km_jaar):
        self.prijs = prijs
        self.km_jaar = km_jaar

        if len(kenteken) != 8:
            if len(kenteken) != 6:
                print('Vul een geldig kenteken in (voorbeeld: 12-ab-cd) >>> ')
                self.kenteken = str(input())
        else:
            self.kenteken = kenteken

    def set_CO2(self):
        self.CO2 = True

    def get_data(self, persoon):
        # Convert kenteken, length is either 6 or 8
        if len(self.kenteken) == 8:
            self.kenteken = self.kenteken.upper()
        else:  # is 6
            self.kenteken = (self.kenteken[:2] + '-' + self.kenteken[2:4] + '-' + self.kenteken[4:6]).upper()

        print('Getting vehicle data ...')
        start = time.perf_counter()

        # Get html data
        ini_url = 'https://www.kentekencheck.nl/kenteken?i=' + self.kenteken
        ini_html = read_html(ini_url)
        link_to_rapport = regex_lookup("<iframe src=\"(.*?)\"", ini_html)
        html = read_html(link_to_rapport)

        # Read stuff
        self.merk_nummer = regex_lookup("Merk<\/td>\s*<td style=\"width:60%;\">(.*?)<\/td>", html) + ' ' + regex_lookup(
            "<td>Type<\/td>\s*<td>(.*?)<\/td>", html)
        self.bouwjaar = regex_lookup("<td>Bouwjaar<\/td>\s*<td>.*(\d{4})<\/td>", html)
        self.brandstof = regex_lookup("<td>Brandstof<\/td>\s*<td>(.*?)<\/td>", html)
        self.nieuwprijs = regex_lookup("<td>Nieuwprijs<\/td>\s*<td>&euro; (.*?)<\/td>", html).replace('.', '')
        self.gewicht = regex_lookup("<td>Massa ledig voertuig<\/td>\s*<td>(\d*) KG<\/td>", html)
        self.verbruik = round(
            1 / float(regex_lookup("<td>Verbruik gecombineerd<\/td>\s*<td>.*\(1:(.*?)km\)<\/td>", html)), 4)
        self.wegenbelasting = int(
            regex_lookup("<td>" + persoon.provincie + "<\/td>\s*.*\s*<td>&euro;(\d*)<\/td>", html))
        self.CO2 = int(regex_lookup("<td>CO2 uitstoot<\/td>\s*<td>(\d*?) g\/km<\/td>", html))

        print('Success! Data found in {} seconds'.format(round(time.perf_counter() - start, 2)))
        print('{}, {}, {}, {}, {}, {}, {}m {}'.format(self.merk_nummer, self.bouwjaar, self.brandstof, self.nieuwprijs,
                                                      self.gewicht, self.wegenbelasting, str(self.verbruik),
                                                      str(self.CO2)))


def regex_lookup(regex_string, data_to_search):
    reg = re.compile(r"" + regex_string + "")
    data = reg.search(data_to_search)
    return data.group(1)


def read_html(url):
    response = urllib.request.urlopen(url)
    html = response.read().decode(response.headers.get_content_charset())
    return html
