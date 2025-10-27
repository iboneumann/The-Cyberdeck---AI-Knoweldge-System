+++
date = '2025-10-25T09:03:51+02:00'
draft = false
title = "The reg_prepare.py script"
weight = 17
+++

### Creating data points from Websites
```batch
rag_prepare.py

List available analysis files
python3 rag_prepare.py --list-files

Interactive mode with a specific file
python3 rag_prepare.py \
--file analysis_free_lessions_on_chemics_20251024_191813.json \
--interactive

Automatic processing with custom settings
python3 rag_prepare.py --file analysis_chemistry.json \
--max-domains 8 \
--chunk-size 800

Use different Ollama model
python3 rag_prepare.py --file analysis_chemistry.md --model mistra
```

```batch

#!/usr/bin/env python3
"""
RAG Preparation Script - Extracts and structures content from 
GoogleSearch analysis for RAG systems
"""

import os
import json
import argparse
import ollama
import datetime
import re
import html
import hashlib
from collections import OrderedDict
import requests
from bs4 import BeautifulSoup
import time

def get_rag_base_path():
    """Get the Documents/Googlesearch/Textextractions/RAGingbase 
directory path"""
    documents_path = os.path.expanduser("~/Documents")
    rag_base_path = os.path.join(documents_path, "Googlesearch", 
"Textextractions", "RAGingbase")
    os.makedirs(rag_base_path, exist_ok=True)
    return rag_base_path

def get_googlesearch_path():
    """Get the Documents/Googlesearch directory path"""
    documents_path = os.path.expanduser("~/Documents")
    googlesearch_path = os.path.join(documents_path, "Googlesearch")
    return googlesearch_path

def list_analysis_files():
    """List all available analysis files in Documents/Googlesearch"""
    googlesearch_path = get_googlesearch_path()
    
    if not os.path.exists(googlesearch_path):
        print("❌ Googlesearch directory not found")
        return []
    
    analysis_files = []
    for filename in os.listdir(googlesearch_path):
        if filename.endswith('.json') and ('analysis' in filename or 
'search_results' in filename):
            filepath = os.path.join(googlesearch_path, filename)
            analysis_files.append({
                'filename': filename,
                'path': filepath,
                'size': os.path.getsize(filepath),
                'type': 'json'
            })
        elif filename.endswith('.md') and ('analysis' in filename or 'chat' 
in filename):
            filepath = os.path.join(googlesearch_path, filename)
            analysis_files.append({
                'filename': filename,
                'path': filepath,
                'size': os.path.getsize(filepath),
                'type': 'markdown'
            })
    
    return sorted(analysis_files, key=lambda x: x['filename'])

def load_analysis_file(filename):
    """Load analysis data from JSON or Markdown file"""
    googlesearch_path = get_googlesearch_path()
    
    # Check if filename is already a full path
    if os.path.exists(filename):
        filepath = filename
    else:
        filepath = os.path.join(googlesearch_path, filename)
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return None
    
    try:
        # Try to load as JSON first
        if filename.endswith('.json'):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        # Try to parse as Markdown
        elif filename.endswith('.md'):
            print("📄 Loading Markdown analysis file...")
            return parse_markdown_analysis(filepath)
        else:
            print("❌ Unsupported file format. Please use .json or .md files")
            return None
            
    except json.JSONDecodeError:
        # If JSON fails, try as Markdown
        print("🔄 File is not JSON, trying to parse as Markdown...")
        return parse_markdown_analysis(filepath)
    except Exception as e:
        print(f"❌ Error loading file: {str(e)}")
        return None

def parse_markdown_analysis(filepath):
    """Parse markdown analysis file and extract domain information"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        domains = []
        current_domain = None
        
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for domain headers: "### 1. domain.com"
            if line.startswith('### '):
                if current_domain:
                    domains.append(current_domain)
                
                # Extract domain number and name
                match = re.match(r'###\s*(\d+)\.\s*(.+)', line)
                if match:
                    current_domain = {
                        'number': int(match.group(1)),
                        'domain': match.group(2),
                        'url': '',
                        'occurrences': 1,
                        'snippet': '',
                        'content': '',
                        'analysis_text': ''
                    }
            
            # Look for URL
            elif line.startswith('- **URL**:') and current_domain:
                url_match = re.search(r'\[(.+?)\]\((.+?)\)', line)
                if url_match:
                    current_domain['url'] = url_match.group(2)
            
            # Look for occurrences
            elif line.startswith('- **Occurrences**:') and current_domain:
                occ_match = re.search(r'- \*\*Occurrences\*\*:\s*(\d+)', line)
                if occ_match:
                    current_domain['occurrences'] = int(occ_match.group(1))
            
            # Look for analysis section
            elif line.startswith('#### Analysis') and current_domain:
                analysis_lines = []
                i += 1
                while i < len(lines) and not (lines[i].startswith('####') or 
lines[i].startswith('###') or lines[i].startswith('---')):
                    if lines[i].strip():
                        analysis_lines.append(lines[i])
                    i += 1
                current_domain['analysis_text'] = '\n'.join(analysis_lines)
                continue  # Don't increment i again since we already did 
in the while loop
            
            i += 1
        
        # Add the last domain
        if current_domain:
            domains.append(current_domain)
        
        return {
            'domains': domains,
            'query': extract_query_from_markdown(content),
            'timestamp': datetime.datetime.now().isoformat()
        }
    
    except Exception as e:
        print(f"❌ Error parsing markdown file: {str(e)}")
        return None

def extract_query_from_markdown(content):
    """Extract query from markdown content"""
    match = re.search(r'# Search Analysis:\s*(.+)', content)
    if match:
        return match.group(1).strip()
    return "Unknown query"

def fetch_website_content_rag(url, max_length=10000):
    """Fetch content from website for RAG preparation"""
    try:
        response = requests.get(url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) 
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        })
        response.raise_for_status()
        
        # Check content type
        content_type = response.headers.get('Content-Type', '').lower()
        if 'html' not in content_type:
            return f"Non-HTML content: {content_type}"
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unnecessary elements
        for element in soup(['script', 'style', 'header', 'footer', 'nav'
, 'aside', 'form', 'iframe']):
            element.decompose()
            
        # Extract title
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No title"
        
        # Extract main content
        text_content = ' '.join(soup.stripped_strings)
        
        # Try to find main content areas
        main_content = soup.find(['main', 'article']) or soup.find('div'
, class_=re.compile(r'content|main|article'))
        if main_content:
            main_text = ' '.join(main_content.stripped_strings)
            if len(main_text) > len(text_content) * 0.3:  # If main content 
is substantial
                text_content = main_text
        
        content = text_content[:max_length] if max_length > 0 else text_content
        
        return {
            'title': title_text,
            'content': content,
            'url': url,
            'content_length': len(content)
        }
        
    except Exception as e:
        return {
            'title': f"Error: {str(e)}",
            'content': f"Content fetch error: {str(e)}",
            'url': url,
            'content_length': 0
        }

def chunk_content_for_rag(content, chunk_size=1000, overlap=200):
    """Split content into chunks for RAG with overlap"""
    if len(content) <= chunk_size:
        return [content]
    
    chunks = []
    start = 0
    
    while start < len(content):
        end = start + chunk_size
        
        # If we're not at the end, try to break at a sentence boundary
        if end < len(content):
            # Look for sentence endings in the last 100 characters of the chunk
            sentence_end = max(content.rfind('. ', start, end),
                             content.rfind('? ', start, end),
                             content.rfind('! ', start, end))
            
            if sentence_end != -1 and sentence_end > start + chunk_size * 0.5:
                end = sentence_end + 1  # Include the period/space
        
        chunk = content[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start position, accounting for overlap
        start = end - overlap
        if start < 0:
            start = 0
    
    return chunks

def extract_structured_content_rag(domain, model, max_content_length=15000):
    """Extract structured, clean content from domain for RAG"""
    print(f"🔍 Extracting structured content from {domain['domain']}...")
    
    # Fetch fresh content or use existing
    if 'content' not in domain or domain['content'].startswith("🚫") or 
len(domain.get('content', '')) < 500:
        print(f"🌐 Fetching fresh content from {domain['url']}...")
        content_data = fetch_website_content_rag(domain['url'], 
max_content_length)
        content = content_data['content']
        title = content_data['title']
    else:
        content = domain['content']
        title = domain.get('domain', 'No title')
    
    if len(content) < 100:
        return {
            'domain': domain['domain'],
            'url': domain['url'],
            'title': title,
            'chunks': [],
            'total_chunks': 0,
            'total_content_length': 0,
            'status': 'insufficient_content'
        }
    
    # Use Ollama to clean and structure the content
    cleaning_prompt = f"""
    Clean and structure this web content for a RAG (Retrieval Augmented 
Generation) system.
    
    Please:
    1. Remove any navigation text, ads, cookie notices, or boilerplate
    2. Extract the core informational content
    3. Preserve the factual information and key concepts
    4. Maintain proper formatting for readability
    5. Remove any duplicate or redundant information
    
    Return only the cleaned, structured content without additional commentary.
    
    Source: {domain['domain']} - {title}
    URL: {domain['url']}
    
    Content to clean:
    {content[:12000]}
    """
    
    try:
        print(f"🤖 Cleaning content with {model}...")
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': cleaning_prompt}],
            options={'temperature': 0.1}
        )
        cleaned_content = response['message']['content']
        
        # Chunk the cleaned content
        chunks = chunk_content_for_rag(cleaned_content)
        
        return {
            'domain': domain['domain'],
            'url': domain['url'],
            'title': title,
            'cleaned_content': cleaned_content,
            'chunks': chunks,
            'total_chunks': len(chunks),
            'total_content_length': len(cleaned_content),
            'status': 'success'
        }
        
    except Exception as e:
        print(f"❌ Error cleaning content: {str(e)}")
        # Fallback: chunk the original content
        chunks = chunk_content_for_rag(content[:max_content_length])
        return {
            'domain': domain['domain'],
            'url': domain['url'],
            'title': title,
            'cleaned_content': content[:max_content_length],
            'chunks': chunks,
            'total_chunks': len(chunks),
            'total_content_length': len(content),
            'status': 'fallback'
        }

def generate_chunk_id(domain, chunk_index, total_chunks):
    """Generate a unique ID for each chunk"""
    base_id = hashlib.md5(domain['url'].encode()).hexdigest()[:8]
    return f"{base_id}_{chunk_index:03d}_{total_chunks:03d}"

def save_rag_data(rag_data, source_file, chunk_size=1000):
    """Save RAG-prepared data in multiple formats"""
    rag_base_path = get_rag_base_path()
    
    # Generate safe filename base
    safe_query = re.sub(r'[^\w\s]', '', rag_data['query'])[:30].strip()
.replace(' ', '_')
    safe_source = os.path.basename(source_file).replace('.json', '')
.replace('.md', '')[:20]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    base_filename = f"rag_{safe_query}_{safe_source}_{timestamp}"
    
    # Save as JSONL (for vector databases)
    jsonl_path = os.path.join(rag_base_path, f"{base_filename}.jsonl")
    with open(jsonl_path, 'w', encoding='utf-8') as f:
        for domain_data in rag_data['domains']:
            for chunk_index, chunk in enumerate(domain_data['chunks']):
                chunk_id = generate_chunk_id(domain_data, chunk_index, 
domain_data['total_chunks'])
                
                record = {
                    'id': chunk_id,
                    'content': chunk,
                    'metadata': {
                        'domain': domain_data['domain'],
                        'url': domain_data['url'],
                        'title': domain_data['title'],
                        'source_file': source_file,
                        'query': rag_data['query'],
                        'chunk_index': chunk_index,
                        'total_chunks': domain_data['total_chunks'],
                        'content_length': len(chunk),
                        'timestamp': datetime.datetime.now().isoformat(),
                        'status': domain_data['status']
                    }
                }
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    # Save as structured JSON
    json_path = os.path.join(rag_base_path, f"{base_filename}.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(rag_data, f, indent=2, ensure_ascii=False)
    
    # Save summary
    summary_path = os.path.join(rag_base_path, f"{base_filename}_summary.md")
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"# RAG Data Preparation Summary\n\n")
        f.write(f"**Source File**: {source_file}\n")
        f.write(f"**Query**: {rag_data['query']}\n")
        f.write(f"**Generated**: {datetime.datetime.now().strftime
('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Domains**: {len(rag_data['domains'])}\n")
        f.write(f"**Total Chunks**: {rag_data['total_chunks']}\n")
        f.write(f"**Total Content Length**: {rag_data['total_content_length'
]} characters\n\n")
        
        f.write("## Domain Details\n\n")
        for domain_data in rag_data['domains']:
            f.write(f"### {domain_data['domain']}\n")
            f.write(f"- **URL**: {domain_data['url']}\n")
            f.write(f"- **Title**: {domain_data['title']}\n")
            f.write(f"- **Chunks**: {domain_data['total_chunks']}\n")
            f.write(f"- **Status**: {domain_data['status']}\n")
            f.write(f"- **Content Length**: {domain_data['total_content
_length']} characters\n\n")
            
            # Show first chunk as sample
            if domain_data['chunks']:
                f.write("#### Sample Chunk\n")
                f.write("```\n")
                f.write(domain_data['chunks'][0][:500] + "...\n" 
if len(domain_data['chunks'][0]) > 500 else domain_data['chunks'][0])
                f.write("\n```\n\n")
    
    print(f"💾 RAG data saved:")
    print(f"   - JSONL: {jsonl_path}")
    print(f"   - JSON: {json_path}")
    print(f"   - Summary: {summary_path}")
    
    return {
        'jsonl': jsonl_path,
        'json': json_path,
        'summary': summary_path
    }

