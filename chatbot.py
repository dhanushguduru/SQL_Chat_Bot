from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from streamlit_option_menu import option_menu

from db import CreateDataBase
from prompt import LLM_PROMPT
from llm import *



## Streamlit App
selected = option_menu(
    menu_title=None,
    options=["SQL LLM", "Create DataBase"],
    icons=["chat-square-text-fill", "database-add"],
    default_index=0,
    menu_icon="cast",
    orientation="horizontal",
    # styles={
    #         "container": {"padding": "0!important", "background-color": "#fafafa"},
    #         "icon": {"color": "orange", "font-size": "25px"},
    #         "nav-link": {
    #             "font-size": "25px",
    #             "text-align": "left",
    #             "margin": "0px",
    #             "--hover-color": "#eee",
    #         },
    #         "nav-link-selected": {"background-color": "green"},
    #         },
)

# Sql Chat Bot
if selected == "SQL LLM":
    st.header(":blue[Chat With DataBase]")

    col1,col2 = st.columns(2)

    database_path = col1.file_uploader("Upload DataBase", type=["db"])

    css = '''
    <style>
        [data-testid='stFileUploader'] {
            width: max-content;
        }
        [data-testid='stFileUploader'] section {
            padding: 0;
            float: left;
        }
        [data-testid='stFileUploader'] section > input + div {
            display: none;
        }
        [data-testid='stFileUploader'] section + div {
            float: right;
            padding-top: 0;
        }

    </style>
    '''
    col1.markdown(css, unsafe_allow_html=True)

    option = col2.selectbox('Select The Model',('Gemini Pro', 'llama3', 'llama2', "tinyllama"), index=None)

    if option == "Gemini Pro":
        api_key = st.text_input("Enter The API Key: ",key="API Key")

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content" : "How May I Assist You?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input('Please type your message here')

    if user_input:
        st.session_state.messages.append({"role":"user", "content":user_input})
        
        with st.chat_message("user"):
            st.write(user_input)

        if option == "Gemini Pro":
            try:
                response=GetResponse(user_input, LLM_PROMPT, api_key)
                response=Query(response, "database/" + database_path.name)
                
            except:
                response= [["Unable Find The Solution, please try another question"]]

            with st.chat_message("assistant"):
                for row in response:
                    st.session_state.messages.append({"role":"assistant", "content":row[0]})
                    st.write(row[0])

        else:
            response = get_stream(st, option)
            with st.chat_message("assistant"):
                with st.status(label="Generating...", expanded=True) as status:
                    st.write_stream(response)
                    st.session_state.messages.append({"role":"assistant", "content":response})
                    status.update(label="Here is Your Answer", state="complete")

# Create DataBase
if selected == "Create DataBase":
    st.header(":blue[Create DataBase]")
    with st.form(key='Create DataBase'):
        db_name = st.text_input("Data Base Name: ",key="DB Name")
        table_name = st.text_input("Table Name: ",key="Table Name")
        file = st.file_uploader("Upload Data", type=["csv", "xlsx"])
        submit_button = st.form_submit_button(label='Create DataBase')

    if submit_button:
        if not db_name.endswith(".db"):
            name = "database/" + db_name + ".db"
        else:
            name = "database/" + db_name

        file_type = file.name.split(".")[-1]
        if file_type == "csv":
            CreateDataBase.loadCsv(file, table_name, name)
        if file_type == "xlsx":
            CreateDataBase.loadExcel(file, table_name, name)

        st.write("Table Name is : ", table_name)
        st.write("Data Base Created At : ", name)

