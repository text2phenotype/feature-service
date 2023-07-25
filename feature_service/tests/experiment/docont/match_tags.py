
def inspect(meta:dict)->dict:
    meta['head'] = meta['head'].upper()
    head = meta['head']
    if 3 >= len(head):
        meta['abbr'] = True

    if 'LIST' in head.split():
        meta['style'] = 'StyleType.lists'
    return meta

def cons(**kwargs)->dict:
    out = dict()
    for key, value in kwargs.items():
        if 'head' in key:
            out[key] = value.strip().upper()
        else:
            out[key] = value
    return inspect(out)

def strict(text:str)->dict:# strict match (default) section heading
    return cons(head=text, relax=False)

def relax(text:str)->dict: # relax match, potential match in sentence
    return cons(head=text, relax=True)

def multi(text:str)->dict: # Homonym, multiple context
    return cons(head=text, multi=True, relax=True)

def finding(text:str)->dict: # subtype, usually problems or phys exam
    return cons(head=text, finding=True)

def abbr(text:str)->dict: # abbreviation
    return cons(head=text, abbr=True)

def negate(text:str): # negate (Polarity.NEGATIVE)
    return cons(head=text, rank='low', negate=True)

def rank_low(text:str): # lower importance
    return cons(head=text, rank='low')

def strict(text:str): # higher importance
    return cons(head=text, rank='high')

def reason(text:str): # reason for visit, chief complaint, (patient stated)
    return cons(head=text, rank='high', reason=True)

def indication(text:str): # indication for test/procedures/etc, (doctor/RN stated)
    return cons(head=text, rank='high', indication=True)

def hosp(text:str): # admission / hospitalized
    return cons(head=text, rank='high', hosp=True)

def admit(text): # admission / hospitalized

    res = dict()
    if isinstance(text, str):
        res = cons(head=text, rank='high', hosp=True, admit=True)
    else:
        pass
    #return cons(head=text, rank='high', hosp=True, admit=True)

def discharge(text:str): # admission / hospitalized
    return cons(head=text, rank='high', hosp=True, discharge=True)

def legal(text:str):
    return cons(head=text, rank='low', negate=True, style='StyleType.legal')

def vital(text):
    return cons(head=text, relax=True, vital=True)

def vital_slang(text):
    return cons(head=text, relax=True, vital=True, slang=True)

def body(text):
    if isinstance(text, list):
        return [body(t) for t in text]
    else:
        return cons(head=text, body=True, style='StyleType.subheading')

