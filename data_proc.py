import pandas as pd
import re


def dfs():

    df = pd.read_csv("olympic_hosts.csv")

    print(df[:5])

    df2 = pd.read_csv("olympic_medals_changed.csv", sep=";")

    df2 = df2[["slug_game", "event_title", "discipline_title", "event_gender", "medal_type", "participant_type", "athlete_full_name", "country_name", "game_season", "country_3_letter_code"]]

    country_mapping = {
        "Russian Federation": "Russia",
        "People's Republic of China": "China",
        "Olympic Athletes from Russia": "Russia",
        "Soviet Union": "Russia",
        "ROC": "Chinese Taipai",
        "Federal Republic of Germany": "Germany",
        "Germany": "Germany",
        "German Democratic Republic (Germany)": "Germany",
        "Democratic People's Republic of Korea": "North Korea",
        "Republic of Korea": "South Korea"
        }

    country_letter_mapping = {
            "OAR": "RUS",
            "FRG": "GER",
            "URS": "RUS",
            "GDR": "GER"
            }

    mask = df2['country_name'].isin(country_mapping.keys())
    mask2 = df2["country_3_letter_code"].isin(country_letter_mapping.keys())

    df2.loc[mask, "country_name"] = df2.loc[mask, "country_name"].replace(country_mapping)
    df2.loc[mask2, "country_3_letter_code"] = df2.loc[mask2, "country_3_letter_code"].replace(country_letter_mapping)

    df2['discipline_event_country'] = df2['discipline_title'] + df2['event_title'] + df2['country_name'] + df2["event_gender"] + df2["participant_type"] + df2["slug_game"]

    def sortby(df):
        gold_counts = {}
        silver_counts = {}
        bronze_counts = {}
        gold_result = []
        silver_result = []
        bronze_result = []

        for idx, row in df.iterrows():
            key = row['discipline_event_country']

            #Gold
            if row['medal_type'] == 'GOLD':
                if key not in gold_counts:
                    gold_counts[key] = 1
                    gold_result.append(1)
                else:
                    gold_result.append(0)
            else:
                gold_result.append(0)
            #Silver
            if row['medal_type'] == 'SILVER':
                if key not in silver_counts:
                    silver_counts[key] = 1
                    silver_result.append(1)
                else:
                    silver_result.append(0)
            else:
                silver_result.append(0)
            #Bronze
            if row['medal_type'] == 'BRONZE':
                if key not in bronze_counts:
                    bronze_counts[key] = 1
                    bronze_result.append(1)
                else:
                    bronze_result.append(0)
            else:
                bronze_result.append(0)

        
        return gold_result, silver_result, bronze_result


    df2["Gold"], df2["Silber"], df2["Bronze"] = sortby(df2)

    print(df2[:-5])

    return df, df2

def medal_tally(df2, country=None, season=None, sport=None, game=None, sex=None):
    if country != "All":
        df2 = df2[df2["country_name"] == country]

    if season != "All":
        df2 = df2[df2["game_season"] == season]

    if sport != "All":
        df2 = df2[df2["discipline_title"] == sport]

    if game != "All":
        df2 = df2[df2["slug_game"] == game]

    if sex != "All":
        df2 = df2[df2["event_gender"] == sex]

    medal_tally_table = df2.groupby("country_name").sum()[["Gold", "Silber", "Bronze"]] 
    medal_tally_table["Total"] = medal_tally_table["Gold"] + medal_tally_table["Silber"] + medal_tally_table["Bronze"]
    medal_tally_table = medal_tally_table.sort_values(by="Gold", ascending=False).reset_index()
    medal_tally_table["Platzierung"] = medal_tally_table.index + 1
    medal_tally_table["Country"] = medal_tally_table["country_name"]

    return medal_tally_table


