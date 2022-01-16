import pandas as pd
import requests
import html
import re
from bs4 import BeautifulSoup
from datetime import date

_states = ["Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg", "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen",
           "Nordrhein-Westfalen", "Rheinland-Pfalz", "Saarland", "Sachsen", "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen"]

_states_e = ["Baden-Wuerttemberg", "Bavaria", "Berlin", "Brandenburg", "Bremen", "Hamburg", "Hesse", "Mecklenburg-Western Pomerania", "Lower Saxony",
             "North Rhine-Westphalia", "Rhineland-Palatinate", "Saarland", "Saxony", "Saxony-Anhalt", "Schleswig-Holstein", "Thuringia"]

_states_a = ["bw", "by", "be", "bb", "hb", "hh", "he", "mv", "ns", "nw", "rp", "sl", "sn", "st", "sh", "th"]

_registers = ["GnR", "HRA", "HRB", "PR", "VR"] 

_subjects = ["-- Alle Bekanntmachungen innerhalb des Verfahrens --", "Sicherungsmaßnahmen", "Eröffnungen", "Termine", "Entscheidungen im Verfahren",
             "Entscheidungen nach Aufhebung des Verfahrens","Sonstiges", "Entscheidungen im Restschuldbefreiungsverfahren", 
             "Verteilungsverzeichnisse (§ 188 InsO) d. Verw./Treuh.", "Überwachte Insolvenzpläne", "Abweisungen mangels Masse"]

_subjects_e = ["All Subjects", "Protective measures", "Openings","Events", "Decisions taken in proceedings", "Decisions taken after proceedings",
               "Others", "Decisions taken in the residual-debt exemption proceedings", "Distribution records (§ 188 InsO) of custodians/trustees",
               "Monitored insolvency plans", "Dismissals due to lack of assets"]

_default_url = ['https://alt.insolvenzbekanntmachungen.de/cgi-bin', '/bl_suche.pl?PHPSESSID=971ac0cbc174f6cfc71ed602a6787558&','Suchfunktion=',
              'uneingeschr', '&Absenden=Suche+starten&Bundesland=', '--+Alle+Bundesl%E4nder+--', '&Gericht=','--+Alle+Insolvenzgerichte+--',
              '&Datum1=', '', '&Datum2=', '', '&Name=', '', '&Sitz=', '', '&Abteilungsnr=', '', '&Registerzeichen=', '--', '&Lfdnr=',
              '', '&Jahreszahl=', '--', '&Registerart=','--+keine+Angabe+--', '&select_registergericht=&Registergericht=', '--+keine+Angabe+--', '&Registernummer=',
              '', '&Gegenstand=','--+Alle+Bekanntmachungen+innerhalb+des+Verfahrens+--', '&matchesperpage=100&sortedby=Datum&page=', '1', '#Ergebnis']

_respe = [""] * 3
_respe[0] = ": No records found"
_respe[1] = """For the detailed search an insolvency court needs to be specified,
    among family / firm name, domicile of debtor or the bankruptcy court file number
    or in case of a firm the registration number and the registration court."""
_respe[2] = """For the detailed search family / firm name, domicile of debtor or the bankruptcy court file number
      or in case of a firm the registration number and the registration court need to be specified."""

def _urlencode(text = ""):
    inp = ['ü', 'ö', 'ä', 'Ü', 'Ö', 'Ä', 'ß', '§', '(', ')', '/', '?', '*']
    outp = ['%FC', '%F6', '%E4', '%DC' , '%D6', '%C4', '%DF', '%A7', '%28', '%29', '%2F', '%3F', '%2A'] 
    dict_urlenc = dict(zip(inp, outp))
    for key in dict_urlenc.keys():
     text = text.strip().replace(key, dict_urlenc[key]) 
    return text

def _prepare_argument(answer="", choices ="", empty = ""):
   answer = answer.strip()
   if len(answer)!=0:
         selection = _urlencode(choices[int(answer)].replace(" ","+"))
   else:
         selection = empty
   return selection

