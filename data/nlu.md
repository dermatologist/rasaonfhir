## intent:greet
- hey
- hello
- hi
- good morning
- good evening
- hey there

## intent:goodbye
- bye
- goodbye
- see you around
- see you later

## intent:affirm
- yes
- indeed
- of course
- that sounds good
- correct

## intent:deny
- no
- never
- I don't think so
- don't like that
- no way
- not really

## intent:mood_great
- perfect
- very good
- great
- amazing
- wonderful
- I am feeling very good
- I am great
- I'm good

## intent:mood_unhappy
- sad
- very sad
- unhappy
- bad
- very bad
- awful
- terrible
- not very good
- extremely sad
- so sad

## intent:bot_challenge
- are you a bot?
- are you a human?
- am I talking to a bot?
- am I talking to a human?

## intent:search_fhir
- show me a [patient](fhir_resource)
- show me the [patient](fhir_resource) with [id](search_param) [equals](search_qualifier) [23452](search_value)
- show me the [encounter](fhir_resource) with [subject](search_param) [as](search_qualifier) [7c248588-701c-4d91-9aa0-5307b2b06998](search_value)
- show me the [observation](fhir_resource) with [subject](search_param) [as](search_qualifier) [7c248588-701c-4d91-9aa0-5307b2b06998](search_value)
- bring me the [observation](fhir_resource) 

## intent:clear_search
- clear my search
- start over
- search again

## intent:inform
- [Patient](fhir_resource)
- [subject](search_param)
- [encounter](fhir_resource)
- [visit](fhir_resource)
- [observation](fhir_resource)

## synonym:=
- equals
- equal
- as
- same as

## synonym:Encounter
- encounter
- visit
