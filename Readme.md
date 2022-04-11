# Running the Feature Extracter code
***
1. Create a virtual enviroment with python version 3.8
 * Step-1: Install virtualenv, and pyenv
 * Step-2: download python version 3.8.0 using pyenv
 * Step-3:virtualenv -p ~/.pyenv/versions/3.8.0/bin/python ./new_env,
 * Step-4:. ./new_env/bin/activate
2. Install Medcat using :- pip install medcat==1.2.7
3. Install the Medcat model using :- 
!wget https://medcat.rosalind.kcl.ac.uk/media/medmen_wstatus_2021_oct.zip -P ./data/
>(this will load the model in to the data folder)
4. Install spacy using :- 
 * pip install pymupdf
 * python -m spacy download en_core_web_md
 * pip install spacy-langdetect
5. cd to the files folder and Run "python extract_names.py" 
## Testing Multiple reports
Add multiple input files and the actual output files into the files folder.
Running the script " python test.py ", will run the program on multiple input files and checks wether the input and the output files match
