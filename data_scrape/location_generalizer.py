import os
import json
import pickle
import re
import demoji
import textwrap
import pandas as pd
from together import Together

def deEmojify(inputString):
    return demoji.replace_with_desc(inputString.encode('utf-16', 'surrogatepass').decode('utf-16'))

class LocationGeneralizer:
    def __init__(self, all_locations):

        self.loc_country_map = {}
        self.failed = []
        self.all_locations = all_locations
        self.template = """
        You are given a list of user-specified locations. Your task is to map each location to the appropriate country.
        Return the result as a JSON list, with each item containing two keys: "location" and "country".
        If a location cannot be generalized to a specific country, assign the value "None" to "country".

        Example: 
        ["London, UK", "Japan", "Banana", "Washington"] ->
        [{{"location": "London, UK", "country": "England"}}, 
        {{"location": "Japan", "country": "Japan"}},  
        {{"location": "Banana", "country": "None"}}, 
        {{"location": "Washington", "country": "United States"}}]

        Guidelines: 
        - Do NOT include explanations, comments, or any additional text.
        - ONLY return the output in JSON format.
        - Ensure the JSON is properly formatted and contains no trailing commas or unnecessary spaces.
        - Do NOT use "United Kingdom" or "UK" as a country if given a country within the UK - e.g. the location "Wales, UK" should be mapped to "Wales".
        - ONLY map the given locations in the Task section. Do NOT map the locations given in the Example section unless the locations are given in the Task section.

        Task: 
        Now map each of the following locations to their respective countries: {locations}

        JSON output:
        """
        self.client = Together(api_key=os.environ.get('TOGETHER_API_KEY'))
    
    def map_locations(self, locations):

        response = self.client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            messages=[{"role": "user", "content": self.template.format(locations=locations)}],
            max_tokens=1200
        )

        out = response.choices[0].message.content
        formatted_out = textwrap.dedent(out.strip())

        try: 
            return json.loads(formatted_out)

        except json.JSONDecodeError:
            print("JSONDecoderError - see following output")
            print(formatted_out)
            self.failed.append(formatted_out)
            return []

        except UnicodeDecodeError:
            print("UnicodeDecodeError - see following output")
            print(formatted_out) 
            self.failed.append(formatted_out)
            return []

        except: 
            self.failed.append(formatted_out)
            return []

    def update_map(self, mapped_locations):

        for loc_country_dict in mapped_locations:
            if loc_country_dict["location"] not in self.loc_country_map:
                self.loc_country_map[loc_country_dict["location"]] = loc_country_dict["country"]
    
    def map_all_locations(self):
        
        for i in range(20, len(self.all_locations) + 1 + 20, 20):
            locations = self.all_locations[i - 20:i]
            out = self.map_locations(locations=locations)
            self.update_map(out)

        return self.loc_country_map, self.failed

if __name__ == "__main__":

    replies = pd.read_csv("/home/jasmine/PROJECTS/research/data_scrape/REPLIES_FINAL.csv")
    # only English tweets
    replies = replies[replies["lang"] == "en"]

    places = replies["place"].unique()
    places = [re.search(r"fullName='(.*?)'", place).group(1) for place in places[1:]]

    generalizer = LocationGeneralizer(places)
    place_country_map, failed = generalizer.map_all_locations()

    with open('PLACE_TO_COUNTRY_MAP.pickle', 'wb') as handle:
        pickle.dump(place_country_map, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('FAILED_PLACES.pickle', 'wb') as handle:
        pickle.dump(failed, handle, protocol=pickle.HIGHEST_PROTOCOL)

    
    # unique_locations = replies["user_location"].unique().tolist()
    # unique_locations = [deEmojify(str(location)) for location in unique_locations]
    
    # generalizer = LocationGeneralizer(unique_locations)
    # loc_country_map, failed = generalizer.map_all_locations()

    # with open('LOCATION_TO_COUNTRY_MAP.pickle', 'wb') as handle:
    #     pickle.dump(loc_country_map, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # with open('FAILED.pickle', 'wb') as handle:
    #     pickle.dump(failed, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"All locations mapped; len(provided) = {len(places)}; len(map) = {len(place_country_map)}")