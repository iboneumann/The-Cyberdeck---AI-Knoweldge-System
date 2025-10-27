+++
date = '2025-10-23T18:34:29+02:00'
draft = false
title = "About Deck & Parser Script"
weight = 6
+++

### About The Obsidian Deck & AI parser Script

Obviously, that is quite a bit of a script and
part of a set of scripts running in a Python
environment.

All scripts have been created using DeepSeek
and underwent sever testing.

DeepSeek does not print functional scripts,
but will correct and adjust the script it wrote
based on error and feedback.

The system is a Linux Mint 19.3 which by
excessive pythoning is impossible to be upgraded,
easily, with several different Ollama llama
models spread over the several computers.

Installing all required components is not for
the faint hearted, but and adventure and journey
creating the most stable Linux OS I ever used.
This Cluster is rock solid.

Ollama models also take no advantage of the
Beowulf Cluster, but the Python libraries the
scripts pull do in some cases.

Designing the batch processing scripts into a
long chain architecture using the computer
cluster on a LAN level to split the workload
up into junks served to the on LAN waiting ollama
servers does help tremendously to save time.

This is the AIparser10.py:
```batch
import os
import re
import json
import time
import logging
import html2text
import requests
import random
import socket
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler("obsidian_processor.log")]
)
logger = logging.getLogger(__name__)

# Node configuration with simpler setup for testing
NODES = {
    "node1": {
        "url": "http://raspi5:11434/api/generate",
        "models": ["gemma2:2b"],
        "user": "mpiuser"
    },
    "node4": {
        "url": "http://node4:11434/api/generate", 
        "models": ["llama3:latest", "mistral:latest"],  # Simpler models first
        "user": "mpiuser"
    },
    "node5": {
        "url": "http://node5:11434/api/generate",
        "models": ["llama2:latest"],
        "user": "mpiuser"
    },
}

# Configuration
OLLAMA_TIMEOUT = 120  # Reduced timeout
TAG_PROMPT = """
Analyze the following content and extract:
1. 3-5 relevant tags for Obsidian knowledge management (comma-separated)
2. A concise 2-3 sentence summary
3. Key concepts (3-5 most important terms)

Format your response EXACTLY as:
TAGS: tag1, tag2, tag3
SUMMARY: This is a summary...
CONCEPTS: term1, term2, term3

Content:
{content}
"""

class NodeManager:
    """Manages distributed nodes with comprehensive error handling"""
    def __init__(self, nodes_config):
        self.nodes = {}
        self.model_to_nodes = defaultdict(list)
        self.initialize_nodes(nodes_config)
        self.test_all_nodes()  # Test nodes at startup
        
    def initialize_nodes(self, config):
        """Set up node information with diagnostics"""
        for node_name, node_info in config.items():
            self.nodes[node_name] = {
                "url": node_info["url"],
                "models": node_info["models"],
                "user": node_info.get("user", ""),
                "status": "unknown",
                "last_used": 0,
                "error_count": 0,
                "active_tasks": 0,
                "last_error": "",
                "available_models": []  # Track which models actually work
            }
            
            for model in node_info["models"]:
                self.model_to_nodes[model].append(node_name)
        
        logger.info(f"Initialized {len(self.nodes)} nodes")
    
    def test_all_nodes(self):
        """Test all nodes at startup to verify connectivity and models"""
        logger.info("Testing node connectivity and model availability...")
        for node_name in self.nodes:
            if self.test_node_connection(node_name):
                self.test_node_models(node_name)
            else:
                self.nodes[node_name]["status"] = "offline"
                logger.error(f"❌ {node_name} is offline")
    
    def test_node_connection(self, node_name):
        """Test if we can connect to the node"""
        try:
            node_url = self.nodes[node_name]["url"]
            # Extract host and port for socket test
            host = node_url.split("//")[1].split(":")[0]
            port = int(node_url.split(":")[2].split("/")[0])
            
            # Test network connectivity
            with socket.create_connection((host, port), timeout=10):
                logger.info(f"✅ {node_name} network connection successful")
                return True
        except Exception as e:
            logger.error(f"❌ {node_name} connection failed: {str(e)}")
            self.nodes[node_name]["last_error"] = f"Connection failed: {str(e)}"
            return False
    
    def test_node_models(self, node_name):
        """Test which models are available on the node"""
        working_models = []
        for model in self.nodes[node_name]["models"]:
            if self.test_model(node_name, model):
                working_models.append(model)
        
        self.nodes[node_name]["available_models"] = working_models
        if working_models:
            self.nodes[node_name]["status"] = "available"
            logger.info(f"✅ {node_name} has working models: {working_models}")
        else:
            self.nodes[node_name]["status"] = "no_models"
            logger.error(f"❌ {node_name} has no working models")
    
    def test_model(self, node_name, model):
        """Test if a specific model works with a simple prompt"""
        try:
            test_prompt = "Respond with just 'OK'"
            payload = {
                "model": model,
                "prompt": test_prompt,
                "stream": False
            }
            
            response = requests.post(
                self.nodes[node_name]["url"], 
                json=payload, 
                timeout=30
            )
            
            if response.status_code == 200:
                return True
            else:
                logger.warning(f"⚠️ {node_name} model {model} failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            logger.warning(f"⚠️ {node_name} model {model} test failed: {str(e)}")
            return False
    
    def get_available_node(self):
        """Get any available node that's online and has working models"""
        available_nodes = []
        
        for node_name, node_info in self.nodes.items():
            if (node_info["status"] == "available" and 
                node_info["error_count"] < 3 and
                node_info["available_models"]):
                available_nodes.append(node_name)
        
        if available_nodes:
            # Prefer nodes with fewer errors and more models
            return min(available_nodes, 
                      key=lambda x: (self.nodes[x]["error_count"], 
                                   -len(self.nodes[x]["available_models"])))
        return None
    
    def extract_metadata(self, content, node_name):
        """Use specified node to extract metadata with robust error handling"""
        if node_name not in self.nodes or not self.nodes[node_name]["available_models"]:
            raise Exception(f"Node {node_name} has no available models")
        
        # Use first available model
        model = self.nodes[node_name]["available_models"][0]
        url = self.nodes[node_name]["url"]
        
        # Use shorter content for testing
        content_sample = content[:2000]  # Reduced from 8000
        prompt = TAG_PROMPT.format(content=content_sample)
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": 500  # Limit response length
            }
        }
        
        try:
            start_time = time.time()
            logger.info(f"Querying {node_name} with {model}...")
            
            response = requests.post(url, json=payload, timeout=OLLAMA_TIMEOUT)
            
            if response.status_code != 200:
                error_msg = f"HTTP {response.status_code}"
                try:
                    error_data = response.json()
                    error_msg = error_data.get("error", error_msg)
                except:
                    error_msg = response.text[:100]
                raise Exception(f"{error_msg}")
                
            result = response.json()
            response_text = result.get("response", "")
            
            if not response_text:
                raise Exception("Empty response from model")
            
            processing_time = time.time() - start_time
            logger.info(f"✅ {node_name} processed in {processing_time:.2f}s")
            
            # Parse the response with flexible matching
            tags_match = re.search(r"TAGS:\s*(.+)", response_text, re.IGNORECASE)
            summary_match = re.search(r"SUMMARY:\s*(.+)", response_text, re.IGNORECASE)
            concepts_match = re.search(r"CONCEPTS:\s*(.+)", response_text, re.IGNORECASE)
            
            # Fallback: if standard format fails, try to extract any lists
            tags = tags_match.group(1).strip() if tags_match else self.extract_fallback_list(response_text, "tags")
            summary = summary_match.group(1).strip() if summary_match else self.extract_fallback_summary(response_text)
            concepts = concepts_match.group(1).strip() if concepts_match else self.extract_fallback_list(response_text, "concepts")
            
            # Update node status on success
            self.nodes[node_name]["error_count"] = 0
            self.nodes[node_name]["last_used"] = time.time()
            
            return {
                "tags": tags,
                "summary": summary, 
                "concepts": concepts,
                "processing_time": processing_time
            }
            
        except Exception as e:
            error_msg = str(e)
            self.nodes[node_name]["error_count"] += 1
            self.nodes[node_name]["last_error"] = error_msg
            logger.error(f"❌ {node_name} failed: {error_msg}")
            raise
    
    def extract_fallback_list(self, text, list_type):
        """Fallback extraction for lists if format doesn't match exactly"""
        # Look for any comma-separated list
        lines = text.split('\n')
        for line in lines:
            if ':' in line and len(line.split(':')) > 1:
                key, value = line.split(':', 1)
                if list_type in key.lower() and value.strip():
                    return value.strip()
        return f"{list_type}-not-found"
    
    def extract_fallback_summary(self, text):
        """Fallback extraction for summary"""
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if 'summary' in line.lower() and i + 1 < len(lines):
                return lines[i + 1].strip()
        return "Summary not available"

# Initialize node manager
node_manager = NodeManager(NODES)

def html_to_markdown(html_file):
    """Convert HTML to Markdown using python-html2text library"""
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        converter.ignore_images = True
        converter.ignore_emphasis = False
        converter.body_width = 0
        
        markdown = converter.handle(html_content)
        return markdown.strip()
    except Exception as e:
        logger.error(f"HTML to Markdown conversion failed: {str(e)}")
        return None

def create_obsidian_note(md_content, metadata, filename):
    """Create Obsidian note with YAML frontmatter"""
    clean_tags = metadata['tags'].replace('"', '').replace("'", "")
    clean_concepts = metadata['concepts'].replace('"', '').replace("'", "")
    
    frontmatter = (
        "---\n"
        f"title: '{Path(filename).stem}'\n"
        f"date: {datetime.now().strftime('%Y-%m-%d')}\n"
        f"tags: [{clean_tags}]\n"
        f"concepts: [{clean_concepts}]\n"
        "---\n\n"
    )
    
    note_content = (
        f"{frontmatter}"
        f"## Summary\n{metadata['summary']}\n\n"
        "---\n\n"
        "## Content\n"
        f"{md_content}"
    )
    
    return note_content

def process_single_file(file, output_dir):
    """Process a single HTML file"""
    try:
        logger.info(f"📄 Processing: {file.name}")
        
        # Convert HTML to Markdown
        md_content = html_to_markdown(file)
        if not md_content:
            logger.warning(f"⏭️ Skipping {file.name} - conversion failed")
            return False
        
        # Get available node
        target_node = node_manager.get_available_node()
        if not target_node:
            logger.error(f"❌ No available nodes for {file.name}")
            return False
        
        logger.info(f"🔧 Using {target_node} for {file.name}")
        
        # Extract metadata
        metadata = node_manager.extract_metadata(md_content, target_node)
        
        # Create Obsidian note
        note_content = create_obsidian_note(md_content, metadata, file.name)
        output_file = output_dir / f"{file.stem}.md"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(note_content)
        
        logger.info(f"✅ Created: {output_file.name}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed {file.name}: {str(e)}")
        return False

def main():
    home_dir = Path.home()
    download_dir = home_dir / "/media/ibo/512SSDUSB/DeepSeek_html"
    obsidian_dir = home_dir / "Obsidian"
    
    logger.info("🚀 Starting Distributed Obsidian Processor")
    logger.info(f"📁 Source: {download_dir}")
    logger.info(f"💾 Target: {obsidian_dir}")
    
    # Display node status
    logger.info("🔍 Node Status:")
    for node, info in node_manager.nodes.items():
        status_icon = "✅" if info["status"] == "available" else "❌"
        models = info["available_models"] if info["available_models"] else "NO WORKING MODELS"
        logger.info(f"  {status_icon} {node}: {info['status']} | Models: {models}")
    
    # Check if we have any working nodes
    available_nodes = [n for n, info in node_manager.nodes.items() 
                      if info["status"] == "available"]
    if not available_nodes:
        logger.error("💥 CRITICAL: No working nodes available! Exiting.")
        return
    
    # Create directories
    obsidian_dir.mkdir(exist_ok=True, parents=True)
    
    # Process HTML files
    html_files = list(download_dir.glob("*.html"))
    logger.info(f"📊 Found {len(html_files)} HTML files to process")
    
    # Process files sequentially for stability
    processed = 0
    for i, file in enumerate(html_files):
        logger.info(f"📦 Progress: {i+1}/{len(html_files)}")
        if process_single_file(file, obsidian_dir):
            processed += 1
        # Small delay between files
        time.sleep(1)
    
    # Final report
    logger.info("📈 Final Report:")
    for node, info in node_manager.nodes.items():
        status = "✅" if info["error_count"] == 0 else f"❌ (errors: {info['error_count']})"
        logger.info(f"  {status} {node}: {info.get('last_error', 'No errors')}")
    
    logger.info(f"🎉 Processed {processed}/{len(html_files)} files successfully")

if __name__ == "__main__":
    main()
```




