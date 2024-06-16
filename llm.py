import sqlite3
import os
import google.generativeai as genai

import ollama

# ollama
def get_stream(st, model):
    stream = ollama.chat(
        model = model,
        messages=st.session_state["messages"],
        stream=True
    )

    for c in stream:
        yield c["message"]["content"]

# google gemini pro with api Key
# =os.getenv("GEMINI_API_KEY")
def GetResponse(question,prompt, api_key):
    genai.configure(api_key=api_key)
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

def Query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    return rows