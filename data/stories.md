## happy path
* greet
  - utter_greet
* inform
  - fhir_search_form
  - form{"name": "fhir_search_form"}
  - form{"name": null}
* clear_search
  - utter_confirm
* affirm
  - clear_search_action
  - utter_noworries
* goodbye
  - utter_noworries

## second path
* deny
  - utter_greet
* inform
  - fhir_search_form
  - form{"name": "fhir_search_form"}
  - form{"name": null}
* clear_search
  - utter_confirm
* affirm
  - clear_search_action
  - utter_noworries
* goodbye
  - utter_noworries

