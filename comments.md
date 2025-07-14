# General comments
The following comments apply for all py and js files.
1. The code lacks documentation in the form of docstrings and appropriate comments
2. Some variables and functions names are very vague
3. There are chunks of commented code that should be deleted
4. 

# Installation
1. pip can't find numpy==1.21.5 specified in the requiremets.txt file
2. I installed the packages manually with the latest available versions of the libraries, see the requirements_OR.txt file attached

# app.py
## Bugs
1. Page not found when clicking on the Envismetrics title at the top left
2. When uploading the example file to hyd_elec, I get a red cross, I first thought that this was an error, now I see that is a button to delete the file. Is this included in the documentation?
3. In hyd_elec, after loading the file, clicking on the go back or start over buttons do the same.
4. When clicking the choose files button, selecting a file and deleting it, I was not able to upload the same file again. I had to select a different one, delete that one with the cross and then select it again. The same happens with the cyclic voltammetry module and the chronoamperometry module.
5. When uploading the example text file with a different name, hyd_elec does not plot it.
6. Validate all text entries. I wrote a word on a field expecting a number and it broke the server. 
7. Error in the server when trying to upload the test chronoamperogram to the chronoamperogmetry module

## Suggestions
1. Add links to the logos of NJIT and Biosmart so people can visit if interested  

## Questions
1. In hyd_elec, what does HDV-1 mean and why is it there?
2. How does the webapp know what potentiostat the data file is from? Do you need the txt file to be formatted in a specific way? Why are the columns separated by semi colons? The most standardised way would be using commas in either a .txt or .csv.
3. For hyd_elec, can the webapp upload several files? This would be required to construct the koutecky and koutecky-levich plots. Also, how does the webapp know the rotation speed? Does the file need to have a specific name?
4. What happens if I add a file that is not a voltammogram, doesn't follow the naming convention or the specific columns shown in the example data file?
5. What experiment was performed to get the test data file for hyd_elec? Please provide details
6. Why is the folder around 400 MB? It seems excesive to me for a webapp. The data folder is about 250 MB and the .git folder is about 150 MB, this should be cleaned.

## Comments
1. The code lacks comments. The few there seem to be in chinese. It is very difficult to understand what the developers did without any comments to help contributors.
2. Name of functions and variables, quite vague, this is not helpful for contributors. Example: "form1", "form2", "kk"
3. Functions lack docstrings. They should ideally have a short description of what the function does, parameters with their data types, and returns.
4. There are commented blocks of code, please remove

