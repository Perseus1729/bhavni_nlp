from medcat.cat import CAT
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector
from collections import defaultdict
import re
import json 

@Language.factory("language_detector")
def get_lang_detector(nlp, name):
   return LanguageDetector()

# Download the model_pack from the models section in the github repo.
DATA_DIR = "../data/"
model_pack_path = DATA_DIR + "medmen_wstatus_2021_oct.zip"
cat = CAT.load_model_pack(model_pack_path)
print("--------------------------------------")
# Test it
# text = """NAME Sandhya, REF BY: DR.DUMMY DUMMY, SAMPLE REPORT
# Sample ID | MMG20200057563 Sample Type | Oropharyngeal/Nasopharyngeal_
# | Gender | Male Sample Collected On Oct 30, 2020 : 10;00
# | Age / DOB 3 | Report Date Oct 30, 2020 : 23:17
# | Aadhar Number 1234 5678 9101 Mobile Number 123456789
# Referred By Hospital
# | Passport Number 123456 ‘Nationality Nie
# RT-PCR test for COVID-19 (NOVEL CORONA VIRUS)

# Result

# | Investigation CT Value Result |
# SARS-CoV-2 virus detection (N Gene) Undetermined y  (Positive)
# """
keys = []
values = []
with open('input.txt', 'r') as file:
    text = file.read().replace('\n', '')
type_ids_filter = ['T033']
cui_filters = set()
for type_ids in type_ids_filter:
  cui_filters.update(cat.cdb.addl_info['type_id2cuis'][type_ids])
cat.cdb.config.linking['filters']['cuis'] = cui_filters
doc=cat(text)
idx=0
for ent in doc.ents:
    if str(ent)!="detection":
        keys.append('Covid-Result')
        values.append(str(ent))
    print(ent)
doc2 = cat(text)
#print(f"The size of the cdb is now: {len(cui_filters)}")
print("--------------------------------------")

nlp = spacy.load('en_core_web_md')
# temp_data = {
#     "DATE": ["Jan 10, 1197", "Mar 24, 1020", "Jun 17, 29"],
#     "PERSON": ["Hitesh", "Janie", "Suresh","Mike","Harvey"]
# }

# nlp.add_pipe("concise_concepts", config={"data":temp_data,"ent_score": True})
text1= nlp(text)
for w in text1.ents:
    if w.label_=='DATE':
        keys.append('DATE')
        values.append(w.text)
        print(w.text)
        break
print("--------------------------------------")
text2 = nlp(text)
for w in text2.ents:
  if w.label_=='PERSON':
    keys.append('PERSON')
    values.append(w.text)
    print(w.text)
    break
print("--------------------------------------")

# (beams, somethingelse) = nlp.entity.beam_parse([ doc ], beam_width = 16, beam_density = 0.0001)

# # beams = nlp.entity.beam_parse([ text1 ], beam_width = 16, beam_density = 0.001)
# entity_scores = defaultdict(float)
# for beam in beams:
#   for score, ents in nlp.entity.moves.get_beam_parses(beam):
#       for start, end, label in ents:
#         entity_scores[(start, label)] += score
# threshold = 0.2
# for key in entity_scores:
#   start, label = key
#   score = entity_scores[key]
#   if score > threshold:
#       print ('Label: {}, text:{}, Confidencelevel: {}'.format(label, text1[start: start+1], score))
# print("--------------------------------------")
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
jsonFile = open("output.json", "w")
jsonFile.write(json_object)
jsonFile.close()
print(json_object)
print("--------------------------------------")
# Valid_data= [ text, { "entities": [ [ 5, 12, "PERSON" ] ] } ]
# # examples = []
# # for text, annots in Valid_data:
# #     predicted=nlp(text)
# #     example=Example.from_dict(predicted, annots)
# #     examples.append(example)
# # scorer = Scorer()
# # scorer.score(examples)
# def evaluate(ner_model, examples):
#   scorer = Scorer()
#   example = []
#   for input_, annot in examples:
#     pred = ner_model(input_)
#     temp = Example.from_dict(pred, annot)
#     example.append(temp)
#     scores = scorer.score(example)
#   return scores
# results = evaluate(nlp, Valid_data)
# print(results)
# # Calculate sample size
# from collections import Counter
# ent = []
# for x in text:
#   ent += [i[-1] for i in x[1]['entities']]
# print(Counter(ent))
# print("--------------------------------------")
# # Construction via add_pipe with custom model
# config = {"model": {"@architectures": "my_spancat"}}
# # parser = nlp.add_pipe("spancat", config=config)

# # Construction from class
# spancat = nlp.add_pipe("spancat")
# scores = spancat.predict(text1)
# spancat.set_annotations(text1, scores)
# print(scores)
# print("--------------------------------------")
nlp.add_pipe('language_detector', last=True)
doc = nlp(text)
print(doc._.language)
print("--------------------------------------")
