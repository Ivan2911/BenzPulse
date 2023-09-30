from flask import Flask, render_template, jsonify, redirect, url_for, request
from flask import redirect, url_for
from googlesearch import search
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import openai
from datetime import datetime

app = Flask(__name__)

# Initialize the OpenAI API (replace "YOUR-API-KEY" with your actual API key)
openai.api_key = "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"

today = datetime.now().date()

message = {
    "role": "system",
    "content": "You are a supply chain expert that work for the best automtive company in the world and helpful assistant."
}

def fetch_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Your code to fetch the article text
    paragraphs = soup.find_all('p')
    article_text = ' '.join([p.text for p in paragraphs])
    
    # Hypothetical code to fetch the article date
    # The actual tag and class will depend on how the date is stored on the website
    date_tag = soup.find('span', {'class': 'article-date'})
    if date_tag:
        article_date = date_tag.text
    else:
        article_date = "No date found"  # Default to current date if not available
    return article_text, article_date

def assess_reliability(url):
    domain = urlparse(url).netloc
    user_message = {
        "role": "user",
        "content": f"Very short and do in one sentence on how reliable is the source {domain}?"
    }
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[message, user_message]
    )
    source_reliability = response['choices'][0]['message']['content']
    return source_reliability

queries = ["current trade wars news",
           "last major strikes announced",
           "hurricane forecasts",
           "major factory closures today",
           "recent major cyberattacks",
           "new trade regulations announced",
           "major port closures news",
           "transportation strikes today",
           "infrastructure failure alerts",
           "transportation strikes today",
           "political unrest and protests today",
           "common car complaints this month",
           "top reported car problems this year",
           "car forums top issues discussed",
           "potential car recalls announced",
           "precautionary vehicle model pullbacks",
           "major car brands recall alerts"
           ]

@app.route('/')
def home():
    return render_template('index.html', queries=queries, summaries=[])


@app.route('/submit_query', methods=['POST'])
def submit_query():
    query = request.form.get('query')
    return redirect(url_for('get_summaries', query=query))

@app.route('/get_summaries', methods=['GET'])
def get_summaries():
    # Retrieve the query from URL parameters
    query = request.args.get('query', "major strikes announced today")  # Default search term if none is provided

    search_terms = [query]  # Use the selected query as the search term

    summaries = []

    for term in search_terms:
        urls = [result for result in search(term, num_results=1)]

        for url in urls[1:2]: # use the last url as its the final news
            article_text, article_date = fetch_article(url)
            if article_date is None:
                article_date = "===="
            source_reliability = assess_reliability(url)
            
            #Summary
            user_message = {
                "role": "user",
                "content": f"Please summarize the following article based on the provided excerpt:{article_text[:500]}"
            }
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[message, user_message]
            )
            summary = response['choices'][0]['message']['content']
            
            # For Impact Analysis
            user_message_impact = {
                "role": "user",
                "content": f"If the news summary provided contains relevant information about Mercedes, please analyze and provide key points about its potential impact on Mercedes. Based on the summary, how relevant is this news as of {today}? If no relevant information is found, please refrain from providing an analysis. News: {summary}"

            }
            response_impact = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[message, user_message_impact]
            )
            impact_analysis = response_impact['choices'][0]['message']['content']

            # For Recommended Action
            user_message_action = {
                "role": "user",
                "content": f"If the news has a high likelihood of impacting Mercedes-Benz, provide actionable key points detailing short-term and long-term actions Mercedes-Benz should take in response. If no major impacts, state: 'No risks expected: {summary}'. Highlight any expected risks or impacts."
            }
            response_action = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[message, user_message_action]
            )
            detailed_recommended_action = response_action['choices'][0]['message']['content']

            summaries.append({
                "url": url,
                "reliability": source_reliability,
                "summary": summary,
                "impact": impact_analysis,
                "recommendation": detailed_recommended_action,
                "date": article_date  # add date information
            })
    
    return render_template('index.html', summaries=summaries, queries=queries)

if __name__ == '__main__':
    app.run(debug=True)




