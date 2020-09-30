from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from typing import Dict, Text, Any, List

import requests
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction

# We use the medicare.gov database to find information about 3 different
# healthcare facility types, given a city name, zip code or facility ID
# the identifiers for each facility type is given by the medicare database
# xubh-q36u is for hospitals
# b27b-2uc7 is for nursing homes
# 9wzi-peqs is for home health agencies

# http://hapi.fhir.org/baseR4/Patient?_id=1271537
# http://hapi.fhir.org/baseR4/Encounter?subject=94ed9c20-7f16-4e27-aa79-66c883fccd19


# Resource (Encounter) - parameter (subject) - qualifier (=) - value (585457)
# http://hapi.fhir.org/baseR4/Encounter?subject=585457&&&
ENDPOINT = "http://hapi.fhir.org/baseR4/{}?{}{}{}&{}{}{}&{}{}{}&{}{}{}"

class SearchFhirEndpoint(Action):
    """This action class retrieves a FHIR bundle 
    according to a search criteria."""

    def name(self) -> Text:
        """Unique identifier of the action"""

        return "search_fhir_endpoint"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict]:

        fhir_resource = tracker.get_slot("fhir_resource")
        search_param = tracker.get_slot("search_param")
        search_qualifier = tracker.get_slot("search_qualifier")
        search_value = tracker.get_slot("search_value")
        full_path = ENDPOINT.format(fhir_resource, search_param, search_qualifier, search_value)
        results = requests.get(full_path).json()
        return results
    



