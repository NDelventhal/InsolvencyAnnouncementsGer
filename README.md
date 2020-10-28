<!-- TOC -->
## Table of Content
- [InsolvencyAnnouncementsGER](#insolvencyannouncementsger) 
- [Background](#background)
- [Intended Audience: Science/Research](#intended-audience-scienceresearch)
- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [Support](#support)
- [Data protection and online privacy](#data-protection-and-online-privacy)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)
- [License](#license)
- [Contact](#contact)
<!-- /TOC -->


# InsolvencyAnnouncementsGer

InsolvencyAnnouncementsGer is a Python library for searching, viewing and scraping public announcements of German bankruptcy courts from https://www.insolvenzbekanntmachungen.de. 

*Please note:* Downtime of the by the library accessed German justice portal may occur and also changes of the official register may affect the functionality of the library. 

## Background

The library was written by the author for research purposes of the Institute of Accounting and Auditing of the Humboldt University of Berlin and the [TRR 266 Accounting for Transparency](https://www.accounting-for-transparency.de/), a trans-regional Collaborative Research Center funded by the German Research Foundation (Deutsche Forschungsgemeinschaft – DFG) as part of its Open Science Data Center under the supervision of [Prof. Dr. Joachim Gassen](https://github.com/joachim-gassen). 

In this context the library's output aims to contribute to transparent research and, through the collection of field data, which is used to analyze the perception, processing and handling of accounting information, to evidence-based policy making. A use case example in education: The output of this library was used in a class project of the PhD Class [VHB-ProDok "Quantitative Empirical Accounting Research and Open Science Methods"](https://github.com/joachim-gassen/vhb_qear20) in order to derive quasi-experiments, to analyse the negative liquidity shock caused by the corona crisis and the effects of the decision of German regulators to temporarily disable the debtor's statutory obligation to file for insolvency as a measure to combat the COVID-19 headwinds. 

## Intended Audience: Science/Research

The library target audience is primarily researchers. The library also intends to diminish the barriers non-German speaking researchers may face working with the German justice portal of interest. 

## Installation

Available through The Python Package Index (PyPI): 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install InsolvencyAnnouncementsGer 

```python
pip install InsolvencyAnnouncementsGer
```
Or install through the author's Github repository 

```python
pip install git+https://github.com/NDelventhal/InsolvencyAnnouncementsGER
```

## Requirements 

The following libraries are required: 
- pandas 
- requests 
- beautifulsoup4

The package manager [pip](https://pip.pypa.io/en/stable/) can be used to install these.

```python
pip install pandas requests beautifulsoup4
```

## Usage

```python
import InsolvencyAnnouncementsGer as ia
```
```python
ia.regcourts_scr() 
```
Returns a pd.DataFrame listing German registrations courts and corresponding register types.

```python
ia.inscourts_scr()
```
Returns a pd.DataFrame containing insolvency courts and German state abbreviations.

```python
ia.insol_proc_scrprep()
```
Prepares arguments prior to the insolvency proceedings scraping. Requires user input to define search criteria and returns a pd.DataFrame containing scraped content in case of findings. Refer to the docstring of insol_proc_scr() for more information on the output.

```python
ia.insol_proc_scr(reg = ["HRA", "HRB"], state = "Berlin",date_from = "30.08.2020", date_to = "", name = "",
                  domicile = "", department_number = "", register_reference = "", seq_number  = "", year = "",
                  reg_court = "", reg_number = "", subject = "", search_type = "unlimited", ins_court = "",
                  scrape_html = True)
```

Returns scraped search results for all insolvency announcements of the register types 'HRA' and 'HRB' from the specified date ('date_from') in the form day-month-year (DD.MM.YYYY) in the state Berlin. The unlimited search (search_type = "unlimited") is limited to data released within the last two weeks. Returns search results according to entered arguments, search arguments may be defined with the help of ia.insol_proc_scrprep().
Returns pd.DataFrame containing scraped content in case of findings. Data columns contain the scrape date, the selected registry type, the URL of the scraped announcement, the scraped hyperlink information for each observation and optional the scraped website content of the announcement.

```python
ia.insol_proc_scrpar(df, url = "url", scraped_html= "", convert_html_to_text = True, register_type = False):
```
Parses the scraped insolvency proceedings annoucements, the pd.DataFrame output from insol_proc_scr() or insol_proc_scrprep(). Returns the  input pd.DataFrame with appended columns listing for each announcement as variables the corresponding insolvency court, the insolvency court abbreviation, the court file number, the name or firm name of the debtor, the domicile of the debtor, the subject of the annoucement, the registration court, the identified register type (optional), the register number, the German state abbreviation, the date, timestamp and the scraped_text (optional)

```python
ia.update_url(url) 
```
Updates a single scraped url of an announcement, in case it turned invalid

```python
ia.insol_ann_daily_summary(subject= "Openings", date_from = "24.10.2020",  date_to = "28.10.2020"):
```
Returns a summary overview of counts of the specified announcement subject (example: "Openings") by German state and register type and non-register linked annoucements of specified date range.  

*For more details and examples, please refer to the documentation/docstrings.*

## Support 

More information on the insolvency announcement data is available under the followings links of the used data source: 
- https://www.insolvenzbekanntmachungen.de/en/fragen.html
- https://www.insolvenzbekanntmachungen.de/en/hinweise.html

## Data protection and online privacy

The library scrapes data from the official register of the German justice portal. According to the German justice portal the following information on an access of the contents from https://www.insolvenzbekanntmachungen.de is stored for six weeks, before the data is made anonymous and is further solely used for statistical purposes:

- the name of the file requested
- the date and time of the request
- the quantity of data transmitted
- the error status 
- the IP address of the accessing computer

Please refer to https://www.insolvenzbekanntmachungen.de/en/hinweise.html for further information. 

## Roadmap

- Development (Q3 2020) 
- Add library to The Python Package Index (PyPI) (Q4 2020)
- Develop test routines (Q4 2020 - Q3 2021)
- Add visuals, including Choropleth maps (Q4 2020 - Q1 2021)

Please also check the open issues for other proposed features.

## Contributing
Contributions are welcome. Please do not hesitate to open an issue or pull request. Prior to pull requests containing major changes, please communicate these changes via a new issue. Please try to avoid duplicate and have a look at the open issues for a list of known issues and proposed changes prior to it.  

## Acknowledgments

I would like to thank [Prof. Dr. Joachim Gassen](https://github.com/joachim-gassen) for his supervision of this library during its development and for his contribution to the code. 

See the list of contributors who participated in this project [here](https://github.com/NDelventhal/InsolvencyAnnouncementsGer/graphs/contributors).

## License

This project is licensed under the [MIT License](https://github.com/NDelventhal/InsolvencyAnnouncementsGer/blob/main/LICENSE).

## Contacts

- The author: Niall Delventhal - ni.delventhal@gmail.com

- Institute of Accounting and Auditing, School of Business and Economics - Humboldt-Universität zu Berlin: wpruefung@wiwi.hu-berlin.de

- Project Link Accounting for Transparency: Find the contact details of the TRR 266‘s participating institutions [here](https://www.accounting-for-transparency.de/contact/)