import pandas as pd
from Viaplay import Viaplay
from Tele2PlayPlus import Tele2PlayPlus
from DisneyPlus_FI_NO_DK_SE import DisneyPlus_FI_NO_DK_SE
from TV4Play import TV4PLAY_SE
from Cmore_FI import CmoreFI
from AppleTVPlus import AppleTVPlus
from HBOMax_SE import HBOMax_SE
from Netflix import Netflix
from Discovery_plus_SE import Discoveryplus_SE
from Ruutu_FI import Ruutu_FI
from AmazonPrime_SE import AmazonPrime_SE
from Skyshowtime import SkyShowTime
from TV2Denmark import TV2_DK
from TV2Norge import TV2_NO
from MTV import MTV
from YoutubePremium_SE import YoutubePremium_SE
from Eurosport_player import EurosportPlayer
from Strim_NO import Strim_NO
from YouSee_DK import YouSee_DK
from datetime import date
import chromedriver_autoinstaller


# --- Hayu --- requires VPN for Denmark, Finland and Norway
from Hayu import Hayu

# --- VPN FI ---
from VPN_FI import VPN_FI, AmazonPrimeFI, YoutubePremiumFI, EurosportPlayerFI
from DNA_FI import DNA_TV_FI

# --- VPN NO ---
from VPN_NO import VPN_NO, AmazonPrimeNO, YoutubePremiumNO, EurosportPlayerNO

# --- VPN DK ---
from VPN_DK import VPN_DK, AmazonPrimeDK, YoutubePremiumDK, EurosportPlayerDK
from NordiskFilmPlus import NordiskFilmPlus

file_SE = 'video_SE_2023.xlsx'
file_NO = 'video_NO_2023.xlsx'
file_FI = 'video_FI_2023.xlsx'
file_DK = 'video_DK_2023.xlsx'
today = date.today()
d1 = today.strftime("%Y-%m-%d")

countries = ['SE', 'FI', 'NO', 'DK']
class MergeOutput:
    def __init__(self):
        self.SE_d2c = None
        self.NO = None
        self.DK = None
        self.FI = None

    # Method to combine all different dicts to one
    def combine_dicts(self, dictList):
       
        mergeDict = dict((k, [d[k] for d in dictList]) for k in dictList[0])
        print("mergedict", mergeDict)
        mergeDict['Package'] = [item for elem in mergeDict['Package'] for item in elem]
        mergeDict['Price'] = [item for elem in mergeDict['Price'] for item in elem]
        mergeDict['Campaign'] = [item for elem in mergeDict['Campaign'] for item in elem]
        mergeDict['Information'] = [item for elem in mergeDict['Information'] for item in elem]
        mergeDict['ID'] = [item for elem in mergeDict['ID'] for item in elem]
        return mergeDict

# --- D2C services ---
# Create dataframes from the scraped data.
# Merge with the existing data in the files
def create_dataframe(file,d2c_object, df_d2c, country):
    if country == "SE" or country == "FI" or country == "NO":
        columns = ['Dates', 'ID', 'Package', 'Price', 'Campaign', 'Information']
    else:
        columns = ['Dates', 'Package', 'Price', 'Campaign', 'Information']
    
    # ---- D2C ----
    # Create a dataframe
    df_d2c_1 = pd.DataFrame(columns=columns)
    dates = []
    for _ in range(len(d2c_object['Package'])):
        dates.append(d1)
    df_d2c_1['Dates'] = dates
    if country == "SE" or country == "FI" or country == "NO":
        df_d2c_1['ID'] = d2c_object['ID']
    df_d2c_1['Package'] = d2c_object['Package']
    df_d2c_1['Price'] = d2c_object['Price']
    df_d2c_1['Campaign'] = d2c_object['Campaign']
    df_d2c_1['Information'] = d2c_object['Information']
    frames = [df_d2c, df_d2c_1]
    result_d2c = pd.concat(frames)
    with pd.ExcelWriter(file, mode="w", engine="openpyxl") as writer:
        result_d2c.to_excel(writer, index=False, header=True, sheet_name='d2c')

