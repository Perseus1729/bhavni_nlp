from cgitb import enable
from medcat.cat import CAT
import spacy

# Download the model_pack from the models section in the github repo.
DATA_DIR = "./data/"
model_pack_path = DATA_DIR + "medmen_wstatus_2021_oct.zip"
cat = CAT.load_model_pack(model_pack_path)
# Test it
text = """NAMR DUMMY, REF BY: DR.DUMMY DUMMY, SAMPLE REPORT
Sample ID | MMG20200057563 Sample Type | Oropharyngeal/Nasopharyngeal_
| Gender | Male Sample Collected On Oct 30, 2020 : 10;00
| Age / DOB 3 | Report Date Oct 30, 2020 : 23:17
| Aadhar Number 1234 5678 9101 Mobile Number 123456789
Referred By Hospital
| Passport Number 123456 ‘Nationality Nie
RT-PCR test for COVID-19 (NOVEL CORONA VIRUS)

Result

| Investigation CT Value Result |
SARS-CoV-2 virus detection (N Gene) Undetermined y Not Detected (Negative)
"""
type_ids_filter = ['T033']
cui_filters = set()
for type_ids in type_ids_filter:
  cui_filters.update(cat.cdb.addl_info['type_id2cuis'][type_ids])
cat.cdb.config.linking['filters']['cuis'] = cui_filters
#print(f"The size of the cdb is now: {len(cui_filters)}")
print("-------------------------------------------------------\n")
doc=cat(text)
for ent in doc.ents:
    print(ent)
print("-------------------------------------------------------\n")
# doc2 = cat(text)
# # Identify the persons
# persons = [ent.text for ent in doc2.ents if ent.label_ == 'PERSON']

# # Return persons
# print(persons)
# Identifying person name, patient ID, Result
nlp = spacy.load("en", disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])

sentence =  """NAME Hitesh Kumar, REF BY: DR.Dummy Dummy, SAMPLE REPORT
Sample ID | MMG20200057563 Sample Type | Oropharyngeal/Nasopharyngeal_
| Gender | Male Sample Collected On Oct 30, 2020 : 10;00
| Age / DOB 3 | Report Date Oct 30, 2020 : 23:17
| Aadhar Number 1234 5678 9101 Mobile Number 123456789"""

doc = nlp(sentence.lower())

print([(X.text,X.label_) for X in doc.ents if X.label_ == 'PERSON'])
#displacy.render(nlp(str(sentence)), jupyter=True, style='ent')
print("-------------------------------------------------------\n")
print([(X.text,X.label_) for X in doc.ents if X.label_ == 'NORP'])
print("-------------------------------------------------------\n")
print([(X.text,X.label_) for X in doc.ents])