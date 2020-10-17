"""
 Copyright 2020 Bell Eapen
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
     http://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from typing import Dict, Text, Any, List

import requests
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction, AllSlotsReset
from rasa_sdk.forms import FormAction

from collections import defaultdict


# http://hapi.fhir.org/baseR4/Patient?_id=1271537
# http://hapi.fhir.org/baseR4/Encounter?subject=94ed9c20-7f16-4e27-aa79-66c883fccd19


# Resource (Encounter) - parameter (subject) - qualifier (=) - value (585457)
# http://hapi.fhir.org/baseR4/Encounter?subject=585457&&&
# ENDPOINT = "http://hapi.fhir.org/baseR4/{}?{}{}{}&{}{}{}&{}{}{}&{}{}{}"


def _find_fhir_records(fhir_resource, search_string) -> Dict:
    ENDPOINT = "http://hapi.fhir.org/baseR4/{}?{}"
    full_path = ENDPOINT.format(fhir_resource, search_string)
    print(full_path)  # for debugging
    results = requests.get(full_path).json()
    # if entry key in results
    if "entry" in results:
        return results['entry']
    else:
        {}


class ClearSearch(Action):
    """This action clears previous slot."""

    def name(self) -> Text:
        """Unique identifier of the action"""

        return "clear_search_action"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List:

        # TODO: update rasa core version for configurable `button_type`
        dispatcher.utter_message("Cleared previous search.")
        return [AllSlotsReset()]

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
        search_results = tracker.get_slot('search_results')
        search_string = tracker.get_slot('search_string')
        if search_string:
            search_string = search_string + search_param + search_qualifier + search_value + "&"
        else:
            search_string = search_param + search_qualifier + search_value + "&"
        results = _find_fhir_records(fhir_resource,
                                     search_string)
        button_name = "Resource"
        if not results and not search_results:  # Results is an empty Dict
            dispatcher.utter_message(
                "Sorry, we could not find a {}".format(button_name))
            return [AllSlotsReset()]

        buttons = []
        # limit number of results to 3 for clear presentation purposes

        # ! Somehow the payload gets set as the fhir_resource slot. Cannot figure out why!
        try:
            for entry in results[:3]:
                payload = entry['resource']['resourceType']
                buttons.append(
                    {"title": "{}".format(entry['resource']['id']), "payload": payload})
        except:
            dispatcher.utter_message(
                "Sorry, we could not find a {}".format(button_name))
            return [AllSlotsReset()]
            
        if len(buttons) == 0:  # Results is an empty Dict
            dispatcher.utter_message(
                "Sorry, we could not find a {}".format(button_name))
            return [AllSlotsReset()]

        if len(buttons) == 1:
            message = "Here is the resource {} you searched:".format(
                button_name)
        else:
            message = "Here are {} {}s:".format(len(buttons),
                                                         button_name)

        print(buttons)  # Debug
        # TODO: update rasa core version for configurable `button_type`
        dispatcher.utter_button_message(message, buttons)
        return [AllSlotsReset(), SlotSet("search_string", search_string), SlotSet("search_results", results)]
