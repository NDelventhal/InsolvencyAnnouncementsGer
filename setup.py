import setuptools

setuptools.setup(
    name="InsolvencyAnnouncementsGer",
    packages = ["InsolvencyAnnouncementsGer"], 
    version="0.2.1",
    license='MIT',  
    url="https://github.com/NDelventhal/InsolvencyAnnouncementsGer",
    author="Niall Delventhal",
    author_email="ni.delventhal@gmail.com",
    description="InsolvencyAnnouncementsGer is a Python library for searching, viewing and scraping public announcements of German bankruptcy courts from https://www.insolvenzbekanntmachungen.de",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    download_url = 'https://github.com/NDelventhal/InsolvencyAnnouncementsGer/archive/v_021.tar.gz',
    install_requires=["pandas", "requests", "beautifulsoup4"],
    classifiers=['Intended Audience :: Science/Research', 
    'License :: OSI Approved :: MIT License', 
    'Development Status :: 3 - Alpha', 
         'Programming Language :: Python :: 3.7',],
)
