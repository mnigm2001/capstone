from bs4 import BeautifulSoup
import requests
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
    #@param self: object of class MyDrug
    #@param allDrugs_file: json file to store drug search list
    #@param data: dict to store content
    #@param type: single   (0) - returns only the first result
    #             multiple (1) - returns a list of drugs
    def quickSearch(self, allDrugs_file, data,mode=1):
        front_side = self.front_side
        back_side  = self.back_side
        color = self.color
        shape = self.shape

        outfile = open(allDrugs_file, "w")

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
        if(mode):
            drug_list_without_ads = drug_list_with_ads.find_all("div", attrs={"class":"ddc-card"})
        else:
            drug_list_without_ads = drug_list_with_ads.find("div", attrs={"class":"ddc-card"})
            drug_list_without_ads = [drug_list_without_ads]
        #print(drug_list_without_ads)
        

        #For Every Drug: 1) Store a picture 2) Drug Name 3) Drug Strength 4) Imprint 5) color 6) Shape
        
        drug_table_titles = ["Image", "Link", "Strength", "Imprint", "Color", "Shape"] 
        
        
        for drug in drug_list_without_ads:
            image = drug.find("img") #Extracting top image per drug
            #print(f"image: {image['src']}")
            
            label = drug.find("a") #Extracting drug's name + link
            #print(f'label is {label}')
            name = label.text
            link = "https://www.drugs.com" + label['href']

            strength, imprint, color, shape = drug.find_all("dd") #Extracting individual data

            #print(strength.text, imprint.text, color.text, shape.text)
            drug_info = [image['src'], link, strength.text, imprint.text, color.text, shape.text]
            data[name] = dict(zip(drug_table_titles, drug_info))
        
        

        # if(len(data) == 0):
        #     ############## WEBMD.COM (Separate function) ###############
        #     url = f'https://www.webmd.com/pill-identification/search-results?imprint1={front_side}&imprint2={back_side}&color={color}&shape={shape}' 
        #     drugs_page = requests.get(url, timeout=5)
        #     content = BeautifulSoup(drugs_page.content, "html.parser")
        #     print(content)
        #     print(drugs_page.cookies)
        #     drug_list = content.find("div", attrs={"class":"search-results"})
        #     print(drug_list)
                
        

        #print("data = \n", data)
        json.dump(data, outfile, indent=2)    
        outfile.close()         

    ##Detailed Search
    #@param self: object of class MyDrug
    #@param name: name of the drug
    #@param allDrugs_file: JSON file containing initial list of searched drugs
    #@param oneDrug_file: JSON file to store drug's detailed content
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
        li_dict = {"avoid_when":[], "side_effects":{"common":[],"rare":[]}} #Append fields when ready
        #Step 3: Record 'avoid if'
        li_dict = self.avoidIf(content, li_dict)

        #Step 4: Record "side_effects"
        li_dict = self.sideEffects(content, li_dict)

        #Step 5: Dump and close files
        json.dump(li_dict, outfile, indent=2)
        infile.close()
        outfile.close()

    ##Avoid if search
    #@param self: object of class MyDrug
    #@param content: html page to scrape
    #@param li_dict: variable to store scraped info
    def avoidIf(self, content, li_dict):
        target_string = "Before taking" #header to start search from
        first_target_header = content.find('h2', string=lambda s: target_string in str(s))
        if first_target_header : end_target_header = first_target_header.find_next("h2") #"end search" header
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
    
    ##Side effects search
    #@param self: object of class MyDrug
    #@param content: html page to scrape
    #@param li_dict: variable to store scraped info
    def sideEffects(self,content,li_dict):
        common_flag, rare_flag = 0,0 #Flags set to indicate type of side effect
        target_string = re.compile(r"side effects", re.IGNORECASE)
        first_target_header = content.find('h2', string=target_string)
        end_target_header = first_target_header.find_next("h2") #"end search" header
        print(f'{first_target_header} \n {end_target_header}')
        
        if first_target_header and end_target_header:
            content_between_headers = first_target_header.find_all_next(['li', 'h2', 'h3', 'p'])
            #print(content_between_headers)
            for _, item in enumerate(content_between_headers):
                #end list after next header
                if item == end_target_header:
                    break
                #spotting common side effects
                elif (("common" in item.text.lower()) or ("less serious" in item.text.lower())) and (item.name == 'p' or item.name == 'h3'):
                    common_flag = 1
                #spotting rare side effects    
                elif (("stop" in item.text.lower()) or ("serious" in item.text.lower()) or ("call your doctor at once" in item.text)) and (item.name == 'p'):
                    common_flag = 0
                
                if(common_flag and item.name == 'li'):
                    #clear unecessary marks and append
                    li_dict["side_effects"]["common"].append(self.clear_text(item.get_text(strip=True)))
                elif (not(common_flag) and item.name == 'li'):
                    li_dict["side_effects"]["rare"].append(self.clear_text(item.get_text(strip=True)))
                

            #print(li_dict["avoid_when"])

        return li_dict
    

    