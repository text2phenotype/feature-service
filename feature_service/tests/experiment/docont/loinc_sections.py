from feature_service.tests.experiment.docont import test_biomed_1431_sections_rwd

from .grammar import Who, When, Where, Why
from .grammar import Visit, Measure, Exam, Impress, Instruct
from .grammar import Problem, Drug, Procedure
from .grammar import Match, Style, Rank, Flag
from .grammar import suggest

################################################################
#
# shorthand
strict = Match.strict
relax = Match.relax
abbr  = Match.abbr
pref = Match.pref
multi = Flag.multi
common = Flag.common

################################################################
#
# make merged


def make():
    merged = dict()
    merged.update(make_encounter())
    merged.update(make_demographics())
    merged.update(make_social())
    merged.update(make_medication())
    merged.update(make_allergy())
    merged.update(make_immunization())
    merged.update(make_vital())
    merged.update(make_lab())
    merged.update(make_imaging())
    merged.update(make_finding())
    merged.update(make_physical())
    merged.update(make_symptom())
    merged.update(make_problem())
    merged.update(make_diagnosis())
    merged.update(make_procedure())
    merged.update(make_pathology())
    merged.update(make_surgery())
    merged.update(make_device())
    merged.update(make_instructions())
    merged.update(make_coversheet())
    return merged


################################################################
#
# Visit.encounter

def make_encounter():
    """
    :return:
    """
    return suggest(
        Visit.encounter(
            Who.patient(
                Style.choice(
                    dict_encounter()))))


def dict_encounter():
    """
    :return:
    """
    return {
        '67162-8': Rank.first(Who.patient(When.transfer(Impress.interpret(strict([
            pref('Patient Disposition'),
            'DISPOSITION', 'Patient Disposition', 'DISPOSITION ON DISCHARGE', 'DISCHARGE DISPOSITION',
            'POSTPARTUM DISPOSITION', 'PROCEDURE DISPOSITION']))))),

        '78033-8': Rank.first(Who.patient(Where.hosp(Style.calendar([
            pref('Hospital stay duration'), multi(abbr('LOS')),
            'Length of stay', 'HOSPITALIZATION STAY'])))),

        '46240-8': Rank.first(Where.hosp(When.history(Who.patient(strict([
            pref('History of Hospitalization'),
            'HISTORY OF HOSPITALIZATIONS', 'Hx of Hospitalization',
            'HOSPITALIZATION/MAJOR', relax('HOSPITALIZATIONS'), multi(common('HOSPITALIZATION')),
            'HISTORY OF ENCOUNTERS', multi(common('EPISODES'))]))))),

        '11347-2': Where.outpatient(strict([
            pref('History of outpatient visits'),
            'Outpatient Visits', 'Outpatient Visit', multi('Outpatient')])),

        '52536-0': [
            pref('Admission Information')],

        '34111-5': Rank.high(Where.emergency(Who.patient([
            pref('Emergency department'),
            'EMERGENCY VISITS', 'EMERGENCY VISIT', 'ED VISITS', 'ED VISIT', 'ER VISIT']))),

        '75504-1': Rank.high(Where.outpatient(Who.patient([
            pref('Urgent care center'),
            'Urgent care visit', 'Urgent care encounter']))),

        '85208-7': [pref('Telehealth Consult'), 'Telemedecine', 'Virtual'],

        '76427-4': Rank.high(Who.patient(Style.calendar(relax([
            pref('Visit date'), 'date of visit',
            'ENCOUNTER DATE', 'Enc Date', 'REGISTRATION DATE', 'SERVICE DATE', 'DATE ISSUED',
            'Report Date', 'RECORD DATE',
            'Study Date', 'Episode Date',
            relax('TODAY IS'), relax('DATE TIME'), common('DATE')])))),

        '91582-7': [pref('Report Status'), 'Report Stage', 'Document Status'],

        '52455-3': Rank.high(Who.patient(Style.calendar([
            pref('Admission date'), 'ADMISSION DATA']))),

        '52525-3': Rank.high(Who.patient(Style.calendar(strict([
            pref('Discharge date'),
            'Discharge Date/Time', 'DISCHARGE TIME', 'DISCHARGE DATE TIME', 'DISCHARGE DATETIME', 'DATE OF DISCHARGE'])))),

        '92707-9': Who.provider(common([
            pref('Care team'), 'Treatment Team',
            'CARE PROVIDER', multi('PROVIDER'), 'Physician', 'DOCTOR', 'NURSE',
            'ORDERING PHYSICIAN', 'Testing Performed By',
            strict('PCP'), strict('OBSTETRICIAN'), strict('PATHOLOGIST'), strict('RADIOLOGIST'), strict('SURGEON'),
            multi('ATTENDING'), multi('ADMITTING'), multi('RESIDENT'), multi('SUPERVISING')])),

        '44951-2': Who.provider(Style.unique(strict([
            pref('Physician NPI'), abbr('NPI'), 'PHYSICIAN DETAILS',
            'National Provider Identifier', 'PROVIDER INFORMATION', 'PROVIDER ID', 'PROVIDER NUMBER']))),

        '46209-3': Who.provider(multi(relax([
            pref('Provider orders'),
            strict('ORDERING PROVIDER'),
            abbr('CPOE'), strict('COMPUTERIZED PHYSICIAN ORDER ENTRY'),
            'ORDERS', 'ORDER', 'ORDER DATE', 'ORDERED', 'ORDER DETAILS', 'ORDER STATUS']))),

        '18770-8': Who.provider(Style.printer(relax([
            pref('Dictation'),
            'DICTATED BY',
            Style.calendar('DICTATED ON'),
            Style.calendar('Dictated Date'),
            'DICTATED',
            'Transcribed Document Print', 'Transcribed By',
            Style.calendar('Transcribed Date'),
            'Transcribed Document',
            'Printed from', 'PRINTED BY', 'PRINTED',
            Style.calendar('PRINTED ON'), Style.calendar('Date Printed'),
            'AUTHOR', 'AUTHORED BY',
            multi('Requested by'),
            Style.calendar('Generated on'), 'Generated By',
            Style.calendar('Last Updated'), 'Last Updated By', 'MODIFIED REPORT',
            'COMPLETED BY', 'ENTERED BY', 'SEEN BY',
            multi('FINAL REPORT'), 'END OF REPORT']))),

        '76696-4': Where.department(Style.unique(common(multi([
            pref('Facility Name'),
            'Facility', 'SERVICE', 'BUILDING', 'CAMPUS', 'DEPARTMENT', 'LabCorp'])))),

        '80412-0': Where.department(relax(
            [pref('Encounter location'),
             'Visit location', 'LOCATION OF VISIT',
             multi('LOCATION'), multi('ROOM')])),

        '18841-7': Who.provider(Where.consult(Style.narrative(multi([
            pref('Hospital consultations'),
            'CONSULT', 'CONSULTATION'])))),

        '48768-6': Rank.low(Who.payer(Style.unique([
            pref('Payment sources'),
            'BILLING INFORMATION', 'INSURANCE GROUP NUMBER', 'INSURANCE NUMBER',
            relax('MEDICARE'), strict('MEDICARE PPO'), relax('MEDICAID'),
            relax('GROUP #'), multi(abbr('INS'))]))),

        '76428-2': Rank.ignore(strict([
            pref('Visit charge'),
            'Encounter charge', relax('CHARGES'), relax('CHARGE FOR')])),

        '75519-9': Style.unique(relax([
            pref('Encounter identifier'),
            'ENCOUNTER ID', 'ENCOUNTER NUM', 'ENCOUNTER #',
            'ACCESSION', 'VISIT ID', 'CASE NUM', 'CASE #', 'CASE#',
            'REQUISITION'])),

        '57122-4': relax([pref('Type of encounter'),
                          'ENCOUNTER INFORMATION', 'ENCOUNTER INFO', 'ENCOUNTER',
                          'APPOINTMENT', 'APPOINTMENTS', 'APPOINTMENT INFORMATION']),

        '11293-8': Who.provider(Where.consult([
            pref('Referral source'),
            'REFERRED BY', relax('Referral'), 'Referring provider', 'ADMIT PROVIDER'])),

        '39289-4': When.plan([
            pref('Follow-up'),
            relax('Follow up'), 'FOLLOW UP APPOINTMENT', 'FOLLOW UP APPOINTMENTS']),

        '85647-6': Rank.ignore(Style.legal(relax([
            pref('Signature'),
            'SIGNATURE LINE',
            'ELECTRONICALLY SIGNED', 'SIGNED', 'SIGNED by', 'Signed Off By',
            'SIGNED ELECTRONICALLY BY', 'SIGNATURE ON FILE']))),

        '80567-1': Style.subhead([
            pref('Flowsheet'), strict('FLOW SHEET'), relax(common(multi('FLOW')))]),

        '89442-8': Who.family(relax(multi([ # use FHX context above, then Rank higher OB/GYN
            pref('Obstetrics Administrative'),
            Who.patient('PAST GYNECOLOGICAL HISTORY'),
            abbr('NSVD'),
            'CESAREAN STATUS',
            'DELIVERY DATE',
            'MATERNAL TRANSFER',
            'POSTPARTUM MEASLES MUMPS RUBELLA VACCINE',
            'POSTPARTUM CARE SITE',
            'PRIMARY PEDIATRIC CARE',
            'PRIMARY PEDIATRICIAN',
            'CESAREAN STATUS',
            'BREAST FEEDING AT DISCHARGE',
            'DELIVERY', 'PRENATAL SCREENS',
            'EPIDURAL VAGINAL DELIVERY',
            'UTERINE INCISION TYPE',
            'Nursery records',
            'VAGINAL DELIVERY'])))
}

