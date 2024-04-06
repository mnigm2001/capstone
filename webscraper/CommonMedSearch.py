from bs4 import BeautifulSoup
import requests
import time
import json
from webscraper import MyDrug


start = time.time()
#Global Variables
data = dict()
outfile = "common_data.json"

front_side = ['L484','AD','M','210','TEVA','APO','W961','A',
              'LUPIN','C','1010','TEVA','E','IG','551','437',
              '93','5','VIBRA','Lilly3240', 'VASO','F+L','NEXIUM',
              'MSD','DIFLUCAN+100','DISTA+3105','LASIX+40',
              'NEURONTIN', 'MICROZIDE','P','Advil','2872',
              'LAMICTAL+25','TAP','SYNTHROID','135','CLARITIN+10',
              '952','MEVACOR','M','BMS+6060','b','51+51','SINGULAIR',
              'ALEVE','FL','PROCARDIA','LILLY','607','OP','PROTONIX',
              'PAXIL','DELTASONE+20','pfizer','INDERAL+10','SEROQUEL+100',
              'ALTACE+10+mg','Z','JANSSEN','20','ZD4522+20','ZOLOFT',
              'ZOCOR','IMITREX','1mg','C+20','Flomax+0.4mg','RESTORIL+30mg',
              '4 MG','TOP','104','ULTRAM','DESYREL+MJ776','a+NS',
              'NVR','W+75','DuPont','AMB+5','X+ANA+X','WYETH+4188',
              'A-007+5','T','Lilly+3229','WELLBUTRIN+100','SB+4140',
              '7767','M','CLEOCIN+300+mg','w+50','ARICEPT','414','VISTARIL',
              'M367','L612','G+037','K+56','AN+627','L194','I-2','1+2']
back_side  = ['','30','255','','3109','ATV20','','54','500',
              '94','20','833','34','283','R','','318','',
              'PFIZER095','30mg','10','10','40','963','ROERIG',
              'PROZAC+20','HOECHST','300','12.5+mg','2','','','',
              'PREVACID+30','88','ZESTRIL','458','','MSD+731','15',
              '500','928+7+1/2','GEIGY','MRK+117','','10','PFIZER+260',
              '4112','PRILOSEC+20','10','','2+0','','PGN+150','I','',
              'HOECHST','150','R+1','Xa','','50+MG','MSD+740','100','f617',
              '','BI+58','','','25','20','06+59','','','D+O','704',
              'COUMADIN+10','5401','2','C200','','107','40+mg','','',
              '200','024','','','5','','PFIZER+541','','','','','','','','']
color = '12'
shape = '24'

# for i in range(len(front_side)):
#     print(f'i={i}, front: {type(front_side[i])},{front_side[i]}, back:{type(back_side[i])},{back_side[i]}')
#     drug = MyDrug(front_side[i],back_side[i], color, shape)
#     #Calling the quick search function based on passed-in info (with mode 0 to return first result only)
#     drug.quickSearch(outfile,data,0) 
         
end = time.time()
print(f'\n\nElapsed time = {end - start} seconds')

search = MyDrug('L484','', color, shape)
result = search.quickSearch2(mode=1)
print(result)
print(len(result.keys()))


