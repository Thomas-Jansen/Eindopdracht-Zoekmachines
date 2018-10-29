import sys
import json
from elasticsearch import Elasticsearch
from wordcloud import WordCloud
from datetime import datetime
import collections as c

import numpy as np
import matplotlib.pyplot as plt

#Connect to elastic cloud
HOST = 'https://558a85fda07b4bbea2ff78028c0f63a1.europe-west1.gcp.cloud.es.io:9243/'
es = Elasticsearch(hosts=[HOST], http_auth=('elastic','UgYdqcaJjmsYDaU5HfNwlDyL'), verify_certs=False)

file_directory = "Data1.json"

query={
 "query": {
    "match": {
        "content": "term"
    }
  }
}

#Makes the results into a SERP
def wrapStringInHTMLWindows(term, program, list_results, body):
    import datetime
    from webbrowser import open_new_tab

    now = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")

    filename = program + '.html'
    f = open(filename,'w')

    # Fill in blocks with results from queries
    wrapper = """<html>
    <head>
    <title>%s output - %s</title>
    </head>
    <body>
    <div style="text-align:center">
    <h1>Your top 10 searchresults for: %s</h1>
    </div>
    <div style="background:grey">
    <p>
    %s
    </p>
    </div>
    <div style="background:grey">
    <p>
    %s
    </p>
    </div>
    <div style="background:grey">
    <p>
    %s
    </p>
    </div>
    <div style="background:grey">
    <p>
    %s
    </p>
    </div>
    <div style="background:grey">
    <p>
    %s
    </p>
    </div>
    <div style="background:grey">
    <p>
    %s
    </p>
    </div>
    <div style="background:grey">
    <p>
    %s
    </p>
    </div>
    <div style="background:grey">
    <p>
    %s
    </p>
    </div>
    <div style="background:grey">
    <p>
    %s
    </p>
    </div>
    <div style="background:grey">
    <p>
    %s
    </p>
    </div>
    </body>
    </html>"""

    #Write it into html file and open once finished
    whole = wrapper % (program, now, term, list_results[0], list_results[1], list_results[2], list_results[3], list_results[4], list_results[5], list_results[6], list_results[7], list_results[8], list_results[9])
    f.write(whole)
    f.close()

    open_new_tab(filename)

#Wrap results into hrefs to place in result blocks
def wrapinresults(url, question):
    wrapper = """<p><a href=%s>%s</a></p>"""
    whole = wrapper % (url, question)
    return(whole)

#Makes wordcloud, removing stopwords, showing image
def makeWordCloud(term ,text):
    text = text.lower()
    text = text.replace(term, '')
    text = text.replace('de', '')
    text = text.replace('het', '')
    text = text.replace('een', '')
    text = text.replace('zijn', '')
    wordcloud = WordCloud().generate(text)
    image = wordcloud.to_image()
    image.show()

#Shows in which year the most hits have been made
def showTimeLine(res):
    from datetime import datetime
    import matplotlib.pyplot as plt

    timeline = []
    #finds date of creatio of the questions
    for doc in res['hits']['hits']:
        date = doc['_source']['Date']
        date = date.split(" ", 1)[0]
        datetime_object = datetime.strptime(date, '%Y-%m-%d').date()
        timeline.append(datetime_object)

    #creates figure
    x = timeline
    y = range(len(timeline))

    fig, ax = plt.subplots()
    ax.bar(timeline, y, width = 10)

    fig.autofmt_xdate()
    plt.show()

#Performs actual search
def search(term, filter):
    text = ''
    quest = es.get(index="zoekmachine", doc_type="question", id=5)['_source']

    #Connect to cloud and find results
    results = []
    res = es.search(index="zoekmachine", doc_type="question", body={"query": {"match": {"Question": term}}})
    print("%d documents found" % res['hits']['total'])
    #Create the results to print on SERP
    for doc in res['hits']['hits']:
        url = "https://www.startpagina.nl/v/vraag/" + doc['_source']['Number'] + "/"
        title = doc['_source']['Question']

        text = text + title

        date = doc['_source']['Date']
        date = date.split("-", 1)[0]
        if int(date) >= int(filter):
            results.append(wrapinresults(url, title))

    #Show all work to user
    makeWordCloud(term, text)
    docscount = len(results)
    if docscount < 10:
        for x in range(0, (10 - docscount)):
            results.append("")
    wrapStringInHTMLWindows(term, "serp", results, "body")
    showTimeLine(res)

#Ask user for query
def simple():
    print("What are you looking for?")
    term =  sys.stdin.readline()
    search(term, 0000)