# A function to read data from excel files.
# Check date and if not today is included --> scrape
def read_data(file, d2c_object, country):
     df_d2c = pd.read_excel(file,  engine='openpyxl', sheet_name='d2c')
     all_dates_d2c = df_d2c['Dates'].to_list()
     print('D2C', all_dates_d2c)
     if d1 in all_dates_d2c:
         print('Dagens datum finns redan')
     else:
         print('Måste generera ny data')
         create_dataframe(file, d2c_object, df_d2c, country)


# Create dataframes from the scraped data.
# Merge with the existing data in the files
def create_dataframe_d2c(file, object, df):

    columns = ['Dates', 'ID', 'Package', 'Price', 'Campaign', 'Information']
  
    # Create a dataframe
    df_1 = pd.DataFrame(columns=columns)
    dates = []
    for _ in range(len(object['Package'])):
        dates.append(d1)


    df_1['Dates'] = dates
    df_1['ID'] = object['ID']
    df_1['Package'] = object['Package']
    df_1['Price'] = object['Price']
    df_1['Campaign'] = object['Campaign']
    df_1['Information'] = object['Information']
    frames = [df, df_1]
    result = pd.concat(frames)
    with pd.ExcelWriter(file, mode="w", engine="openpyxl") as writer:
        result.to_excel(writer, index=False, header=True, sheet_name='d2c')

# A function to read data from excel files.
# Check date and if not today is included --> scrape
def read_data_d2c(file, object, country):
    df = pd.read_excel(file, engine='openpyxl', sheet_name='d2c')
    all_dates = df['Dates'].to_list()
    print(all_dates)
    if country == 'DK':
        print('Danmark')
        create_dataframe_d2c(file, object, df)

    if d1 in all_dates:
        print('Dagens datum finns redan')
    else:
        print('Måste generera ny data')
        create_dataframe_d2c(file, object, df)

# SWEDISH VPN
def Sweden_VPN(merge_output):
    # ---- Services "D2C" ----
    # Apple TV+
    apple_obj = AppleTVPlus()
    apple_obj.create_object('SE')

    # HBO Max - SE
    HBO_obj_SE = HBOMax_SE()
    HBO_obj_SE.create_object()

    # Discovery_plus - SE
    discovery_obj_SE = Discoveryplus_SE()
    discovery_obj_SE.create_object()

    # Viaplay - FI, NO, SE and DK.
    viaplay_obj = Viaplay()
    viaplay_obj.create_objects_viaplay('SE')

    # Disney plus - SE
    disney_obj_SE = DisneyPlus_FI_NO_DK_SE()
    disney_obj_SE.create_object('SE')

    # Tele2PlayPlus - SE
    tele2playplus_obj = Tele2PlayPlus()
    tele2playplus_obj.create_object()

    # SE
    TV4Play_obj_SE = TV4PLAY_SE()
    TV4Play_obj_SE.create_object()

    # Netflix
    netflix_obj = Netflix()
    netflix_obj.create_object('SE')

    # AmazonPrime - SE
    AmazonPrime_SE_obj = AmazonPrime_SE()
    AmazonPrime_SE_obj.create_object()

    # Youtube Premium - SE
    YoutubePremium_SE_obj = YoutubePremium_SE()
    YoutubePremium_SE_obj.scrape_all()

    # Eurosportplayer
    EurosportPlayer_SE_obj = EurosportPlayer()
    EurosportPlayer_SE_obj.create_object_SE()

    # Hayu - SE
    Hayu_obj_SE = Hayu()
    Hayu_obj_SE.create_object('SE')

    # Skyshowtime pd. Paramount plus
    SkyShowTime_obj = SkyShowTime()
    SkyShowTime_obj.create_object('SE')

    # Viaplay - FI, NO, SE and DK.
    viaplay_obj_DK = Viaplay()
    viaplay_obj_DK.create_objects_viaplay('DK')

    # Initilize class to merge data before read/write to excel
    # --- Combine dicts D2C services ---
    merge_output.SE_d2c = merge_output.combine_dicts([apple_obj.SE, TV4Play_obj_SE.SE,discovery_obj_SE.SE, 
         disney_obj_SE.SE,
         HBO_obj_SE.SE,
            netflix_obj.SE, 
           # AmazonPrime_SE_obj.SE,
            SkyShowTime_obj.SE,tele2playplus_obj.SE,viaplay_obj.SE
            ,
            YoutubePremium_SE_obj.SE,
            EurosportPlayer_SE_obj.SE, Hayu_obj_SE.SE])


    # Read/write to the excel files
    read_data(file_SE, merge_output.SE_d2c, 'SE')
    read_data_d2c(file_DK, viaplay_obj_DK.DK, 'DK')