# <select id="color-select" name="color" size="1">
# 						<option value="">Any color</option>
# 						<option value="0" disabled="">---------</option>
# 							<option value="12">White</option>
# 	<option value="0" disabled="">---------</option>
# 	<option value="14">Beige</option>
# 	<option value="73">Black</option>
# 	<option value="1">Blue</option>
# 	<option value="2">Brown</option>
# 	<option value="3">Clear</option>
# 	<option value="4">Gold</option>
# 	<option value="5">Gray</option>
# 	<option value="6">Green</option>
# 	<option value="44">Maroon</option>
# 	<option value="7">Orange</option>
# 	<option value="74">Peach</option>
# 	<option value="8">Pink</option>
# 	<option value="9">Purple</option>
# 	<option value="10">Red</option>
# 	<option value="11">Tan</option>
# 	<option value="12">White</option>
# 	<option value="13">Yellow</option>
# 	<option value="0" disabled="">---------</option>
# 	<option value="69">Beige &amp; Red</option>
# 	<option value="55">Black &amp; Green</option>
# 	<option value="70">Black &amp; Teal</option>
# 	<option value="48">Black &amp; Yellow</option>
# 	<option value="52">Blue &amp; Brown</option>
# 	<option value="45">Blue &amp; Gray</option>
# 	<option value="75">Blue &amp; Green</option>
# 	<option value="71">Blue &amp; Orange</option>
# 	<option value="53">Blue &amp; Peach</option>
# 	<option value="34">Blue &amp; Pink</option>
# 	<option value="19">Blue &amp; White</option>
# 	<option value="26">Blue &amp; White Specks</option>
# 	<option value="21">Blue &amp; Yellow</option>
# 	<option value="47">Brown &amp; Clear</option>
# 	<option value="54">Brown &amp; Orange</option>
# 	<option value="28">Brown &amp; Peach</option>
# 	<option value="16">Brown &amp; Red</option>
# 	<option value="57">Brown &amp; White</option>
# 	<option value="27">Brown &amp; Yellow</option>
# 	<option value="49">Clear &amp; Green</option>
# 	<option value="46">Dark &amp; Light Green</option>
# 	<option value="51">Gold &amp; White</option>
# 	<option value="61">Gray &amp; Peach</option>
# 	<option value="39">Gray &amp; Pink</option>
# 	<option value="58">Gray &amp; Red</option>
# 	<option value="67">Gray &amp; White</option>
# 	<option value="68">Gray &amp; Yellow</option>
# 	<option value="65">Green &amp; Orange</option>
# 	<option value="63">Green &amp; Peach</option>
# 	<option value="56">Green &amp; Pink</option>
# 	<option value="43">Green &amp; Purple</option>
# 	<option value="62">Green &amp; Turquoise</option>
# 	<option value="30">Green &amp; White</option>
# 	<option value="22">Green &amp; Yellow</option>
# 	<option value="42">Lavender &amp; White</option>
# 	<option value="40">Maroon &amp; Pink</option>
# 	<option value="50">Orange &amp; Turquoise</option>
# 	<option value="64">Orange &amp; White</option>
# 	<option value="23">Orange &amp; Yellow</option>
# 	<option value="60">Peach &amp; Purple</option>
# 	<option value="66">Peach &amp; Red</option>
# 	<option value="18">Peach &amp; White</option>
# 	<option value="15">Pink &amp; Purple</option>
# 	<option value="37">Pink &amp; Red Specks</option>
# 	<option value="29">Pink &amp; Turquoise</option>
# 	<option value="25">Pink &amp; White</option>
# 	<option value="72">Pink &amp; Yellow</option>
# 	<option value="17">Red &amp; Turquoise</option>
# 	<option value="35">Red &amp; White</option>
# 	<option value="20">Red &amp; Yellow</option>
# 	<option value="33">Tan &amp; White</option>
# 	<option value="59">Turquoise &amp; White</option>
# 	<option value="24">Turquoise &amp; Yellow</option>
# 	<option value="32">White &amp; Blue Specks</option>
# 	<option value="41">White &amp; Red Specks</option>
# 	<option value="38">White &amp; Yellow</option>
# 	<option value="31">Yellow &amp; Gray</option>
# 	<option value="36">Yellow &amp; White</option>
# 					</select>

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


# <select id="shape-select" name="shape">
# 						<option value="0">Any shape</option>
# 							<option value="1">Barrel</option>
# 	<option value="5">Capsule/Oblong</option>
# 	<option value="6">Character-shape</option>
# 	<option value="9">Egg-shape</option>
# 	<option value="10">Eight-sided</option>
# 	<option value="11">Oval</option>
# 	<option value="12">Figure eight-shape</option>
# 	<option value="13">Five-sided</option>
# 	<option value="14">Four-sided</option>
# 	<option value="15">Gear-shape</option>
# 	<option value="16">Heart-shape</option>
# 	<option value="18">Kidney-shape</option>
# 	<option value="23">Rectangle</option>
# 	<option value="24">Round</option>
# 	<option value="25">Seven-sided</option>
# 	<option value="27">Six-sided</option>
# 	<option value="32">Three-sided</option>
# 	<option value="33">U-shape</option>
# 					</select>

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