def regcourts_scr():
 """
 Scrapes the registration courts of all register types.
 
 Returns:
     A Dataframe, data columns are as follows: 
            ==================  ======================================================================
            registration_court  German registration courts (as `str`)
            reg                 register types either {"GnR", "HRA", "HRB", "PR", "VR"} (as `str`)
            ==================  ======================================================================
            
 Raises:
    Exception: If target website does not not respond or if there is no internet connection.
 
 """    
 try:
    html_page = requests.get("".join(_default_url)).content
    text = BeautifulSoup(html_page, 'html.parser').get_text()
    df = pd.DataFrame(columns=["registration_court", "reg"])
    for i in _registers:
        temp = pd.DataFrame()
        s = 'RegisterArray\[\"'+ i + '\"\] = new Array\(' + '(.+?)\);' 
        courts = (re.search(s, text).group(1)).replace('"', '').split(",")
        courts = [x for x in courts if x!= "-- keine Angabe --"] 
        temp["registration_court"] = courts
        temp["reg"] = i
        df = df.append(temp)
    df = df.reset_index(drop=True)
 except: 
    print("Target website may not respond or the internet connection may have caused the error.")
 return df 

def inscourts_scr():
 """
 Scrapes the insolvency courts of each German state from the webpage alt.insolvenzbekanntmachungen.de.

 Returns:
     A Dataframe, data columns are as follows: 
            ==================  ======================================================================
            insolvency_court    German insolvency courts  (as `str`)
            state_abbr          German state abbreviations (as `str`)
            ==================  ======================================================================     
 Raises:
    Exception: If target website does not not respond or if there is no internet connection.
 """ 
 try:
    html_page = requests.get("".join(_default_url)).content
    text = BeautifulSoup(html_page, 'html.parser').get_text() 
    df = pd.DataFrame(columns=["insolvency_court", "state_abbr"])
    for i, y in zip(_states, _states_a):
       temp = pd.DataFrame()
       s = 'BundeslandArray\[\"'+ i + '\"\] = new Array\(' + '(.+?)\);' 
       courts = (re.search(s, text).group(1))
       courts = courts.replace('"', '').split(",") 
       temp["insolvency_court"] = courts
       temp["state_abbr"] = y
       df = df.append(temp)
    df = df.reset_index(drop=True)
 except: 
    print("Target website may not respond or the internet connection may have caused the error.")
 return df 