def medal_tally_heat(df2, country=None, season=None, sport=None, game=None, sex=None):
    if country != "All":
        df2 = df2[df2["country_name"] == country]

    if season != "All":
        df2 = df2[df2["game_season"] == season]

    if sport != "All":
        df2 = df2[df2["discipline_title"] == sport]

    if game != "All":
        df2 = df2[df2["slug_game"] == game]

    if sex != "All":
        df2 = df2[df2["event_gender"] == sex]

    medal_tally_table = df2.groupby(["country_name", "country_3_letter_code"]).sum()[["Gold", "Silber", "Bronze"]] 

    max_Gold = medal_tally_table["Gold"].max() 
    max_Silber = medal_tally_table["Silber"].max() 
    max_Bronze = medal_tally_table["Bronze"].max() 

    medal_tally_table["Gold_normalized"] = medal_tally_table["Gold"]/max_Gold if max_Gold > 0 else 0
    medal_tally_table["Silber_normalized"] = medal_tally_table["Silber"]/max_Silber if max_Silber > 0 else 0
    medal_tally_table["Bronze_normalized"] = medal_tally_table["Bronze"]/max_Bronze if max_Bronze > 0 else 0

    medal_tally_table["Total"] = medal_tally_table["Gold"] + medal_tally_table["Silber"] + medal_tally_table["Bronze"]
    medal_tally_table = medal_tally_table.sort_values(by="Gold", ascending=False).reset_index()
    medal_tally_table["Platzierung"] = medal_tally_table.index + 1
    medal_tally_table["Country"] = medal_tally_table["country_name"]

    return medal_tally_table

def ath():
    ath = pd.read_csv("olympic_athletes.csv")
    def extract_medals(medals_str):
            if pd.isna(medals_str):
                return 0, 0, 0
            
            # Bereinigen von Whitespace-Zeichen
            medals_str = ''.join(medals_str.split()).strip()
            
            # Standardwerte für Gold, Silber und Bronze
            gold, silver, bronze = 0, 0, 0
            
            # Verwenden von regulären Ausdrücken, um die Anzahl der Medaillen zu extrahieren
            gold_match = re.search(r'(\d+)G', medals_str)
            silver_match = re.search(r'(\d+)S', medals_str)
            bronze_match = re.search(r'(\d+)B', medals_str)
            
            if gold_match:
                gold = int(gold_match.group(1))
            if silver_match:
                silver = int(silver_match.group(1))
            if bronze_match:
                bronze = int(bronze_match.group(1))
            
            return gold, silver, bronze

        # Anwenden der Funktion auf die athlete_medals-Spalte und Spalten hinzufügen
    ath[['Gold', 'Silber', 'Bronze']] = ath['athlete_medals'].apply(lambda x: pd.Series(extract_medals(x)))
    
    return ath

def ath_med(ath):
    ath_sum_gold = ath["Gold"].sum()
    ath_sum_silber = ath["Silber"].sum()
    ath_sum_bronze = ath["Bronze"].sum()

    ath_sum_athletes = len(ath["athlete_full_name"])

    ath_no_medal = ath[(ath["Gold"] == 0) & (ath["Silber"] == 0) & (ath["Bronze"] ==0)]
    ath_no_medal_count = len(ath_no_medal["athlete_full_name"])

    perc_gold = (ath_sum_gold * 100)/(ath_sum_athletes)
    perc_silber = (ath_sum_silber * 100)/(ath_sum_athletes)
    perc_bronze = (ath_sum_bronze * 100)/(ath_sum_athletes)
    perc_no_medal = (ath_no_medal_count * 100)/(ath_sum_athletes)

    df = pd.DataFrame({"id" : [1, 2, 3, 4],
          "medal_type": ["Gold", "Silber", "Bronze", "No Medal"],
          "percentage": [perc_gold, perc_silber, perc_bronze, perc_no_medal]})

    return df

def medal_tally_bar(df2, season=None, sport=None, game=None, sex=None, country=None):
    if country != "All":
        df2 = df2[df2["country_name"] == country]

    if season != "All":
        df2 = df2[df2["game_season"] == season]

    if sport != "All":
        df2 = df2[df2["discipline_title"] == sport]

    if game != "All":
        df2 = df2[df2["slug_game"] == game]

    if sex != "All":
        df2 = df2[df2["event_gender"] == sex]

    medal_tally_table = df2.groupby(["country_3_letter_code", "country_name"]).sum()[["Gold", "Silber", "Bronze"]] 
    medal_tally_table["Total"] = medal_tally_table["Gold"] + medal_tally_table["Silber"] + medal_tally_table["Bronze"]
    medal_tally_table = medal_tally_table.sort_values(by="Total", ascending=False).reset_index()
    medal_tally_table["Platzierung"] = medal_tally_table.index + 1

    return medal_tally_table

def ath_medal_table(ath):

    ath = ath.sort_values(by="Gold", ascending=False).reset_index()
    ath["Platzierung"] = ath.index + 1 

    return ath
