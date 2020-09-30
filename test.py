import requests
from collections import defaultdict
from typing import Dict, Text, Any, List

def _find_fhir_records(*args) -> List[Text]:
    ENDPOINT = "http://hapi.fhir.org/baseR4/{0[fhir_resource]}?{0[search_param]}{0[search_qualifier]}{0[search_value]}&{0[search_param1]}{0[search_qualifier1]}{0[search_value1]}"
    kwargs = {
        'fhir_resource': args[0], 
        'search_param': args[1], 
        'search_qualifier': args[2], 
        'search_value': args[3]
    }
    full_path = ENDPOINT.format(defaultdict(str, kwargs))
    results = requests.get(full_path).json()
    to_return = []
    for entry in results['entry']:
        print(entry['fullUrl']) 
        to_return.append(entry['fullUrl'])
    return to_return

if __name__ == "__main__":
    _find_fhir_records('Encounter', "subject", "=", "585457")