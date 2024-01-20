from bs4 import BeautifulSoup
import requests
import time
import json
import re

class MyDrug:
    ##Constructor
    def __init__(self,front_side,back_side,color,shape):
        self.front_side = front_side
        self.back_side = back_side
        self.color = color
        self.shape = shape

    ##Clear text
    def clear_text(self, input_text):
        if(input_text.find(";") != -1):
            final_text = input_text[:input_text.find(";")]
        elif(input_text.find(".") != -1):
            final_text = input_text[:input_text.find(".")]
        else:
            final_text = input_text

        return final_text
    
    ##Initial Search
    def quickSearch(self, allDrugs_file, data):
        front_side = self.front_side
        back_side  = self.back_side
        color = self.color
        shape = self.shape

        outfile = open(allDrugs_file, "w")
        # page = requests.get("https://quotes.toscrape.com")
        # soup = BeautifulSoup(page.text, "html.parser")

        # quotes = soup.findAll("span", attrs={"class":"text"})
        # authors = soup.findAll("small", attrs={"class":"author"})

        # for (quote,author) in zip(quotes,authors):
        #     #print(f'{quote.text} - {author.text}')
        #     print("kk")
        #     print(quote.text + " - " + author.text)

        ############## DRUGS.COM ##################
        front_side = front_side.replace(" ", "+")#Removes any spaces inputted by the user 
        back_side = back_side.replace(" ", "+")
        imprint = f'{front_side}+{back_side}'

        url = f'https://www.drugs.com/imprints.php?imprint={imprint}&color={color}&shape={shape}' 
        drugs_page = requests.get(url, timeout=5)
        content = BeautifulSoup(drugs_page.content, "html.parser")
        #content = BeautifulSoup(drugs_page.text, "html.parser")
        #print (content)
        
        #Retrieving the entire results page
        drug_list_with_ads = content.find("div", attrs={"class":"ddc-pid-list"})
        #print(drug_list_with_ads)

        #Excluding Ads
        drug_list_without_ads = drug_list_with_ads.find_all("div", attrs={"class":"ddc-card"})
        #print(drug_list_without_ads)
        #print(len(drug_list_without_ads))

        #For Every Drug: 
        # 1) Store a picture
        # 2) Drug Name
        # 3) Drug Strength
        # 4) Imprint
        # 5) color
        # 6) Shape
        
        drug_table_titles = ["Image", "Link", "Strength", "Imprint", "Color", "Shape"] 
        
        
        for drug in drug_list_without_ads:
            image = drug.find("img") #Extracting top image per drug
            #print(image['src'])
            
            label = drug.find("a") #Extracting drug's name + link
            name = label.text
            link = "https://www.drugs.com" + label['href']

            strength, imprint, color, shape = drug.find_all("dd") #Extracting individual data

            #print(strength.text, imprint.text, color.text, shape.text)
            drug_info = [image['src'], link, strength.text, imprint.text, color.text, shape.text]
            data[name] = dict(zip(drug_table_titles, drug_info))
        
        

        if(len(data) == 0):
            ############## WEBMD.COM (Separate function) ###############
            url = f'https://www.webmd.com/pill-identification/search-results?imprint1={front_side}&imprint2={back_side}&color={color}&shape={shape}' 
            drugs_page = requests.get(url, timeout=5)
            content = BeautifulSoup(drugs_page.content, "html.parser")
            print(content)
            print(drugs_page.cookies)
            drug_list = content.find("div", attrs={"class":"search-results"})
            print(drug_list)
                
        

        #print("data = \n", data)
        json.dump(data, outfile, indent=2)    
        outfile.close()         

    ##Detailed Search
    def detailedSearch(self, name, allDrugs_file, oneDrug_file):
        #Step 1: Fetch the link from data.json
        infile = open(allDrugs_file, "r")
        data = json.load(infile)
        #print(data[name]["Link"])
        url = data[name]["Link"]
        
        #Step 2: Scrape using the link
        drugs_page = requests.get(url, timeout=5)
        content = BeautifulSoup(drugs_page.content, "html.parser")
        
        outfile = open(oneDrug_file, "w")
        li_dict = {"avoid_when": [], "side_effects":[]} #Append fields when ready
        #Step 3: Record 'avoid if'
        li_dict = self.avoidIf(content, li_dict)

        #Step 4: Record "side_effects"
        li_dict = self.sideEffects(content, li_dict)

        #Step 5: Dump and close files
        json.dump(li_dict, outfile, indent=2)
        infile.close()
        outfile.close()

    ##Avoid if search
    def avoidIf(self, content, li_dict):
        target_string = "Before taking this medicine" #header to start search from
        first_target_header = content.find('h2', string=lambda s: target_string in str(s))
        end_target_header = first_target_header.find_next("h2") #"end search" header
        #print(f'{first_target_header} \n {end_target_header}')
        
        if first_target_header and end_target_header:
            content_between_headers = first_target_header.find_all_next(['li', 'h2'])
            #print(content_between_headers)
            for _, item in enumerate(content_between_headers):
                #end list after next header
                if item == end_target_header:
                    #content_between_headers = content_between_headers[:index]
                    break
                
                #clear unecessary marks and append
                li_dict["avoid_when"].append(self.clear_text(item.get_text(strip=True)))

            #print(li_dict["avoid_when"])
        
        return li_dict
    
    def sideEffects(self,content,li_dict):
        target_string = re.compile(r"side effects", re.IGNORECASE)
        first_target_header = content.find('h2', string=target_string)
        end_target_header = first_target_header.find_next("h2") #"end search" header
        print(f'{first_target_header} \n {end_target_header}')
        
        if first_target_header and end_target_header:
            content_between_headers = first_target_header.find_all_next(['li', 'h2'])
            #print(content_between_headers)
            for _, item in enumerate(content_between_headers):
                #end list after next header
                if item == end_target_header:
                    #content_between_headers = content_between_headers[:index]
                    break
                
                #clear unecessary marks and append
                li_dict["side_effects"].append(self.clear_text(item.get_text(strip=True)))

            #print(li_dict["avoid_when"])

        return li_dict
    
if __name__ == "__main__":
    start = time.time()
    #Global Variables
    data = dict()
    allDrugs_file = "allDrugs.json"
    oneDrug_file = "oneDrug.json"
    drug = MyDrug('I', '', '', '0')

    #Calling the quick search function based on passed-in info
    drug.quickSearch(allDrugs_file,data)

    #Calling the detailed search after a drug is selected
    drug.detailedSearch("Ibuprofen", allDrugs_file, oneDrug_file)

    end = time.time()
    print(f'\n\nElapsed time = {end - start} seconds')
    