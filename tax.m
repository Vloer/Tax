clear all
%syms NB Bladel
close all
%% 
leeftijd = 28;
% provincie = NB;
% Gemeente = Bladel;
bruto_loon_mnd = 3050;
bruto_loon_jr = bruto_loon_mnd*12;
vakantiegeld = 0.08*bruto_loon_jr;
bonus = 2000;
speciaal = vakantiegeld+bonus;
totaalloon = bruto_loon_jr+speciaal;
uitgavenlaag = 600*12;
uitgavenhoog = 400*12;
autogekocht = 10000;
CO2Auto = 60;
diesel = 0;
dieseltoeslag = 88.43;
spaargeld = 1000;
gasverbruik = 1500;
Stroomverbruik = 3500;
gastaks = 0.3547;
stroomtaks = 0.1193;
auto = 1;
gewichtauto = 700;
roken = 2; %pakjes per week
alcohol = 40; %glazen per week



opcenten = 0.85;
accijnsbenzine = 0.78773;
accijnsdiesel = 0.49569;
accijnsroken = 0.57;
accijnsalcohol = 1.06;
btwbenzine = 0.17*1.70;
kmjaar = 20000;
verbruik = 1/15;
MRB = 60*4;
rioolheffing = 200;
afvalheffing = 257;
OZB = 280;

if leeftijd >= 67
    AOW = 1 
else
    AOW = 0
end

loontaks = [0.3665 0.3810 0.3810 0.5175];
loontaksAOW = [0.1875 0.2020 0.3810 0.5175];
btw = [0.09 0.21]


CO2uitstoot = [0 71 95 139 156];
CO2AutoBPM1 = [360 502 1942 7706 11361];
CO2AutoBPM2 = [2 60 131 215 429];

%% BTW


btwlaag = uitgavenlaag*0.09;
btwhoog = uitgavenhoog*0.21+kmjaar*verbruik*btwbenzine;
btw = btwhoog+btwlaag;
%%
rokenalcohol = 52*(roken*accijnsroken*6.50+alcohol*accijnsalcohol*0.3)*1.21;

%% Energie en gemeente

rioolheffing = rioolheffing;
afvalheffing = afvalheffing;
OZB = OZB;
Energietaks = (Stroomverbruik*stroomtaks+gasverbruik*gastaks);

%% AUTO

accijnsbrandstof = (kmjaar)*verbruik*accijnsbenzine;

if diesel == 1
    accijnsbrandstof = kmjaar*verbruik*accijnsdiesel;
end
    

if CO2Auto == 0
    BPM = 0
end

if CO2Auto > CO2uitstoot(1) & CO2Auto < CO2uitstoot(2)
    BPM = CO2AutoBPM1(1)+(CO2AutoBPM2(1)*CO2uitstoot(1));
end

if CO2Auto > CO2uitstoot(2) & CO2Auto < CO2uitstoot(3)
    BPM = CO2AutoBPM1(2)+(CO2AutoBPM2(2)*(CO2Auto-CO2uitstoot(2)));
end

if CO2Auto > CO2uitstoot(3) & CO2Auto < CO2uitstoot(4)
    BPM = CO2AutoBPM1(3)+(CO2AutoBPM2(3)*(CO2Auto-CO2uitstoot(3)));
end

if CO2Auto > CO2uitstoot(4) & CO2Auto < CO2uitstoot(5)
    BPM = CO2AutoBPM1(4)+(CO2AutoBPM2(4)*(CO2Auto-CO2uitstoot(4)));
end

if CO2Auto > CO2uitstoot(5)
    BPM = CO2AutoBPM1(5)+(CO2AutoBPM2(5)*(CO2Auto-CO2uitstoot(5)));
end

if diesel == 1 && CO2Auto > 61;
    
    BPM = BPM + dieseltoeslag*(CO2Auto-61);
    
end

%% Loon

if bruto_loon_jr <= 20384;
loon_taks = loontaks(1)*bruto_loon_jr;
loon_taks = loon_taks;
end
if bruto_loon_jr > 20384 & bruto_loon_jr < 34300;
loon_taks = 20384*loontaks(1)+(bruto_loon_jr-20384)*loontaks(2);
loon_taks = loon_taks;
end
if bruto_loon_jr >= 34301 & bruto_loon_jr < 68507;
loon_taks = 20384*loontaks(1)+(34300-20384)*loontaks(2)+(bruto_loon_jr-34301)*loontaks(3);
loon_taks = loon_taks;
end
if bruto_loon_jr > 68507
loon_taks = 20384*loontaks(1)+(34300-20384)*loontaks(2)+(68507-34301)*loontaks(3)+(bruto_loon_jr-68507)*loontaks(4);
loon_taks = loon_taks;
end

if totaalloon <= 20384;
speciaaltaks = loontaks(1)*speciaal;
end
if totaalloon > 20384 & totaalloon < 34300;
speciaaltaks = loontaks(2)*speciaal;
end
if totaalloon >= 34301 & totaalloon < 68507;
speciaaltaks = loontaks(3)*speciaal;
end
if bruto_loon_jr > 68507
speciaaltaks = loontaks(4)*speciaal;
end

if totaalloon <= 20384;
speciaaltaksAOW = loontaksAOW(1)*speciaal;
end
if totaalloon > 20384 & totaalloon < 34300;
speciaaltaksAOW = loontaksAOW(2)*speciaal;
end
if totaalloon >= 34301 & totaalloon < 68507;
speciaaltaksAOW = loontaksAOW(3)*speciaal;
end
if bruto_loon_jr > 68507
speciaaltaksAOW = loontaksAOW(4)*speciaal;
end