#Ask user for query in which time setting
def advanced():
    print("What are you looking for? (ADV)")
    term =  sys.stdin.readline()
    print("From what year on?")
    year = sys.stdin.readline()
    search(term, year)

#Return that the choice was not available
def invalid():
    print("Not a valid choice")

#List of all categories in data set
switcherGetCat =  {
    "1"	: "Alle categorieën",
    "2"	: "Persoon & Gezondheid",
    "3"	: "Maatschappij",
    "4"	: "Financiën & Werk",
    "5"	: "Vervoer",
    "6"	: "Computers & Internet",
    "7"	: "Elektronica",
    "8"	: "Entertainment & Muziek",
    "9"	: "Eten & Drinken",
    "10": "Sport, Spel & Recreatie",
    '11': "Huis & Tuin",
    "12": "Wetenschap",
    "13": "Vakantie & Reizen",
    "14": "Kunst & Cultuur",
    "15":  "Overig",
    '16': "Biologie",
    "17":  "Wiskunde",
    "18": "Natuur- en scheikunde",
    "19": "Psychologie",
    "20": "Sociale wetenschap",
    "21": "Overig",
    "22": "Auto's",
    "23" : "Vliegtuigen",
    "24" : "Boten",
    "25" : "Openbaar vervoer",
    "26" : "Motorfietsen",
    "27" : "Fietsen",
    "28": 'Overig',
    "29": 'Spellen',
    "30": 'Computergames',
    "31": "Hobby\'s",
    "32": "Sporten",
    "33": "Overig",
    "34": 'Caraïben',
    "35": "Noord-Amerika",
    "36": 'Zuid-Amerika',
    "37": "Afrika",
    "38": 'Antarctica',
    "39": 'Azië',
    '40': 'Europa',
    "41": "Midden-Amerika",
    '42': "Midden-Oosten",
    "43": "Oceanië",
    "44": "Overig",
    "45": "Overig",
    "46": "Mode & Accessoires",
    "47": "Familie & Relatie",
    "48": "Gezondheid",
    "49": "Zwangerschap",
    "50": 'Onderwijs',
    "51": 'Milieu',
    "52": "Politiek & Overheid",
    "53": "Samenleving",
    "54": 'Overig',
    "55": "Boeken & Auteurs",
    "56": "Genealogie",
    "57": 'Geschiedenis',
    "58": 'Filosofie',
    "59": 'Poëzie',
    "60": "Beeldende kunst",
    "61": "Overig",
    "62": "Schoonmaken & Wassen",
    "63": 'Interieur',
    "64": 'Doe-Het-Zelf',
    "65": 'Tuin',
    "66": 'Huisdieren',
    "67": 'Overig',
    "68": 'Dranken',
    "69": 'Koken & Recepten',
    "70": 'Vegetarisch & Veganistisch',
    "71": "Uit eten",
    "72": "Overig",
    "73": 'Beroemdheden',
    "74": 'Stripboeken & Tekenfilms',
    "75": 'Tijdschriften',
    "76": 'Horoscoop',
    "77": 'Films',
    "78": 'Muziek',
    "79": 'Radio',
    "80": 'Televisie',
    "81": 'Overig',
    "82": 'Videocameras',
    "83": "Camera\'s",
    "84": "Telefoon & Abonnementen",
    "85": 'Spelcomputers',
    "86": 'Audio',
    "87": "Handhelds & Smartphones",
    "88": "Televisies",
    "89": 'Overig',
    "90": 'Hardware',
    "91": 'Software',
    "92": 'Internet',
    "93": 'Programmeren & Design',
    "94": 'Veiligheid',
    "95": 'Overig',
    "96": 'Carrière & Werk',
    "97": 'Financiën',
    "98": 'Huren & Vastgoed',
    "100": 'Belasting',
    "101": 'Overig',
    "103": 'Ondernemen',
    "104": "Religie",
    "106": 'Vrachtwagens & Transport',
    "107": 'Treinen',
    "108": "Taal",
    "109": "Spiritualiteit",
    "110": 'Ruimtevaart & Sterrenkunde',
    "111": "Besturingssystemen",
    "113": "Voetbal",
    "114": 'Wielrennen',
    "115": 'Tennis',
    "116": "Formule 1",
    "117": "Hockey",
    "118": 'Schaatsen',
    "119": 'Overig',
    "120": 'Vragen aan mannen',
    "121": 'Vragen aan vrouwen',
    "122": "GoeieVraag.nl",
    "123": "Ouderschap & Opvoeding",
    "124": 'Wetgeving',
    "125": 'Wintersport',
    "126": 'Feestdagen',
    "127": "Sinterklaas",
    "128": 'Kerst',
    "129": 'Pasen',
    "130": "Andere feestdagen",
    "131": "Seksualiteit",
    "132": "Aardrijkskunde & Aardwetenschappen",
    "133":  "Energie",
    "134": "Verzekeringen",
    "135": "Sparen & Beleggen",
    "136":  "Overig",
    "137": "Alternatieve geneeswijzen",
    "138": "Gebit",
    "139": 'Psyche',
    "140": 'Voeding',
    "141": "Ziekten",
    "142": "Optiek",
    "143": "Lichamelijke klachten",
    "144": "Mannelijk lichaam",
    "145": "Vrouwelijk lichaam",
    "146":  "Overig",
    "147":  'Kinderen',
    "148": "Reparaties",
    "149": "Banden",
    "150": "Brom- & Snorfietsen",
    "151": "Weblogs",
    "152": 'Webshops',
    "156": "Meteorologie",
    "157": "Lenen",
    "158": "Sparen",
    "159": "Hypotheek",
    "160":  "Economie",
    "161": "Techniek",
    "162": "Landbouw & Veeteelt",
    "163": "Medicijnen",
    "164":  "Huid-, haarverzorging en Make-up",
    "165": "Fotografie",
    "166":  'Winkels',
    "167": "Huishoudelijke apparaten",
    "168": "Sociale Media"
}