def display_domain_info(domains):
    """Display information about loaded domains"""
    if not domains:
        print("❌ No domains loaded")
        return
    
    print(f"\n📊 Loaded {len(domains)} domains:")
    print("=" * 80)
    for domain in domains:
        print(f"#{domain['number']}: {domain['domain']}")
        print(f"   URL: {domain['url']}")
        print(f"   Occurrences: {domain['occurrences']}")
        
        # Show analysis summary if available
        if 'analysis_text' in domain and domain['analysis_text']:
            analysis_preview = domain['analysis_text'][:150] + "..." 
if len(domain['analysis_text']) > 150 else domain['analysis_text']
            print(f"   Analysis: {analysis_preview}")
        print("-" * 40)

def prepare_rag_from_analysis(analysis_data, source_file, model, 
max_domains=10, chunk_size=1000):
    """Prepare RAG data from analysis file"""
    domains = analysis_data.get('domains', [])[:max_domains]
    query = analysis_data.get('query', 'Unknown query')
    
    print(f"🧠 Preparing RAG data for: {query}")
    print(f"📊 Processing {len(domains)} domains...")
    
    rag_domains = []
    total_chunks = 0
    total_content_length = 0
    
    for i, domain in enumerate(domains, 1):
        print(f"\n[{i}/{len(domains)}] Processing {domain['domain']}...")
        
        rag_domain_data = extract_structured_content_rag(domain, model)
        rag_domains.append(rag_domain_data)
        
        total_chunks += rag_domain_data['total_chunks']
        total_content_length += rag_domain_data['total_content_length']
        
        print(f"   ✅ {rag_domain_data['total_chunks']} chunks, 
{rag_domain_data['total_content_length']} chars, status: {rag_domain_data
['status']}")
        
        # Small delay to be respectful
        time.sleep(1)
    
    # Prepare final RAG data structure
    rag_data = {
        'query': query,
        'source_file': source_file,
        'timestamp': datetime.datetime.now().isoformat(),
        'domains': rag_domains,
        'total_domains': len(rag_domains),
        'total_chunks': total_chunks,
        'total_content_length': total_content_length,
        'preparation_settings': {
            'model': model,
            'max_domains': max_domains,
            'chunk_size': chunk_size
        }
    }
    
    return rag_data

def interactive_rag_mode(analysis_data, source_file, model):
    """Interactive mode for RAG preparation"""
    print("\n🔍 Interactive RAG Preparation Mode")
    print("Available commands:")
    print("  prepare [max_domains] - Prepare RAG data (default: 5 domains)")
    print("  list                  - Show loaded domains")
    print("  preview #<num>        - Preview content from specific domain")
    print("  exit                  - Quit interactive mode\n")
    
    while True:
        try:
            user_input = input("RAG> ").strip()
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit']:
                break
                
            if user_input.lower() == 'list':
                display_domain_info(analysis_data.get('domains', []))
                continue
                
            # Handle domain preview
            if user_input.lower().startswith('preview '):
                match = re.match(r'preview\s+#(\d+)', user_input, 
re.IGNORECASE)
                if match:
                    domain_num = int(match.group(1))
                    domain = next((d for d in analysis_data.get('domains'
, []) if d['number'] == domain_num), None)
                    
                    if domain:
                        print(f"\n🔍 Previewing domain #{domain_num}: 
{domain['domain']}")
                        print(f"URL: {domain['url']}")
                        
                        # Show analysis if available
                        if 'analysis_text' in domain and domain['analysis
_text']:
                            print(f"\nAnalysis:\n{domain['analysis_text']
[:500]}...")
                        
                        # Test content extraction
                        test_data = extract_structured_content_rag(domain, 
model, 5000)
                        print(f"\nContent Preview ({test_data['status']}):")
                        if test_data['chunks']:
                            print(f"First chunk ({len(test_data['chunks'][0])
} chars):")
                            print(test_data['chunks'][0][:300] + "..." if 
len(test_data['chunks'][0]) > 300 else test_data['chunks'][0])
                        print(f"\nTotal chunks: {test_data['total_chunks']}")
                    else:
                        print(f"❌ Domain #{domain_num} not found")
                else:
                    print("❌ Invalid format. Use: preview #[number]")
                continue
                
            # Handle RAG preparation
            if user_input.lower().startswith('prepare'):
                parts = user_input.split()
                max_domains = 5  # default
                
                if len(parts) > 1:
                    try:
                        max_domains = int(parts[1])
                    except ValueError:
                        print("❌ Invalid number for max_domains")
                        continue
                
                print(f"🚀 Preparing RAG data from {max_domains} domains...")
                rag_data = prepare_rag_from_analysis(analysis_data, source
_file, model, max_domains)
                
                # Save the data
                saved_files = save_rag_data(rag_data, source_file)
                
                print(f"\n✅ RAG preparation complete!")
                print(f"   📊 Domains processed: {rag_data['total_domains']}")
                print(f"   📄 Total chunks: {rag_data['total_chunks']}")
                print(f"   📝 Total content: {rag_data['total_content
_length']} characters")
                print(f"   💾 Files saved in: {get_rag_base_path()}")
                continue
                
            print("❌ Unknown command. Available: prepare, preview, list, 
exit")
            
        except KeyboardInterrupt:
            print("\nExiting interactive mode...")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description='Prepare RAG (Retrieval Augmented Generation) data 
from GoogleSearch analysis',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--file', type=str, help='Analysis file to load 
(JSON or MD)')
    parser.add_argument('--list-files', action='store_true', help='List 
available analysis files')
    parser.add_argument('--model', type=str, default='llama3', help='Ollama 
model name')
    parser.add_argument('--max-domains', type=int, default=10, help='Maximum 
number of domains to process')
    parser.add_argument('--chunk-size', type=int, default=1000, help='Chunk 
size for RAG data')
    parser.add_argument('--interactive', action='store_true', help='Start 
interactive mode')
    
    args = parser.parse_args()
    
    # List available files
    if args.list_files:
        files = list_analysis_files()
        if not files:
            print("No analysis files found in Documents/Googlesearch")
            return
        
        print("\n📁 Available analysis files:")
        print("=" * 100)
        for file_info in files:
            size_kb = file_info['size'] / 1024
            file_type = file_info.get('type', 'unknown')
            print(f"{file_info['filename']} ({size_kb:.1f} KB, {file_type})")
        return
    
    # Load specific file
    if args.file:
        analysis_data = load_analysis_file(args.file)
        if not analysis_data:
            print("❌ Failed to load analysis file")
            return
        
        domains = analysis_data.get('domains', [])
        query = analysis_data.get('query', 'Unknown query')
        
        print(f"✅ Loaded analysis: {query}")
        print(f"📊 Domains: {len(domains)}")
        
        # Interactive mode
        if args.interactive:
            interactive_rag_mode(analysis_data, args.file, args.model)
        else:
            # Automatic RAG preparation
            print(f"🚀 Starting automatic RAG preparation for {args.max
_domains} domains...")
            rag_data = prepare_rag_from_analysis(analysis_data, args.file, 
args.model, args.max_domains, args.chunk_size)
            
            # Save the data
            saved_files = save_rag_data(rag_data, args.file, args.chunk_size)
            
            print(f"\n✅ RAG preparation complete!")
            print(f"   📊 Domains processed: {rag_data['total_domains']}")
            print(f"   📄 Total chunks: {rag_data['total_chunks']}")
            print(f"   📝 Total content: {rag_data['total_content_length']} 
characters")
            print(f"   💾 Files saved in: {get_rag_base_path()}")
    
    else:
        print("❌ Please specify an analysis file with --file or use 
--list-files to see available files")
        print("\nUsage examples:")
        print("  python rag_prepare.py --list-files")
        print("  python rag_prepare.py --file analysis_chemistry.json 
--interactive")
        print("  python rag_prepare.py --file analysis_chemistry.json 
--max-domains 8 --chunk-size 800")
        print("  python rag_prepare.py --file analysis_chemistry.md 
--model llama3")

if __name__ == "__main__":
    main()
```
