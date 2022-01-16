import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

def insol_ann_state_summary(subject= "", date_from = "",  date_to = ""):
    """
 Returns a daily summary overview of the specified announcement subject (example: "Openings") by German state of 
 specified date range.
 
   Args:
       date_from (str): DD.MM.YYYY
       date_to (str): DD.MM.YYYY
       subject (str): subject selection either {"Protective measures", "Openings","Events", "Decisions taken in proceedings", "Decisions taken after proceedings", "Others", "Decisions taken in the residual-debt exemption proceedings", "Distribution records","Monitored insolvency plans", "Dismissals due to lack of assets"}
  
   Returns:
       A Dataframe, data columns are as follows: 
        ======================  ==============================================================
        State                   the German state (as `str`) 
        Date                    the date range (as `str`) 
        Subject                 the specified subject (as `str`) 
        HRA                     the number of announcement (as `str`) 
        HRB                     the number of announcement (as `str`) 
        GnR                     the number of announcement (as `str`) 
        PR                      the number of announcement (as `str`) 
        VR                      the number of announcement (as `str`) 
        Other                   the number of announcements not linked to reg. type (as `str`)
    """      
    _states = ["Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg", "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen",
           "Nordrhein-Westfalen", "Rheinland-Pfalz", "Saarland", "Sachsen", "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen"]
    _reg = ["HRA", "HRB", "GnR", "PR", "VR", "--+keine+Angabe+--"]
        
    def _translate(text = ""):
        outp = ["Sicherungsmaßnahmen", "Eröffnungen", "Termine", "Entscheidungen im Verfahren",
             "Entscheidungen nach Aufhebung des Verfahrens","Sonstiges", "Entscheidungen im Restschuldbefreiungsverfahren", 
             "Verteilungsverzeichnisse", "Überwachte Insolvenzpläne", "Abweisungen mangels Masse"]
        inp = ["Protective measures", "Openings","Events", "Decisions taken in proceedings", "Decisions taken after proceedings",
            "Others", "Decisions taken in the residual-debt exemption proceedings", "Distribution records",
               "Monitored insolvency plans", "Dismissals due to lack of assets"]
        dict_urlenc = dict(zip(inp, outp,))
        for key in dict_urlenc.keys():
             text = text.strip().replace(key, dict_urlenc[key]) 
        return text
    
    def _urlencode(text = ""):
        inp = ['ü', 'ö', 'ä', 'Ü', 'Ö', 'Ä', 'ß', '§', '(', ')', '/', '?', '*']
        outp = ['%FC', '%F6', '%E4', '%DC' , '%D6', '%C4', '%DF', '%A7', '%28', '%29', '%2F', '%3F', '%2A'] 
        dict_urlenc = dict(zip(inp, outp))
        for key in dict_urlenc.keys():
             text = text.strip().replace(key, dict_urlenc[key]) 
        return text

    subjects = _translate(text = subject).replace("Verteilungsverzeichnisse", "Verteilungsverzeichnisse (§ 188 InsO) d. Verw./Treuh.")
    subjects = subjects.replace("Verteilungsverzeichnisse", "Verteilungsverzeichnisse (§ 188 InsO) d. Verw./Treuh.")
    subjects = _urlencode(str(subjects)).replace(" ","+")
    
    df = pd.DataFrame()
    
    for state in _states:
        stat = state
        temp = pd.DataFrame()
        state = _urlencode(str(state))
        date_range = date_from + " - " + date_to
        output =  [stat, date_range, subject]
        for r in _reg: 
            url = ("https://alt.insolvenzbekanntmachungen.de/cgi-bin/bl_suche.pl?PHPSESSID=0bf78007299d3c5cd66ae29a5fbed458&Suchfunktion=uneingeschr&Absenden=Suche+starten&Bundesland=" + 
            state + "&Gericht=--+Alle+Insolvenzgerichte+--&Datum1=" + date_from + "&Datum2="+ date_to +"&Name=&Sitz=&Abteilungsnr=&Registerzeichen=--&Lfdnr=&Jahreszahl=--&Registerart="+ r +
            "&select_registergericht=&Registergericht=--+keine+Angabe+--&Registernummer=&Gegenstand=" + subjects + "&matchesperpage=10&sortedby=Datum&page=2#Ergebnis")
            html_page = requests.get(url).content
            soup = BeautifulSoup(html_page, 'html.parser')
            text = soup.find_all('table')[1].find_all('p')[0].find_all('b')[0].get_text()
            if text.find("Treffer") > 0:
                search_results = int(re.findall('wurden\s*(.*?)Treffer\s*',text)[0])
            elif text.find("keine mit Ihrer Suchanfrage übereinstimmenden Veröffentlichungen") > 0:
                search_results = 0 
            output.append(search_results)
        temp = pd.DataFrame([output], columns = ["State", "Date", "Subject", "HRA", "HRB", "GnR", "PR", "VR", "Other"])
        df = df.append(temp)
    df = df.reset_index(drop=True)
    cols = ["HRA", "HRB", "GnR", "PR", "VR"]
    df["Other"] = df["Other"] - df[cols].sum(axis=1)
    return df
