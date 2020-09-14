# Search

## format

In the simplest case, a search is executed by performing a GET operation in the RESTful framework:

```
 GET [base]/[type]?name=value&...{&_format=[mime-type]}}
```
```
POST  [base]/[type]/_search{?[parameters]{&_format=[mime-type]}}
```
*the parameters are a series of name=[value] pairs encoded in the URL or as an application/x-www-form-urlencoded submission for a POST
[type] is resources such as Patient, Observation etc

### Search Parameter Types

Number
Date/DateTime
String
Token
Reference
Composite
Quantity
URI
Special

### Parameters for all resources	
_id
_lastUpdated
_tag
_profile
_security
_text
_filter
_content
_list
_has
_query
_type

### Search result parameters
_sort
_count
_include
_revinclude
_summary
_total
_elements
_contained
_containedType

### Contexts
* A specified resource type: GET [base]/[type]?parameter(s)
* A specified compartment, perhaps with a specified resource type in that compartment: GET [base]/Patient/[id]/[type]?parameter(s)
* All resource types: GET [base]?parameter(s) (parameters common to all types). If the _type parameter is included, all other search parameters SHALL be common to all provided types. If _type is not included, all parameters SHALL be common to all resource types.

### tag

 GET [base]/Condition?_tag=http://acme.org/codes|needs-review
searches for all Condition resources with the tag:

```
{
  "system" : "http://acme.org/codes",
  "code" : "needs-review"
}
```

### id

```
GET [base]/Patient?_id=23
```

### missing

```
:missing; e.g. gender:missing=true (or false). Searching for gender:missing=true will return all the resources that don't have a value for the gender parameter (which usually equates to not having the relevant element in the resource). 
```

:exact, :contains, :text, :in, :not-in, :below, :above
eq, ne, gt, lt, ge, le, sa (starts after), eb (ends before), ap (approximately)

```
GET [base]/RiskAssessment?probability=gt0.8
GET [base]/Patient/23/Procedure?date=ge2010-01-01&date=le2011-12-31
[base]/Patient?given:contains=eve

```

* The modifier :above or :below can be used to indicate that partial matching is used. For example:

 GET [base]/ValueSet?url:below=http://acme.org/fhir/
 GET [base]/ValueSet?url:above=http://acme.org/fhir/ValueSet/123/_history/5
 
### Token

[parameter]=[code]: the value of [code] matches a Coding.code or Identifier.value irrespective of the value of the system property
[parameter]=[system]|[code]: the value of [code] matches a Coding.code or Identifier.value, and the value of [system] matches the system property of the Identifier or Coding
[parameter]=|[code]: the value of [code] matches a Coding.code or Identifier.value, and the Coding/Identifier has no system property
[parameter]=[system]|: any element where the value of [system] matches the system property of the Identifier or Coding

#### special case
:of-type	The search parameter has the format system|code|value, where the system and code refer to a Identifier.type.coding.system and .code, and match if any of the type codes match. All 3 parts must be present


### Examples
 GET [base]/Patient?identifier=http://acme.org/patient|2345
Search for all the patients with an identifier with key = "2345" in the system "http://acme.org/patient"
 GET [base]/Patient?gender=male
Search for any patient with a gender that has the code "male"
 GET [base]/Patient?gender:not=male
Search for any patient with a gender that does not have the code "male". Note that for :not, the search does not return any resources that have a gen
 GET [base]/Composition?section=48765-2
Search for any Composition that contains an Allergies and adverse reaction section
 GET [base]/Composition?section:not=48765-2
Search for any Composition that does not contain an Allergies and adverse reaction section. Note that this search does not return "any document that has a section that is not an Allergies and adverse reaction section" (e.g. in the presence of multiple possible matches, the negation applies to the set, not each individual entry)
 GET [base]/Patient?active=true
Search for any patients that are active
 GET [base]/Condition?code=http://acme.org/conditions/codes|ha125
Search for any condition with a code "ha125" in the code system "http://acme.org/conditions/codes"
 GET [base]/Condition?code=ha125
Search for any condition with a code "ha125". Note that there is not often any useful overlap in literal symbols between code systems, so the previous example is generally preferred
 GET [base]/Condition?code:text=headache
Search for any Condition with a code that has a text "headache" associated with it (either in the text, or a display)
 GET [base]/Condition?code:in=http%3A%2F%2Fsnomed.info%2Fsct%3Ffhir_vs%3Disa%2F126851005
Search for any condition in the SNOMED CT value set "http://snomed.info/sct?fhir_vs=isa/126851005" that includes all descendants of "Neoplasm of liver"
 GET [base]/Condition?code:below=126851005
Search for any condition that is subsumed by the SNOMED CT Code "Neoplasm of liver". Note: This is the same outcome as the previous search
 GET [base]/Condition?code:in=http://acme.org/fhir/ValueSet/cardiac-conditions
Search for any condition that is in the institutions list of cardiac conditions
 GET [base]/Patient?identifier:otype=http://terminology.hl7.org/CodeSystem/v2-0203|MR|446053
Search for the Medical Record Number 446053 - this is useful where the system id for the MRN is not known

#### Quantity
GET [base]/Observation?value-quantity=5.4|http://unitsofmeasure.org|mg
Search for all the observations with a value of 5.4(+/-0.05) mg where mg is understood as a UCUM unit (system/code)
 GET [base]/Observation?value-quantity=5.40e-3|http://unitsofmeasure.org|g
Search for all the observations with a value of 0.0054(+/-0.000005) g where g is understood as a UCUM unit (system/code)
 GET [base]/Observation?value-quantity=5.4||mg
Search for all the observations with a value of 5.4(+/-0.05) mg where the unit - either the code (code) or the stated human unit (unit) are "mg"
 GET [base]/Observation?value-quantity=5.4
Search for all the observations with a value of 5.4(+/-0.05) irrespective of the unit
 GET [base]/Observation?value-quantity=le5.4|http://unitsofmeasure.org|mg
Search for all the observations where the value of is less than 5.4 mg exactly where mg is understood as a UCUM unit
 GET [base]/Observation?value-quantity=ap5.4|http://unitsofmeasure.org|mg
Search for all the observations where the value of is about 5.4 mg where mg is understood as a UCUM unit (typically, within 10% of the value - see above)


### References

Some references may point to more than one type of resource; e.g. subject: Reference(Patient|Group|Device|..). In these cases, multiple resources may have the same logical identifier. Servers SHOULD reject a search where the logical id refers to more than one matching resource across different types. In order to allow the client to perform a search in these situations the type is specified explicitly:

 GET [base]/Observation?subject=Patient/23
This searches for any observations where the subject refers to the patient resource with the logical identifier "23". A modifier is also defined to allow the client to be explicit about the intended type:

 GET [base]/Observation?subject:Patient=23


### Examples of using composite parameters:

Search	Description
 GET [base]/DiagnosticReport?result.code-value-quantity=http://loinc.org|2823-3$gt5.4|http://unitsofmeasure.org|mmol/L
Search for all diagnostic reports that contain on observation with a potassium value of >5.4 mmol/L (UCUM)
 GET [base]/Observation?component-code-value-quantity=http://loinc.org|8480-6$lt60
Search for all the observations with a systolic blood pressure < 60. Note that in this case, the unit is assumed (everyone uses mmHg)
 GET [base]/Group?characteristic-value=gender$mixed
Search for all groups that have a characteristic "gender" with a text value of "mixed"
 GET [base]/Questionnaire?context-type-value=focus$http://snomed.info/sct|408934002
Search for all questionnaires that have a clinical focus = "Substance abuse prevention assessment (procedure)"