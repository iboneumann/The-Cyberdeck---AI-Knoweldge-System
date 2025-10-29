+++
date = '2025-10-25T08:42:47+02:00'
draft = false
title = "Ggooglesearch.py script"
weight = 15
+++

### The Updated googlesearch.py script

The manual

googlesearch.py
python3 googlesearch.py "alphabetical linux terminal command list" \
    --search-results 500 \
    --analyze-domains 15 \
    --model llama3 \
    --max-content 40000 \
    --max-analysis 20000 \
    --delay 1 \
    --api-key 	"Your API Key"

--load-analysis
python3 googlesearch.py "free chemistry lessons" --search-results 100
python3 googlesearch.py \
 --load-analysis analysis_free_chemistry_20241201_123456.json

💾 Chat session saved to: search_results /chat
_session_linux_terminal_commands_20240515_1423.json
search_results/analysis_[query]_[timestamp].md
search_results/chat_[query]_[timestamp].md

Command-line Arguments:
Argument	    Description	                        Default
query	        Google search query (required)	         -
--num-results	Number of results to analyze	           5
--api-key	SerpAPI key (uses SERPAPI_KEY env var if not specified)	
Environment variable
--model	        Ollama model to use	                llama3
--max-content	Max characters to extract from websites	5000
--max-analysis	Max characters to send to Ollama	3000
--delay	        Delay between website fetches (seconds)	   2


python3 googlesearch.py "alphabetical linux terminal command list" \
    --search-results 50 \
    --analyze-domains 5 \

python3 googlesearch.py "alphabetical linux terminal command list" \
    --no-chat
    --list-only

