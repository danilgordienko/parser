import requests
from bs4 import BeautifulSoup as BS
from supabase import create_client, Client


def getData():
    data = {}
    r = requests.get("https://db.chgk.info/random")
    html = BS(r.content, 'html.parser')
    for el in html.select(".random-results"):
        allQ = el.find_all(class_="random_question")
        for q in allQ:
            if (q.find('strong').findNext().get('class') != ['collapsible', 'collapsed']):
                continue
            c = q.find(class_="collapsible")
            question = c.previous_element
            answer = c.find("p").find("strong").next_element.next_element
            data[question] = answer
    return data

url: str = "https://eughueucuzinthtorkyt.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV1Z2h1ZXVjdXppbnRodG9ya3l0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDA0ODQ2NDcsImV4cCI6MjAxNjA2MDY0N30.1IXKCtjMpNB0DJ2_ZBixn59MSr7mlxVeebTSYHjzlFY"
supabase: Client = create_client(url, key)

for i in range(1, 16):
    data = getData()
    for key, value in data.items():
        answer = supabase.from_('questions').select('question').eq('question', key).execute()
        if len(answer.data) == 0:
            supabase.table('questions').insert({"question": key, "answer": value}).execute()