################################################################
# Visit.demographics


def make_demographics():
    """
    :return:
    """
    return suggest(
        Visit.demographics(
            Who.patient(
                When.present(
                    Style.lists( dict_demographics())))))


def dict_demographics():
    """
    :return:
    """
    return {
        '79191-3': [
            Rank.high(pref('Patient demographics')), Rank.high('DEMOGRAPHICS'),
            common(multi('PATIENT')), multi(common('SUBJECT')),
            multi('PATIENT INFORMATION'), multi(relax('PATIENT INFO'))],

        '45392-8': Style.unique([pref('FIRST NAME'), 'GIVEN NAME']),

        '45394-4': Style.unique([pref('LAST NAME'), 'FAMILY NAME']),

        '87226-7': Style.unique(Rank.high(strict([pref('PATIENT NAME'), 'LEGAL NAME', 'FULL NAME', 'NICK NAME',
                                 'SUBSCRIBER', 'SUBSCRIBER NAME', 'INSURANCE SUBSCRIBER NAME']))),

        '72143-1': Style.choice(strict([pref('ADMINISTRATIVE GENDER'), 'PATIENT GENDER',
                                 relax('GENDER'), strict('PATIENT SEX'), relax(multi('SEX'))])),

        '21112-8': Rank.first(Style.calendar(Rank.high([pref('BIRTH DATE'), 'DATE OF BIRTH', abbr('DOB'),
                                              'PATIENT DATE OF BIRTH', 'SUBSCRIBER DATE OF BIRTH']))),

        '81954-0': Rank.first(Style.calendar([pref('DATE OF DEATH'), multi('DEATH')])),

        '21612-7': Rank.high([relax(pref('PATIENT AGE')), common('AGE')]),

        '80977-2': Style.choice([pref('PATIENT RACE'), multi(relax('RACE')), 'TABULATED RACE', strict('CDC RACE')]),

        '80978-0': Style.choice([pref('PATIENT ETHNICITY'), relax('ETHNICITY'), strict('CDC ETHNICITY'),
                                 Style.lists('TABULATED ETHNICITY')]),

        '54899-0': Style.choice([pref('PREFERRED LANGUAGE'), 'PREF LANGUAGE', strict('PATIENT LANGUAGE'), 'LANGUAGE']),

        '42078-6': Rank.ignore(Style.unique([Who.family(pref('FOLLOW-UP CONTACT')), Who.family('EMERGENCY CONTACT'),
                                             multi(common('CONTACT')), Style.choice(common('CONTACT BY'))])),

        '76458-9': Style.unique([strict('PATIENT EMAIL ADDRESS'), 'EMAIL ADDRESS', strict('TRUSTED EMAIL'),
                                 multi('EMAIL'), multi('E-MAIL')]),

        '92634-5': Style.choice(multi(['ADDRESS TYPE', 'CITY/ST', 'CITY,ST', 'CITY', common('STATE')])),

        '56799-0': Rank.high(Where.home(['PATIENT ADDRESS', 'HOME ADDRESS', multi('ADDRESS'),
                                         'WORK ADDRESS', 'ADDRESS LINE 1', 'ADDRESS LINE 2', 'STREET ADDRESS',
                                         multi('STREET')])),

        '42077-8': Rank.high(Where.home(Style.unique( [pref('Patient phone number'), 'CELL PHONE', 'HOME PHONE',
                                                       multi('PHONE NUMBER'), common('PHONE'),
                                                       'WORK PHONE', 'PHONE EXTENSION',
                                                       'WORK PHONE EXTENSION',
                                                       multi(common('EXTENSION')),
                                                       'MOBILE PHONE', common('MOBILE')]))),

        '68997-6': [Where.home('PATIENT CITY'), multi(common('CITY'))],
        '46499-0': Where.home(['PATIENT STATE', 'PATIENT HOME STATE', 'STATE OF RESIDENCE', multi(common('STATE'))]),
        '45401-7': ['POSTAL CODE', 'PATIENT ZIP', 'ZIP CODE', multi(relax('ZIP')), relax('POSTAL')],
        '87721-7': [Where.home('COUNTY OF RESIDENCE'), multi('COUNTY')],
        '66477-1': Where.home(['COUNTRY OF CURRENT RESIDENCE', multi('COUNTRY')]),

        '81365-9': Rank.low(Style.choice(['RELIGIOUS AFFILIATION', 'PATIENT RELIGION', relax('RELIGION')])),

        '85658-3': Style.choice(['PROFESSION', 'OCCUPATION', 'OCCUPATION TYPE', 'EMPLOYER NAME', 'EMPLOYER ADDRESS', common('JOB')]),

        '46106-1': Rank.high(Style.unique( [strict('MEDICAL RECORD NUMBER'), strict('MEDICAL RECORD #'), relax('CHART NUMBER'), abbr('MRN')])),

        '45396-9': Rank.first( Style.unique( [abbr('SSN'), strict('SOCIAL SECURITY NUMBER'),
                                              'INSURANCE SUBSCRIBER SSN',
                                              'SOCIAL SECURITY NO', 'SOCIAL SECURITY NUM', 'SOCIAL SEC NO',
                                              'SOC SEC NO', 'SOC. SEC. NO', 'SOCIAL SECURITY #'])),

        '76435-7': Rank.high(Style.unique([strict('PATIENT ID'), strict('PATIENT IDENTIFIER'),
                                           multi(abbr('ACC')), relax('ACCOUNT'), strict('PATIENT NUMBER'),
                                           'IDENTIFICATION DATA', 'IDENTIFYING DATA', multi('IDENTIFICATION'),
                                           'INSURANCE ID NUMBER', 'EXTERNAL ID'])),

        '76437-3': Who.payer(Style.choice(['PRIMARY INSURANCE DATA', 'PRIMARY INSURANCE', 'ACTIVE PRIMARY INSURANCE',
                                             'PAYOR SOURCE', relax('PAYERS'), relax('PAYORS'), relax('INSURANCE'),
                                             'SECONDARY INSURANCE','INSURANCE COMPANY', 'INSURANCE DATA', 'INSURANCE PROVIDERS',
                                             'HEALTH INSURANCE', 'BENEFITS ASSIGNED', relax('INSURANCE')]))
}

# suggest

################################################################
# Visit.social ( Aspect SOCIAL )


def make_social():
    return suggest(
        Visit.social(
            Who.patient(
                Style.narrative(
                    dict_social()))))


def dict_social():
    return {
        '11366-2': Rank.first(When.history([
            pref('SMOKING STATUS'),
            strict('HISTORY OF TOBACCO USE'),
            strict('TOBACCO USE STATUS'),
            relax('SMOKING HISTORY'),
            relax('SMOKING EXPOSURE'),
            relax('SMOKING EXPOSURE'),
            relax('TOBACCO USE'),
            relax('SMOKING'),
            relax('TOBACCO'),
            multi('DATE QUIT'),
            multi('QUIT DATE')])),

        '29762-2': When.history([
            pref('SOCIAL HISTORY'),
            strict('SOCIAL HX'),
            strict('POVERTY STATUS'),
            common(multi('DRINKING')),
            relax('PHYSICAL EXERCISE'),
            common(multi('EXERCISE')),
            common(multi('SOCIAL')),
            relax('HABITS'),
            relax('POVERTY'), relax('HOMELESS'),
            abbr('SHX'),
            abbr('PSH')]),

        '47420-5': Instruct.care([
            pref('Functional status assessment note'),
            'FUNCTIONAL STATUS ASSESSMENT',
            'FUNCTIONAL STATUS', 'FUNCTIONAL ABILITIES',
            'CURRENT HEALTH STATUS', 'Preventive',
            multi('IMPAIRMENTS'),
            When.discharge('DISCHARGE CONDITION'),
            When.discharge('DISCHARGED CONDITION ON DISCHARGE'),
            When.discharge('DISCHARGE STATUS'),
            When.discharge('CONDITION ON DISCHARGE'),
            When.transfer('CONDITION ON TRANSFER')])
    }


################################################################
# Drug.med


def make_medication():
    return suggest(
        Drug.med(
            Who.patient(
                When.present(
                    dict_medication()))))


