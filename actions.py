from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from typing import Dict, Text, Any, List

import requests
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction

from collections import defaultdict

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
# ENDPOINT = "http://hapi.fhir.org/baseR4/{}?{}{}{}&{}{}{}&{}{}{}&{}{}{}"


def _find_fhir_records(*args) -> List:
    ENDPOINT = "http://hapi.fhir.org/baseR4/{0[fhir_resource]}?{0[search_param]}{0[search_qualifier]}{0[search_value]}&{0[search_param1]}{0[search_qualifier1]}{0[search_value1]}"
    kwargs = {
        'fhir_resource': args[0], 
        'search_param': args[1], 
        'search_qualifier': args[2], 
        'search_value': args[3]
    }
    full_path = ENDPOINT.format(defaultdict(str, kwargs))
    print(full_path) # for debugging
    results = requests.get(full_path).json()
    return results['entry']
    # to_return = []
    # for entry in results['entry']:
    #     print(entry['fullUrl']) 
    #     to_return.append(entry['fullUrl'])
    # return to_return
    
class FhirSearchForm(FormAction):
    """Custom form action to fill all slots required to find specific type
    of resources on a FHIR server."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "fhir_search_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""

        return ["fhir_resource", "search_param", "search_qualifier", "search_value"]

    # slots are entities that need to be remembered.
    # Shares the same name here and hence automatically mapped
    # Can be mapped from multiple intents
    # inform could be a single word intent common in many nlu
    def slot_mappings(self) -> Dict[Text, Any]:
        return {
                "fhir_resource": self.from_entity(entity="fhir_resource",
                                                  intent=["inform",
                                                          "search_fhir"]),
                "search_qualifier": self.from_entity(entity="search_qualifier",
                                                  intent=["inform",
                                                          "search_fhir"]),
                "search_value": self.from_entity(entity="search_value",
                                                  intent=["inform",
                                                          "search_fhir"]),
                "search_param": self.from_entity(entity="search_param",
                                             intent=["inform",
                                                     "search_fhir"])
                }

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Once required slots are filled, print buttons for found resources"""

        fhir_resource = tracker.get_slot('fhir_resource')
        search_param = tracker.get_slot('search_param')
        search_qualifier = tracker.get_slot('search_qualifier')
        search_value = tracker.get_slot('search_value')

        results = _find_fhir_records(fhir_resource,
                                      search_param,
                                      search_qualifier,
                                      search_value)
        button_name = "Resource"
        if len(results) == 0:
            dispatcher.utter_message(
                "Sorry, we could not find a {}".format(button_name))
            return []

        buttons = []
        # limit number of results to 3 for clear presentation purposes
        for entry in results[:3]:
            payload = entry['fullUrl']
            buttons.append(
                {"title": "{}".format(entry['id']), "payload": payload})

        if len(buttons) == 1:
            message = "Here is the resource {} you searched:".format(button_name)
        else:
            message = "Here are {} {}s near you:".format(len(buttons),
                                                         button_name)

        # TODO: update rasa core version for configurable `button_type`
        dispatcher.utter_button_message(message, buttons)

        return []




