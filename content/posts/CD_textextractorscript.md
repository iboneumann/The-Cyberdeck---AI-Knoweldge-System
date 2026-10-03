+++
date = '2025-10-25T08:43:04+02:00'
draft = false
title = "The textextractor.py script"
weight = 16
+++

### The website text extractor script

The manual
```batch
textextractor.py
python3 textextractor.py --list-files

python3 textextractor.py --file analysis_chemistry_20241201_123456.json \
 --interactive

python3 textextractor.py --file analysis_chemistry_20241201_123456.json \
 --topic "Chemical Reactions" --domain 1
```
#### Interactive RAG Preparation Mode
```batch
Available commands:
  prepare [max_domains] - Prepare RAG data (default: 5 domains)
  list                  - Show loaded domains
  preview #<num>        - Preview content from specific domain
  exit                  - Quit interactive mode
```

```batch

#!/usr/bin/env python3
"""
Text Extractor - Loads GoogleSearch analysis files and extracts 
structured content
"""

import os
import json
import argparse
import ollama
import datetime
import re
import html
from collections import OrderedDict

def get_textextractions_path():
    """Get the Documents/Googlesearch/Textextractions directory path"""
    documents_path = os.path.expanduser("~/Documents")
    textextractions_path = os.path.join(documents_path, "Googlesearch", 
"Textextractions")
    os.makedirs(textextractions_path, exist_ok=True)
    return textextractions_path

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
        elif filename.endswith('.md') and ('analysis' in filename or
'chat' in filename):
            filepath = os.path.join(googlesearch_path, filename)
            analysis_files.append({
                'filename': filename,
                'path': filepath,
                'size': os.path.getsize(filepath),
                'type': 'markdown'
            })
    
    return sorted(analysis_files, key=lambda x: x['filename'])

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
                while i < len(lines) and not (lines[i].startswith('####')
or lines[i].startswith('###') or lines[i].startswith('---')):
                    if lines[i].strip():
                        analysis_lines.append(lines[i])
                    i += 1
                current_domain['analysis_text'] = '\n'.join(analysis_lines)
                continue  # Don't increment i again since we already 
did in the while loop
            
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

def extract_structured_content(domains, extraction_topic, model, 
max_length=8000):
    """Extract structured content from domains based on a topic"""
    
    # Prepare domain information for the prompt
    domain_info = ""
    for domain in domains:
        domain_info += f"\n\n--- Domain #{domain['number']}: 
{domain['domain']} ---\n"
        domain_info += f"URL: {domain['url']}\n"
        
        if 'analysis_text' in domain and domain['analysis_text']:
            # Clean and shorten analysis text
            analysis_clean = re.sub(r'\n+', ' ', domain['analysis_text'])
            analysis_clean = analysis_clean[:500] + "..." if 
len(analysis_clean) > 500 else analysis_clean
            domain_info += f"Analysis: {analysis_clean}\n"
    
    extraction_prompt = f"""
    Create a comprehensive, well-structured essay or summary about: 
{extraction_topic}
    
    Use the analyzed website information below as your source material. 
Focus on creating 
    a coherent document that synthesizes information from the available 
sources.
    
    Requirements:
    - Create a clear structure with headings and subheadings
    - Include key concepts, definitions, and important details
    - Maintain academic or professional tone
    - Synthesize information from multiple sources when possible
    - Focus on accuracy and completeness
    
    Structure your response as a proper document with:
    1. Introduction
    2. Main content with logical sections
    3. Key findings or important points
    4. Conclusion
    
    Available source information:
    {domain_info}
    
    Now create a comprehensive structured document about: {extraction_topic}
    """
    
    try:
        print("🤖 Generating structured content...")
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': extraction_prompt}],
            options={'temperature': 0.3}
        )
        return response['message']['content']
    except Exception as e:
        return f"❌ Extraction error: {str(e)}"

def extract_domain_specific_content(domain, extraction_task, model):
    """Extract specific content from a single domain"""
    # For markdown files, we don't have full content, so we use analysis text
    available_content = ""
    if 'content' in domain and domain['content'] and not domain['content']
.startswith("🚫"):
        available_content = domain['content'][:5000]
    elif 'analysis_text' in domain and domain['analysis_text']:
        available_content = domain['analysis_text']
    else:
        return "❌ No content available for extraction"
    
    extraction_prompt = f"""
    Extract specific information based on this task: {extraction_task}
    
    Focus on extracting relevant, accurate information from the content below.
    Structure your response clearly and include only verified information.
    
    Source: {domain['domain']} ({domain['url']})
    
    Content to analyze:
    {available_content}
    """
    
    try:
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': extraction_prompt}],
            options={'temperature': 0.1}
        )
        return response['message']['content']
    except Exception as e:
        return f"❌ Extraction error: {str(e)}"

def save_extraction(content, topic, source_file, extraction_type):
    """Save extracted content to Textextractions directory"""
    textextractions_path = get_textextractions_path()
    
    # Generate safe filename
    safe_topic = re.sub(r'[^\w\s]', '', topic)[:50].strip().replace(' ', '_')
    safe_source = os.path.basename(source_file).replace('.json', '').replace
('.md', '')[:30]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if extraction_type == "structured":
        filename = f"essay_{safe_topic}_{safe_source}_{timestamp}.md"
    else:
        filename = f"extraction_{safe_topic}_{safe_source}_{timestamp}.md"
    
    filepath = os.path.join(textextractions_path, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# {extraction_type.capitalize()} Extraction: {topic}\n\n")
        f.write(f"**Source File**: {source_file}\n")
        f.write(f"**Generated**: {datetime.datetime.now().strftime('%Y-%m-%d 
%H:%M:%S')}\n")
        f.write(f"**Type**: {extraction_type}\n\n")
        f.write("---\n\n")
        f.write(content)
    
    print(f"💾 Extraction saved to: {filepath}")
    return filepath

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

def interactive_extraction_mode(domains, source_file, model):
    """Interactive mode for extracting content"""
    print("\n🔍 Interactive Extraction Mode")
    print("Available commands:")
    print("  essay <topic>         - Create structured essay from all domains")
    print("  extract <topic> from #<num> - Extract from specific domain")
    print("  list                  - Show loaded domains")
    print("  exit                  - Quit interactive mode\n")
    
    while True:
        try:
            user_input = input("Extraction> ").strip()
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit']:
                break
                
            if user_input.lower() == 'list':
                display_domain_info(domains)
                continue
                
            # Handle essay creation
            if user_input.lower().startswith('essay '):
                topic = user_input[6:]
                if not topic:
                    print("❌ Please specify a topic for the essay")
                    continue
                    
                print(f"📝 Creating structured essay about: {topic}")
                essay_content = extract_structured_content(domains, topic, 
model)
                
                print("\n" + "=" * 80)
                print("Generated Essay:")
                print("=" * 80)
                print(essay_content)
                print("=" * 80)
                
                # Save essay
                save_path = save_extraction(essay_content, topic, source_file
, "structured")
                print(f"💾 Essay saved to: {save_path}")
                continue
                
            # Handle domain-specific extraction
            if user_input.lower().startswith('extract '):
                # Pattern: "extract [topic] from #[number]"
                match = re.match(r'extract\s+(.+?)\s+from\s+#(\d+)', 
user_input, re.IGNORECASE)
                if match:
                    topic = match.group(1)
                    domain_num = int(match.group(2))
                    
                    domain = next((d for d in domains if d['number'] == 
domain_num), None)
                    if not domain:
                        print(f"❌ Domain #{domain_num} not found")
                        continue
                        
                    print(f"🔍 Extracting '{topic}' from {domain['domain']
}...")
                    extracted = extract_domain_specific_content(domain, 
topic, model)
                    
                    print("\n" + "=" * 80)
                    print(f"Extraction from {domain['domain']}:")
                    print("=" * 80)
                    print(extracted)
                    print("=" * 80)
                    
                    # Save extraction
                    save_path = save_extraction(extracted, topic, 
source_file, "domain_specific")
                    print(f"💾 Extraction saved to: {save_path}")
                else:
                    print("❌ Invalid format. Use: extract [topic] 
from #[number]")
                continue
                
            print("❌ Unknown command. Available: essay, extract, list, exit")
            
        except KeyboardInterrupt:
            print("\nExiting interactive mode...")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description='Extract structured content from GoogleSearch analysis 
files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--file', type=str, help='Analysis file to load 
(JSON or MD)')
    parser.add_argument('--list-files', action='store_true', help=
'List available analysis files')
    parser.add_argument('--model', type=str, default='llama3', help=
'Ollama model name')
    parser.add_argument('--topic', type=str, help='Topic for automatic 
extraction')
    parser.add_argument('--domain', type=int, help='Specific domain number 
to extract from')
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
        
        display_domain_info(domains)
        
        # Automatic extraction mode
        if args.topic:
            if args.domain:
                # Extract from specific domain
                domain = next((d for d in domains if d['number'] == args
.domain), None)
                if domain:
                    print(f"🔍 Extracting '{args.topic}' from {domain
['domain']}...")
                    extracted = extract_domain_specific_content(domain, 
args.topic, args.model)
                    print("\n" + "=" * 80)
                    print(extracted)
                    print("=" * 80)
                    save_extraction(extracted, args.topic, args.file, 
"domain_specific")
                else:
                    print(f"❌ Domain #{args.domain} not found")
            else:
                # Create structured essay from all domains
                print(f"📝 Creating structured essay about: {args.topic}")
                essay_content = extract_structured_content(domains, 
args.topic, args.model)
                print("\n" + "=" * 80)
                print(essay_content)
                print("=" * 80)
                save_extraction(essay_content, args.topic, args.file,
"structured")
        
        # Interactive mode
        elif args.interactive or (not args.topic and not args.domain):
            interactive_extraction_mode(domains, args.file, args.model)
    
    else:
        print("❌ Please specify an analysis file with --file or use 
--list-files to see available files")
        print("\nUsage examples:")
        print("  python textextractor.py --list-files")
        print("  python textextractor.py --file analysis_myquery
_20241201_123456.json --interactive")
        print("  python textextractor.py --file analysis_
myquery_20241201_123456.md --interactive")
        print("  python textextractor.py --file analysis_myquery_
20241201_123456.json --topic 'Chemistry Basics'")
        print("  python textextractor.py --file analysis_myquery
_20241201_123456.md --topic 'Lab Safety' --domain 1")

if __name__ == "__main__":
    main()
```
