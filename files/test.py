import filecmp
import os
def test_output():  
    for i in range(1,4):
        file1 = "act_output "+str(i)+".json"
        file2 = "output.json"
        file3 = "input_"+str(i)+".txt"
        print(file3)
        os.system("python -Wignore extract_name.py --input "+file3)
        if filecmp.cmp(file1, file2):
            print(str(file1)+" is correct")
        else:
            print(str(file1)+" is incorrect")
        print("--------------------------------------------------------------------------------")
  
if __name__ == "__main__":  
    test_output()  
    print("Everything passed")  