from urllib.parse import urlparse, parse_qs
import requests
import dotenv
import sys
import os

dotenv.load_dotenv()

def get_scholar_author_info(author_id, api_key=os.environ['api_key']):
    url = f"https://serpapi.com/search.json?engine=google_scholar_author&author_id={author_id}&hl=en&api_key={api_key}"
    response = requests.get(url)
    return response.json()

def get_citation(cite_id, api_key=os.environ['api_key']):
    url = f"https://serpapi.com/search.json?engine=google_scholar_author&view_op=view_citation&citation_id={cite_id}&api_key={api_key}"
    response = requests.get(url)
    return response.json()

def format_dict(dictionary):
    formatted_str = '\n'.join(f'{key}: {value}' for key, value in dictionary.items())
    return formatted_str

def write_to(filename, string):
    with open(filename, 'w+') as file:
        file.write(string)

def extract(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    user_id = query_params.get("user", [None])[0]

    details = get_scholar_author_info(user_id)

    author_details = dict()
    author_details['Name'] = details['author']['name']
    author_details['Affliation'] = details['author']['affiliations']

    ids = [cite['citation_id'] for cite in details['articles']]
    publications = []
    titles = set()

    for id in ids:
        result = get_citation(id)['citation']

        publication = dict()
        publication['Title'] = result['title']
        
        if publication['Title'] in titles:
            continue
        titles.add(publication['Title'])

        try:
            publication['Publication Date'] = result['publication_date']
        except KeyError:
            pass

        try:
            publication['Authors'] = result['authors']
        except KeyError:
            pass

        try:
            publication['Abstract'] = result['description']
        except KeyError:
            pass

        try:
            publication['URL Link'] = result['link']
        except KeyError:
            pass

        publications.append(publication)

    write_to('AUTHOR.txt', author_details['Name'])
    write_to('DATA.txt', "\n\n".join(map(format_dict, publications)))

if __name__ == '__main__':
    args = sys.argv
    if len(args)!=2: 
        raise Exception("Please pass Google Scholar URL as an arguement in \"\"")
    url = args[1]
    extract(url)