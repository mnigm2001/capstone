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

    number_to_color = {
    '12': 'White',
    '14': 'Beige',
    '73': 'Black',
    '1': 'Blue',
    '2': 'Brown',
    '3': 'Clear',
    '4': 'Gold',
    '5': 'Gray',
    '6': 'Green',
    '44': 'Maroon',
    '7': 'Orange',
    '74': 'Peach',
    '8': 'Pink',
    '9': 'Purple',
    '10': 'Red',
    '11': 'Tan',
    '13': 'Yellow',
    '69': 'Beige & Red',
    '55': 'Black & Green',
    '70': 'Black & Teal',
    '48': 'Black & Yellow',
    '52': 'Blue & Brown',
    '45': 'Blue & Gray',
    '75': 'Blue & Green',
    '71': 'Blue & Orange',
    '53': 'Blue & Peach',
    '34': 'Blue & Pink',
    '19': 'Blue & White',
    '26': 'Blue & White Specks',
    '21': 'Blue & Yellow',
    '47': 'Brown & Clear',
    '54': 'Brown & Orange',
    '28': 'Brown & Peach',
    '16': 'Brown & Red',
    '57': 'Brown & White',
    '27': 'Brown & Yellow',
    '49': 'Clear & Green',
    '46': 'Dark & Light Green',
    '51': 'Gold & White',
    '61': 'Gray & Peach',
    '39': 'Gray & Pink',
    '58': 'Gray & Red',
    '67': 'Gray & White',
    '68': 'Gray & Yellow',
    '65': 'Green & Orange',
    '63': 'Green & Peach',
    '56': 'Green & Pink',
    '43': 'Green & Purple',
    '62': 'Green & Turquoise',
    '30': 'Green & White',
    '22': 'Green & Yellow',
    '42': 'Lavender & White',
    '40': 'Maroon & Pink',
    '50': 'Orange & Turquoise',
    '64': 'Orange & White',
    '23': 'Orange & Yellow',
    '60': 'Peach & Purple',
    '66': 'Peach & Red',
    '18': 'Peach & White',
    '15': 'Pink & Purple',
    '37': 'Pink & Red Specks',
    '29': 'Pink & Turquoise',
    '25': 'Pink & White',
    '72': 'Pink & Yellow',
    '17': 'Red & Turquoise',
    '35': 'Red & White',
    '20': 'Red & Yellow',
    '33': 'Tan & White',
    '59': 'Turquoise & White',
    '24': 'Turquoise & Yellow',
    '32': 'White & Blue Specks',
    '41': 'White & Red Specks',
    '38': 'White & Yellow',
    '31': 'Yellow & Gray',
    '36': 'Yellow & White',
    }

    number_to_shape = {
        '1': 'Barrel',
        '5': 'Capsule/Oblong',
        '6': 'Character-shape',
        '9': 'Egg-shape',
        '10': 'Eight-sided',
        '11': 'Oval',
        '12': 'Figure eight-shape',
        '13': 'Five-sided',
        '14': 'Four-sided',
        '15': 'Gear-shape',
        '16': 'Heart-shape',
        '18': 'Kidney-shape',
        '23': 'Rectangle',
        '24': 'Round',
        '25': 'Seven-sided',
        '27': 'Six-sided',
        '32': 'Three-sided',
        '33': 'U-shape',
    }

    def get_color_number(self, color):
        for key, value in self.number_to_color.items():
            if value == color:
                return key
        return None
    
    def get_shape_number(self, shape):
        for key, value in self.number_to_shape.items():
            if value == shape:
                return key
        return None

    ##Clear text
    def clear_text(self, input_text):
        #Beginning
        if(input_text.startswith('\n')):
            input_text = input_text[1:]

        #End
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
        li_dict = {'intake_method':'', 'avoid_when':[], 'side_effects':{'common':[],'rare':[]}} #Append fields when ready

        #Step 3: Record "method of intake"
        li_dict = self.intakeMethod(content,li_dict)
        
        #Step 4: Record 'avoid if'
        li_dict = self.avoidIf(content, li_dict)

        #Step 5: Record "side_effects"
        li_dict = self.sideEffects(content, li_dict)

        #Step 6: Dump and close files
        json.dump(li_dict, outfile, indent=2)
        infile.close()
        outfile.close()

    ##Intake method search
    #@param self: object of class MyDrug
    #@param content: html page to scrape
    #@param li_dict: variable to store scraped info
    def intakeMethod(self, content, li_dict):
        #Possible intake methods and keywords to scrape for
        intake_method_list = ['Swallow the pill whole with a glass of water','Break the pill in half, then swallow with water',
                              'Crush the pill, then swallow with water','Take the pill with food','Take the pill with milk',
                              'Dissolve the pill in water or another liquid before consuming',
                              'Place the pill under your tongue and let it dissolve','Chew the pill',
                              'Follow any specific instructions provided by your healthcare provider or pharmacist']
        intake_method_keywords = ['swallow','break','crush','food','milk','dissolve','tongue','chewable','N/A']

        target_string = "How should I take" #header to start search from
        first_target_header = content.find('h2', string=lambda s: target_string in str(s))
        if first_target_header : end_target_header = first_target_header.find_next("h2") #"end search" header
        #print(f'{first_target_header} \n {end_target_header}')
        
        if first_target_header and end_target_header:
            content_between_headers = first_target_header.find_all_next(['p','h2'])
            #print(content_between_headers)
            for _, item in enumerate(content_between_headers):
                #print(f'item : {item.text()}')
                for keyword in intake_method_keywords:
                    #print(f'keyword : {keyword} ::: {item.text.lower()}')
                    if (item == end_target_header):
                        li_dict['intake_method'] = intake_method_list[intake_method_keywords.index('N/A')]
                        print(li_dict["intake_method"])
                        return li_dict
                    if(keyword in item.text.lower()):
                        li_dict['intake_method'] = intake_method_list[intake_method_keywords.index(keyword)]
                        print(f'keyword : {keyword} ::: {item.text.lower()}')
                        print(li_dict["intake_method"])
                        return li_dict     
    
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
                #print(self.clear_text(item.get_text()))
                li_dict["avoid_when"].append(self.clear_text(item.get_text()))

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
        #print(f'{first_target_header} \n {end_target_header}')
        
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
    
    def quickSearch2(self, mode=1):
        front_side = self.front_side
        back_side  = self.back_side
        color = self.get_color_number(self.color)
        shape = self.get_shape_number(self.shape)

        if not color or not shape:
            print("Color or shape")
            return None

        data = dict()

        ############## DRUGS.COM ##################
        front_side = front_side.replace(" ", "+")#Removes any spaces inputted by the user 
        back_side = back_side.replace(" ", "+")
        imprint = f'{front_side}+{back_side}'

        url = f'https://www.drugs.com/imprints.php?imprint={imprint}&color={color}&shape={shape}' 
        drugs_page = requests.get(url, timeout=5)
        content = BeautifulSoup(drugs_page.content, "html.parser")
        
        #Retrieving the entire results page
        drug_list_with_ads = content.find("div", attrs={"class":"ddc-pid-list"})

        # print(drug_list_with_ads)

        if drug_list_with_ads is None:
            return None
        
        #Excluding Ads
        if(mode):
            drug_list_without_ads = drug_list_with_ads.find_all("div", attrs={"class":"ddc-card"})
        else:
            drug_list_without_ads = drug_list_with_ads.find("div", attrs={"class":"ddc-card"})
            drug_list_without_ads = [drug_list_without_ads]        

        #For Every Drug: 1) Store a picture 2) Drug Name 3) Drug Strength 4) Imprint 5) color 6) Shape
        drug_table_titles = ["Image", "Link", "Strength", "Imprint", "Color", "Shape"] 
        
        
        for drug in drug_list_without_ads:
            image = drug.find("img") #Extracting top image per drug
            
            label = drug.find("a") #Extracting drug's name + link
            name = label.text
            link = "https://www.drugs.com" + label['href']

            try:
                strength, imprint, color, shape = drug.find_all("dd") #Extracting individual data
            except ValueError:
                return None
            drug_info = [image['src'], link, strength.text, imprint.text, color.text, shape.text]
            data[name] = dict(zip(drug_table_titles, drug_info))
        
        return data


    