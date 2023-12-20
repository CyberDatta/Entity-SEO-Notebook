from tkinter import *
import textrazor
import pandas as pd
import home 
import json
import os

def change_textrazor_key(new_key):
    # Get the current working directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the directory and file name
    json_file_path = os.path.join(current_directory, 'data/keys.json')

# Read data from the JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

# Modify the data (for example, adding a new key-value pair)
    data['text_razor']['key'] = new_key

# Write the modified data back to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def read_textrazor_key():
# Get the current working directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the directory and file name
    json_file_path = os.path.join(current_directory, 'data/keys.json')

# Read data from the JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

# Modify the data (for example, adding a new key-value pair)
    return data['text_razor']['key']

def request_textrazor(main_input,entity_flag,phrase_flag,input_type_flag,name):
    #check if params are of correct type
    # print(url)
    # print(entity_flag)
    # print(phrase_flag)

    #hardcoded authentication
    # textrazor.api_key = "6209fb60849a4e5637a72d77a9f9757ece1f96fca958ab5de1e8ccb7"
    textrazor.api_key=read_textrazor_key()

    #build request with desired data (entities and noun phrases)
    filters=[]
    if(entity_flag==1):
        filters.append("entities")
    if(phrase_flag==1):
        filters.append("phrases")
        filters.append("words")
    client = textrazor.TextRazor(extractors=filters)

    #get and handle the response object by selecting appropriate input types used
    if(input_type_flag==0):
        response = client.analyze_url(main_input)
    else:
        response = client.analyze(main_input)

    #sort desired sections of response into arrays
    entities_array=[]
    nounphrase_array=[]
    if(entity_flag==1):
        for entity in response.entities():
            entities_array.append(entity.id)
    if(phrase_flag==1):
        for phrase in response.noun_phrases():
            nounphrase=""
            for words in phrase.words:
                nounphrase=nounphrase + words.token + " "
            nounphrase_array.append(nounphrase)

    # manipulate the arrays so that they can be stored in a dataframe, Pad the shorter list with NaN values to match the maximum length
    max_length = max(len(entities_array), len(nounphrase_array))
    entities_array += [pd.NaT] * (max_length - len(entities_array))
    nounphrase_array += [pd.NaT] * (max_length - len(nounphrase_array))
    df=pd.DataFrame({"Entities":entities_array,"Noun Phrases":nounphrase_array})
    
    excel_file_path=name +'.xlsx'
    df.to_excel(excel_file_path, index=False)


def openkeywindow(source):
    #  destroy the previous window
    if(source!="null"):
        source.destroy()
    #open a new window
    global keychange_window
    keychange_window=Tk()
    keychange_window.title("Change Text Razor API Key")

    #go back to the text razor window
    back_button=Button(keychange_window,text="Back",command=lambda: openwindow(keychange_window))
    back_button.grid(row=0,column=0)

    #input field for new api key
    keychange_label=Label(keychange_window,text="Insert input here: ")
    keychange_label.grid(row=1,column=0)

    key_input=Entry(keychange_window)
    key_input.grid(row=1, column=1)

    #submit button to change key
    submit_button=Button(keychange_window,text="Submit",command=lambda: change_textrazor_key(key_input.get()))
    submit_button.grid(row=2,column=0)

    keychange_window.mainloop()

def openwindow(source):
    # destroy the previous window
    if(source!="null"):
        source.destroy()

    # open a new window
    global api_window
    api_window = Tk()
    api_window.title("Textrazor")

    # create a button to return to home
    back_button=Button(api_window,text="Back",command=lambda: home.home_window(api_window))
    back_button.grid(row=0,column=0)

    # radio button between text input or url input
    input_label=Label(api_window,text="Choose Input Format:")
    input_label.grid(row=1,column=0)
    
    input_type_flag=IntVar()
    URL_option_phrase= Radiobutton(api_window,text="URL",variable=input_type_flag,value=0)
    URL_option_phrase.grid(row=1,column=1)     
    
    TEXT_option_phrase=Radiobutton(api_window,text="TEXT",variable=input_type_flag,value=1)
    TEXT_option_phrase.grid(row=1,column=2) 

    #input window for url or text
    url_label=Label(api_window,text="Insert input here: ")
    url_label.grid(row=2,column=0)

    main_input=Entry(api_window)
    main_input.grid(row=2, column=1)

    # Checkbutton for entities and noun phrasess
    filter_label=Label(api_window,text="choose fields to display: ")
    filter_label.grid(row=3,column=0)

    entity_flag=IntVar()
    filter_option_entities=Checkbutton(api_window,text="Entities",variable=entity_flag)
    filter_option_entities.grid(row=3,column=1)
    
    phrase_flag=IntVar()
    filter_option_phrase=Checkbutton(api_window,text="Noun-Phrases",variable=phrase_flag)
    filter_option_phrase.grid(row=3,column=2)

    #input window to choose desired name

    name_label=Label(api_window,text="Provide file location")
    name_label.grid(row=4,column=0)

    name=Entry(api_window)
    name.insert(END,"TextRazor_NLP_Analysis")
    name.grid(row=4, column=1)

    #button to submit api request to text razor
    submit_Button=Button(api_window,text="Submit",command=lambda: request_textrazor(main_input.get(),entity_flag.get(),phrase_flag.get(),input_type_flag.get(),name.get()))
    submit_Button.grid(row=5,column=0)

    #button to change api key
    Key_Change_Button=Button(api_window,text="Change API key",command=lambda: openkeywindow(api_window))
    Key_Change_Button.grid(row=6,column=0)

    api_window.mainloop()
    
if __name__ == '__main__':
    openwindow("null")