def dict_medication():
    return {
        '10160-0': relax([
            Rank.first(pref('MEDICATION LIST')),
            Rank.first('FINAL MEDICATIONS'),
            Rank.high(strict('HISTORY OF MEDICATION USE')),
            Rank.high(strict('LIST MEDICATIONS')),
            Rank.high('CONDITION MEDICATIONS'),
            Rank.high(When.present('CURRENT MEDICATIONS')),
            When.plan('AS NEEDED MEDICATIONS'),
            relax('THE FOLLOWING MEDICATIONS'),
            'FOLLOWING MEDICATIONS',
            'FOLLOWING MEDICATIONS',
            'DRUG HISTORY',
            Where.home('HOME MEDICATIONS'),
            Where.home('MEDICATIONS AT HOME'),
            When.admit(Where.hosp('INHOSPITAL MEDICATIONS')),
            When.present('MOST RECENT MEDICATIONS'),
            When.present('NEW MEDICATIONS'),
            Rank.high('MEDICATION CHANGES'),
            Where.outpatient('MEDICATIONS AT REHAB'),
            Where.outpatient('MEDICATIONS AT REHABILITATION'),
            When.admit('MEDICATIONS ON PRESENTATION'),
            Where.outpatient('OUTPATIENT MEDICATIONS'),
            'NUMBER OF DOSES REQUIRED APPROXIMATE',
            Where.home(relax('MEDS AT HOME')),
            common('MEDS'),
            common('PRESCRIPTIONS'),
            common('PRN MEDICATIONS'),
            common('MEDICATIONS'),
            common('MEDICATION')]),

        '42346-7': Rank.second( When.admit( Where.hosp( strict(
            [pref('Medications on admission'),
             'ADMISSION MEDICATIONS',  'MEDICATIONS AT ADMISSION', 'MEDICATIONS UPON ADMISSION',
             'MEDICATIONS AT THE TIME OF ADMISSION', 'MEDICATIONS AT TIME OF ADMISSION',
             'MEDICATION CHANGES MADE DURING THIS ADMISSION',
             relax('RX ON ADMIT'),
             When.history('MEDICATIONS PRIOR TO ADMISSION'),
             Rank.low(Where.surgery(When.history('PREADMISSION MEDICATIONS'))),
             Rank.low(Where.surgery(When.history('PREOP MEDICATIONS'))),
             Rank.low(Where.surgery('PREOPERATIVE MEDICATIONS')),
             Where.home('HOME MEDICATIONS ON ADMISSION'),
             'BLOCK MEDICATIONS ON ADMISSION'])))),

        '29549-3': Where.hosp([multi(pref('Medication administered')), 'MEDICATION ADMINISTERED',
                               relax('FLUIDS RECEIVED'), common('IV FLUIDS'), common('FLUIDS')]),

        '10183-2': Rank.first( When.discharge( Where.hosp(strict(
            ['HOSPITAL DISCHARGE MEDICATIONS',
                'DISCHARGE MEDICATIONS',
                'DISCHARGE MEDICATIONS INCLUDE',
                'DISCHARGE MEDICATION',
                'DISCHARGED TO HOME ON THE FOLLOWING MEDICATIONS',
                'ADDENDUM TO MEDICATIONS ON DISCHARGE',
                'REHABILITATION HOSPITAL DISCHARGE MEDICATIONS',
                'MEDICATIONS UPON DISCHARGE',
                'MEDICATION AT THE TIME OF DISCHARGE',
                'MEDICATION AT TIME OF DISCHARGE',
                'MEDICATIONS AT THAT TIME OF DISCHARGE',
                'MEDICATIONS AT THE TIME OF DISCHARGE',
                'MEDICATIONS AT TIME OF DISCHARGE',
                'MEDICATIONS ON DISCHARGE',
                'MEDICATION ON DISCHARGE',
                'MEDICATIONS AT DISCHARGE',
                When.transfer('MEDICATIONS UPON TRANSFER'),
                When.transfer('MEDICATIONS ON TRANSFER'),
                When.transfer('TRANSFER MEDICATIONS'),
                When.transfer('MEDICATIONS AT THE TIME OF TRANSFER'),
                When.transfer('MEDICATIONS AT THE TIME OF TRANSFER TO THE CCU'),
                When.transfer('MEDICATIONS AT THE TIME OF TRANSFER TO THE ICU'),
                When.transfer('MEDS ON TRANSFER')])))),

        '45841-4': Where.hosp([pref('Chemotherapy'), relax('CHEMO')]),

        '45851-3': Where.hosp([pref('Transfusions')]),

        '45843-0': Where.hosp([pref('IV medication'), strict('IV medications'), common('IV')]),
}


################################################################
# Drug.allergy

def make_allergy():
    return suggest(
        Rank.high(
            Drug.allergy(
                Who.patient(
                    When.present(
                        dict_allergy() )))))


def dict_allergy():
    """
    :return:
    """
    return {
        '48765-2': [
            pref('ALLERGY LIST'),
            'ALLERGIES, ADVERSE REACTIONS, ALERTS', 'ALLERGIES & ADVERSE REACTIONS',
            'ALLERGIES AND ADVERSE REACTIONS', 'ADVERSE DRUG REACTIONS', 'ADVERSE REACTIONS',
            'DRUG ALLERGIES','POTENTIALLY SERIOUS INTERACTION','SERIOUS INTERACTION',
            strict('ALLERGIES LIST'),
            multi('ALERTS'),
            'MEDICATION ALLERGIES',
            'MEDICATION ALLERGY',
            strict('ALLERGIES'), 'ALLERGY',
            multi('REACTIONS'), multi('REACTION'),
            Rank.ignore('ENVIRONMENTAL ALLERGIES'),
            Rank.ignore('FOOD ALLERGIES'),
            Rank.ignore('NO KNOWN ALLERGIES'),
            Rank.ignore('NO KNOWN DRUG ALLERGIES'),
            Rank.ignore(abbr('NKA')),
            Rank.ignore(abbr('N.K.A.')),
            Rank.ignore(abbr('NKDA')),
            Rank.ignore(abbr('N.K.D.A.'))]
    }

################################################################
# Drug.immunization


def make_immunization():
    return suggest(
        Drug.immunization(
            Who.patient(
                When.history(
                    Style.lists( dict_immunization() )))))


def dict_immunization():
    return {
        '11369-6': [
            pref(multi('HISTORY OF IMMUNIZATION')),
            strict('HISTORY OF IMMUNIZATIONS'), strict('IMMUNIZATION HISTORY'), strict('IMMUNIZATIONS AND VACCINES'),
            strict('LIST OF VACCINES'), strict('VACCINES LIST'),
            strict('IMMUNIZATIONS LIST'), strict('IMMUNIZATIONS PROVIDED'),
            relax('IMMUNIZATION'), relax('IMMUNIZATIONS'),
            relax('VACCINE'), relax('VACCINES'),
            Rank.low(When.plan('IMMUNIZATIONS RECOMMENDED'))]}


################################################################
# Measure.vitals

def make_vital():
    return suggest(
        Measure.vital(
            Who.patient(
                When.present(
                    dict_vital()))))


def dict_vital():
    return {
        '8716-3': [
            pref('VITAL SIGNS'),  strict('VITAL SIGNS PANEL'),
            When.admit('VITALS ON ADMISSION'),
            'VS/MEASUREMENTS',
            relax('Filed Vitals'),
            common('VS'),
            multi(relax('VITALS')),
            multi(relax('Pulse')),
            relax('Body temperature'),
            strict('Temperature chart'), relax('Temperature charts'),
            multi(relax('Temperature')), multi(relax('Temp')),
            multi(relax('Heart Rate')),
            multi(relax('Respiratory Rate')),
            multi(relax('Blood Pressure')),
            common(multi('RATE'))],
    }

################################################################
# Measure.lab

def make_lab():
    return suggest(
        Measure.lab(
            Who.patient(
                Style.lists (
                    dict_lab()))))