# SET FINNISH VPN
def Finland_VPN(merge_output):

    # --- Services classified as D2C
    # HBO AND DISCOVERY -- requires finnish VPN
    VPN_FI_obj = VPN_FI()
    VPN_FI_obj.create_object()

    # AmazoonPrime
    AmazonPrimeFI_obj = AmazonPrimeFI()
    AmazonPrimeFI_obj.create_object()

    # Youtube Premium
    YoutubePremiumFI_obj = YoutubePremiumFI()
    YoutubePremiumFI_obj.create_object()

    # Eurosportplayer
    EurosportPlayerFI_obj = EurosportPlayerFI()
    EurosportPlayerFI_obj.create_object()

    # Hayu - FI
    Hayu_obj_FI = Hayu()
    Hayu_obj_FI.create_object('FI')

    DNA_TV_FI_obj = DNA_TV_FI()
    DNA_TV_FI_obj.create_object()

    SkyShowTime_obj = SkyShowTime()
    SkyShowTime_obj.create_object('FI')

    # --- Services that also works with Swedish VPN ---

    # Apple TV+
    apple_obj = AppleTVPlus()
    apple_obj.create_object('FI')

    # Ruutu FI
    Ruutu_FI_obj = Ruutu_FI()
    Ruutu_FI_obj.create_object()

    # Viaplay - FI, NO, SE and DK.
    viaplay_obj = Viaplay()
    viaplay_obj.create_objects_viaplay('FI')

    # FI
    disney_obj_FI_NO_DK_SE_obj = DisneyPlus_FI_NO_DK_SE()
    disney_obj_FI_NO_DK_SE_obj.create_object('FI')
    # FI
    mtv_obj = MTV()
    mtv_obj.create_object()

    # Netflix
    netflix_obj = Netflix()
    netflix_obj.create_object('FI')


    # Merge the output and read/write to excel
    merge_output.FI = merge_output.combine_dicts([apple_obj.FI, mtv_obj.FI, DNA_TV_FI_obj.FI, VPN_FI_obj.DISCO_FI,
                                                   disney_obj_FI_NO_DK_SE_obj.FI,
                                                  viaplay_obj.FI, VPN_FI_obj.HBO_FI, netflix_obj.FI, AmazonPrimeFI_obj.AMAZON_FI,
                                                   Ruutu_FI_obj.FI, SkyShowTime_obj.FI, 
                                                   YoutubePremiumFI_obj.FI,
                                                   EurosportPlayerFI_obj.FI, Hayu_obj_FI.FI])


    read_data_d2c(file_FI, merge_output.FI, 'FI')

