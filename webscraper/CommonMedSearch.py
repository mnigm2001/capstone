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
color = ''
shape = '0'

for i in range(len(front_side)):
    print(f'i={i}, front: {type(front_side[i])},{front_side[i]}, back:{type(back_side[i])},{back_side[i]}')
    drug = MyDrug(front_side[i],back_side[i], color, shape)
    #Calling the quick search function based on passed-in info (with mode 0 to return first result only)
    drug.quickSearch(outfile,data,0) 
         
end = time.time()
print(f'\n\nElapsed time = {end - start} seconds')