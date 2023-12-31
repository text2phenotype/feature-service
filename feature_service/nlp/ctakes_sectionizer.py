from text2phenotype.ccda import ccda


# TODO: read up on cTAKES sectionizer
def get_section_aspect_map_ctakes():
    """
    Get a list of sections known by cTAKES

    # http://ctakes.apache.org/apidocs/3.1.1/ctakes-type-system/org/apache/ctakes/typesystem/type/textspan/Segment.html
    # https://issues.apache.org/jira/browse/CTAKES-200
    # https://cwiki.apache.org/confluence/display/CTAKES/cTAKES+3.0+-+Clinical+Documents+Pipeline

    :return: dict() key=val where key is
    """
    sections = {}

    for line in __ctakes_sections__.splitlines():
        tokens = line.split(',')

        if len(tokens) > 1:

            print(tokens)

            oid = tokens[0]
            code = tokens[1]
            titles = tokens[2:]
            aspect = ccda.section_template_map.get(code).aspect

            for t in titles:
                sections[t.strip().upper()] = aspect

    return sections


#######################################################################################################################
# This file is used by ctakes-core/sectionizer
# It uses rules and RegEx to match the section headers
# It is derived from the Consolidated CDA/HL7 standard
# http://bluebuttonplus.org/healthrecords.html
# http://cdatools.org/infocenter/index.jsp
# The format is as follows:
# HL7 template id,LOINC Section Code,n list of header names
# Custom ones can be added to the below mapping file
# By Default,they are case insenstive and spaces trimmed.
#######################################################################################################################

__ctakes_sections__ = """
2.16.840.1.113883.10.20.22.2.21,42348-3,Advance Directives
2.16.840.1.113883.10.20.22.2.6.1,48765-2,Allergies,Adverse Reactions,allergy
2.16.840.1.113883.10.20.22.2.25,59774-0,Anesthesia Section
2.16.840.1.113883.10.20.22.2.9,51847-2,ASSESSMENT AND PLAN
2.16.840.1.113883.10.20.22.2.8,51848-0,Assessments
2.16.840.1.113883.10.20.22.2.13,46239-0,Chief Complaint and Reason for Visit
1.3.6.1.4.1.19376.1.5.3.1.1.13.2.1,10154-3,CHIEF COMPLAINT,admit diagnosis,principal discharge diagnosis,principal diagnosis,principal diagnoses,secondary diagnosis,other medical issues considered at this time
2.16.840.1.113883.10.20.22.2.37,55109-3,Complications
1.3.6.1.4.1.19376.1.5.3.1.3.33,42344-2,Discharge Diet
2.16.840.1.113883.10.20.22.2.22.1,46240-8,Encounters,History of encounters,Surgeries,ED visits
2.16.840.1.113883.10.20.22.2.15,10157-6,Family History
2.16.840.1.113883.10.20.22.2.14,47420-5,FUNCTIONAL STATUS,Functional and Cognitive Status,impairments
2.16.840.1.113883.10.20.2.5,10210-3,GENERAL STATUS,CURRENT HEALTH STATUS
2.16.840.1.113883.10.20.22.2.20,11348-0,HISTORY OF PAST ILLNESS,PAST MEDICAL HISTORY
1.3.6.1.4.1.19376.1.5.3.1.3.4,10164-2,HISTORY OF PRESENT ILLNESS,brief history of physical illness,history of present illness,history of the present illness
2.16.840.1.113883.10.20.22.2.2.1,11369-6,History of immunizations,Immunizations,Immunizations and vaccines
2.16.840.1.113883.10.20.22.2.1.1,10160-0,HISTORY OF MEDICATION USE,Medications,current medications
2.16.840.1.113883.10.20.22.2.43,46241-6,HOSPITAL ADMISSION DX,rx on admit
2.16.840.1.113883.10.20.22.2.41,8653-8,HOSPITAL DISCHARGE INSTRUCTIONS,Discharge Instructions,	Written discharge instructions
2.16.840.1.113883.10.20.22.2.24,11535-2,Hospital Discharge Diagnosis,discharge diagnosis,FINAL DIAGNOSIS
2.16.840.1.113883.10.20.22.2.16,11493-4,Hospital Discharge Studies Summary
2.16.840.1.113883.10.20.22.2.45,69730-0,Instructions
2.16.840.1.113883.10.20.22.2.10,18776-5,Treatment plan,Care Plan
2.16.840.1.113883.10.20.22.2.11.1,10183-2,HOSPITAL DISCHARGE MEDICATIONS,Discharge Medications
1.3.6.1.4.1.19376.1.5.3.1.3.1,42349-1,Reason for Referral
2.16.840.1.113883.10.20.7.12,10216-0,Operative Note Fluids
2.16.840.1.113883.10.20.7.14,10223-6,Operative Note Surgical
2.16.840.1.113883.10.20.2.10,29545-1,PHYSICAL EXAMINATION,physical exam
2.16.840.1.113883.10.20.22.2.18,48768-6,Payers
2.16.840.1.113883.10.20.22.2.5.1,11450-4,PROBLEMS,Problem List,Concerns,complaints,observations
2.16.840.1.113883.10.20.22.2.7.1,47519-4,Procedures,	History of procedures
2.16.840.1.113883.10.20.22.2.3.1,30954-2,Results,laboratory tests,LABORATORY INFORMATION,laboratory data,laboratories
2.16.840.1.113883.10.20.22.2.17,29762-2,Social History,Observations like smoking,drinking
2.16.840.1.113883.10.20.22.2.4.1,8716-3,Vital Signs
"""

__ctakes_documents__ = """
2.16.840.1.113883.10.20.22.1.1,34133-9,Header,Patient information and demographics,IDENTIFYING DATA,identification,record
"""
