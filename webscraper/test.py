import time
from webscraper import MyDrug

if __name__ == "__main__":
    start = time.time()
    #Global Variables
    data = dict()
    allDrugs_file = "allDrugs.json"
    oneDrug_file = "oneDrug.json"
    drug = MyDrug('R 029', '', '', '0')

    #Calling the quick search function based on passed-in info
    drug.quickSearch("random.json",data,0)

    #Calling the detailed search after a drug is selected
    drug.detailedSearch("Alprazolam", "random.json", oneDrug_file)

    end = time.time()
    print(f'\n\nElapsed time = {end - start} seconds')