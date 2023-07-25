from .loinc_sections import relax, multi

#########################################################################################################################
# CDC "R5" criteria define 5 race types --
#
# NOTICE: hospital records for "race" are rather sloppy --
# the same patient treated at different hospitals may have stated their race (patient reported)
# differently from hospital to the next, though usually the same race codes are used.
# The detailed dictionary of race hierarchy terms is rarely available or documented.

README ='https://phinvads.cdc.gov/vads/ViewValueSet.action?id=67D34BBC-617F-DD11-B38D-00188B398520'

demographics_race_cdc_r5 = {
    '1002-5': ['AMERICAN INDIAN OR ALASKA NATIVE',
               relax('AMERICAN INDIAN'),
               relax('ALASKA NATIVE'),
               relax('NATIVE AMERICAN'),
               relax('FIRST PEOPLE')],

    '2028-9': ['ASIAN INDIAN', 'ASIAN', 'OTHER ASIAN', 'VIETNAMESE', 'CHINESE', 'JAPANESE', 'KOREAN'],

    '2054-5': ['BLACK OR AFRICAN AMERICAN',
               'AFRICAN AMERICAN',
               multi('BLACK')],

    '2076-8': ['NATIVE HAWAIIAN',
               relax('HAWAIIAN'),
               'OTHER PACIFIC ISLANDER',
               relax('PACIFIC ISLANDER'), 'SAMOAN'],

    '2131-1':['OTHER RACE', 'GUAMANIAN OR CHAMORRO', 'GUAMANIAN', 'CHAMORRO',],

    '2106-3':[multi('WHITE')]
}