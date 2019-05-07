#!python3
import urllib.request
import re
import time
import string
import datetime
import openpyxl
import os


class Persoon:

    def __init__(self, postcode, leeftijd, bruto_loon_mnd, bonus, uitgaven_laag, uitgaven_hoog, spaargeld,
                 verbruik_gas, verbruik_stroom, verbruik_water):
        params_init = locals()
        params = check_input(params_init, [0], range(1, 10))

        self.postcode = params['postcode']
        self.leeftijd = params['leeftijd']
        self.bruto_loon_mnd = params['bruto_loon_mnd']
        self.bonus = params['bonus']
        self.uitgaven_laag = params['uitgaven_laag'] * 12
        self.uitgaven_hoog = params['uitgaven_hoog'] * 12
        self.spaargeld = params['spaargeld']
        self.verbruik_gas = params['verbruik_gas']
        self.verbruik_stroom = params['verbruik_stroom']
        self.verbruik_water = params['verbruik_water']
        self.bruto_loon_jr = self.bruto_loon_mnd * 12
        self.vakantiegeld = self.bruto_loon_jr * 0.08
        self.roken = 0
        self.alcohol = 0
        self.loon_totaal = self.bruto_loon_jr + self.bonus + self.vakantiegeld

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


class Voertuig:

    def __init__(self, persoon, kenteken, prijs, km_jaar):
        params_init = locals()
        params = check_input(params_init, [1], [2, 3])

        self.persoon = persoon
        self.kenteken = params['kenteken']
        self.prijs = params['prijs']
        self.km_jaar = params['km_jaar']

        if not (len(self.kenteken) != 8 or len(self.kenteken) != 6):
            self.kenteken = input('Kenteken moet 6 (12abcd) of 8 (12-ab-cd) tekens zijn >>> ')

    def get_data(self):
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
        time.sleep(1)
        link_to_rapport = regex_lookup("<iframe src=\"(.*?)\"", ini_html)
        html = read_html('https://www.kentekencheck.nl' + link_to_rapport)

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
            regex_lookup("<td>" + self.persoon.provincie + "<\/td>\s*.*\s*<td>&euro;(\d*)<\/td>", html))
        self.CO2 = int(regex_lookup("<td>CO2 uitstoot<\/td>\s*<td>(\d*?) g\/km<\/td>", html))

        print('Success! Data found in {} seconds'.format(round(time.perf_counter() - start, 2)))
        print('{}, {}, {}, {}, {}, {}, {}, {}'.format(self.merk_nummer, self.bouwjaar, self.brandstof, self.nieuwprijs,
                                                      self.gewicht, self.wegenbelasting, str(self.verbruik),
                                                      str(self.CO2)))


class Belasting:

    def __init__(self, persoon, auto, huishouden_personen):
        self.persoon = persoon
        self.auto = auto
        try:
            self.huishouden_personen = int(huishouden_personen)
        except ValueError:
            self.huishouden_personen = input('Vul een geldig getal in voor het aantal personen in huis: >>> ')

        current_year = str(datetime.datetime.now().year)

        # Auto
        print('Getting car...')
        url = "https://www.unitedconsumers.com/tanken/informatie/opbouw-brandstofprijzen.asp"
        html = read_html(url)
        self.benzine_prijs = float(regex_lookup("Opbouw Benzine .*?<strong>(.*?)<\/strong>", html).replace(',', '.'))
        self.benzine_btw = regex_lookup("Opbouw Benzine .*?BTW.*?(\d*)%", html)
        self.benzine_accijns = regex_lookup("Opbouw Benzine .*?Accijns.*?(\d*)%", html)
        self.diesel_prijs = float(regex_lookup("Opbouw Diesel .*?<strong>(.*?)<\/strong>", html).replace(',', '.'))
        self.diesel_btw = regex_lookup("Opbouw Diesel .*?BTW.*?(\d*)%", html)
        self.diesel_accijns = regex_lookup("Opbouw Diesel .*?Accijns.*?(\d*)%", html)
        self.MRB = self.auto.wegenbelasting

        # Gemeente
        print('Getting gemeente...')
        url = "https://www.coelo.nl/images/Gemeentelijke_belastingen_{}.xlsx".format(current_year)
        url_opcenten = "https://www.coelo.nl/images/Provinciale_opcenten_{}.xlsx".format(current_year)
        urllib.request.urlretrieve(url, url.split('/')[-1])
        urllib.request.urlretrieve(url_opcenten, url_opcenten.split('/')[-1])

        wb = openpyxl.load_workbook(os.path.abspath(url.split('/')[-1]))['Gegevens per gemeente']
        if self.huishouden_personen > 1:
            col = ['I', 'N', 'S']
        else:
            col = ['I', 'L', 'Q']
        for row in range(5, wb.max_row + 1):
            if wb['B' + str(row)].value == self.persoon.gemeente:
                self.OZB = round(wb[col[0] + str(row)].value, 2)
                self.afvalheffing = round(wb[col[1] + str(row)].value,2)
                self.rioolheffing = wb[col[2] + str(row)].value
                break

        # Opcenten
        wb = openpyxl.load_workbook(os.path.abspath(url_opcenten.split('/')[-1]))['Gegevens per provincie']
        for row in range(6, 18):
            if wb['B' + str(row)].value == self.persoon.provincie:
                self.opcenten = round(wb['C' + str(row)].value / 100, 4)
                break

class Calculation:

    def __init__(self, persoon, auto, belasting):
        self.persoon = persoon
        self.auto = auto
        self.belasting = belasting


def regex_lookup(regex_string, data_to_search):
    reg = re.compile(r"" + regex_string + "", re.DOTALL)
    data = reg.search(data_to_search)
    return data.group(1)


def read_html(url):
    response = urllib.request.urlopen(url)
    html = response.read().decode(response.headers.get_content_charset())
    return html


def check_input(arguments, str_idx, int_idx):
    arg_list_keys = list(arguments.keys())[1:]  # don't include self
    arg_list_values = list(arguments.values())[1:]
    for idx in str_idx:
        while True:
            if type(arg_list_values[idx]) == str:
                break
            else:
                arg_list_values[idx] = input(
                    'Value \'{}\' of variable \'{}\' is not the correct type. Please insert letters only >>> '.format(
                        arg_list_values[idx], arg_list_keys[idx]))
                arguments[arg_list_keys[idx]] = arg_list_values[idx]
                continue
    print('Checked all strings\n')
    for idx in int_idx:
        while True:
            if type(arg_list_values[idx]) == int:
                break
            else:
                arg_list_values[idx] = input(
                    'Value \'{}\' of variable \'{}\' is not the correct type. Please insert numbers only >>> '.format(
                        arg_list_values[idx], arg_list_keys[idx]))
                try:
                    arg_list_values[idx] = int(arg_list_values[idx])
                    arguments[arg_list_keys[idx]] = arg_list_values[idx]
                    break
                except ValueError:
                    continue
    print('Checked all ints\n')
    return arguments