# SET NORWEGIAN VPN
def Norway_VPN(merge_output):
    # --- Services classifed as D2C ---
    # Needs Norwegian VPN
    NO_VPN_obj = VPN_NO()
    NO_VPN_obj.create_object()

    # AmazoonPrime
    AmazonPrimeNO_obj = AmazonPrimeNO()
    AmazonPrimeNO_obj.create_object()

    # YoutubePremium NO
    YoutubePremiumNO_obj = YoutubePremiumNO()
    YoutubePremiumNO_obj.create_object()

    # Eurosportplayer NO
    EurosportPlayerNO_obj = EurosportPlayerNO()
    EurosportPlayerNO_obj.create_object()

    # Hayu - NO
    Hayu_obj_NO = Hayu()
    Hayu_obj_NO.create_object('NO')

    # --- Services that also works with Swedish VPN ---
    # Apple TV+
    apple_obj = AppleTVPlus()
    apple_obj.create_object('NO')

    # Viaplay - FI, NO, SE and DK.
    viaplay_obj = Viaplay()
    viaplay_obj.create_objects_viaplay('NO')

    # FI, NO, DK
    #disney_obj_FI_NO_DK_SE_obj = DisneyPlus_FI_NO_DK_SE()
    #disney_obj_FI_NO_DK_SE_obj.create_object('NO')

    # Netflix
    netflix_obj = Netflix()
    netflix_obj.create_object('NO')

    # TV2 Norway
    TV2_NO_obj = TV2_NO()
    TV2_NO_obj.create_object()

    # Strim Norway
    Strim_NO_obj = Strim_NO()
    Strim_NO_obj.create_object()

    # Skyshowtime fd. Paramount +
    SkyShowTime_obj = SkyShowTime()
    SkyShowTime_obj.create_object('NO')

    # Merge the output and read/write to excel
    merge_output.NO = merge_output.combine_dicts([ apple_obj.NO, NO_VPN_obj.DISCO_NO,
                                                  # disney_obj_FI_NO_DK_SE_obj.NO,
                                                   NO_VPN_obj.HBO_NO, netflix_obj.NO,
                                                   AmazonPrimeNO_obj.AMAZON_NO,SkyShowTime_obj.NO,
                                                   Strim_NO_obj.NO, TV2_NO_obj.NO, viaplay_obj.NO,
                                                   YoutubePremiumNO_obj.NO,
                                                    EurosportPlayerNO_obj.NO,  Hayu_obj_NO.NO])

    read_data_d2c(file_NO, merge_output.NO, 'NO')


# SET DANISH VPN
def Denmark_VPN(merge_output):
    # Services classified as D2C
    # --- NEEDS DANISH VPN ---
    DK_VPN_obj = VPN_DK()
    DK_VPN_obj.create_object()

    # AmazoonPrime
    AmazonPrimeDK_obj = AmazonPrimeDK()
    AmazonPrimeDK_obj.create_object()

    # Youtube Premium
    #YoutubePremiumDK_obj = YoutubePremiumDK()
    #YoutubePremiumDK_obj.create_object()

    # Eurosportplayer DK
    EurosportPlayerDK_obj = EurosportPlayerDK()
    EurosportPlayerDK_obj.create_object()

    # YouSee
    YouSee_DK_obj = YouSee_DK()
    YouSee_DK_obj.create_object()

    # Hayu DK
    Hayu_obj_DK = Hayu()
    Hayu_obj_DK.create_object('DK')

    # NordiskFilmPlus DK
    NordiskFilmPlus_obj = NordiskFilmPlus()
    NordiskFilmPlus_obj.create_object()

    # Skyshowtime fd. Paramount
    SkyShowTime_obj = SkyShowTime()
    SkyShowTime_obj.create_object('DK')

    # --- Services that also works with Swedish VPN ---
    # Apple TV+
    apple_obj = AppleTVPlus()
    apple_obj.create_object('DK')

    # FI, NO, DK
    disney_obj_FI_NO_DK_SE_obj = DisneyPlus_FI_NO_DK_SE()
    disney_obj_FI_NO_DK_SE_obj.create_object('DK')

    # Netflix - DK
    netflix_obj = Netflix()
    netflix_obj.create_object('DK')

    # TV2 DK
    TV2_DK_obj = TV2_DK()
    TV2_DK_obj.create_object()

    # Merge the output and read/write to excel
    merge_output.DK = merge_output.combine_dicts([netflix_obj.DK, 
                                                disney_obj_FI_NO_DK_SE_obj.DK,
                                                #DK_VPN_obj.HBO_DK,
                                                DK_VPN_obj.DISCO_DK,
                                                AmazonPrimeDK_obj.AMAZON_DK, TV2_DK_obj.DK, apple_obj.DK,
                                                EurosportPlayerDK_obj.DK, Hayu_obj_DK.DK, 
                                                NordiskFilmPlus_obj.DK,
                                               # YoutubePremiumDK_obj.DK,
                                                SkyShowTime_obj.DK, YouSee_DK_obj.DK])

    read_data_d2c(file_DK, merge_output.DK, 'DK')

if __name__ == "__main__":
    chromedriver_autoinstaller.install()
    merge_output = MergeOutput()
    # SWEDEN
    # Sweden_VPN(merge_output)
    # FINLAND
    #Finland_VPN(merge_output)
    # NORWAY
    #Norway_VPN(merge_output)
    # DENMARK
    Denmark_VPN(merge_output)