if bruto_loon_jr <= 20384;
loon_taksAOW = loontaksAOW(1)*bruto_loon_jr;
loon_taksAOW = loon_taksAOW;
end
if bruto_loon_jr > 20384 & bruto_loon_jr < 34300;
loon_taksAOW = 20384*loontaksAOW(1)+(bruto_loon_jr-20384)*loontaksAOW(2);
loon_taksAOW = loon_taksAOW;
end
if bruto_loon_jr >= 34301 & bruto_loon_jr < 68507;
loon_taksAOW = 20384*loontaksAOW(1)+(34300-20384)*loontaksAOW(2)+(bruto_loon_jr-34301)*loontaksAOW(3);
loon_taksAOW = loon_taksAOW;
end
if bruto_loon_jr > 68507
loon_taksAOW = 20384*loontaksAOW(1)+(34300-20384)*loontaksAOW(2)+(68507-34301)*loontaksAOW(3)+(bruto_loon_jr-68507)*loontaksAOW(4);
loon_taksAOW = loon_taksAOW;
end

if bruto_loon_jr <= 20384
    alg_korting = 2477;
end
if bruto_loon_jr > 20384 & bruto_loon_jr < 68507;
    alg_korting = 2477-0.05147*(bruto_loon_jr-20384);
end
if bruto_loon_jr > 68507
    alg_korting = 0;
end

if bruto_loon_jr <= 9694
    arbeidskorting = 0.01754*bruto_loon_jr;
end
if bruto_loon_jr > 9694 & bruto_loon_jr < 20940;
    arbeidskorting = 170+0.28712*(bruto_loon_jr-9694);
end
if bruto_loon_jr > 20940 & bruto_loon_jr < 34060;
    arbeidskorting = 3399;
end
if bruto_loon_jr > 34060 & bruto_loon_jr < 90710;
    arbeidskorting = 3399-0.06*(bruto_loon_jr-34060);
end
if bruto_loon_jr > 90710
    arbeidskorting = 0;
end

if bruto_loon_jr <= 20384
    alg_kortingAOW = 1268;
end
if bruto_loon_jr > 20384 & bruto_loon_jr < 68507;
    alg_kortingAOW = 1268-0.02633*(bruto_loon_jr-20384);
end
if bruto_loon_jr > 68507
    alg_kortingAOW = 0;
end
if bruto_loon_jr <= 9694
    arbeidskortingAOW = 0.00898*bruto_loon_jr;
end
if bruto_loon_jr > 9694 & bruto_loon_jr < 20940;
    arbeidskortingAOW = 88+0.14689*(bruto_loon_jr-9694);
end
if bruto_loon_jr > 20940 & bruto_loon_jr < 34060;
    arbeidskortingAOW = 1740;
end
if bruto_loon_jr > 34060 & bruto_loon_jr < 90710;
    arbeidskortingAOW = 1740-0.03069*(bruto_loon_jr-34060);
end
if bruto_loon_jr > 90710
    arbeidskortingAOW = 0;
end

premievolk = (loon_taks-(alg_korting+arbeidskorting)) - loon_taksAOW;

if AOW == 0 
    loon_taks = loon_taks;
    Taksl = loon_taks;
    korting = alg_korting + arbeidskorting;
    premievolk = (loon_taks-(alg_korting+arbeidskorting)) - loon_taksAOW;
end

if AOW == 1
    loon_taksAOW = loon_taksAOW;
    Taksl = loon_taksAOW;
    korting = alg_kortingAOW + arbeidskortingAOW;
    premievolk = 0;
end

if spaargeld < 30360
    vermogensbelasting = 0
end
if spaargeld > 30360 & spaargeld < 71650
    vermogensbelasting = spaargeld*0.67*0.13+spaargeld*0.33*0.056;
end
if spaargeld > 71651 & spaargeld < 989736
    vermogensbelasting = spaargeld*0.21*0.13+spaargeld*0.79*0.056;
end
if spaargeld > 989737
    vermogensbelasting = 0.056*spaargeld;
end

Taksl = (Taksl - korting)-premievolk;
    
Taks = Taksl+premievolk+btw+rioolheffing+afvalheffing+OZB+Energietaks+accijnsbrandstof+MRB+speciaaltaks+vermogensbelasting+rokenalcohol;
Taksarray = [Taksl premievolk btwlaag btwhoog rioolheffing afvalheffing OZB Energietaks accijnsbrandstof MRB speciaaltaks vermogensbelasting rokenalcohol]
Takslabels = {'Inkomensbelasting - kortingen', 'Premie volksverzekeringen','BTW laag', 'BTW hoog','Rioolheffing', 'Afvalstoffenheffing', 'OZB (Indirect)', 'Energiebelasting', 'Accijns op brandstof', 'Motorrijtuigen', 'Belasting op bonussen en vakantiegeld', 'Vermogensbelasting', 'Belasting op tabak en alcohol'}
Taksratio = (Taks)/(bruto_loon_jr+speciaal)

txt = ['Totale jaarlijkse belasting: ' num2str(Taks) ' Euro'  '='  num2str(Taksratio*100) '%'];
figure
pie(Taksarray,Takslabels)
title(txt);