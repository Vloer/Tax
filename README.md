# Filename: Tax  


### Classes
#### Persoon
Inputs : 
- postcode ('1234ab')
- leeftijd
- bruto loon per maand
- eventuele bonus
- uitgaven per maand met lage btw (voedsel etc)
- uitgaven per maand met hoge btw (niet essentiële goederen)
- spaargeld
- schulden
- verbruik gas per maand
- verbruik stroom per maand
- verbruik water per maand

Als de persoon rookt en/of drinkt kun je dit aangeven met:  
`naam persoon`.roken_per_week = `aantal pakjes per week`  
`naam persoon`.alcohol_per_week = `aantal glazen alcohol per week`
  
  
  
#### Voertuig
Inputs :
- naam van gedefiniëerde persoon (eerste class)
- kenteken ('12abcd of 12-ab-cd of ab123c of ab-123-c)
- aankoopprijs
- aantal gereden kilometers per jaar  

Aanvullende informatie over de auto (bouwjaar, brandstofverbruik etc) **moet** worden opgehaald door:  
`naam auto`.get_data()  

  
  
#### Belasting
Inputs:
- naam van Persoon
- naam van Auto
- aantal personen in je huishouden
- fiscale partner (0 voor nee, 1 voor ja)  
  
  
  
#### Calculation
Inputs:
- naam van Persoon
- naam van Auto
- naam van Belasting

