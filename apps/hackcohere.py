import streamlit as st
import cohere
import pandas as pd
import pdfplumber
import torch
import sys
import googletrans
from googletrans import Translator

# Index page
#page1 = pdf.pages[1]

#@title Get Embeddings helper function
def get_embeddings(co = cohere.Client, model_name = None, texts = None, truncate: str = "RIGHT"):
    output = co.embed(model=model_name, texts=texts, truncate=truncate)
    return output.embeddings

def get_similarity(target = None, candidates = None, top_k = 5):
    # Semantic Similarity
    torchfy = lambda x: torch.as_tensor(x, dtype=torch.float32)
    candidates = torchfy(candidates).transpose(0, 1) # shape (768, bs)
    target = torchfy(target) # shape (1, 768)
    dot_scores = torch.mm(target, candidates)
    
    scores, indices = torch.topk(dot_scores, k=top_k)
    similarity_hits = [{'id': idx, 'score': score} for idx, score in zip(indices[0].tolist(), scores[0].tolist())]

    return similarity_hits

def Semantic_Search(query_text):
    COHERE_API_KEY = "k0y7ovAGZM6Zazty1sx6yFXnhcS9ut0uiSfzkdBo"
    co = cohere.Client(COHERE_API_KEY)

    columns = ['text', 'pg']
    df = pd.DataFrame(columns=columns)

    section_text = ['What you need to know in your first few days',
                    'What you need to know about the Ukrainian Sponsorship Scheme – the Homes for Ukraine Scheme'
        , 'Opening a bank account', 'Claiming Social Security Benefits and getting a National Insurance Number'
        , 'Accessing essential public services', 'Accessing healthcare', 'Finding a job and paying tax'
        , 'Childcare and Education Services', 'Finding accommodation after your sponsorship ends']

    page_num = ['8', '16', '18', '20', '23', '24', '29', '37', '45']

    df['text'] = section_text
    df['pg'] = page_num

    pdf = pdfplumber.open("Ukraine_Welcome_Guide.pdf")

    model_name = 'multilingual-22-12'
    embeddings = get_embeddings(co=co, model_name = model_name, texts = df.text.to_list())

    #query_text = "отримання медичної допомоги" # Getting healthcare
    #[query_text]
    #query_text = "банківський рахунок" # bank account in Ukrainian
    #query_text = st.text_input("Input Query", value="")

    query_embeddings = get_embeddings(co=co, model_name = model_name, texts = [query_text])

    top_k = 1
    similarity_hits = get_similarity(target=query_embeddings, candidates=embeddings, top_k=top_k)

    max_id = similarity_hits[0]['id']
    match_text = df.loc[max_id]['text']
    page_num = int(df.loc[max_id]['pg'])

    query_page = pdf.pages[page_num].extract_text().replace("\n", "")
    t = query_page

    #t.find('2.1: Opening a bank account')

    tstart = t.find(match_text)
    #tend = t.find("18")
    tend = t.find(str(page_num))
    if tstart == -1 or tend == -1:
        sys.exit(0)
    tend += len("tend")-5

    output = t[tstart:tend]

    output = ''.join(output.split(".")[1:])
    
    translator = Translator()
    result = translator.translate(output, src='en', dest='uk')
    #question = translator.translate(query_text, src='uk', dest='en')
    
    #st.write(question.origin)
    st.write(result.text)
    
    #st.write(question.text)
    st.write(result.origin)