import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ## In case of later improvements following code is helpful for testing the
# ## data-algorithmn before launching in gui
# service_ulr = "https://opendata.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0.geojson"
# r = requests.get(service_ulr)
# packages_json = r.json()

# with open("Data_RKI", "w") as Data_RKI:
    # json.dump(packages_json, Data_RKI, ensure_ascii=False, indent=4)

# # # JSON Data is ordered like this:
# # # dict_keys(['type', 'name', 'features'])

# # # Attribute keys:
# # # dict_keys(['FID', 'IdBundesland', 'Bundesland', 'Landkreis',
# # # 'Altersgruppe', 'Geschlecht', 'AnzahlFall', 'AnzahlTodesfall'
# # # , 'Meldedatum', 'IdLandkreis', 'Datenstand', 'NeuerFall', 'Ne
# # # uerTodesfall', 'Refdatum', 'NeuGenesen', 'AnzahlGenesen', 'Is
# # # tErkrankungsbeginn', 'Altersgruppe2'])

# with open("Data_RKI", "r") as Data_RKI:
    # packages_json = json.load(Data_RKI)

# # print(dataframe["name"])



class Data:
    """Following code reads API Data of several health institutes and
   makes it human readable"""


    def __init__(self, data):
        self.data = pd.DataFrame(data)
        dicts_of_feds = {}
        list_of_county = []
        for i in range(len(self.data["features"]) - 1):
            if self.data["features"][i]["properties"]["Bundesland"] in dicts_of_feds:
                pass
            else:
                dicts_of_feds[self.data["features"][i]["properties"]["Bundesland"]] = self.data["features"][i]["properties"]["IdBundesland"]

            if self.data["features"][i]["properties"]["Landkreis"] in list_of_county:
                pass
            else:
                list_of_county.append(self.data["features"][i]["properties"]["Landkreis"])
        self.dicts_of_feds = dicts_of_feds
        self.list_of_county = list_of_county
        self.list_of_fed = self.dicts_of_feds.keys()

    def total_death_number(self):
        """Following method returns total number of deaths of repuplic"""

        deaths = 0
        for i in range(len(self.data["features"]) - 1):
            deaths += self.data["features"][i]["properties"]["AnzahlTodesfall"]
        return deaths

    def total_ndeath_number(self):
        """Following method returns total number of new deaths of repuplic"""

        ndeaths = 0
        for i in range(len(self.data["features"]) - 1):
            if self.data["features"][i]["properties"]["NeuerTodesfall"] >= 0:
                ndeaths += self.data["features"][i]["properties"]["NeuerTodesfall"]
        return ndeaths

    def total_recov_number(self):
         """Following method returns total number of recovered patients of repuplic"""
        recov = 0
        for i in range(len(self.data["features"]) - 1):
            recov += self.data["features"][i]["properties"]["AnzahlGenesen"]
        return recov

    def total_nrecov_number(self):
        """Following method returns total number of new recovered patients of repuplic"""

        nrecov = 0
        for i in range(len(self.data["features"]) - 1):
            if self.data["features"][i]["properties"]["NeuGenesen"] >= 0:
                nrecov += self.data["features"][i]["properties"]["NeuGenesen"]
        return nrecov

    def total_infections_number(self):
        """Following method returns total number of corona patients of republic"""
        positive = 0
        for i in range(len(self.data["features"]) - 1):
            positive += self.data["features"][i]["properties"]["AnzahlFall"]
        return positive

    def total_ninfections_number(self):
        """Following method returns total number of corona patients of republic"""
        npositive = 0
        for i in range(len(self.data["features"]) - 1):
            if self.data["features"][i]["properties"]["NeuerFall"] >= 0:
                npositive += self.data["features"][i]["properties"]["NeuerFall"]
        return npositive

    def sex_deseased(self, sex):
        """Method that returns the total number of deseased corona patients ordered
       by Sex either M or W of republic"""
        if not (sex == "M" or sex == "W"):
            raise KeyError("M for male or W for woman ar valid keywords")
        deaths = 0
        for i in range(len(self.data["features"]) - 1):
            if self.data["features"][i]["properties"]["Geschlecht"] == sex:
                deaths += self.data["features"][i]["properties"]["AnzahlTodesfall"]
        return deaths

    def sex_age_infec(self):
        """Following method returns the number of infected corona patients
       depending of sex and age-group"""
        ages = ["A00-A04", "A05-A14", "A15-A34", "A35-A59", "A60-A79", "A80+"]
        ages_infec_male = {}
        ages_infec_female = {}
        for elem in ages:
            x = 0
            y = 0
            for i in range(len(self.data["features"]) - 1):
                if elem == self.data["features"][i]["properties"]["Altersgruppe"]:
                    if self.data["features"][i]["properties"]["Geschlecht"] == "M":
                        x += self.data["features"][i]["properties"]["AnzahlFall"]
                    elif self.data["features"][i]["properties"]["Geschlecht"] == "W":
                        y += self.data["features"][i]["properties"]["AnzahlFall"]
            ages_infec_male[elem] = x
            ages_infec_female[elem] = y
        return (ages_infec_female, ages_infec_male)
    
    def sex_age_death(self):
        """Following method returns the number of deseased corona patients
        depending of sex and age-group"""
        ages = ["A00-A04", "A05-A14", "A15-A34", "A35-A59", "A60-A79", "A80+"]
        ages_deaths_male = {}
        ages_deaths_female = {}
        for elem in ages:
            x = 0
            y = 0
            for i in range(len(self.data["features"]) - 1):
                if elem == self.data["features"][i]["properties"]["Altersgruppe"]:
                    if self.data["features"][i]["properties"]["Geschlecht"] == "M":
                        x += self.data["features"][i]["properties"]["AnzahlTodesfall"]
                    elif self.data["features"][i]["properties"]["Geschlecht"] == "W":
                        y += self.data["features"][i]["properties"]["AnzahlTodesfall"]
            ages_deaths_male[elem] = x
            ages_deaths_female[elem] = y
        return (ages_deaths_female, ages_deaths_male)

    def death_number_fed(self, federal_state):
        """Method that returns the total number of deaths in specific federal state"""
        number = int(self.dicts_of_feds[str(federal_state)])
        deaths = 0
        for i in range(len(self.data["features"]) - 1):
            if self.data["features"][i]["properties"]["IdBundesland"] == number:
                deaths += self.data["features"][i]["properties"]["AnzahlTodesfall"]
        return deaths
    
    def ndeath_number_fed(self, federal_state):
        """Method that returns the total number of new deaths in specific federal state"""
        number = int(self.dicts_of_feds[str(federal_state)])
        ndeaths = 0
        for i in range(len(self.data["features"]) - 1):
            if self.data["features"][i]["properties"]["IdBundesland"] == number\
                and self.data["features"][i]["properties"]["NeuerTodesfall"] >= 0:
                ndeaths += self.data["features"][i]["properties"]["NeuerTodesfall"]
        return ndeaths

    def recov_number_fed(self, federal_state):
        """Method that returns the total number of recoveries in specific federal state"""
        number = int(self.dicts_of_feds[str(federal_state)])
        recov = 0
        for i in range(len(self.data["features"]) - 1):
            if self.data["features"][i]["properties"]["IdBundesland"] == number:
                recov += self.data["features"][i]["properties"]["AnzahlGenesen"]
        return recov

    def nrecov_number_fed(self, federal_state):
        """Method that returns the total number of new recoveries in specific federal state"""

        number = int(self.dicts_of_feds[str(federal_state)])
        nrecov = 0
        for i in range(len(self.data["features"]) - 1):
            if self.data["features"][i]["properties"]["IdBundesland"] == number\
               and self.data["features"][i]["properties"]["NeuGenesen"] >= 0:
                nrecov += self.data["features"][i]["properties"]["NeuGenesen"]
        return nrecov

    def infections_number_fed(self, federal_state):
        """Method that returns the total number of corona patients of federal state"""

        number = int(self.dicts_of_feds[str(federal_state)])
        positive = 0
        for i in range(len(self.data["features"]) - 1):
            if self.data["features"][i]["properties"]["IdBundesland"] == number:
                positive += self.data["features"][i]["properties"]["AnzahlFall"]
        return positive

    def ninfections_number_fed(self, federal_state):
        """Method that returns the total number of new corona patients of federal state"""

        number = int(self.dicts_of_feds[str(federal_state)])
        npositive = 0
        for i in range(len(self.data["features"]) - 1):
            if self.data["features"][i]["properties"]["IdBundesland"] == number \
               and self.data["features"][i]["properties"]["NeuerFall"] >= 0:
                npositive += self.data["features"][i]["properties"]["NeuerFall"]
        return npositive

    def death_number_county(self, county):
        """Method that returns the total number of deseased corona patients from
        specific county"""
        if county not in self.list_of_county:
            raise KeyError("This county does not exist")
        deaths = 0
        for i in range(len(self.data["features"]) - 1):
            if self.data["features"][i]["properties"]["Landkreis"] == county:
                deaths += self.data["features"][i]["properties"]["AnzahlTodesfall"]
        return deaths

    def ndeath_number_county(self, county):
        """Method that returns the total number of new deseased corona patients from
        specific county"""
        if county not in self.list_of_county:
            raise KeyError("This county does not exist")
        deaths = 0
        for i in range(len(self.data["features"]) - 1):
            if self.data["features"][i]["properties"]["Landkreis"] == county \
                and self.data["features"][i]["properties"]["NeuerTodesfall"]\
                    >= 0:
                deaths += self.data["features"][i]["properties"]["NeuerTodesfall"]
        return deaths

    def infections_number_county(self, county):
        """Method that returns the total number of corona patient in specific
        county"""
        if county not in self.list_of_county:
            raise KeyError("This county does not exist")
        positive = 0
        for i in range(len(self.data["features"]) - 1):
            if self.data["features"][i]["properties"]["Landkreis"] == county:
                positive += self.data["features"][i]["properties"]["AnzahlFall"]
        return positive

    def ninfections_number_county(self, county):
        """Method that returns the total number new of corona patient in specific
        county"""
        if county not in self.list_of_county:
            raise KeyError("This county does not exist")
        positive = 0
        for i in range(len(self.data["features"]) - 1):
            if self.data["features"][i]["properties"]["Landkreis"] == county \
               and self.data["features"][i]["properties"]["NeuerFall"] >= 0:
                positive += self.data["features"][i]["properties"]["NeuerFall"]
        return positive

    
    def recov_number_county(self, county):
        """Method that returns the total number of revoveries in specific county"""
        if county not in self.list_of_county:
            raise KeyError("This county does not exist")
        recov = 0
        for i in range(len(self.data["features"]) - 1):
            if self.data["features"][i]["properties"]["Landkreis"] == county:
                recov += self.data["features"][i]["properties"]["AnzahlGenesen"]
        return recov

    def nrecov_number_county(self, county):
        """Method that returns the total number of revoveries in specific county"""

        if county not in self.list_of_county:
            raise KeyError("This county does not exist")
        recov = 0
        for i in range(len(self.data["features"]) - 1):
            if self.data["features"][i]["properties"]["Landkreis"] == county \
               and self.data["features"][i]["properties"]["NeuGenesen"] >= 0:
                recov += self.data["features"][i]["properties"]["NeuGenesen"]
        return recov

    # """Method that returns a bar plot of corona deaths depending on age and sex"""
    # def plot_data(self):
        # female, male = self.sex_age_death()
        # ticks = female.keys()
        # x = np.arange(len(ticks))
        # fig, ax = plt.subplots()
        # ax.bar(x - 0.2, female.values(), width=0.4, label="weiblich")
        # ax.bar(x + 0.2, male.values(), width=0.4, label="männlich")
        # ax.set_xticks(x)
        # ax.set_xticklabels(female.keys())
        # ax.set_xlabel("Altersgruppe")
        # ax.legend()
        # plt.tight_layout()
        # plt.show()
if __name__ is "__main__":
    data = Data(packages_json)