def dict_lab():
    return {
        '30954-2': [
            pref('Relevant diagnostic tests/laboratory data'),
            Rank.high(strict('RELEVANT DIAGNOSTIC TESTS LABORATORY DATA')),
            Rank.high(strict('RELEVANT DIAGNOSTIC TESTS OR LABORATORY DATA')),
            Rank.first(strict('NOTABLE LABS')),
            Rank.high('PERTINENT LAB VALUES'),
            Rank.high('PERTINENT LABORATORY RESULTS'),
            Rank.high('PERTINENT LABORATORY TESTS AND RESULTS'),
            Rank.high('PERTINENT LABORATORY TESTS AND STUDIES'),
            Rank.high('PERTINENT LABS UPON PRESENTATION'),
            Rank.high('PERTINENT LABS'),
            Rank.high('RELEVANT LABS'),
            Rank.first('NOTABLE LABORATORY VALUES ON ADMISSION'),
            Rank.high('PERTINENT LABORATORY DATA ON ADMISSION'),
            Rank.high('PERTINENT LABS ON ADMISSION'),
            Rank.first('RELEVANT ADMISSION LABS'),
            Rank.first(relax('SIGNIFICANT LABS ON ADMISSION')),
            Rank.first(relax('LABORATORIES OF NOTE')),
            'ADMISSION LAB', 'ADMISSION LABS', 'ADMISSION LABS AND STUDIES',
            'ADMISSION LABORATORY', 'ADMISSION LABORATORIES',
            'ADMISSION LABORATORY DATA', 'ADMISSION LABORATORY STUDIES',
            'ADMISSION LABORATORY RESULTS', 'ADMISSION LABORATORY VALUES',
            'ADMISSIONS LABORATORIES', 'ADMITTING LABORATORY',
            multi('LABORATORY FINDINGS ON ADMISSION'),
            Why.reason('PREOPERATIVE LAB'),
            Why.reason('PREOPERATIVE LABS'),
            Why.reason('PREOPERATIVE LABORATORY DATA'),
            Why.reason('PREOPERATIVE LABORATORY RESULTS'),
            Why.reason('PREOPERATIVE LABORATORY VALUES'),
            Why.reason(common('PREOP LABS')),
            relax('ADMIT LABS'),
            'LAB STUDIES ON ADMISSION',
            'LABORATORIES ON ADMISSION',
            'LABORATORY DATA AT ADMISSION', 'LABORATORY DATA ON ADMISSION', 'LABORATORY DATA UPON ADMISSION',
            'LABORATORY EXAM ON ADMISSION', 'LABORATORY EXAMS UPON ADMISSION', 'LABORATORY ON ADMISSION',
            'LABORATORY STUDIES ON ADMISSION', 'LABORATORY STUDIES UPON ADMISSION', 'LABORATORY VALUES ON ADMISSION',
            'LABS AND STUDIES ON ADMISSION',
            'LABS AT ADMISSION', 'LABS ON ADMISSION', 'LABS ON ADMIT', 'LABS UPON ADMISSION',
            Measure.finding(multi('RESULTS DIAGNOSTIC FINDINGS')),
            'INITIAL LABORATORY DATA', 'INITIAL LABORATORY STUDIES',
            'LABORATORY DATA', 'LAB RESULTS',
            'LABORATORY EXAM', 'LABORATORY EXAMS',
            'LABORATORY EVALUATION', 'LABORATORY EXAMINATION',
            'LABORATORY TESTS', 'LAB VALUES',
            'CHEMISTRY STUDIES',
            Measure.objective(multi(common('STUDIES'))),
            multi('LABORATORY INFORMATION'), strict('LABORATORY RESULTS'),
            strict('LABORATORY STUDIES'), strict('LABORATORY VALUES'),
            Rank.low(relax('BENIGN LABS')),
            Rank.low(relax('NORMAL LABS')),
            Measure.finding(multi('RESULTS DIAGNOSTIC FINDINGS')),
            Measure.objective(multi('LABS AND DIAGNOSTIC STUDIES')),
            Measure.objective(multi('DIAGNOSTIC STUDIES')),
            Measure.objective(multi('DIAGNOSTIC DATA')),
            Measure.finding(multi('DIAGNOSTIC TESTS')),
            Impress.interpret(multi(relax('SHOWED THE FOLLOWING RESULTS'))),
            Impress.interpret(multi(relax('RESULTS SUMMARY'))),
            Measure.objective(common(multi('TESTS'))),
            Measure.objective(common(multi('RESULTS'))),
            Measure.objective(common(multi('OBSERVATIONS'))),
            Measure.objective(multi('PERTINENT RESULTS')),
            Measure.objective(multi('TEST NAME')),
            Impress.interpret(Measure.objective(multi('RESULTS/INTERPRETATION'))),
            Measure.objective(relax('LAB DATA')),
            relax('LABORATORIES'),
            relax('LABORATORY'),
            relax('CHEMISTRIES'),
            relax('LABORATORY STUDIES WERE SENT OFF INCLUDING'),
            When.plan('Follow-up Laboratory Testing'),
            When.plan('Follow up Laboratory Testing'),
            When.plan('Follow up Labs'),
            When.plan(relax('LABS TO FU')),
            Style.narrative(multi(common('LABS'))),
            Style.narrative(multi(common('LAB'))),
            Style.choice(relax('LAB NO')),
            Style.choice(relax('LAB NO.'))],

        # https://www.labcorp.com/tests/139650/respiratory-pathogen-profile-pcr
        '82159-5': Style.subhead([
            pref('Respiratory Pathogen Profile, PCR'),
            'Adenovirus',
            'Coronavirus HKU1', abbr('HKU1'),
            'Coronavirus NL63', abbr('NL63'),
            'Coronavirus 229E', abbr('229E'),
            'Coronavirus OC43', abbr('OC43'),
            'Human Metapneumovirus',
            'Human Rhinovirus/Enterovirus', 'Rhinovirus', 'Enterovirus',
            'Influenza A',
            'Influenza A/H1',
            'Influenza A/H1-2009',
            'Influenza A/H3',
            'Influenza B',
            'Parainfluenza 1', abbr('PIVI'),
            'Parainfluenza 2', abbr('PIV2'),
            'Parainfluenza 3', abbr('PIV3'),
            'Parainfluenza 4', abbr('PIV4'),
            'Respiratory Syncytial Virus', 'RESP SYNCYTIAL VIRUS',
            'Bordetella pertussis', 'Bordetella PARAPERTUSSIS',
            'Chlamydophila pneumoniae',
            'Mycoplasma pneumoniae']),

        # @@@ Viral screening and immunizations
        # RESPIRATORY PATHOGEN PCR PANEL
        # https://loinc.org/78922-2/
        # nasopharyngeal swab.
        # serum antibody testing
        # HLA-B27 ( ankylosing spondylitis )
        '77029-7': ['Respiratory pathogens DNA and RNA 14 panel'],

        '50023-1': [pref('Hepatitis C virus RNA panel'), 'Viral screens and immunizations'],

        '664-3': [strict('GRAM STAIN FINAL'), relax('GRAM STAIN')],

        # Aspect.lab RelTime.discharge
        '11493-4': Rank.high( When.discharge( Where.hosp([
            Impress.interpret('HOSPITAL DISCHARGE STUDIES SUMMARY'),
            'DISCHARGE LAB DATA',
            'DISCHARGE LABORATORIES',
            'DISCHARGE LABORATORY DATA',
            'DISCHARGE LABORATORY VALUES',
            'DISCHARGE LABS',
            'LAB VALUES ON DAY OF DISCHARGE',
            'LABORATORY DATA AT DISCHARGE',
            'LABORATORY DATA ON DISCHARGE',
            'LABORATORY VALUES ON DISCHARGE',
            'LABORATORY STUDIES ON DISCHARGE',
            'LABORATORY STUDIES UPON DISCHARGE',
            'LABS AT DISCHARGE',
            'LABS AT TIME OF DISCHARGE',
            'LABS ON DAY OF DISCHARGE',
            'LABS ON TRANSFER',
            When.plan(Rank.ignore('LABORATORY PENDING ON DISCHARGE'))]))),

        '61149-1': Style.narrative(Measure.objective(
                                   [multi(common('OBJECTIVE')),
                                    multi(relax('OBJECTIVE DATA'))])),

        '18723-7': Style.narrative([Where.department(
            pref('HEMATOLOGY STUDIES')),
            Where.department(relax('HEMATOLOGY')),
            Where.department(relax('HEMATOLOGIC')),
            'COAGULATION STUDIES',
            multi(abbr('HEME'))]),

        '56846-9': multi(relax([
            pref('CARDIAC BIOMARKERS'), 'LIPID PANEL', 'METABOLIC PANEL', common('CHOLESTEROL')])),

        '18729-4': Style.subhead([
            pref('Urinalysis studies'),
            relax('URINALYSIS'), relax('UA ANALYSIS'), relax('URINE OUTPUT')]),

        '18728-6': ['Toxicology studies', relax('TOXICOLOGY')],

        '56874-1': multi(relax([
            pref('Serology and blood bank studies'),
            relax('SEROLOGY'),
            abbr('IGG'), abbr('IGM'), abbr('igg/igm'), abbr('igg+igm'), common('Antibodies')])),

        '18725-2': Where.department([pref('MICROBIOLOGY STUDIES'), relax(multi('MICROBIOLOGY'))]),

        '56847-7': [relax('CALCULATED AND DERIVED VALUES'), relax('DERIVED VALUES')],

        '19147-8': Style.subhead([
            pref('Reference lab test reference range'), 'Reference Range', common('REFERENCE'), common('RANGE')]),

        '94531-1': Rank.first([
            strict('SARS coronavirus 2 RNA panel'),'2019 Novel Coronavirus',
            strict('SARS-CoV-2 RNA'),
            multi(strict('rtPCR')), relax('PCR'), relax('NAA'),
            multi('COVID-19'), multi('COVID19'), relax('COVID19'),
            relax('COVID+'), relax('COVID'),
            multi('SARS-CoV'), multi('SARS-CoV-2'),
            'MERS-CoV', 'SARS-CoV',
            'coronavirus', abbr('HKU1'), abbr('NL63'), abbr('229E'), abbr('OC43')]),

        '11502-2': Style.subhead(multi(common([
            pref('Laboratory report (columns)'),
            strict('REFERENCE RANGE'),
            'COMPONENT', 'RANGE', 'FLAG']))),

        '92236-9': Measure.objective(Style.subhead(common(multi([
            pref('RESULT STATUS'),
            'RESULT TYPE', 'RESULT DATE', 'RESULT STATUS', 'RESULTED', 'RESULT TITLE'])))),
    }


################################################################
# Measure.imaging

def make_imaging():
    return suggest(
        Measure.imaging(
            Where.radiology(
                Who.patient(Impress.interpret(
                    dict_imaging())))))

def dict_imaging():
    return {
        '19005-8': [pref('RADIOLOGY IMAGING STUDY IMPRESSION')],

        '18783-1': [pref(When.plan('RADIOLOGY STUDY RECOMMENDATION'))],

        '18834-2': [pref('RADIOLOGY COMPARISON STUDY OBSERVATION'), common('Comparison')],

        '55111-9': Style.narrative([multi('CURRENT IMAGING PROCEDURE DESCRIPTIONS'), multi('CURRENT IMAGING PROCEDURE'),
                                    multi('Diagnostic Procedure')]),

        '55115-0': [pref('REQUESTED IMAGING STUDIES INFORMATION'),
                    strict('REQUESTED IMAGING STUDIES'),
                    strict('IMAGING STUDIES'),
                    strict('RADIOGRAPHIC STUDIES'),
                    strict('RADIOLOGIC STUDIES'),
                    strict('RADIOLOGY IMAGING'),
                    Rank.high(Measure.finding('IMAGING RESULTS')),
                    Rank.high('RELEVANT IMAGING'),
                    relax('RADIOGRAPHIC'),
                    multi(common('RADIOLOGY')),
                    multi(common('IMAGING')),
                    common(abbr('ECG')), common(abbr('EKG')),
                    common(abbr('ECHO')), common('ELECTROCARDIOGRAM'),
                    common(abbr('CXR')),  common('CHEST XRAY'),
                    common(relax('X-RAY')), common('XRAY'), common('XR'),
                    common(abbr('KUB')),  # kidney, ureter, and bladder
                    common(abbr('MRA KIDNEY')),
                    common(abbr('MRI')),
                    common(abbr('MRI HEAD'))],

        '55113-5': [Rank.first('KEY IMAGES')]
}


