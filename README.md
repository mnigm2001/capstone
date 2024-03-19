# capstone
This repository manages capstone related work. It is broken down into four domains
    1. Frontend
    2. Webscraper
    3. Image Recognition API
    4. Backend/Database


# Webscraper
webscraper.py: Main scraper class definition
test.py: a simple test script (for verification purposes)
commonMedSearch.py: A script to fetch 100 most common medications (drug list is hardcoded for now) 

allDrugs.json: Contains a premilinary list of fetched medications and their basic info (physical attributes + image)
oneDrug.json: Contians advanced information of the scraped drug (When to avoid + side effects)

# Useful Git Commands:

git clone <URL LINK> . : clones repo once we are in the desired path

git pull : pull TOTT

git add <filename> : adds to the current commit

git diff --stat --cached : shows the files to be pushed

git commit -m "##" : commit message 

git push : push to repo


git reset HEAD^ --hard && git push origin -f : reverts everything to the first commit

git revert <CL> : reverts specified CL and keeps changes before and after it

git reset --hard <CL> : reverts everything including and after the specified CL
