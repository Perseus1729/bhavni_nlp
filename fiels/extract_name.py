from medcat.cat import CAT
import spacy
from collections import defaultdict
import re
import json 
# Download the model_pack from the models section in the github repo.
DATA_DIR = "./data/"
model_pack_path = DATA_DIR + "medmen_wstatus_2021_oct.zip"
cat = CAT.load_model_pack(model_pack_path)
print("--------------------------------------")
# Test it
text = """NAME Sandhya, REF BY: DR.DUMMY DUMMY, SAMPLE REPORT
Sample ID | MMG20200057563 Sample Type | Oropharyngeal/Nasopharyngeal_
| Gender | Male Sample Collected On Oct 30, 2020 : 10;00
| Age / DOB 3 | Report Date Oct 30, 2020 : 23:17
| Aadhar Number 1234 5678 9101 Mobile Number 123456789
Referred By Hospital
| Passport Number 123456 ‘Nationality Nie
RT-PCR test for COVID-19 (NOVEL CORONA VIRUS)

Result

| Investigation CT Value Result |
SARS-CoV-2 virus detection (N Gene) Undetermined y  (Positive)
"""
type_ids_filter = ['T033']
cui_filters = set()
for type_ids in type_ids_filter:
  cui_filters.update(cat.cdb.addl_info['type_id2cuis'][type_ids])
cat.cdb.config.linking['filters']['cuis'] = cui_filters
doc=cat(text)
for ent in doc.ents:
    print(ent)
doc2 = cat(text)
#print(f"The size of the cdb is now: {len(cui_filters)}")
print("--------------------------------------")
keys = []
values = []
nlp = spacy.load('en_core_web_md')
text1= nlp(text)
for w in text1.ents:
    if w.label_=='DATE':
        keys.append('DATE')
        values.append(w.text)
        print(w.text)
print("--------------------------------------")
text2 = nlp(text.lower())
for w in text2.ents:
  if w.label_=='PERSON':
    keys.append('PERSON')
    values.append(w.text)
    print(w.text)
print("--------------------------------------")
beams = nlp.entity.beam_parse([ text1 ], beam_width = 16, beam_density = 0.001)
entity_scores = defaultdict(float)
for beam in beams:
  for score, ents in nlp.entity.moves.get_beam_parses(beam):
      for start, end, label in ents:
        entity_scores[(start, label)] += score
print("--------------------------------------")
def patientID(text):
  ID_REG = re.compile(r'[a-zA-Z0-9\.\-+_]{14}')
  IDs = re.findall(ID_REG,text)
  patientID = ",".join(IDs)
  patientID = patientID.split(',')
  patientID = patientID[0]

  return patientID
patientID=patientID(text)
list_words= text.split()
index =list_words.index("ID")
pre_IDs=list_words[index-3:index+3]
for i in pre_IDs:
  if i==patientID:
    ID=i
keys.append('PATIENT ID')
values.append(ID)
print(ID)
print("--------------------------------------")
dictionary = dict(zip(keys, values))
json_object = json.dumps(dictionary, indent = 4) 
print(json_object)