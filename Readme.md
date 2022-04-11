# Running the Feature Extracter code
***
1. Create a virtual enviroment with python version 3.8
<br>
'''
(
<br>
 * Step-1: Install virtualenv, and pyenv
<br>
 * Step-2: download python version 3.8.0 using pyenv
<br>
 * Step-3:virtualenv -p ~/.pyenv/versions/3.8.0/bin/python ./new_env,
<br>
 * Step-4:. ./new_env/bin/activate
 <br>
 )
 '''
<br>
2. Install Medcat using :- pip install medcat==1.2.7
<br>
3. Install the Medcat model using :- 
<br>
!wget https://medcat.rosalind.kcl.ac.uk/media/medmen_wstatus_2021_oct.zip -P ./data/
<br>
(this will load the model in to the data folder)
<br>
4. Install spacy using :- 
<br>
                         pip install pymupdf
                         <br>
                         python -m spacy download en_core_web_md
                         <br>
                         pip install spacy-langdetect
<br>
5. cd to the files folder and Run "python extract_names.py" 
