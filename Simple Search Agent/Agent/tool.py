from typing import Annotated
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

@tool
def search_web(query:str)->str:
    """Search the web using the DuckDuckGo to find the information or relevent links."""
    search = DuckDuckGoSearchRun()
    return search.run(query)

@tool
def scrape_and_analyze(company_name:str)->str:
    """Generate the serch query for a company's IT services,find URLs,
    and extract text content from the first available website."""
    keywords = ["IT Services", "managed IT", "technology solutions"]
    queries = [f"{company_name} {keyword}" for keyword in keywords]
    
    search = DuckDuckGoSearchRun()
    results = []
    
    for query in queries:
        search_results = search.run(query)
        urls = re.findall(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            search_results
        )
        
        if urls:
            target_url = urls[0]
            try:
                response = requests.get(target_url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "html.parser")
                text = soup.get_text(separator=" ", strip=True)
                text = re.sub(r'\s+', ' ', text)
                results.append(f"[Source: {target_url}] {text[:2000]}")
            except Exception as e:
                results.append(f"Failed scraping {target_url}: {e}")
    
    return "\n\n".join(results) if results else "No relevant information found."

@tool
def save_to_file(data:str,filename:str="leads_output.txt")->str:
    """Saves formatted text or structured lead insights securely to a text file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Leads Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}!"

all_tools = [search_web, scrape_and_analyze, save_to_file]