#Search for documents containing the query and make a list of categories
def searchFAC(term):
    text = ''
    quest = es.get(index="zoekmachine", doc_type="question", id=5)['_source']

    results = []
    cat = c.Counter()
    res = es.search(index="zoekmachine", doc_type="question", body={"query": {"match": {"Question": term}}})
    print("%d documents found" % res['hits']['total'])
    for doc in res['hits']['hits']:
        url = "https://www.startpagina.nl/v/vraag/" + doc['_source']['Number'] + "/"
        title = doc['_source']['Question']

        text = text + title
        results.append(wrapinresults(url, title))

        caterogynr= doc['_source']['Category']

        cat[switcherGetCat.get(caterogynr, "None")] += 1
    return cat, res

#Search for documents containing the query and filter out unwanted categories
def searchFAC2(term, catNr):
    text = ''
    quest = es.get(index="zoekmachine", doc_type="question", id=5)['_source']

    results = []
    res = es.search(index="zoekmachine", doc_type="question", body={"query": {"match": {"Question": term}}})
    print("%d documents found" % res['hits']['total'])
    for doc in res['hits']['hits']:
        url = "https://www.startpagina.nl/v/vraag/" + doc['_source']['Number'] + "/"
        title = doc['_source']['Question']

        text = text + title
        if int(doc['_source']['Category']) == catNr:
            results.append(wrapinresults(url, title))

    makeWordCloud(term, text)
    docscount = len(results)
    if docscount < 10:
        for x in range(0, (10 - docscount)):
            results.append("")
    wrapStringInHTMLWindows(term, "serp", results, "body")

    # makeWordCloud(text)
    wrapStringInHTMLWindows(term, "serp", results, "body")

#Show the user all possible categories and make them choose one
def getUserCat(cat):
    for c in cat:
        print(c, "("+str(cat[c])+")")
    print("\nPlease, type categorie:")
    dingenCat = sys.stdin.readline()
    # dingenCat = dingenCat
    catNr = "geen categorie"
    for number in switcherGetCat:
        if switcherGetCat.get(number) + "\n" == dingenCat:
            catNr = int(number)

    if not isinstance(catNr, int):
        print("Category doesn't exist\n")
        getUserCat(cat)
    else:
        return catNr

#Let user choose in which category to search for query
def faceted():
    print("What are you looking for? (FAC)")
    dingen = sys.stdin.readline()
    cat, res = searchFAC(dingen)
    catNr = getUserCat(cat)

    res = searchFAC2(dingen, catNr)

#Let user choose which type of search to execute, then forward to that search
def getUserInput():
    print("Welcome to our search engine in terminal")
    print("What kind of search would you like?")
    print("Input a for simple search")
    print("Input b for advanced search")
    print("Input c for faceted search")
    choise = sys.stdin.readline().split()[0]

    #Forward to right search method
    switcher = {
        'a': simple,
        "b": advanced,
        "c": faceted,
    }
    switcher.get(choise, invalid)()

##Put information into the cloud
#json_data=open(file_directory)

#counter = 0
#for line in json_data:
#    data = json.loads(line)
#    if('index' not in data.keys()) :
#        counter += 1

        # Test if succesfull in writing
#        resp = es.index(index='zoekmachine', doc_type='question', id=counter, body=data)
#        print(counter)



#Get the searchterm from the user
getUserInput()
