from django.shortcuts import render
from django.http import HttpResponse
from openai import OpenAI
import requests
from bs4 import BeautifulSoup 
import string
import csv



client = OpenAI()#API key removed

# Create your views here.
def home(request):
    return render(request, 'homepage.html')

def about(request):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a sports analyis and write articles about player stats"},
        {"role": "user", "content": "Write me an about page for the website"}
    ]
    )
    response = completion.choices[0].message.content
    return render(request, 'response.html', {'response': response})

def testing_summaries(request):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a sports analyis and write articles about player stats"},
        {"role": "user", "content": "Write player summaries for the top players in the MLB. \
        Send response in html format that will look nice on the webpage. Only display text, dont choose colors, \
            dont choose title"}
    ]
    )
    response = completion.choices[0].message.content
    return render(request, 'test_sum.html', {'response': response})

def scrape_data(request):
    r = requests.get('https://www.baseball-reference.com/leagues/') 
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('div', id = 'div_leagues_active')
    contents = s.find_all('td') 
    grouped_data = []
    for i in range(0, len(contents), 3):
        data_dict = {
            'League': contents[i].text,
            'Champion': contents[i + 1].text,
            'MVP': contents[i + 2].text,
        }
        grouped_data.append(data_dict)
    
    user_message = " "
    for data in grouped_data:
        user_message += f"{data['League']} champion: {data['Champion']}, MVP: {data['MVP']}\n"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a sports anylist who writes papers for a sports magazine. \
                write a few paragraphs (not a list) about some interesting things in the data. you will be provided a list like string where \
                the first value is the league, the second value is the team who won the AL/NL chapionship and the \
                player who won mvp that season. Players are not on the associated with the teams who \
                won mvp that season. response should be in hml format"},
            {"role": "user", "content": user_message}
        ]
    )
    response = completion.choices[0].message.content
    return render(request, 'scrapedData.html', {'response': response})
    
    # uncomment to get mlb data
    # return render(request, 'scrapedData.html', {'response': grouped_data})

    # uncomment to send data to csv file
    # filename = 'WSHistory.csv'
    # with open(filename, 'w', newline="") as f:
    #     w = csv.DictWriter(f, ['League', 'Champion', 'MVP'])
    #     w.writeheader()
    #     w.writerows(grouped_data)







