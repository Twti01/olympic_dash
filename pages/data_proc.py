import pandas as pd


def dfs():

    df = pd.read_csv("olympic_hosts.csv")

    print(df[:5])

    df2 = pd.read_csv("olympic_medals.csv")

    df2 = df2[["slug_game", "event_title", "discipline_title", "event_gender", "medal_type", "participant_type", "athlete_full_name", "country_name"]]

    country_mapping = {
        "Russian Federation": "Russia",
        "Soviet Union": "Russia",
        "People's Republic of China": "China",
        "ROC": "China",
        "Federal Republic of Germany": "Germany",
        "Germany": "Germany",
        "German Democratic Republic (Germany)": "Germany",
        "Democratic People's Republic of Korea": "South Korea",
        "Republic of Korea": "South Korea"
        }

    mask = df2['country_name'].isin(country_mapping.keys())

    df2.loc[mask, "country_name"] = df2.loc[mask, "country_name"].replace(country_mapping)

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

def medal_tally(df2, sport=None, game=None, sex=None):
    if sport != "All":
        df2 = df2[df2["discipline_title"] == sport]

    if game != "All":
        df2 = df2[df2["slug_game"] == game]

    if sex != "All":
        df2 = df2[df2["event_gender"] == sex]

    medal_tally_table = df2.groupby("country_name").sum()[["Gold", "Silber", "Bronze"]] 
    medal_tally_table["Total"] = medal_tally_table["Gold"] + medal_tally_table["Silber"] + medal_tally_table["Bronze"]
    medal_tally_table = medal_tally_table.sort_values(by="Total", ascending=False).reset_index()
    medal_tally_table["Platzierung"] = medal_tally_table.index + 1
    medal_tally_table["Country"] = medal_tally_table["country_name"]

    return medal_tally_table

