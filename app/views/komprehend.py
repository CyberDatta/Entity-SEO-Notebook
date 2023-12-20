import paralleldots as plds
from tkinter import *
import pandas as pd
import home
import requests
from bs4 import BeautifulSoup
import json
import os


def url2text(url_input):
    response = requests.get(url_input)
    if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text_output=""
        for paragraph in paragraphs:
            text_output=text_output + paragraph.get_text()
        return text_output
    return "error"


def change_komprehend_key(new_key):
    # Get the current working directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the directory and file name
    json_file_path = os.path.join(current_directory, 'data/keys.json')

# Read data from the JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

# Modify the data (for example, adding a new key-value pair)
    data['komprehend']['key'] = new_key

# Write the modified data back to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def read_komprehend_key():
# Get the current working directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the directory and file name
    json_file_path = os.path.join(current_directory, 'data/keys.json')

# Read data from the JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

# Modify the data (for example, adding a new key-value pair)
    return data['komprehend']['key']

def request_komprehend(main_input,entity_flag,keyword_flag,name,input_type_flag):
    plds.set_api_key(read_komprehend_key())

    #sort desired sections of response into arrays
    entities_array=[]
    categories_array=[]
    keyword_array=[]

    if(input_type_flag==0):
        main_input=url2text(main_input)

    if(entity_flag==1):
        response_entities= plds.ner(main_input)
        for entity in response_entities['entities']:
            entities_array.append(entity['name'])
            categories_array.append(entity['category'])

    if(keyword_flag==1):
        response_keywords=plds.keywords(main_input)
        for keyword_dict in response_keywords['keywords']:
            keyword_array.append(keyword_dict['keyword'])

    # insert arrays into an excel spreadsheet
# Determine the maximum length of the lists
    max_length = max(len(entities_array), len(categories_array), len(keyword_array))

# Pad the shorter lists with NaN values to match the maximum length
    entities_array += [pd.NaT] * (max_length - len(entities_array))
    categories_array += [pd.NaT] * (max_length - len(categories_array))
    keyword_array += [pd.NaT] * (max_length - len(keyword_array))

# Create a DataFrame from the lists
    df = pd.DataFrame({'Entities': entities_array, 'Category of Entity': categories_array, 'Keywords': keyword_array})

    excel_file_path=name +'.xlsx'
    df.to_excel(excel_file_path, index=False)

def openkeywindow(source):
    #  destroy the previous window
    if(source!="null"):
        source.destroy()
    #open a new window
    global keychange_window
    keychange_window=Tk()
    keychange_window.title("Change Komprehend API Key")

    #go back to the text razor window
    back_button=Button(keychange_window,text="Back",command=lambda: openwindow(keychange_window))
    back_button.grid(row=0,column=0)

    #input field for new api key
    keychange_label=Label(keychange_window,text="Insert input here: ")
    keychange_label.grid(row=1,column=0)

    key_input=Entry(keychange_window)
    key_input.grid(row=1, column=1)

    #submit button to change key
    submit_button=Button(keychange_window,text="Submit",command=lambda: change_komprehend_key(key_input.get()))
    submit_button.grid(row=2,column=0)

    keychange_window.mainloop()

#function to open the komprehend window
def openwindow(source):
    # destroy the previous window
    if(source!="null"):
            source.destroy()

    # open a new window
    global api_window
    api_window = Tk()
    api_window.title("Komprehend")

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
    url_label=Label(api_window,text="Insert TEXT input here: ")
    url_label.grid(row=2,column=0)

    main_input=Entry(api_window)
    main_input.grid(row=2, column=1)

    # Checkbutton for entities and noun phrasess
    filter_label=Label(api_window,text="choose fields to display: ")
    filter_label.grid(row=3,column=0)

    entity_flag=IntVar()
    filter_option_entities=Checkbutton(api_window,text="Entities with Category",variable=entity_flag)
    filter_option_entities.grid(row=3,column=1)
    
    keyword_flag=IntVar()
    filter_option_phrase=Checkbutton(api_window,text="Keywords",variable=keyword_flag)
    filter_option_phrase.grid(row=3,column=2)

    #input window to choose desired name
    name_label=Label(api_window,text="Provide file name: ")
    name_label.grid(row=4,column=0)

    name=Entry(api_window)
    name.insert(END,"Komprehend_NLP_Analysis")
    name.grid(row=4, column=1)

    #button to submit api request to text razor
    submit_Button=Button(api_window,text="Submit",command=lambda: request_komprehend(main_input.get(),entity_flag.get(),keyword_flag.get(),name.get(),input_type_flag.get()))
    submit_Button.grid(row=5,column=0)

   #button to change api key
    Key_Change_Button=Button(api_window,text="Change API key",command=lambda: openkeywindow(api_window))
    Key_Change_Button.grid(row=6,column=0)

    api_window.mainloop()

if __name__ == '__main__':
    openwindow("null")