def insol_proc_scr(reg = "",
                   state = "",
                   date_from = "", 
                   date_to = "",
                   name = "",
                   domicile = "",
                   department_number = "",
                   register_reference = "",
                   seq_number  = "",
                   year = "",
                   reg_court = "",
                   reg_number = "",
                   subject = "",
                   search_type = "",
                   ins_court = "",
                   scrape_html = True):
 """Scrapes insolvency proceedings information on alt.insolvenzbekanntmachungen.de.
    Default arguments contain no search specification, with exception of the search type 
    (default: uneingeschr or unlimited). The unlimited search is limited to data released within the last two weeks,
    while for the detailed search sufficient information needs to be entered.
    For the detailed search an insolvency court needs to be specified, among family / firm name, 
    domicile of debtor or the bankruptcy court file number or in case of a registered firm the registration number 
    and the registration court.
    See https://alt.insolvenzbekanntmachungen.de/hilfe.html for more information. 
    
    Args:
        reg (str or list of str): The register type of the proceeding announcement {"GnR", "HRA", "HRB", "PR", "VR"}
        state (str): The name of the German state in URL encoded format
        date_from (str): DD.MM.YYYY 
        date_to (str): DD.MM.YYYY
        name (str): The name of the debtor 
        domicile (str): The domicile of the debtor 
        department_number (str): Represents the first part of the Bankruptcy court file number and is listed prior to 
        the register reference of either {"IN", "IK", "IE"} 
        register_reference (str): The register reference of the German bankruptcy court file number 
        {"IN", "IK", "IE"}
        seq_number (str): The sequential number following of the German bankruptcy 
        the register_reference of {"IN", "IK", "IE"}
        year (str): The last two digits of the year the opening of the bankruptcy proceeding occured
        reg_court (str): The register court of the bankruptcy proceeding 
        reg_number (str): The register number, but without the register type of {"GnR", "HRA", "HRB", "PR", "VR"} 
        subject (str): Subject of the proceedings announcements
        ins_court (str): The insolvency court is required information for a detailed search
        scrape_html (bool): Should the html content of the proceeding get scraped?
        search_type (str): Defines the search type {"detail", "unlimited"/"uneingeschr"}
        
    Returns:
        Dataframe: 
            Containing unparsed insolvency proceeding data. Data columns are as follows: 
            ============ ========================================================
            scrape_date  scrape_date (as `str`) 
            registry     either {"GnR", "HRA", "HRB", "PR", "VR"} (as `str`)
            url          URL of the scraped proceeding announcement (as `str`)
            href         scraped href information of each observation (as `str`)
            scraped_html scraped html content of the announcement (as `str`)
            ============ ========================================================
            
 """
 _u = _default_url
    
 if search_type == "unlimited":
    search_type = "uneingeschr"
    
 args = [search_type, state, ins_court, date_from, date_to, name, domicile, department_number,
     register_reference, seq_number, year, reg, reg_court, reg_number, subject]

 for i, arg in zip(list(range(3, 33, 2)),args):
    if len(arg) == 0 and len(_default_url[i]) != 0:
       _u[i] = _default_url[i]
    elif type(arg) is list:
      continue
    else:
      _u[i] = _urlencode(str(arg)).replace(" ","+")
 
 if len(reg) == 0:
    _u[25] = [_u[25]]
 elif type(reg) == str:      
    _u[25] = [reg]
 elif type(reg) == list:      
    _u[25] = reg
 
 df = pd.DataFrame()
 for x in _u[25]:
    print('Register type:', x)
    _u[25] = x
    if _u[33] != str(1):
       _u[33] = str(1)
    url = "".join(_u)
    html_page = requests.get(url).content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all('table')[1].find_all('p')[0].find_all('b')[0].get_text()
    if text.find("Treffer") > 0:
       search_results = int(re.findall('wurden\s*(.*?)Treffer\s*',text)[0])
    elif text.find("keine mit Ihrer Suchanfrage übereinstimmenden Veröffentlichungen") > 0:
       print("Registry", x, _respe[0])
       continue
    elif text.find("wählen Sie bei der Detailsuche ein Insolvenzgericht aus") > 0: 
       print(_respe[1])
       return
    elif text.find("geben Sie als Suchkriterium den Familiennamen") > 0:
       print(_respe[2])
       return
    else: 
       print('Website returns:', text)
       return
    max_pages = -(-search_results // 100)
    print('Number of search results:', search_results)
    print('Scrape', max_pages, 'pages')
    links = soup.select('a[href^="javascript:"]')
    print('Scraping page:', _u[33])
    temp = pd.DataFrame(links)
    if max_pages > 1:
      for i in range(2, max_pages + 1):
        print("Registry", x, ": Continuing with search page:", i)
        _u[33] = str(i)
        url = "".join(_u)
        html_page  = requests.get(url).content
        soup = BeautifulSoup(html_page, 'html.parser')
        links = soup.select('a[href^="javascript:"]')
        temp = temp.append(links, ignore_index=True)
    temp.columns = ['href']
    temp = temp[temp['href'].astype(str).str.startswith('<a href="javascript:NeuFenster')].reset_index(drop=True)
    temp['href'] = temp['href'].apply(lambda x: "'" + str(x) + "'") 
    temp['registry'] = x
    temp['scrape_date'] = date.today()
    temp['url'] = temp['href'].astype(str).apply(lambda x: re.findall("cgi-bin\s*(.*?)\s*'",x)[0])
    temp['url'] = _u[0]+ temp["url"].apply(html.unescape)
    temp = temp[['scrape_date', 'registry', 'url', 'href']] 
    if scrape_html == True:
        print("Registry", x, ": Scraping HTML content.")
        temp['scraped_html'] = temp['url'].apply(lambda url: requests.get(url).content).apply(lambda x: "'" + str(x) + "'") 
    print('Registry', x, ': Scraped', len(temp['url']), 'entries.')
    df = df.append(temp)
 return df

def update_url(url = ""):
 """Updates the PHP SESSION ID of the as URL entered link of proceedings from alt.insolvenzbekanntmachungen.de, 
  which turn invalid after some time. 
  
  Args:
        url (str): The URL of a proceeding announcement from alt.insolvenzbekanntmachungen.de containing a PHP SESSION ID
        
  Returns:
        url (str): The URL of the annoucement with a newly generated PHP SESSION ID
        
  Raises:
        ValueError: If the entered URL cannot be processed
 """            
 try:
    html_page = requests.get("".join(_default_url)).content
    soup = BeautifulSoup(html_page, 'html.parser') 
    text = soup.get_text()
    if text.find("Es wurden keine mit Ihrer Suchanfrage übereinstimmenden Veröffentlichungen gefunden") > 0:
          print("Replacement of the PHP Session ID is currently not possible due to no current records.")
          return
    else: 
          link = soup.select('a[href^="javascript:NeuFenster"]')[0]
          new = re.search("PHPSESSID\=(.+?)\&", str(link)).group(1)
          old = re.search("PHPSESSID\=(.+?)\&", str(url)).group(1)
          url_new = url.replace(old, new)
          print("Generated PHPSESSID:", new)
 except: 
    raise ValueError('The entered ULR' + url + ' cannot be processed.') 
 return url_new

def regcourts_state_scr():
 ''' Function scrapes the register courts of each German state. It returns a tuple, containing lists of all 16 states in alpabetical order. Please note: source is Wikipedia (URL = https://de.wikipedia.org/wiki/Liste_deutscher_Registergerichte)'''  
 url = "https://de.wikipedia.org/wiki/Liste_deutscher_Registergerichte"
 html_page = requests.get(url).content
 soup = BeautifulSoup(html_page, 'html.parser')
 states_d = dict(zip(_states, _states_a))   
 for key, value in states_d.items(): 
     state = soup.find(id=key)
     globals()[f'list_{value}'] = []  # requires Python 3.6 or higher   
     register_courts = state.find_next('ul')
     for y in register_courts:
        globals()[f'list_{value}'].append(y.string.replace("Amtsgericht ", ""))
        if '\n' in globals()[f'list_{value}']: globals()[f'list_{value}'].remove('\n')
 return list_bw, list_by, list_be, list_bb, list_hb, list_hh, list_he, list_mv, list_ns, list_nw, list_rp, list_sl, list_sn, list_st, list_sh, list_th

def insol_proc_scrpar(df = "", url = "", scraped_html= "", convert_html_to_text = True, register_type = False):
 """
 Parses information from the scraped insolvency proceedings - the output from insol_proc_scr() or insol_proc_scrprep() pandas.DataFrame.
 
   Args:
       df (Dataframe): The dataframe as output of insol_proc_scr() or insol_proc_scrprep()
       url (str column): The URL of the proceeding announcement
       scraped_html (str column): Scraped html content of the proceeding
       convert_html_to_text (bool): Shall the text be parsed?
       register_type (bool): Shall the register_types be identified and returned? 
  
   Returns:
       A Dataframe, data columns are as follows: 
            ======================  ====================================================================================
            insolvency_court        the insolvency court (as `str`) 
            court_file_number       the court file number (as `str`) 
            court_file_number_2     the court file number (as `str`) 
            name_debtor             the name or firm name of the debtor (as `str`)
            domicile_debtor         the registered domicile or offices location of the debtor (as `str`)
            subject                 the identified subject of the proceding announcement (as `str`)
            registration_court      the registration court (as `str`)
            register_type           (optional) the identified register type {"GnR", "HRA", "HRB", "PR", "VR"} (as `str`)
            register_number         the register number without either {"GnR", "HRA", "HRB", "PR", "VR"} (as `str`)
            registered              is debtor registered? (as `bool`)
            state_abbr              German state abbreviations (as `str`)
            insolvency_court_abbr   the insolvency court abbreviations (as `str`) 
            court_file_number_year  the last two digits of the year the insovency proceeding was initiated (as `str`) 
            date                    date of the insolvency proceeding announcement (as `str`)
            time                    time (UTC Offset: +2:00 hours) (as `str`)
            scraped_text            (optional) parsed text from the html output (as `str`)
            ======================  ====================================================================================
 """    
 
 try:
    content_tag = df.scraped_html.apply(lambda x: re.search('keywords" CONTENT=(.*)head', str(x), re.IGNORECASE).group(1).split('>', 1)[0].split('"', 1)[1].rsplit('"', 1)[0])
    content_tag = content_tag.str.split('~',expand=True)
    df[['insolvency_court', 'court_file_number', 'name_debtor', 'domicile_debtor', 'subject',
        'registration_court', 'register_type', 'register_number', 'registered']] = content_tag
    df[['state_abbr','insolvency_court_abbr', 'court_file_number_year', 'court_file_number_2', 'date']] = df.url.apply(lambda x: re.search('gerichte/\s*(.*?)\s*.htm',x).group(1)).str.split('/',expand=True)
    df["time"] = df.date.apply(lambda x: x[12:20]).str.replace("_", ":")
    df["date"] = df.date.apply(lambda x: x[0:10]).str.replace("_", "-")

    def decode(text = ""):
      inp = ['Amtsgericht', 'AG', '\\xe4', '\\xc4',  '\\xdf', '\\xfc', '\\xdc', '\\xf6', '\\xd6', '\\xa7', '\\xe9']
      outp = ['', '', 'ä', 'Ä', 'ß', 'ü', 'Ü', 'ö', 'Ö', '§', 'é']  
      for key in dict(zip(inp, outp)).keys():
        text = text.replace(key, dict(zip(inp, outp))[key]).strip() 
      return text
    for i in ['insolvency_court', 'name_debtor', 'domicile_debtor', 'subject','registration_court', 'insolvency_court_abbr']:
      df[i] = df[i].apply(lambda x: html.unescape(x) if type(x) == str else "")
      df[i] = df[i].apply(lambda x: decode(text = x) if type(x) == str else "")
    if convert_html_to_text == True: 
      df["scraped_text"] = df.scraped_html.apply(lambda x: BeautifulSoup(x, 'lxml').get_text())
      df["scraped_text"] = df["scraped_text"].str.split('Bekanntmachung', 1, expand=True)[1].apply(lambda x: x[:-2])
    if register_type == False:
      del df["register_type"]
 except: 
    raise ValueError('The parsing has failed. Are you really using the output from insol_proc_scr() or insol_proc_scrprep() as input?') 
 return df

def insol_proc_scrprep():  
 '''  
 Prepares arguments prior to the insolvency proceedings scraping. Requires user input, confirm entries with keyboard command Enter.
 Scrapes insolvency proceedings information on alt.insolvenzbekanntmachungen.de. See the documentation for insol_proc_scr() for more information.
    Args:
       user input, confirm entries with keyboard command Enter
    
    Returns:
       A Dataframe, data columns are as follows: 
            ======================  ====================================================================================
            insolvency_court        the insolvency court (as `str`) 
            court_file_number       the court file number (as `str`) 
            court_file_number_2     the court file number (as `str`) 
            name_debtor             the name or firm name of the debtor (as `str`)
            domicile_debtor         the registered domicile or offices location of the debtor (as `str`)
            subject                 the identified subject of the proceding announcement (as `str`)
            registration_court      the registration court (as `str`)
            register_type           (optional) the identified register type {"GnR", "HRA", "HRB", "PR", "VR"} (as `str`)
            register_number         the register number without either {"GnR", "HRA", "HRB", "PR", "VR"} (as `str`)
            registered              is debtor registered? (as `bool`)
            state_abbr              German state abbreviations (as `str`)
            insolvency_court_abbr   the insolvency court abbreviations (as `str`) 
            court_file_number_year  the last two digits of the year the insovency proceeding was initiated (as `str`) 
            date                    date of the insolvency proceeding announcement (as `str`)
            time                    time (UTC Offset: +2:00 hours) (as `str`)
            scraped_text            (optional) parsed text from the html output (as `str`)
            ======================  ====================================================================================
 """    

 Raises:
       IndexError: If the entered input variable is not an integer or is outside of the specified range 
 
 ''' 
 df1 = regcourts_scr()
 df2 = inscourts_scr()
 ve = '''Your entry is outside of the specified range. Please specify solely the number of the selection and type in solely the integer.'''

 print("""\nPlease specify your search criteria and confirm with Enter. Solely type in the integer. For no selection press Enter without an entry. 
 \nFor the detailed search an insolvency court needs to be specified, among family / firm name, domicile of debtor or the bankruptcy court file number
 or in case of a firm the registration number and the registration court.\n""")

 for i,ger,eng in zip([*range(0, 2, 1)],["Uneingeschränkte Suche", "Detail-Suche"],
                  ["Unlimited search", "Detailed Search"]):
    print(i, "  ", ger, " / ", eng)
    
 search_type = input("Search type number:")
 if len(search_type)!=0:
  try: 
     search_type =  ["uneingeschr", "detail"][int(search_type)]    
  except: 
     raise IndexError(ve) 

 for i,ger,eng in zip([*range(0, len(_states) + 1, 1)],_states,_states_e):
    print(i, "  ", ger, " / ", eng)
    
 state = input("State number:")
 
 try:
  if len(state)!=0:
    df2 = df2[df2['state_abbr'].str.contains(_states_a[int(state)])]
    courts = df2["insolvency_court"].reset_index(drop=True)
    state = _states[int(state)] 
  else:
    courts = df2["insolvency_court"]
 except:
   raise IndexError(ve)

 for i, inscourt in enumerate(courts, start=0):
    print(i," ",inscourt)
                        
 ins_court = input("Insolvency court:") 
 if len(ins_court)!=0:
  try:
    ins_court = courts[int(ins_court)]
  except:
    raise IndexError(ve)
 
 print("\nPress Enter to skip or write dates as DD.MM.YYYY")
 date_from = input("Starting date of the annoucement search:").strip() 
 date_to = input("Ending date of the annoucement search:").strip()  
 
 print("""\nFor the following inputs (name and domicile of the debtor) you may use the following wildcards:
 - a question mark ? serves as a placeholder for a single character
 - an asterisk * is a placeholder for either no character or any number of characters""")

 name = input("""\nFirm or name of the debtor:""").strip() 
 domicile = input("\nOffices or domicile of the debtor:").strip() 

 print("""\nA Bankruptcy court file number may be specified in the following. It consists out of the department number, followed by the register reference (IN, IK or IE), 
 the sequential number and the year reference. In the following the example 5 IN 432 / 04 is split up accordingly.""")
 
 print("\nThe departement number in the example above is 5.")
 department_number = input("Department number:").strip()
 print("The register reference in the example above is IN.")
 register_reference = input("Register reference:").strip()  

 print("The sequential number in the example above is 432")
 seq_number = input("The sequential number:").strip()  
 print("The year reference are the last two digits of the year. In the example above the year reference is 04")
 year = input("Year reference:").strip() 
 print("""\nChoose a single register type or multiple register types or leave empty for no specification. 
 In case multiple register are chosen, seperate the numbers with a comma.""") 

 for i, regist in enumerate(_registers, start=0):
    print(i," ",regist) 
    
 reg = input("Register Type:")
 if len(reg)!=0:
    reg_type = reg.split(",")
    reg = []
    for i in reg_type:
       reg.append(_registers[int(i)])
    def _match(x):
      for i in reg:
        if i in x: 
            return True
        else:
            return False
    
 reg_court = input("""Type in the registration court: (Enter 'opt' to see the entry options)
                   """)
 if reg_court == "opt" or "'opt'":
    for court in list(df1.registration_court):
        print(court)        
    reg_court = input("""Type in the registration court:""")
    
 reg_number = input("\nRegister number:").strip()
 print("\nSubject of the announcements may be specified with one of the following. Please type in solely the number of the subject.")
 for i,ger,eng in zip([*range(0, len(_subjects) + 1, 1)], _subjects, _subjects_e):
    print(i, "  ", ger, " / ", eng) 
    
 subject = input("Subject number:") 
 if len(subject) != 0: 
  try:
    subject = _subjects[int(subject)]
  except:
    raise IndexError(ve)

 print("Summary of the prepared arguments used:")
 print("search_type: ",search_type, "ins_court: ",ins_court,
      "ins_court: ",ins_court,"state: ",state,
      "date_from: ",date_from, "date_to: ",date_to,
      "name: ",name, "domicile: ",domicile,
      "department_number: ",department_number,
      "register_reference: ",register_reference,
      "year: ",year, "reg: ",reg,
      "reg_court: ",reg_court,
      "reg_number: ",reg_number,
      "subject: ",subject)

 start = input("Start scraping? (Y/N)").strip()
 if start != "Y":
    return 
 else:
   df = insol_proc_scr(reg, state, date_from, date_to,
                   name, domicile, department_number,
                   register_reference, seq_number,
                   year, reg_court, reg_number,
                   subject, search_type, ins_court,
                   scrape_html = True)  
 return df