################################################################
# Measure.finding

def make_finding():
    return suggest(
        Measure.finding(
            Who.patient(
                Impress.interpret(
                    dict_finding()))))


def dict_finding():
    return {
        '75321-0': multi(relax([ pref('Clinical finding'), relax('FINDINGS')])),

        '59776-5': Where.surgery([multi(pref('PROCEDURE FINDINGS')), 'OPERATIVE FINDINGS']),

        '18782-3': [Where.radiology('RADIOLOGY STUDY OBSERVATION FINDINGS')],
}


################################################################
# Measure.physical

def make_physical():
    return suggest(
        Measure.finding(
            Exam.physical(
                Who.patient(
                    When.present(
                        Style.subhead(
                            dict_physical()))))))


def dict_physical():
    return  {
        '22029-3': strict([
            'PHYSICAL EXAM',
            'HEAD EYES EARS NOSE THROAT',
            'ADMISSION PHYSICAL EXAMINATION',
            'PHYSICAL EXAMINATION',
            When.admit('PHYSICAL EXAM ON ADMISSION'),
            When.admit('PHYSICAL EXAMINATION ON ADMISSION'),
            When.admit('PHYSICAL EXAMINATION UPON ADMISSION'),
            When.discharge('PHYSICAL EXAMINATION ON DISCHARGE'),
            When.discharge('HOSPITAL DISCHARGE PHYSICAL'),
            'PHYSICAL EXAMINATION ON PRESENTATION']),

        '10184-0': [Measure.finding(When.discharge('HOSPITAL DISCHARGE PHYSICAL FINDINGS'))],

        '10210-3': [Measure.finding('PHYSICAL FINDINGS OF GENERAL STATUS'),
                    Impress.interpret(multi('GENERAL STATUS'))],

        '10187-3': Exam.ros(['REVIEW OF SYSTEMS', 'GENERAL ROS', abbr('ROS')]),

        '10190-7': [Exam.ros('MENTAL STATUS')],

        '29545-1': Style.narrative( Measure.finding( ['PHYSICAL FINDINGS', 'Phys find'])),

        '11384-5': Style.subhead(multi(common( [
            'EXAM', 'EXAMINATION',
            abbr('ABD'), strict('ABDOMEN'),
            'ADNEXA',
            'APPEARANCE',
            'BACK',
            abbr('BMI'), strict('BODY MASS INDEX'),
            'BREASTS',
            'CHEST',
            'CARDIAC', 'CARDIAC EXAMINATION',
            abbr('CARDS'), abbr('CVS'),
            'CARDIOVASCULAR', 'CARDIOVASCULAR EXAM', 'CARDIOVASCULAR STATUS',
            'CAROTIDS',
            strict('CEREBELLAR EXAM'),
            'COORDINATION',
            'CRANIAL', 'CRANIAL NERVES',
            strict('EAR/NOSE/THROAT'),
            abbr('ENDO'), 'ENDOCRINE',
            'EXTREMITIES',
            strict('EXTREMITY EXAM'),
            strict('EYE EXAM'), 'EYES',
            strict('FOOT EXAM'),
            strict('FUNCTIONAL AND COGNITIVE STATUS'), relax('COGNITION'),
            'GAIT',
            abbr('GEN'), 'GENERAL',
            strict('GENITOURINARY'),
            abbr('GI'), strict('GASTROINTESTINAL'),
            abbr('GU'),
            Rank.high(strict('HEAD EYES EARS NOSE AND THROAT')),
            Rank.high(strict('HEAD EYES EARS NOSE AND THROAT EXAM')),
            Rank.high(strict('HEENT')), Rank.high(relax('HENT')),
            'EARS', 'left ear','right ear',
            'HEART',
            strict('HEMODYNAMICS'),
            strict('INITIAL NEWBORN EXAM'),
            'LUNGS',
            relax('LYMPH'), relax('LYMPH NODES'), relax('NODES'),
            strict('MENTAL STATUS EXAMINATION'),
            abbr('MSK'), relax('MUSCULOSKELETAL'),
            'NECK',
            strict('NEUROLOGICAL EXAMINATION'), abbr('NEURO'), 'NEUROLOGICAL', 'NEUROLOGIC', strict('NEUROLOGIC EXAM'),
            Where.department('NEUROLOGY'),
            Where.department('OPHTHALMOLOGY'),
            abbr('PE'),
            'PELVIC',
            'PSYCH', strict('PSYCHOSOCIAL'),
            abbr('PULM'),
            Where.department('PULMONARY'),
            'PULSE',
            'PUPILS',
            'RECTAL',
            strict('REFLEXES'),
            'RENAL',
            abbr('RESP'), 'RESPIRATORY',
            'SENSORY', strict('SENSORY EXAMINATION'),
            'SKIN',
            'SPINE'])))
    }


################################################################
# Problem.symptom


def make_symptom():
    return suggest(
        Problem.symptom(
            Who.patient(
                When.present(
                    Rank.high(
                        dict_synonym())))))


def dict_synonym():
    return {
        '10154-3':
            Rank.high(Why.complaint(When.admit(Where.hosp(strict(
                ['CHIEF COMPLAINT', 'PATIENT COMPLAINT', 'PATIENT STATES COMPLAINT',
                 common('COMPLAINTS'), relax(multi(abbr('CC')))]))))),

        '46239-0': Rank.high(Why.complaint(When.admit(Where.hosp(strict(
            ['REASON FOR VISIT AND CHIEF COMPLAINT',
             'REASON FOR VISIT/CHIEF COMPLAINT',
             'CHIEF COMPLAINT AND REASON FOR VISIT',
             'CHIEF COMPLAINT REASON FOR VISIT']))))),

        '75325-1': common([
            pref('Symptom'), 'SYMPTOMS', 'PATIENT SYMPTOMS'])
}

################################################################
# Problem.problem


def make_problem():
    return suggest(
        Problem.problem(
            Who.patient(
                dict_problem())))


