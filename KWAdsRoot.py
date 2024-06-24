
# Define the keywords to include
breakdown_keywords = ["breakdown", "roadside assistance", "road side", 
                        "road emergency", "road rescue", "emergency car repair", 
                        "car check", "car rescue", "roadside repair", 
                        "fire damage", "theft damage", "accident assist"]
insurance_keywords = ["insurance", "cover", "policy", "policies",
                        "offer", "offers", "deal", "deals", "claim", "claims", 
                        "services"]

# create a loop to combine the keywords and return as a list
def keyword_combination(breakdown_keywords, insurance_keywords):
    keyword_combinations = []
    for i in breakdown_keywords:
        for j in insurance_keywords:
            keyword_combinations.append(i + " " + j)
    return keyword_combinations

keywordlist = keyword_combination(breakdown_keywords, insurance_keywords)
keywordlist


# Create a function to filter keywords
def filter_keywords(df, breakdown_keywords, insurance_keywords):
    filtered_keywords = []
    for breakdown in breakdown_keywords:
        for insurance in insurance_keywords:
            # Combine keywords for matching
            combined_keywords = [
                f"{breakdown} {insurance.lower()}", f"{breakdown} {insurance.capitalize()}",
                f"{breakdown.capitalize()} {insurance.lower()}", f"{breakdown.capitalize()} {insurance.capitalize()}"
            ]
            filtered_keywords.extend(combined_keywords)
    
    # Filter the dataframe based on the combined keywords
    mask = df['Keyword'].apply(lambda x: any(keyword in x.lower() for keyword in filtered_keywords))
    return df[mask]


# create a new dataframe where Keyword column does not contain "breakdown"
nonbreakdownKWs = filtered_df[~filtered_df['Keyword'].str.contains("breakdown")]
nonbreakdownKWs = nonbreakdownKWs.sort_values('Search Volume', ascending=False)


def pushGSdata(GSID, sheetname, df):
    ''' Push the pandas dataframe to google sheets'''
    # GCP App creds
    creds = ServiceAccountCredentials.from_json_keyfile_name('gsheets-temujim.json', ['https://spreadsheets.google.com/feeds'])

    gc = gspread.authorize(creds)

    # open by gsheet ID: '1Wg-cfsA2IarsbW7dzwesQYXhIetSVABBEQm_ykzZsOs'
    sheet = gc.open_by_key(GSID)

    ws = sheet.worksheet(sheetname)

    set_with_dataframe(ws, df)

    return

# copy dataframe to goglesheets
pushGSdata('1Wg-cfsA2IarsbW7dzwesQYXhIetSVABBEQm_ykzZsOs', 'Filtered_KWsV2', df)

pushGSdata('1Wg-cfsA2IarsbW7dzwesQYXhIetSVABBEQm_ykzZsOs', 'Filtered_KWs', filtered_df)

pushGSdata('1Wg-cfsA2IarsbW7dzwesQYXhIetSVABBEQm_ykzZsOs', 'NonBreakdown', nonbreakdownKWs)