```batch
import argparse
import requests
from bs4 import BeautifulSoup
import ollama
import time
import os
import textwrap
import tldextract
from collections import OrderedDict
import sys
import re
import datetime
import readline  # For better shell input experience
import json
import html
import shutil

def google_search(query, num_results, api_key):
    """Fetch multiple pages of Google search results using SerpAPI"""
    all_results = []
    results_per_page = 10
    pages = (num_results // results_per_page) + (1 if num_results % 
results_per_page else 0)
    
    for page in range(pages):
        params = {
            'q': query,
            'api_key': api_key,
            'num': results_per_page,
            'start': page * results_per_page
        }
        try:
            response = requests.get('https://serpapi.com/search', 
params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('organic_results'):
                break
                
            all_results.extend(data['organic_results'])
            
            if len(all_results) >= num_results:
                break
                
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Google search error: {str(e)}")
            break
    
    return all_results[:num_results]

def extract_base_domains(results):
    """Extract unique base domains from search results"""
    domain_map = OrderedDict()
    extractor = tldextract.TLDExtract()
    
    for result in results:
        url = result.get('link', '')
        if not url:
            continue
            
        try:
            parsed = extractor(url)
            if not parsed.suffix:
                continue
                
            base_domain = f"{parsed.domain}.{parsed.suffix}"
            
            if base_domain not in domain_map:
                domain_map[base_domain] = {
                    'domain': base_domain,
                    'url': url,
                    'snippet': result.get('snippet', ''),
                    'occurrences': 1
                }
            else:
                domain_map[base_domain]['occurrences'] += 1
        except Exception as e:
            print(f"⚠️ Domain extraction error for {url}: {str(e)}")
    
    # Add numbering
    for idx, domain_data in enumerate(domain_map.values(), 1):
        domain_data['number'] = idx
    
    return list(domain_map.values())

def fetch_website_content(url, max_length):
    """Fetch main text content from a webpage"""
    try:
        response = requests.get(url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) 
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        })
        response.raise_for_status()
        
        # Check content type
        content_type = response.headers.get('Content-Type', '').lower()
        if 'html' not in content_type:
            return f"🚫 Non-HTML content: {content_type}"
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unnecessary elements
        for element in soup(['script', 'style', 'header', 'footer', 'nav', 
'aside', 'form']):
            element.decompose()
            
        text_content = ' '.join(soup.stripped_strings)
        return text_content[:max_length] if max_length > 0 else text_content
    except Exception as e:
        return f"🚫 Content fetch error: {str(e)}"

def analyze_with_ollama(content, query, model, max_analysis_length):
    """Analyze content using local Ollama model"""
    # Check if content is an error message
    if content.startswith("🚫"):
        return content
    
    # Format analysis prompt
    analysis_prompt = textwrap.dedent(f"""
    Analyze the website based on these criteria:
    1. Relevance to query: How well does it match '{query}'? (1-10)
    2. Technical Depth: Beginner/Intermediate/Advanced
    3. Credibility: Author credentials, citations, references
    4. Commercial Intent: Information vs product promotion
    5. Content Freshness: Recent updates or outdated
    
    Return analysis in this format:
    Relevance: [score]/10
    Technical Depth: [level]
    Credibility: [assessment]
    Commercial Intent: [assessment]
    Freshness: [assessment]
    Summary: [brief summary]
    
    Content Excerpt:
    {content[:max_analysis_length]}
    """)
    
    try:
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': analysis_prompt}],
            options={'temperature': 0.2}
        )
        return response['message']['content']
    except Exception as e:
        return f"🚫 Ollama error: {str(e)}"

def display_domain_table(domains):
    """Display domains in a formatted table"""
    if not domains:
        print("❌ No domains found")
        return
        
    print("\n" + "="*70)
    print(f"{'#':<4} {'Domain':<40} {'Occurrences':<12} First URL")
    print("-"*70)
    
    for domain in domains:
        truncated_url = (domain['url'][:47] + '...') if len(domain['url']) 
> 50 else domain['url']
        print(f"{domain['number']:<4} {domain['domain']:<40} {domain
['occurrences']:<12} {truncated_url}")
    
    print("="*70 + "\n")

def get_documents_googlesearch_path():
    """Get the Documents/Googlesearch directory path"""
    documents_path = os.path.expanduser("~/Documents")
    googlesearch_path = os.path.join(documents_path, "Googlesearch")
    os.makedirs(googlesearch_path, exist_ok=True)
    return googlesearch_path

def autosave_progress(domains, query, args, stage, chat_history=None):
    """Autosave progress to Documents/Googlesearch directory"""
    googlesearch_path = get_documents_googlesearch_path()
    
    # Generate safe filename
    safe_query = re.sub(r'[^\w\s]', '', query)[:50].strip().replace(' ', '_')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if stage == "search_results":
        filename = f"search_results_{safe_query}_{timestamp}.json"
    elif stage == "analysis":
        filename = f"analysis_{safe_query}_{timestamp}.json"
    elif stage == "chat":
        filename = f"chat_session_{safe_query}_{timestamp}.json"
    else:
        filename = f"progress_{safe_query}_{timestamp}.json"
    
    filepath = os.path.join(googlesearch_path, filename)
    
    # Prepare data for saving
    save_data = {
        'query': query,
        'stage': stage,
        'timestamp': datetime.datetime.now().isoformat(),
        'domains': domains,
        'args': vars(args) if args else {},
        'chat_history': chat_history or []
    }
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Autosaved {stage} to: {filepath}")
        return filepath
    except Exception as e:
        print(f"⚠️ Autosave error: {str(e)}")
        return None

def save_to_markdown(domains, query, args, chat_history=None, session_
type="analysis"):
    """Save full results to a Markdown file"""
    googlesearch_path = get_documents_googlesearch_path()
    
    # Generate safe filename
    safe_query = re.sub(r'[^\w\s]', '', query)[:50].strip().replace(' ', '_')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if chat_history:
        filename = f"{session_type}_{safe_query}_{timestamp}.md"
    else:
        filename = f"analysis_{safe_query}_{timestamp}.md"
    
    filepath = os.path.join(googlesearch_path, filename)
    
    with open(filepath, 'w', encoding='utf-8') as md_file:
        if chat_history:
            md_file.write(f"# {session_type.capitalize()} Session: {query}\n\n")
            md_file.write(f"**Date**: {datetime.datetime.now().strftime
('%Y-%m-%d %H:%M:%S')}\n")
            md_file.write(f"**Model**: {args.model}\n\n")
            
            md_file.write("## Conversation History\n\n")
            for entry in chat_history:
                role = "User" if entry['role'] == 'user' else "Assistant"
                md_file.write(f"### {role}\n")
                md_file.write(f"{html.escape(entry['content'])}\n\n")
        else:
            md_file.write(f"# Search Analysis: {query}\n\n")
            md_file.write(f"**Date**: {datetime.datetime.now().strftime
('%Y-%m-%d %H:%M:%S')}\n")
            md_file.write(f"**Total Results**: {len(domains)}\n")
            md_file.write(f"**Model**: {args.model}\n\n")
            
            md_file.write("## Parameters\n")
            md_file.write(f"- Search Results: {args.search_results}\n")
            md_file.write(f"- Domains Analyzed: {args.analyze_domains}\n")
            md_file.write(f"- Max Content: {args.max_content} characters\n")
            md_file.write(f"- Max Analysis: {args.max_analysis} characters\n\n")
            
            md_file.write("## Domain Analysis\n\n")
            for domain in domains:
                md_file.write(f"### {domain['number']}. {domain['domain']}\n")
                md_file.write(f"- **URL**: [{domain['url']}]({domain['url']})
\n")
                md_file.write(f"- **Occurrences**: {domain['occurrences']}\n")
                md_file.write(f"- **Google Snippet**: {domain['snippet']}\n\n")
                
                if 'content' in domain:
                    md_file.write("#### Content Excerpt\n")
                    md_file.write(f"```\n{html.escape(domain['content']
[:args.max_content])}\n```\n\n")
                
                if 'analysis_text' in domain:
                    md_file.write("#### Analysis\n")
                    md_file.write(f"{html.escape(domain['analysis_text']
)}\n\n")
                
                md_file.write("---\n\n")
    
    return filepath

def extract_content_with_ollama(domain, extraction_task, model):
    """Extract specific content using Ollama"""
    if 'content' not in domain or domain['content'].startswith("🚫"):
        return "Error: No content available for extraction"
    
    extraction_prompt = textwrap.dedent(f"""
    You are an expert content extractor. Perform the following task:
    {extraction_task}
    
    Content to extract from:
    {domain['content'][:5000]}
    """)
    
    try:
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': extraction_prompt}],
            options={'temperature': 0.1}
        )
        return response['message']['content']
    except Exception as e:
        return f"🚫 Extraction error: {str(e)}"

def save_chat_session(chat_history, query, model, filename=None):
    """Save chat session to JSON file"""
    googlesearch_path = get_documents_googlesearch_path()
    
    if not filename:
        safe_query = re.sub(r'[^\w\s]', '', query)[:50].strip().replace
(' ', '_')
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_session_{safe_query}_{timestamp}.json"
    
    filepath = os.path.join(googlesearch_path, filename)
    
    session_data = {
        'query': query,
        'model': model,
        'history': chat_history,
        'saved_at': datetime.datetime.now().isoformat()
    }
    
    with open(filepath, 'w') as f:
        json.dump(session_data, f, indent=2)
    
    return filepath

def load_chat_session(filename):
    """Load chat session from JSON file"""
    googlesearch_path = get_documents_googlesearch_path()
    filepath = os.path.join(googlesearch_path, filename)
    
    if not os.path.exists(filepath):
        # Also check if full path was provided
        if not os.path.exists(filename):
            return None, None, None
        filepath = filename
    
    with open(filepath, 'r') as f:
        session_data = json.load(f)
    
    return session_data['query'], session_data['model'], session_data
['history']

def load_analysis_file(filename):
    """Load analysis data from JSON file"""
    googlesearch_path = get_documents_googlesearch_path()
    filepath = os.path.join(googlesearch_path, filename)
    
    if not os.path.exists(filepath):
        # Also check if full path was provided
        if not os.path.exists(filename):
            return None
        filepath = filename
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"⚠️ Error loading analysis file: {str(e)}")
        return None

def interactive_chat(domains, query, model, analysis_filename):
    """Interactive shell for asking questions about the websites"""
    print("\n💬 Starting interactive chat session...")
    print("Type your questions about the websites or type 'exit' to quit")
    print("Special commands:")
    print("  #<number> [question] - Ask about a specific domain")
    print("  all [question]       - Ask about all domains")
    print("  save                 - Save this chat session")
    print("  extract <task> from #<num> - Extract specific content")
    print("      Example: extract all linux commands from #2")
    print("      Example: extract Shakespeare love poems from #3\n")
    
    chat_history = []
    chat_history.append({
        'role': 'system',
        'content': f"You're an analyst assistant helping with search 
results for: '{query}'. "
                   "You have analyzed multiple websites and can answer 
questions about them. "
                   f"Full analysis is saved in: {analysis_filename}"
    })
    
    # Track saved sessions
    saved_sessions = []
    
    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit']:
                break
                
            # Handle save command
            if user_input.lower() == 'save':
                session_file = save_chat_session(chat_history, query, model)
                saved_sessions.append(session_file)
                print(f"💾 Chat session saved to: {session_file}")
                continue
                
            # Handle extraction command
            if user_input.lower().startswith('extract '):
                # Extract pattern: "extract [what] from #[number]"
                match = re.match(r'extract\s+(.+?)\s+from\s+#(\d+)', 
user_input, re.IGNORECASE)
                if match:
                    extraction_task = match.group(1)
                    domain_num = int(match.group(2))
                    domain = next((d for d in domains if d['number'] == 
domain_num), None)
                    
                    if domain:
                        print(f"🔍 Extracting '{extraction_task}' 
from domain #{domain_num}...")
                        extracted = extract_content_with_ollama
(domain, extraction_task, model)
                        
                        # Display results
                        print(f"\n✅ Extracted content from {domain
['domain']}:")
                        print(extracted)
                        
                        # Add to chat history
                        chat_history.append({
                            'role': 'assistant',
                            'content': f"Extracted content from 
{domain['domain']}:\n{extracted}"
                        })
                    else:
                        print(f"⚠️ Domain #{domain_num} not found")
                else:
                    print("Invalid extract command. Format: extract 
[what] from #[number]")
                continue
                
            # Add context if referencing a specific domain
            if user_input.startswith('#'):
                parts = user_input.split(maxsplit=1)
                if len(parts) < 2:
                    print("Please ask a question after the domain reference")
                    continue
                    
                domain_ref = parts[0][1:]
                question = parts[1]
                
                try:
                    domain_num = int(domain_ref)
                    domain = next((d for d in domains if d['number'] 
== domain_num), None)
                    if not domain:
                        print(f"Domain #{domain_num} not found")
                        continue
                        
                    # Add domain context to the question
                    context = f"Domain #{domain_num}: {domain['domain']}\n"
                    context += f"URL: {domain['url']}\n"
                    
                    if 'analysis_text' in domain:
                        context += f"Previous Analysis:\n{domain['
analysis_text']}\n"
                    
                    if 'content' in domain and not domain['content']
.startswith("🚫"):
                        context += f"Content Excerpt:\n{domain['content']
[:1000]}\n"
                    
                    user_input = f"{context}\nQuestion: {question}"
                except ValueError:
                    print("Invalid domain number format")
                    continue
                    
            elif user_input.lower().startswith('all '):
                question = user_input[4:]
                context = "All analyzed domains:\n"
                for domain in domains:
                    context += f"\n## Domain #{domain['number']}: 
{domain['domain']}\n"
                    if 'analysis_text' in domain:
                        context += f"Analysis Summary: {domain['analysis
_text'][:200]}...\n"
                user_input = f"{context}\nQuestion: {question}"
            
            # Add to chat history
            chat_history.append({'role': 'user', 'content': user_input})
            
            # Get response from Ollama
            print("\n🤖 Thinking...", end="", flush=True)
            response = ollama.chat(
                model=model,
                messages=chat_history,
                options={'temperature': 0.5}  # More creative responses
            )
            print("\r", end="")  # Clear "Thinking" message
            
            assistant_response = response['message']['content']
            print(f"Assistant: {assistant_response}\n")
            
            # Add to chat history
            chat_history.append({'role': 'assistant', 'content': 
assistant_response})
            
        except KeyboardInterrupt:
            print("\nExiting chat...")
            break
        except Exception as e:
            print(f"\n🚫 Error: {str(e)}")
    
    # Save chat history to Markdown
    chat_filename = save_to_markdown(domains, query, args, chat_history
, "chat")
    print(f"\n💾 Chat session saved to: {chat_filename}")
    
    # Offer to save session as JSON
    save_option = input("Save chat session as JSON for later 
continuation? (y/n): ").lower()
    if save_option == 'y':
        session_file = save_chat_session(chat_history, query, model)
        print(f"💾 Session saved to: {session_file}")
        print("Load later with: --load-session " + session_file)
    
    return saved_sessions

def main():
    parser = argparse.ArgumentParser(
        description='Analyze Google search results by top-level 
domains using Ollama',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('query', type=str, help='Google search query', 
nargs='?', default=None)
    parser.add_argument('--search-results', type=int, default=50, 
                        help='Total results to fetch from Google')
    parser.add_argument('--analyze-domains', type=int, default=10, 
                        help='Number of unique domains to analyze')
    parser.add_argument('--api-key', type=str, default=os.getenv
('SERPAPI_KEY'), 
                        help='SerpAPI key (default: from SERPAPI_KEY 
env var)')
    parser.add_argument('--model', type=str, default='llama3', help=
'Ollama model name')
    parser.add_argument('--max-content', type=int, default=5000, 
                        help='Max characters to extract from websites 
(0=no limit)')
    parser.add_argument('--max-analysis', type=int, default=3000, 
                        help='Max characters to send to Ollama (0=no limit)')
    parser.add_argument('--delay', type=int, default=3, 
                        help='Delay between website fetches in seconds')
    parser.add_argument('--list-only', action='store_true', 
                        help='Only list domains without analysis')
    parser.add_argument('--no-chat', action='store_true', 
                        help='Skip interactive chat after analysis')
    parser.add_argument('--load-session', type=str, 
                        help='Load a saved chat session JSON file')
    parser.add_argument('--load-analysis', type=str, 
                        help='Load a saved analysis JSON file')
    
    args = parser.parse_args()

    # Handle analysis loading
    if args.load_analysis:
        print(f"📂 Loading analysis from: {args.load_analysis}")
        analysis_data = load_analysis_file(args.load_analysis)
        
        if not analysis_data:
            print("❌ Failed to load analysis file")
            sys.exit(1)
            
        domains = analysis_data.get('domains', [])
        query = analysis_data.get('query', 'Unknown query')
        
        print(f"✅ Loaded analysis for: '{query}'")
        print(f"🌐 Found {len(domains)} domains")
        
        display_domain_table(domains)
        
        # Start interactive chat
        if not args.no_chat:
            analysis_filename = f"Loaded analysis: {args.load_analysis}"
            interactive_chat(domains, query, args.model, analysis_filename)
        return

    # Handle session loading
    if args.load_session:
        print(f"📂 Loading chat session from: {args.load_session}")
        query, model, chat_history = load_chat_session(args.load_session)
        
        if not query or not chat_history:
            print("❌ Failed to load session")
            sys.exit(1)
            
        print(f"🔁 Continuing chat for: '{query}'")
        print(f"💬 Chat history loaded with {len(chat_history)} messages")
        
        # We need domains for reference, but they're not in session
        # For simplicity, we'll just start chat without domain context
        domains = []
        interactive_chat(domains, query, model, "Loaded session")
        return

    if not args.query:
        print("❌ Search query is required")
        sys.exit(1)
        
    if not args.api_key:
        print("❌ SerpAPI key required. Set SERPAPI_KEY env var or use --api-key")
        sys.exit(1)

    # Step 1: Get Google results
    print(f"🔍 Searching Google for: '{args.query}'")
    print(f"Fetching {args.search_results} results...")
    results = google_search(args.query, args.search_results, args.api_key)
    
    if not results:
        print("❌ No search results found")
        sys.exit(1)
        
    print(f"✅ Received {len(results)} results")
    
    # Autosave search results
    autosave_progress(results, args.query, args, "search_results")
    
    # Step 2: Extract unique base domains
    domains = extract_base_domains(results)[:args.analyze_domains]
    
    if not domains:
        print("❌ No domains found")
        sys.exit(1)
        
    print(f"\n✅ Found {len(domains)} unique top-level domains")
    
    # Display domain table
    display_domain_table(domains)
    
    if args.list_only:
        print("ℹ️ Domain listing complete (--list-only specified)")
        return
    
    # Step 3: Analyze selected domains
    print(f"🧠 Analyzing top {len(domains)} domains...")
    analyzed_count = 0
    
    for domain in domains:
        print(f"\n🔗 Analyzing #{domain['number']}: {domain['domain']}")
        print(f"URL: {domain['url']}")
        print(f"📊 Found in {domain['occurrences']} search results")
        
        # Get website content
        print("🌐 Fetching website content...")
        content = fetch_website_content(domain['url'], args.max_content)
        domain['content'] = content  # Store for later use
        
        # Analyze with Ollama
        print("🤖 Processing with Ollama...")
        analysis = analyze_with_ollama(
            content, 
            args.query, 
            args.model, 
            args.max_analysis
        )
        domain['analysis_text'] = analysis  # Store analysis
        
        # Display results
        print(f"\n📝 Analysis for {domain['domain']}:")
        print(analysis)
        print("\n" + "="*80)
        
        analyzed_count += 1
        
        # Autosave progress after each domain analysis
        if analyzed_count % 3 == 0:  # Autosave every 3 domains
            autosave_progress(domains, args.query, args, "analysis")
        
        time.sleep(args.delay)
    
    # Final autosave after all analysis
    autosave_progress(domains, args.query, args, "analysis")
    
    # Save full analysis to Markdown
    analysis_filename = save_to_markdown(domains, args.query, args)
    print(f"\n💾 Full analysis saved to: {analysis_filename}")
    
    # Start interactive chat
    if not args.no_chat:
        saved_sessions = interactive_chat(domains, args.query, 
args.model, analysis_filename)
        
        # Autosave chat sessions
        for session in saved_sessions:
            print(f"💾 Chat session autosaved: {session}")

if __name__ == "__main__":
    main()

```