def dict_problem():
    return {
        '29299-5': Rank.high( Why.reason( When.admit( Where.hosp( strict(
            ['REASON FOR VISIT', 'REASON FOR ADMISSION',
             'HISTORY AND REASON FOR HOSPITALIZATION',
             'REASON FOR HOSPITALIZATION',
             'HISTORY AND REASON FOR ADMISSION',
             'HISTORY REASON FOR HOSPITALIZATION']))))),

        '42349-1': Rank.high( Why.reason( Where.consult( When.present( strict(
            ['REASON FOR CONSULT', 'REASON FOR CONSULTATION', 'REASON FOR REFERRAL',
             Where.clinic('Reason for clinic visit'),
             Where.clinic('Reason for Appointment'),
             Where.clinic('REASON FOR EXAM'), Where.clinic('REASON FOR THIS EXAMINATION')]))))),

        '59768-2': Rank.high( Why.indication( Where.surgery( When.admit(strict(
            ['PROCEDURE INDICATION', 'PROCEDURE INDICATIONS', 'INDICATION FOR PROCEDURE',
             'INDICATION FOR SURGERY', 'INDICATION FOR INDUCTION', 'INDICATION FOR OPERATION',
             'INDICATION FOR TESTING', 'INDICATION FOR TEST', 'TEST INDICATION',
             multi(relax('INDICATION')), multi(relax('INDICATION')),
             Impress.interpret('PROCEDURE INDICATIONS INTERPRETATION')]))))),

        '18785-6': [Problem.problem(Rank.high(Why.reason('RADIOLOGY REASON FOR STUDY')))],

        '11450-4': Rank.high( When.present( strict(
            ['PROBLEM LIST', 'LIST OF PROBLEM', 'LIST OF PROBLEMS', 'PROBLEMS BY SYSTEMS', 'PROBLEMS BY SYSTEM',
             'PROBLEM LIST AND DIAGNOSIS', 'PROBLEMS AND DIAGNOSIS',
             When.admit('LIST OF PROBLEMS DURING ADMISSION'),
             When.admit('LIST OF PROBLEMS DURING HOSPITALIZATION'),
             Where.hosp('Hospital Problem List'),
             Rank.first('ACTIVE PROBLEMS LIST'),
             Rank.first('ACTIVE PROBLEMS'),
             Rank.first('PRINCIPAL PROBLEM'),
             Rank.first('SIGNIFICANT PROBLEMS'),
             Rank.second('OTHER SIGNIFICANT PROBLEMS'),
             Rank.second('OTHER PROBLEMS'),
             Rank.second('OTHER ASSOCIATED PROBLEMS'),
             Rank.high('PROBLEM CARDIOVASCULAR'),
             relax('NEW PROBLEMS'),
             relax('SPONTANEOUS CONDITION'),
             relax('UNDERLYING MEDICAL CONDITION'),
             common('MEDICAL PROBLEMS'), common('PROBLEM'), common('PROBLEMS'), common('CONDITIONS')]))),

        '61133-5': Impress.interpret( Style.narrative( strict([
            Rank.first(strict('PRIMARY PROBLEM INTERPRETATION')),
            When.admit(relax('IMPRESSION ON ADMISSION')),
            'CLINICAL IMPRESSION', relax('IMPRESSION')]))),

        '51898-5': Rank.high(Style.narrative(strict([
            'RISK FACTORS',
            'CARDIAC RISK FACTORS', 'CORONARY RISK FACTORS',
            'HYPERTENSIVE URGENCY', 'HYPERGLYCEMIC SYMPTOMS']))),

        # Aspect.problem Person.family
        '10157-6': Rank.ignore(Who.family([Style.narrative('HISTORY OF FAMILY MEMBER DISEASES'),
                                           Style.narrative('FAMILY HISTORY'),
                                           Style.narrative(abbr('FHX')),
                                           Style.subhead('FATHER'),
                                           Style.subhead('MOTHER'),
                                           Style.subhead('SIBLINGS'),
                                           Style.subhead('SPOUSE'),
                                           Style.subhead('OFFSPRING'),
                                           Style.subhead('PEDIGREE')])),

        '32435-0': Who.family(multi(relax([
            pref('History of Hereditary disorders'),
            'HEREDITARY', 'ANCESTRAL', 'ANCESTRY', 'HEREDITARY', 'INHERITANCE']))),

        # @@@ Subjective?
        '10164-2': Rank.high(Impress.interpret( Style.narrative( When.present( strict([
            pref('History of Present Illness'), abbr('HPI'),
            'Hx Present Illness',
            'Hx of Pres illness',
            'Hx of Present illness',
            'HISTORY PRESENT ILLNESS',
            'BRIEF HISTORY OF PHYSICAL ILLNESS',
            'BRIEF ADMISSION HISTORY OF PRESENT ILLNESS',
            'BRIEF HISTORY OF PRESENT ILLNESS',
            multi('HISTORY OF PRESENT ILLNESS AND HOSPITAL COURSE'),
            'HISTORY OF PRESENT ILLNESS AND REASON FOR HOSPITALIZATION',
            'HISTORY OF PRESENTING ILLNESS',
            'HISTORY OF THE PRESENT ILLNESS',
            'HISTORY AND PHYSICAL HISTORY OF PRESENT ILLNESS',
            'Health Concerns',
            Exam.physical('HISTORY AND PHYSICAL'),
            Exam.physical('HISTORY AND PHYSICALS'),
            Exam.physical(abbr('H&P')),
            Exam.physical(abbr(Style.printer('H&P BY'))),
            relax('BRIEF HISTORY'),
            relax('PRESENT ILLNESS')]))))),

        '61150-9': Why.complaint( Style.narrative([
            multi(strict('SUBJECTIVE DATA')), multi(relax('SUBJECTIVE'))])),

        '51848-0': Impress.interpret( Style.narrative(relax([
            multi('EVALUATION NOTE'), relax('EVALUATION'), multi('EVAL NOTE'),
            multi('ASSESSMENT/PLAN'),
            relax('ASSESSMENT'), multi('ASSESSMENTS')]))),

        '61146-7': Instruct.care(relax([pref('GOALS'),
                    strict('SHORT TERM GOAL'),
                    strict('LONG TERM GOAL'),
                    'GOAL', 'GOALS', 'GOAL DATE'])),

        '55108-5': Impress.interpret( Style.narrative( strict([
            multi('CLINICAL PRESENTATIONS'), multi('CLINICAL PRESENTATION')]))),

        '55109-3': Rank.high( Impress.notable( When.present( Style.narrative(strict([
            strict('COMPLICATIONS DOCUMENT'), common('COMPLICATIONS'), common('CONCERNS')]))))),

        '55752-0': multi([pref('Clinical information'), 'Clinical data']),

        '11329-0': When.history(multi( [
            pref('History general'), 'MEDICAL GENERAL HISTORY', relax('GENERAL HISTORY'),
            common('BRIEF HISTORY')])),

        '8648-8': Impress.notable( Rank.first( When.transfer( Where.hosp(strict([
            'HOSPITAL COURSE',
            'HOSPITAL COURSE BY SYSTEM', 'HOSPITAL COURSE BY SYSTEMS',
            'SUMMARY OF HOSPITAL COURSE',
            'COURSE BY PROBLEM',
            'BRIEF HOSPITAL COURSE',
            'EMERGENCY DEPARTMENT COURSE',
            'HOSPITAL COURSE BY PROBLEM', 'HOSPITAL COURSE BY PROBLEMS',
            'HOSPITAL COURSE BY SYSTEM AND PROBLEM',
            'HOSPITAL COURSE AND TREATMENT']))))),

        '55112-7': Impress.interpret( Rank.high([
            pref('Document summary'), common('DISCUSSION'), common('SUMMARY')])),
    }


################################################################
# Problem.diagnosis

def make_diagnosis():
    return suggest(
        Problem.diagnosis(
            Who.patient(
                dict_diagnosis())))


def dict_diagnosis():
    return {
        '46241-6': [Rank.first(Why.reason(pref('HOSPITAL ADMISSION DIAGNOSIS'))),
                    Rank.first(Why.reason(strict('HOSPITAL ADMISSION DX')))],

        '11535-2': [Rank.high(strict(pref('HOSPITAL DISCHARGE DX'))),
                    Rank.high(strict('HOSPITAL DISCHARGE DIAGNOSIS'))],

        '42347-5': Impress.interpret( Rank.first( When.admit( Where.hosp( strict( [
            pref('Admission diagnosis'),
            'ADMISSION DIAGNOSES',
            'ADMIT DIAGNOSIS', 'ADMIT DIAGNOSES',
            'ADMITTING DIAGNOSIS', 'ADMITTING DIAGNOSES',
            'LIST OF DIAGNOSIS DURING ADMISSION',
            'PRINCIPAL ADMISSION DIAGNOSIS',
            'PRINCIPAL DIAGNOSIS FOR ADMISSION',
            'PRINCIPAL DIAGNOSIS ON ADMISSION',
            'PRIMARY ADMISSION DIAGNOSIS',
            'PRIMARY ADMITTING DIAGNOSIS',
            'PRIMARY DIAGNOSIS DURING THIS ADMISSION',
            'PRIMARY DIAGNOSIS ON ADMISSION',
            'PRINCIPLE ADMISSION DIAGNOSIS',
            Rank.second('ADDITIONAL ADMITTING DIAGNOSIS'),
            Rank.second('PRELIMINARY DIAGNOSIS')]))))),

        '78375-3': Impress.conclude( When.discharge( Where.hosp( strict([
            Rank.high(pref('Discharge diagnosis')),
            Rank.first('PRINCIPLE DISCHARGE DIAGNOSIS'),
            Rank.second('DISCHARGE DIAGNOSES'),
            Rank.second('ASSOCIATE DISCHARGE DIAGNOSIS'),
            Rank.first('PRINCIPAL DIAGNOSIS ON DISCHARGE'),
            Rank.first('PRINCIPAL DIAGNOSIS ON THIS PATIENT'),
            Rank.first('PRIMARY DISCHARGE DIAGNOSIS'),
            Rank.first('PRINCIPAL DISCHARGE DIAGNOSIS'),
            Rank.first('PRINCIPAL DISCHARGE DIAGNOSES'),
            Rank.first('DIAGNOSIS AT DISCHARGE'),
            Rank.second('ASSOCIATED DISCHARGE DIAGNOSES'),
            Rank.second('OTHER DIAGNOSES ON DISCHARGE'),
            Rank.second('OTHER DIAGNOSIS AT DISCHARGE'),
            Rank.second('OTHER DISCHARGE DIAGNOSES'),
            Rank.second('OTHER MEDICAL DIAGNOSIS'),
            Rank.second('SECONDARY DISCHARGE DIAGNOSES'),
            Rank.second('OTHER DIAGNOSES AND CONDITIONS AFFECTING TREATMENT OR STAY'),
            relax('CONDITION AT DISCHARGE')])))),

        '52534-5': Rank.first(Impress.conclude( When.present( relax(
            [pref('Principal Diagnosis'), 'PRINCIPLE DIAGNOSIS',
             'PRIMARY DIAGNOSIS', 'Primary DX', 'PRIMARY DIAGNOSES', 'PRIMARY MEDICAL DIAGNOSIS',
             common('CURRENT DIAGNOSIS')])))),

        '54531-9': Rank.first(Impress.interpret( When.present(relax([
            pref('Active disease diagnosis'),
            'ACTIVE DISEASE DIAGNOSES', 'ACTIVE DIAGNOSES',
            Rank.first('ACUTE DIAGNOSES'),
            Rank.first('CHRONIC DIAGNOSES'),
            Where.home('HOME CARE DIAGNOSIS'),
            relax('CLINICAL DIAGNOSIS'),
            relax('ACTIVE DIAGNOSIS')])))),

        '54545-9': Rank.high( Impress.notable( relax([
            pref('Additional diagnoses'),
            Rank.second('SECONDARY DIAGNOSIS'),
            Rank.second('SECONDARY DIAGNOSES'),
            Rank.second('RELATED DIAGNOSES'),
            'LIST OF OTHER DIAGNOSES',
            'LIST OF OTHER PROBLEMS AND DIAGNOSES',
            'LIST OF PROBLEMS AND OTHER DIAGNOSES',
            'LISTS OF PROBLEMS AND DIAGNOSES',
            'OTHER SIGNIFICANT DIAGNOSES',
            'OTHER MEDICAL DIAGNOSIS', 'OTHER MEDICAL DIAGNOSES',
            'OTHER PROBLEMS AND DIAGNOSES', 'OTHER PROBLEMS AND DIAGNOSIS',
            'OTHER DIAGNOSES', 'OTHER DIAGNOSIS',
            'ADDITIONAL DIAGNOSES', 'ADDITIONAL DIAGNOSIS',
            'ASSOCIATED DIAGNOSES', 'ASSOCIATED DIAGNOSIS']))),

        '29308-4': When.present(Impress.interpret( [
            pref('Diagnosis'), relax('DIAGNOSES'), common('DIAGNOSES'), common('CONDITION'),
            strict('VISIT DIAGNOSIS'), strict('VISIT DIAGNOSES'),
            strict('ENCOUNTER DIAGNOSIS'), strict('ENCOUNTER DIAGNOSES'),
            strict('DIAGNOSIS LIST'), strict('DIAGNOSES LIST'), strict('LIST OF PROBLEMS AND DIAGNOSES'),
            'LIST OF DIAGNOSES',
            'PROBLEMS AND DIAGNOSIS',
            common('ADDITIONAL DIAGNOSES INCLUDE')])),

        '55110-1': Impress.conclude(multi([
            pref('Conclusions Document'),
            strict('Interpretation Document'),
            strict('CONCLUSIONS INTERPRETATION'),
            strict('DIAGNOSTIC IMPRESSION'),
            Impress.interpret(relax('Interpretation')),
            relax('CONCLUSION'), relax('CONCLUSIONS')])),

        '11348-0': Rank.high( Impress.interpret( When.history( strict([
            pref('Past Medical History'), abbr('PMH'), abbr('PMHX'),
            'CLINICAL HISTORY',
            'PERSONAL HISTORY',
            'PAST HISTORY',
            'History of Past illness',
            'PAST GYN HISTORY',
            'PAST GYNECOLOGIC HISTORY',
            'PAST PSYCHIATRIC HISTORY',
            Where.department(multi(relax('PSYCHIATRIC')))])))),

        '10219-4': Rank.first( Why.indication( Where.surgery( When.admit( [
            pref('Surgical operation note preoperative diagnosis'),
            'SURGICAL OPERATION NOTE PREOPERATIVE DX',
            'PREOPERATIVE DX', 'Operative note pre-op Dx',
            'PREOPERATIVE DIAGNOSES', 'PREOPERATIVE DIAGNOSIS'])))),

        '10218-6': Rank.second( Where.surgery( When.discharge( [
            pref('SURGICAL OPERATION NOTE POSTOPERATIVE DIAGNOSIS'),
            multi('POSTPROCEDURE DIAGNOSIS'),
            strict('POSTOPERATIVE DIAGNOSES'),
            strict('POSTOPERATIVE DIAGNOSIS')]))),

        '93127-9': Rank.high( Why.reason( [
            pref('Risk Adjustment Factor'),
            strict('Risk Score'),
            strict('Risk Adjustment'),
            relax('Risk Factor'),
            common('RISK'),
            multi(abbr('DRG')),
            multi(abbr('HCC')), multi(abbr('HCC/CMS'))])),

        '22637-3': Rank.first(Problem.diagnosis(Impress.conclude(Rank.first([
            pref('Pathology report final diagnosis'),
            'HISTOPATHOLOGICAL DIAGNOSIS',
            'PATHOLOGIC DIAGNOSIS',
            multi('FINAL DIAGNOSES'),
            multi('FINAL DIAGNOSIS')])))),

        '52797-8': Rank.high( Style.lists( Impress.conclude (multi(relax(
            [strict('ICD-10-CM'), strict('ICD-9-CM'),
             'ICD-10', 'ICD-9', 'ICD10', 'ICD9'])))))
        }


