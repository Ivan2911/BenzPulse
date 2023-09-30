from flask import Flask, render_template, jsonify
from googlesearch import search
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import openai

#app = Flask(__name__)

# Initialize the OpenAI API (replace "YOUR-API-KEY" with your actual API key)
openai.api_key = "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"


def fetch_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    article_text = ' '.join([p.text for p in paragraphs])
    return article_text


def assess_reliability(url):
    domain = urlparse(url).netloc
    prompt_for_reliability = f"How reliable is the source {domain}?"
    api_response_reliability = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt_for_reliability,
        max_tokens=50
    )
    source_reliability = api_response_reliability['choices'][0]['text']
    return source_reliability


#@app.route('/get_summaries', methods=['GET'])
def get_summaries():
    search_terms = ["automotive supply chain disruption"]
    summaries = []

    for term in search_terms:
        urls = [result for result in search(term, num_results=2)]

        for url in urls:
            article_text = fetch_article(url)
            source_reliability = assess_reliability(url)
            prompt_for_summary = f"Please summarize the following article about {term}:\n{article_text[:500]}"
            api_response_summary = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt_for_summary,
                max_tokens=50
            )

            prompt_for_summary = f"Please analyze and summarize the relevance and content of the following article concerning {term}:\n{article_text[:500]}"
            api_response_summary = openai.create_completion(
                engine="text-davinci-002",
                prompt=prompt_for_summary,
                max_tokens=50
            )
            summary = api_response_summary['choices'][0]['text']
            
            prompt_for_impact = f"How could the following news potentially impact Mercedes-Benz, consider the time of impact also? {summary}"
            api_response_impact = openai.create_completion(
                engine="text-davinci-002",
                prompt=prompt_for_impact,
                max_tokens=50
            )
            impact_analysis = api_response_impact['choices'][0]['text']

            prompt_for_action = f"What detailed short-term and long-term actions should Mercedes-Benz consider taking in response to this news? {summary}"
            api_response_action = openai.create_completion(
                engine="text-davinci-002",
                prompt=prompt_for_action,
                max_tokens=200
            )
            detailed_recommended_action = api_response_action['choices'][0]['text']
            
            summaries.append({
                "url": url,
                "reliability": source_reliability,
                "summary": summary,
                "impact": impact_analysis,
                "recommendation": detailed_recommended_action
            })

    return render_template('index.html', summaries=summaries)

#if __name__ == '__main__':
    #app.run(debug=True)




search_terms = ["automotive supply chain disruption"]
summaries = []



for term in search_terms:
        urls = [result for result in search(term, num_results=1)]

        for url in urls:
            article_text = fetch_article(url)
            source_reliability = assess_reliability(url)
            prompt_for_summary = f"Please summarize the following article about {term}:\n{article_text[:500]}"
            api_response_summary = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt_for_summary,
                max_tokens=50
            )

            prompt_for_summary = f"Please analyze and summarize the relevance and content of the following article concerning {term}:\n{article_text[:500]}"
            api_response_summary = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt_for_summary,
                max_tokens=50
            )
            summary = api_response_summary['choices'][0]['text']
            
            prompt_for_impact = f"How could the following news potentially impact Mercedes-Benz, consider the time of impact also? {summary}"
            api_response_impact = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt_for_impact,
                max_tokens=50
            )
            impact_analysis = api_response_impact['choices'][0]['text']

            prompt_for_action = f"What detailed short-term and long-term actions should Mercedes-Benz consider taking in response to this news? {summary}"
            api_response_action = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt_for_action,
                max_tokens=200
            )
            detailed_recommended_action = api_response_action['choices'][0]['text']
            
            summaries.append({
                "url": url,
                "reliability": source_reliability,
                "summary": summary,
                "impact": impact_analysis,
                "recommendation": detailed_recommended_action
            })


print(summaries)