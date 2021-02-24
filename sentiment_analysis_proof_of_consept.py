from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


translator = Translator(service_urls=['translate.googleapis.com'])
analyzer = SentimentIntensityAnalyzer()

tweets = ['Hvis TIX vinner den internasjonale finalen skal jeg spise skinnjakka til Anders Grønneberg.',
          'Det er ganske enkelt @ jonasgahrstore og @ Arbeiderpartiet - dere kan nå velge kunnskap og verdighet, '
          'eller straff og moralisme.Støtt rusreformen. ',
          'Det er for galt at folk må i fengsel pga avhengighet, noe alle definerer som sykdom, så\'n Støre må sette '
          'seg ned nå med regjeringen og analysere og vurdere opp mot ekspertkompetansens råd, og bli enig. ',
          'Rusreformer! For faen i Helvete:) Idiotene vi har som ledere klarer ikke dette på første forsøk nei, ikke faen!',
          'Vi må bli kvitt all fossil energibruk i alle sektorer. Da trenger vi utslippsfrie og robuste kraftsystemer, nye energibærere for tungtransport, skip og fly, og industriproduksjon uten utslipp.']

for sentence in tweets:
    translated = translator.translate(sentence).text
    vs = analyzer.polarity_scores(translated)
    print(sentence)
    print(translated)
    print(str(vs))
    print('\n')