################################################################
# Procedure.procedure

def make_procedure():
    return suggest(
        Procedure.procedure(
            Who.patient(
                dict_procedure())))


def dict_procedure():
    return {
        '47519-4': Rank.high( When.history( strict([
            pref('History of Procedures'),
            'Procedures Hx Doc', 'Procedures Hx',
            'PROCEDURE LIST',
            relax('PROCEDURES')]))),

        '59772-4': [Rank.ignore(When.plan('PLANNED PROCEDURE'))],

        '55114-3': When.history(['PRIOR PROCEDURE DESCRIPTIONS',
                                 'PRIOR PROCEDURE HISTORY',
                                 'PROCEDURE HISTORY', 'PROCEDURES HISTORY']),

        '29554-3': Rank.high( When.present( Style.narrative( multi( [
            pref('Procedure Narrative'),
            Rank.first(strict('PRINCIPAL PROCEDURE')),
            strict('PROCEDURE DESCRIPTION'),
            strict('TITLE OF OPERATION'),
            strict('PROCEDURES AND SURGICAL/MEDICAL HISTORY'),
            common('PROCEDURE')])))),

        '59773-2': [pref('Procedure specimens taken'), relax('SPECIMENS TAKEN')],

        '46062-6': Instruct.care(relax([
            pref('Treatments Set'),
            'TREATMENTS', 'CURRENT TREATMENT',
            'Dialysis', 'Ostomy', 'Radiation',  'Suctioning', 'Tracheostomy',
            'Stress Test'])),

        '69967-8': [pref('Procedure code'),
                    strict('PROCEDURE CODES'), strict('ICD Procedures'),
                    multi(abbr('ICD')),
                    abbr('ICD-10-PCS'),
                    abbr('CPT'), strict('Current Procedural Terminology'),
                    abbr('HCPCS'), strict('Healthcare Common Procedure Coding System')]
    }

######################################################################
# Pathology

def make_pathology():
    return suggest(
        Procedure.procedure(
            Who.patient(
                Where.pathology(
                    Impress.interpret(dict_pathology())))))

def dict_pathology():
    return {
        '70949-3': strict([
            pref('Pathology report'),
            'FORMATTED PATH REPORT',
            'Surgical pathology study', 'SURGICAL PATHOLOGY CONSULTATION REPORT', 'SURGICAL PATHOLOGY CONSULT',
            'Pathology Synoptic report',
            'Pathology Consult note',
            'DEPARTMENT OF CANCER PATHOLOGY', 'PATHOLOGY DEPARTMENT',
            'COPATH CYTOLOGY REPORT', 'Department of Pathology', 'PATHOLOGY ADDENDUM',
            'Tamtron Print', 'Powerpath',
            'Cytology Request',
            relax('PATH REPORT'), multi(relax('PATHOLOGY'))]),

    '22635-7': Rank.first(strict( [
        pref('Pathology report microscopic observation'),
        'MICROSCOPIC OBSERVATION',
        'MICROSCOPIC DESCRIPTION',
        'MICROSCOPIC EXAMINATION', common('MICROSCOPIC')])),

    '33732-9': Rank.first([
        pref('Histology grade'),
        'HISTOLOGIC GRADE', relax('HISTOLOGIC'), relax('HISTOLOGY')]),

    '21859-4': [ # 22633-2
        pref('Primary Cancer Site'),
        'ANATOMIC SITE', 'SITE OF TISSUE', 'TISSUE SITE', 'TUMOR LOCATION', 'TUMOR SITE'],

    '21939-4': Rank.low([
        pref('Surgical margins'), relax('MARGINS')]),

    '92833-3': [relax('LYMPH NODES')],

    '42186-7': Rank.low( [
        pref('Specimens received'), 'RECEIVED SPECIMEN', 'SPECIMEN DETAILS', 'SPECIMEN ID',
        'MATERIAL COLLECTED ON', 'MATERIAL RECEIVED ON', 'MATERIAL RECEIVED']),

    '66746-9': Rank.low(['SPECIMEN TYPE', 'SPECIMEN', 'SPECIMENS', 'SPECIMEN source', 'TISSUE SPECIFICATION']),

    '90041-5': Style.subhead([
        pref('Specimen collection'),
        'MATERIAL COLLECTED', 'SPECIMEN SUBMITTED',
        'SPECIMENS SUBMITTED', 'TISSUE SUBMITTED',
        multi('Date collected'), multi('COLLECTION DATE'),
        multi('Date received'),
        multi('Date entered'),
        multi('Date reported')]),

    '67203-0': Rank.high([ pref('AJCC cancer staging'),
                           strict('AJCC STAGING'), relax('AJCC CLASSIFICATION'), abbr('AJCC')]),

    '75621-3': Rank.high([pref('TNM pathologic staging'),
                          'TNM PATHOLOGIC STAGING AFTER SURGERY PANEL', 'TNM PATHOLOGIC STAGING', 'TNM STAGING',
                          strict('PATHOLOGIC STAGE'), strict('PATHOLOGY STAGE'),
                          'NOTTINGHAM HISTOLOGIC SCORE',
                          abbr('TNM STAGE'),
                          common('STAGING')]),

    '51960-3': Rank.second(relax([
        pref('MOLECULAR RESULTS'),
        strict('BIOMARKER TESTING'),
        strict('MUTATION SCREENING'),
        strict('MUTATIONAL ANALYSIS'), strict('Mutation Analysis Panel Report'),
        strict('DNA marker results panel'),
        strict('DNA testing result'),
        strict('Genomic reference sequence'),
        strict('Transcript reference sequence'),
        strict('Genetic variation clinical significance'),
        'Gene Symbol', 'HGNC', common('HUGO'),
        'exon', 'exons', 'intron', 'introns', 'codon', 'codons',
        'Genetic variation',
        'Genetic variant',
        'DNA test result',
        'DNA change',
        'Amino acid change',
        abbr('pHGVS'),
        abbr('c.HGVS'),
        abbr('HGVS')])),

    '33746-9': Where.pathology([pref('Pathologic findings'), 'ADDITIONAL PATHOLOGIC FINDINGS']),

    '22634-0': Where.pathology(strict([
            pref('Pathology report gross observation'),
            'PATHOLOGY REPORT GROSS OBSERVATION', 'PATHOLOGY REPORT GROSS DESCRIPTION',
            'MACROSCOPIC ANATOMIC OBSERVATIONS',
            'MACROSCOPIC OBSERVATIONS', 'MACROSCOPIC DESCRIPTIONS', 'MACROSCOPIC EXAMINATION', 'MACROSCOPY',
            'SPECIMEN INFORMATION', 'SPECIMEN INFO', relax('SPECIMEN'), common('TISSUE'),
            'TUMOR SIZE', 'TUMOR EXTENT', common('TUMOR'),
            'GROSS DESCRIPTION TEXT', 'GROSS DESCRIPTION TEXT', 'GROSS OBSERVATION', 'GROSS TEXT',
            'GROSS FINDINGS'])),

    '2638-1': Impress.interpret(common(['Interpretation', 'results', 'result', 'conclusion', 'comments'])),

    '21902-2': Impress.conclude(Style.choice([
        pref('Stage group'),
        'CLINICAL STAGE', 'CANCER STAGE',
        'Stage IVB', 'Stage IVA', 'Stage IV',
        'Stage IIIC', 'Stage IIIB', 'Stage IIIA','Stage III',
        'Stage IIC', 'Stage IIB', 'Stage IIA','Stage II',
        'Stage IB', 'Stage IA', 'Stage I',
        'Stage IVC', 'Stage IS',
        'Stage IB2', 'Stage IB1',
        'Stage IA2', 'Stage IA1',
        'Stage 0is', 'Stage 0A','Stage 0',
        'Stage IC', 'Stage IE',
        'Stage 2A1', 'Stage 2A2',
        'Stage IIE', 'Stage IIS',
        'Stage 3C1', 'Stage 3C2',
        'Stage IIIE', 'Stage IIIS',
        'Stage IVE', 'Stage IVS'])),
    }

################################################################
# Procedure.surgery

def make_surgery():
    return suggest(
        Procedure.operate(
            Who.patient(
                Where.surgery(
                    Style.narrative(dict_surgery())))))

def dict_surgery():
    return {
        '59774-0': strict([
            pref('Procedure anesthesia'),
            'ANESTHESIA SECTION',
            'PRIMARY ANESTHESIA',
            relax('ANESTHESIA')]),

        '83321-0': [
            pref('Pathology report intraoperative observation in Specimen'),
            relax('intraoperative diagnosis')],

        '8724-7': [ pref('Surgical operation note description'),
                    'DESCRIPTION OF OPERATION', 'OPERATION DESCRIPTION', 'DESCRIPTION OF THE OPERATION',
                    'TITLE OF OPERATION', 'OPERATION PERFORMED', 'NAME OF OPERATION'],

        '59770-8': [pref('Procedure estimated blood loss '),
                    multi('BLOOD LOSS'),
                    relax('ESTIMATED BLOOD LOSS')],

        '8690-0': [pref('History of Surgical procedures'),
                   strict('PAST SURGICAL HISTORY'),
                   strict('SURGICAL HISTORY'),
                   relax('OPERATIONS'),
                   relax('OPERATIONS PERFORMED'),
                   relax('OPERATION'),
                   relax('SURGERIES')],

        '11537-8': ['Surgical drains', 'SURGICAL DRAINS NOTE'],

        '59771-6': ['Procedure implants', common('IMPLANTS')],

        '10216-0': [pref('Surgical operation note fluids'), 'OPERATIVE NOTE FLUIDS'],

        '10223-6': [pref('Surgical operation note surgical procedure'),
                    'OPERATIVE NOTE SURGICAL', 'SURGICAL PROCEDURE'],

        '62387-6': [relax('Interventions'), 'INTERVENTIONS PROVIDED'],
    }


################################################################
# Procedure.device

def make_device():
    return suggest(
        Procedure.device(
            Rank.first(
                Who.patient(
                    dict_device()))))


def dict_device():
    return {
        '46264-8': [pref('History of medical device use'), relax('Medical Device'), relax('Medical Devices')],
        '45752-3': [pref('Ventilator or respirator'), relax('Ventilator'), relax('respirator'), multi(common('VENT'))],
    }


################################################################
# Instruct.care

def make_instructions():
    return suggest(
        Instruct.care(
            Who.patient(
                When.plan(
                    Rank.low(dict_instructions())))))

def dict_instructions():
    return {
        '8653-8': [
            pref('Hospital Discharge instructions'), strict('Discharge instructions')],

        '69730-0': strict([
            pref('INSTRUCTIONS'),
            'CARE AND RECOMMENDATIONS', common('Instructions'),
            'PATIENT EDUCATION', multi(common('EDUCATION'))]),

        '18776-5': strict([
            pref('Plan of care note'),
            'Plan of treatment', 'CARE PLAN', 'CARE RECOMMENDATIONS',  common(multi('PLAN'))]),

        '51847-2': Impress.interpret(When.plan(multi(strict([
            pref('Evaluation + Plan'), 'Evaluation+Plan', 'EVALUATION AND PLAN', 'ASSESSMENT AND PLAN',
            relax('ASSESSMENT & PLAN'), relax('ASSESSMENT/PLAN'), 'IMPRESSION AND PLAN',
            abbr('A+P'), abbr('A&P')])))),

        '61144-2': When.plan(Style.narrative(['DIET AND NUTRITION',
                                              'DIET+NUTRITION',
                                              relax('DIET'),
                                              relax('NUTRITION')])),

        '42344-2': [When.plan('DISCHARGE DIET')],

        '42348-3': When.plan(['ADVANCED DIRECTIVES', 'ADVANCE DIRECTIVES', relax('DIRECTIVES')]),

        '45474-4': When.plan(['Advance directive - do not resuscitate', 'do not resuscitate', abbr('DNR')]),
    }


################################################################
# Instruct.cover

def make_coversheet():
    return Rank.ignore(
        Instruct.cover(
            Visit.encounter(dict_coversheet())))

def dict_coversheet():
    return {
        '64289-2': [pref('Fax cover sheet'), 'cover sheet', 'cover page',
                    'MEDICAL RECORDS REQUEST', 'Record Pull List'],

        '71727-2': Rank.low(Who.provider(Style.unique([
            pref('Fax number'), abbr('FAX'), abbr('EFAX'), abbr('E-FAX'), 'SECURE FAX', 'HEALTHPORT',
            'HEALTH PORT', 'FACESHEET', strict('FACSIMILE TRANSMITTAL SHEET'),
            'FAX FROM', 'FAX TO', strict('FAX #'), 'FAXPHONE']))),

        '19826-7': Rank.ignore(Style.legal(strict([
            pref('Informed consent obtained'),
            'institutional review board', abbr('IRB'),
            relax('IRB approval'), relax('IRB approvals'), relax('IRB approved'),
            'WIRB', 'Western IRB', 'EXEMPTION REQUEST',
            'INFORMED CONSENT', 'PATIENT CONSENT', relax('CONSENT')]))),

        '55277-8': Rank.ignore(multi(Style.legal([
            pref('HIV status'), multi(abbr('HIV')),
            relax('Human Immunodeficiency Virus')]))),

        '76469-6' : Rank.ignore(Style.narrative([
            pref('Federal Agency'),
            abbr('CDC'), 'Centers for Disease Control',
            abbr('DPH'), 'Department of Public Health',
            abbr('FDA'), 'Federal Drug Administration',
            abbr('SSA'), 'Social Security Administration', abbr('SSA-827'), 'DISABILITY DETERMINATION',
            abbr('HIPAA'), 'health insurance portability and accountability act', '45 CFR', '45CFR'])),

        '94137-7': Rank.ignore(strict(Style.narrative([
            pref('Stars and HEDIS Measure Guidelines and Checklist'),
            'Stars and HEDIS® Measure Guidelines and Checklist',
            'HEDIS®', 'HEDIS', 'HEDIS Measure Guidelines and Checklist', 'HEDIS Guidelines',
            relax('HEDIS Measure'), relax('HEDIS Measures')])))
    }



######################################################################
# UNMAPPED ( and observed in real world data, especially Cyan)

# TODO: https://clerkship.medicine.ufl.edu/portfolio/interpersonal-and-communicative-skills/documenting-in-the-medical-record/discharge-summarytransfer-noteoff-service-note-instructions/
# TODO: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4563061/

headers_unmapped = [
    'admission type',
    'office visit',
    'TRIAGE',
    'Nursing Unit',
    'ED Disposition', 'ED Arrival', 'Discharge Destination',
    'PATIENT DATA',
    'Hospital Summary',
    'transfer source',
    'admit provider', 'ordering provider', 'CPOE',
    multi('SUBJECT'),
    relax('SCREEN'),

    'MEDICATIONS ON TRANSFER FROM REHAB',
    'VISIT TYPE', 'office visit',
    'HISTORIES',
    'ADMIT SOURCE', 'ADMIT TYPE',
    'PHARMACY', #Aspect.encounter
    'PHARMACIES',

    'Episode Type',
    relax('Physical Therapy'), # Aspect.treatment
    'Specialized Rehab', 'Rehab',
    'Hospice', #Aspect.encounter
]

TODO = {
    '84907-5' # Cancer pathology panel - Colorectal cancer specimen
    '69459-6' # Care record summary panel
    '81242-0',# Enhanced discharge summary - recommended CDP Set 1 R1.0 sections
    '55168-9',# Data Elements for Emergency Department Systems (DEEDS) Release 1.1
    '18726-0',# Radiology studies (set)
    '81220-6',# Diagnostic imaging report - recommended C-CDA R2.0 and R2.1 sections
    '74293-2',# Oncology plan of care and summary - recommended CDA set
    '82308-8',# Oncology plan of care and summary - recommended CDA R1.2 sections
    '55168-9',# Data Elements for Emergency Department Systems (DEEDS) Release 1.1
    '28650-0',# Clinical notes and chart sections Set
    '26443-2',# Clinical reports.non lab claims attachment
    '...' # Clinical Notes
}
