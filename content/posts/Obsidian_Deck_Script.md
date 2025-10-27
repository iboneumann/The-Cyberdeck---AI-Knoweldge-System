+++
date = '2025-10-23T18:31:51+02:00'
draft = false
title = 'The Obsidian Deck Script'
weight = 5
+++

```bash
import os
import re
import cmd
import yaml
import sys
import argparse
import webbrowser
import urllib.parse
import networkx as nx
import subprocess
import tempfile
import shutil
import time
import threading
import colorsys
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from collections import defaultdict, deque
from datetime import datetime
from textwrap import wrap
import json
import math

class ObsidianKnowledgeExplorer(cmd.Cmd):
    intro = "\n🧠 CYBERDECK KNOWLEDGE EXPLORER\nType 'help' for commands. 'exit' to quit.\n"
    prompt = "obsidian> "
    SUMMARY_MODELS = {
        "mixtral:8x7b": "ollama run mixtral:8x7b",
        "llama3:latest": "ollama run llama3"
    }
    DEBUG = False
    PROCESSING = False

    def __init__(self, vault_path: str):
        super().__init__()
        self.vault_path = vault_path
        self.graph = nx.Graph()
        self.notes = {}
        self.current_cluster = set()
        self.core_cluster = set()
        self.current_cluster_type = None
        self.current_cluster_name = None
        self.summary_model = "llama3:latest"
        self.output_mode = "terminal"
        self.indices_dir = os.path.join(os.path.expanduser("~"), "Vault", "indices")
        self.summaries_dir = os.path.join(os.path.expanduser("~"), "Vault", "summaries")
        self.graphs_dir = os.path.join(self.indices_dir, "graphs")
        self.chat_history = []
        os.makedirs(self.indices_dir, exist_ok=True)
        os.makedirs(self.summaries_dir, exist_ok=True)
        os.makedirs(self.graphs_dir, exist_ok=True)
        self._index_vault()
        print(f"✅ Vault indexed: {len(self.notes)} notes")
        print(f"🧠 Available NLP models: {', '.join(self.SUMMARY_MODELS.keys())}")
        print(f"📤 Output mode: {self.output_mode}")

    def _parse_frontmatter(self, content: str) -> dict:
        fm = {}
        fm_match = re.search(r'^---\s*\n(.+?)\n---', content, re.DOTALL)
        if fm_match:
            try:
                fm = yaml.safe_load(fm_match.group(1))
            except yaml.YAMLError:
                pass
        return fm or {}

    def _index_vault(self):
        self.graph.clear()
        self.notes = {}
        for file in os.listdir(self.vault_path):
            if not file.endswith('.md'):
                continue
            path = os.path.join(self.vault_path, file)
            note_name = os.path.splitext(file)[0]
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception as e:
                if self.DEBUG:
                    print(f"⚠️ Error reading {file}: {str(e)}")
                continue
            word_count = len(re.findall(r'\w+', content))
            fm = self._parse_frontmatter(content)
            summary = ""
            summary_match = re.search(r'^## Summary\n(.+?)(?=\n## |\Z)', content, re.DOTALL | re.IGNORECASE)
            if summary_match:
                summary = summary_match.group(1).strip()
            content_tags = set(re.findall(r'(?<!#)\B#([a-zA-Z0-9_\/-]+)\b', content))
            def safe_get(field, default=None):
                value = fm.get(field, default)
                return value if value is not None else default
            meta_tags = set()
            for mt in safe_get('meta_tags', []):
                if isinstance(mt, str):
                    clean_mt = re.sub(r'[\[\]]', '', mt).strip()
                    if clean_mt:
                        meta_tags.add(clean_mt)
            tags = set(safe_get('tags', [])) | content_tags
            concepts = set(safe_get('concepts', []))
            keywords = set(safe_get('keywords', []))
            note_data = {
                'path': path,
                'content': content,
                'summary': summary,
                'word_count': word_count,
                'frontmatter': fm,
                'tags': tags,
                'meta_tags': meta_tags,
                'concepts': concepts,
                'keywords': keywords
            }
            self.notes[note_name] = note_data
            self.graph.add_node(note_name)
            for link in re.findall(r'\[\[(.*?)\]\]', content):
                target = link.split('|')[0].split('#')[0].strip()
                if target and target in self.notes:
                    self.graph.add_edge(note_name, target)

    def do_combine_cluster(self, arg):
        """Combine multiple tags/concepts: COMBINE_CLUSTER [AND|OR] tag1,tag2 OR concept1,concept2"""
        if not arg:
            print("❌ Format: COMBINE_CLUSTER [AND|OR] tag1,tag2 OR concept1,concept2")
            return
        
        args = arg.split(maxsplit=2)
        if len(args) < 3:
            print("❌ Format: COMBINE_CLUSTER [AND|OR] [tag|concept|meta_tag|meta_keyword] value1,value2")
            return
            
        logic, cluster_type, values_str = args
        logic = logic.upper()
        
        if logic not in ["AND", "OR"]:
            print("❌ Logic must be AND or OR")
            return
            
        if cluster_type not in ["tag", "concept", "meta_tag", "meta_keyword"]:
            print("❌ Type must be: tag, concept, meta_tag, or meta_keyword")
            return
            
        values = [v.strip() for v in values_str.split(',')]
        self.current_cluster = set()
        self.current_cluster_type = f"combined_{cluster_type}"
        self.current_cluster_name = f"{logic}({', '.join(values)})"
        
        if logic == "AND":
            # Find notes that have ALL the specified values
            for note, data in self.notes.items():
                field_data = data[cluster_type + 's']  # tags -> data['tags']
                if all(value in field_data for value in values):
                    self.current_cluster.add(note)
        else:  # OR logic
            # Find notes that have ANY of the specified values
            for note, data in self.notes.items():
                field_data = data[cluster_type + 's']
                if any(value in field_data for value in values):
                    self.current_cluster.add(note)
                    
        self.core_cluster = set(self.current_cluster)
        print(f"🧩 Combined cluster defined: {len(self.current_cluster)} notes with {logic} {cluster_type}(s): {', '.join(values)}")

    def do_set_output(self, arg):
        """Set output mode: SET_OUTPUT [terminal|file|both]"""
        if arg in ["terminal", "file", "both"]:
            self.output_mode = arg
            print(f"📤 Output mode set to: {arg}")
        else:
            print("❌ Invalid mode. Use: terminal, file, both")

    def do_cluster(self, arg):
        """Define a note cluster: CLUSTER [all|tag|concept|meta_tag|meta_keyword] [name]"""
        if not arg:
            print("❌ Please specify cluster type and name")
            return
        
        # Find the first word (cluster type) and the rest as name
        parts = arg.split(maxsplit=1)
        if len(parts) < 2:
            print("❌ Format: CLUSTER [type] [name]")
            print("Types: all, tag, concept, meta_tag, meta_keyword")
            return
            
        cluster_type, name = parts[0].lower(), parts[1]
        self.current_cluster = set()
        self.current_cluster_type = cluster_type
        self.current_cluster_name = name
        
        if cluster_type == "all":
            for note, data in self.notes.items():
                if (name in data['tags'] or 
                    name in data['concepts'] or 
                    name in data['meta_tags'] or 
                    name in data['keywords']):
                    self.current_cluster.add(note)
        elif cluster_type == "tag":
            for note, data in self.notes.items():
                if name in data['tags']:
                    self.current_cluster.add(note)
        elif cluster_type == "concept":
            for note, data in self.notes.items():
                if name in data['concepts']:
                    self.current_cluster.add(note)
        elif cluster_type == "meta_tag":
            for note, data in self.notes.items():
                if name in data['meta_tags']:
                    self.current_cluster.add(note)
        elif cluster_type == "meta_keyword":
            for note, data in self.notes.items():
                if name in data['keywords']:
                    self.current_cluster.add(note)
        else:
            print("❌ Invalid cluster type. Use: all, tag, concept, meta_tag, meta_keyword")
            return
            
        self.core_cluster = set(self.current_cluster)
        print(f"🧩 Cluster defined: {len(self.current_cluster)} notes with {cluster_type} '{name}'")

    def do_remove(self, arg):
        """Remove files from current cluster by number: REMOVE 2 or REMOVE 2 5 7"""
        if not self.current_cluster:
            print("❌ No cluster defined. Use CLUSTER first")
            return
            
        # Get numbered list of current cluster
        cluster_list = sorted(self.current_cluster)
        if not cluster_list:
            print("❌ Current cluster is empty")
            return
            
        print("\nCurrent cluster files:")
        for i, note in enumerate(cluster_list, 1):
            print(f"{i}. {note}")
            
        if not arg:
            print("❌ Please specify file numbers to remove")
            return
            
        try:
            # Parse numbers (can be single or multiple)
            numbers = [int(n.strip()) for n in arg.split()]
            numbers_to_remove = set()
            
            for num in numbers:
                if 1 <= num <= len(cluster_list):
                    numbers_to_remove.add(num - 1)  # Convert to 0-based index
                else:
                    print(f"⚠️ Invalid number: {num}. Must be between 1 and {len(cluster_list)}")
                    
            if not numbers_to_remove:
                print("❌ No valid numbers to remove")
                return
                
            # Remove from current cluster
            notes_to_remove = [cluster_list[i] for i in numbers_to_remove]
            self.current_cluster -= set(notes_to_remove)
            
            # Also remove from core cluster if present
            self.core_cluster -= set(notes_to_remove)
            
            print(f"✅ Removed {len(notes_to_remove)} files from cluster:")
            for note in notes_to_remove:
                print(f"  - {note}")
            print(f"📊 Cluster now has {len(self.current_cluster)} notes")
            
        except ValueError:
            print("❌ Please enter valid numbers (e.g., 'remove 2' or 'remove 2 5 7')")

    def do_list_tags(self, arg):
        """List all tags: LIST_TAGS [--output FILE|TERMINAL]"""
        args = arg.split()
        output_mode = self._parse_output_arg(args)
        tag_index = defaultdict(set)
        for note_name, data in self.notes.items():
            for tag in data['tags']:
                tag_index[tag].add(note_name)
        report_lines = [
            "# TAG INDEX\n",
            "| Tag | Files |",
            "|-----|-------|"
        ]
        sorted_tags = sorted(tag_index.items(), key=lambda x: x[0].lower())
        for tag, files in sorted_tags:
            file_list = ", ".join(sorted(files))
            report_lines.append(f"| #{tag} | {file_list} |")
        report_content = "\n".join(report_lines)
        if output_mode in ["terminal", "both"]:
            self._display_paginated(
                data=sorted_tags,
                title="TAG INDEX",
                formatter=lambda tag, files: (
                    f"#{tag} ({len(files)} files):\n" +
                    self._wrap_file_list(sorted(files))
                ),
                output_mode=output_mode
            )
        if output_mode in ["file", "both"]:
            self._write_to_file("Tag Index", report_content, "tag_index")

    def do_list_concepts(self, arg):
        """List all concepts: LIST_CONCEPTS [--output FILE|TERMINAL]"""
        args = arg.split()
        output_mode = self._parse_output_arg(args)
        concept_index = defaultdict(set)
        for note_name, data in self.notes.items():
            for concept in data['concepts']:
                concept_index[concept].add(note_name)
        report_lines = [
            "# CONCEPT INDEX\n",
            "| Concept | Files |",
            "|---------|-------|"
        ]
        sorted_concepts = sorted(concept_index.items(), key=lambda x: x[0].lower())
        for concept, files in sorted_concepts:
            file_list = ", ".join(sorted(files))
            report_lines.append(f"| {concept} | {file_list} |")
        report_content = "\n".join(report_lines)
        if output_mode in ["terminal", "both"]:
            self._display_paginated(
                data=sorted_concepts,
                title="CONCEPT INDEX",
                formatter=lambda concept, files: (
                    f"{concept} ({len(files)} files):\n" +
                    self._wrap_file_list(sorted(files))
                ),
                output_mode=output_mode
            )
        if output_mode in ["file", "both"]:
            self._write_to_file("Concept Index", report_content, "concept_index")

    def do_list_meta_tags(self, arg):
        """List all meta tags: LIST_META_TAGS [--output FILE|TERMINAL]"""
        args = arg.split()
        output_mode = self._parse_output_arg(args)
        meta_tag_index = defaultdict(set)
        for note_name, data in self.notes.items():
            for meta_tag in data['meta_tags']:
                meta_tag_index[meta_tag].add(note_name)
        report_lines = [
            "# META TAG INDEX\n",
            "| Meta Tag | Files |",
            "|----------|-------|"
        ]
        sorted_meta_tags = sorted(meta_tag_index.items(), key=lambda x: x[0].lower())
        for meta_tag, files in sorted_meta_tags:
            file_list = ", ".join(sorted(files))
            report_lines.append(f"| {meta_tag} | {file_list} |")
        report_content = "\n".join(report_lines)
        if output_mode in ["terminal", "both"]:
            self._display_paginated(
                data=sorted_meta_tags,
                title="META TAG INDEX",
                formatter=lambda meta_tag, files: (
                    f"{meta_tag} ({len(files)} files):\n" +
                    self._wrap_file_list(sorted(files))
                ),
                output_mode=output_mode
            )
        if output_mode in ["file", "both"]:
            self._write_to_file("Meta Tag Index", report_content, "meta_tag_index")

    def do_list_keywords(self, arg):
        """List all keywords: LIST_KEYWORDS [--output FILE|TERMINAL]"""
        args = arg.split()
        output_mode = self._parse_output_arg(args)
        keyword_index = defaultdict(set)
        for note_name, data in self.notes.items():
            for keyword in data['keywords']:
                keyword_index[keyword].add(note_name)
        report_lines = [
            "# KEYWORD INDEX\n",
            "| Keyword | Files |",
            "|---------|-------|"
        ]
        sorted_keywords = sorted(keyword_index.items(), key=lambda x: x[0].lower())
        for keyword, files in sorted_keywords:
            file_list = ", ".join(sorted(files))
            report_lines.append(f"| {keyword} | {file_list} |")
        report_content = "\n".join(report_lines)
        if output_mode in ["terminal", "both"]:
            self._display_paginated(
                data=sorted_keywords,
                title="KEYWORD INDEX",
                formatter=lambda keyword, files: (
                    f"{keyword} ({len(files)} files):\n" +
                    self._wrap_file_list(sorted(files))
                ),
                output_mode=output_mode
            )
        if output_mode in ["file", "both"]:
            self._write_to_file("Keyword Index", report_content, "keyword_index")

    def do_list_contents(self, arg):
        """List all files with metadata: LIST_CONTENTS [--output FILE|TERMINAL]"""
        args = arg.split()
        output_mode = self._parse_output_arg(args)
        report_lines = [
            "# VAULT CONTENTS INDEX\n",
            "| File | Word Count | Tags | Concepts | Summary Preview |",
            "|------|------------|------|----------|-----------------|"
        ]
        sorted_notes = sorted(self.notes.items(), key=lambda x: x[0].lower())
        for note_name, data in sorted_notes:
            tags = ", ".join([f"#{t}" for t in sorted(data['tags'])])
            concepts = ", ".join(sorted(data['concepts']))
            preview = (data['summary'][:100] + '...') if data['summary'] else ""
            report_lines.append(f"| {note_name} | {data['word_count']} | {tags} | {concepts} | {preview} |")
        report_content = "\n".join(report_lines)
        if output_mode in ["terminal", "both"]:
            terminal_width = shutil.get_terminal_size().columns
            max_note_width = max(len(name) for name in self.notes.keys()) if self.notes else 30
            max_note_width = min(max_note_width, terminal_width - 20)
            print("\n" + "=" * terminal_width)
            print(f"{'File':<{max_note_width}} | {'Words'} | {'Tags'}")
            print("-" * max_note_width + "-|-------|" + "-" * (terminal_width - max_note_width - 10))
            for note_name, data in sorted_notes:
                tags = ", ".join([f"#{t}" for t in sorted(data['tags'])])
                print(f"{note_name:<{max_note_width}} | {data['word_count']:>5}   | {tags}")
            print("=" * terminal_width)
        if output_mode in ["file", "both"]:
            self._write_to_file("Vault Contents", report_content, "vault_contents")

    def do_show_cluster(self, arg):
        """Display current cluster with perfect formatting"""
        if not self.current_cluster:
            print("❌ No cluster defined. Use CLUSTER first")
            return
            
        total_words = 0
        cluster_details = []
        for note in self.current_cluster:
            if note not in self.notes:
                continue
            data = self.notes[note]
            total_words += data['word_count']
            tags = ", ".join([f"#{t}" for t in sorted(data['tags'])])
            cluster_details.append({
                "name": note,
                "word_count": data['word_count'],
                "tags": tags
            })
        cluster_details.sort(key=lambda x: x['word_count'], reverse=True)
        
        report_lines = [
            f"# Cluster Report: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- **Cluster size**: {len(self.current_cluster)} notes",
            f"- **Total words**: {total_words}",
            f"- **Cluster type**: {self.current_cluster_type}",
            f"- **Cluster name**: {self.current_cluster_name}",
            "\n## Notes in Cluster:",
            "| Note Name | Word Count | Tags |",
            "|-----------|------------|------|"
        ]
        for detail in cluster_details:
            report_lines.append(f"| {detail['name']} | {detail['word_count']} | {detail['tags']} |")
        report_content = "\n".join(report_lines)
        
        if self.output_mode in ["terminal", "both"]:
            terminal_width = shutil.get_terminal_size().columns
            max_note_width = max(len(d['name']) for d in cluster_details) if cluster_details else 30
            max_note_width = min(max_note_width, terminal_width - 20)
            print("\n" + "=" * terminal_width)
            print(f"{'File':<{max_note_width}} | {'Words'} | {'Tags'}")
            print("-" * max_note_width + "-|-------|" + "-" * (terminal_width - max_note_width - 10))
            for detail in cluster_details:
                print(f"{detail['name']:<{max_note_width}} | {detail['word_count']:>5}   | {detail['tags']}")
            print("=" * terminal_width)
            print(f"Total notes: {len(cluster_details)} | Total words: {total_words}")
            print("=" * terminal_width)
            
        # ALWAYS save show_cluster output to indices directory
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', self.current_cluster_name)[:50] if self.current_cluster_name else "cluster"
        filename = f"Cluster_Report_{safe_name}_{timestamp}.md"
        file_path = os.path.join(self.indices_dir, filename)
        with open(file_path, "w") as f:
            f.write(report_content)
        print(f"💾 Cluster report saved to: {file_path}")

    def do_summarize(self, arg):
        """Generate AI summary: SUMMARIZE [summary|deep]"""
        if not self.current_cluster:
            print("❌ No cluster defined. Use CLUSTER first")
            return
            
        summary_type = arg.lower() if arg else "summary"
        if summary_type not in ["summary", "deep"]:
            print("❌ Invalid type. Use: summary or deep")
            return
            
        prompt = self._generate_prompt("summary" if summary_type == "summary" else "deep_summary")
        print(f"\n🧠 Generating {summary_type} summary using {self.summary_model}...")
        print("⏳ This may take several minutes...")
        print("💡 Press Ctrl+C to cancel and return to prompt")
        
        try:
            self.PROCESSING = True
            progress_thread = threading.Thread(target=self._show_progress)
            progress_thread.daemon = True
            progress_thread.start()
            
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                f.write(prompt)
                tmp_path = f.name
                
            cmd_str = f"{self.SUMMARY_MODELS[self.summary_model]} < {tmp_path}"
            process = subprocess.Popen(
                cmd_str,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )
            stdout, stderr = process.communicate(timeout=3600)
            os.unlink(tmp_path)
            self.PROCESSING = False
            progress_thread.join(timeout=1)
            
            if process.returncode != 0:
                print(f"❌ Model error: {stderr}")
                return
                
            summary = stdout
            
            # ALWAYS save summarize output to summaries directory
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            safe_name = re.sub(r'[^a-zA-Z0-9]', '_', self.current_cluster_name)[:50] if self.current_cluster_name else "cluster"
            summary_path = os.path.join(self.summaries_dir, f"Summary_{summary_type}_{safe_name}_{timestamp}.md")
            
            summary_content = f"""# {summary_type.capitalize()} Summary: {self.current_cluster_name}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Model**: {self.summary_model}
**Cluster Type**: {self.current_cluster_type}
**Notes in Cluster**: {len(self.current_cluster)}

## Summary:
{summary}

## Cluster Details:
- **Total notes**: {len(self.current_cluster)}
- **Cluster type**: {self.current_cluster_type}
- **Cluster name**: {self.current_cluster_name}
- **Generated by**: Obsidian Knowledge Explorer
"""
            
            with open(summary_path, "w") as f:
                f.write(summary_content)
            
            if self.output_mode in ["terminal", "both"]:
                print("\n" + "="*80)
                print(f"📝 {summary_type.capitalize()} Summary:")
                print("="*80)
                print(summary)
                print("="*80)
                
            print(f"💾 Summary saved to: {summary_path}")
            
        except subprocess.TimeoutExpired:
            self.PROCESSING = False
            print("❌ Model timeout: Try a smaller cluster or faster model")
        except KeyboardInterrupt:
            self.PROCESSING = False
            print("🚫 Summarization canceled")
        except Exception as e:
            self.PROCESSING = False
            print(f"❌ Error: {str(e)}")

    def do_model(self, arg):
        """Switch NLP model: MODEL [mixtral:8x7b|llama3:latest]"""
        if not arg:
            print(f"Current model: {self.summary_model}")
            return
        if arg in self.SUMMARY_MODELS:
            self.summary_model = arg
            print(f"🧠 NLP model set to: {arg}")
        else:
            print(f"❌ Invalid model. Choose from: {', '.join(self.SUMMARY_MODELS.keys())}")

    def do_bfs_cluster(self, arg):
        """Expand cluster via relationships: BFS_CLUSTER [depth=2]"""
        if not self.current_cluster:
            print("❌ No cluster defined")
            return
        try:
            depth = int(arg) if arg else 2
            new_notes = set()
            for note in self.current_cluster:
                if note not in self.graph:
                    continue
                visited = set([note])
                queue = [(note, 0)]
                while queue:
                    current, current_depth = queue.pop(0)
                    if current_depth >= depth:
                        continue
                    for neighbor in self.graph.neighbors(current):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append((neighbor, current_depth + 1))
                new_notes |= visited
            self.current_cluster = new_notes
            print(f"🧩 Cluster expanded to {len(self.current_cluster)} notes at depth {depth}")
        except ValueError:
            print("❌ Please enter a valid integer depth")

    def _compute_node_depths(self, max_depth=5):
        if not self.current_cluster or not self.core_cluster:
            return {}
        depths = {}
        queue = deque()
        for note in self.core_cluster:
            if note in self.current_cluster:
                depths[note] = 0
                queue.append(note)
        while queue:
            current = queue.popleft()
            current_depth = depths[current]
            if current_depth >= max_depth:
                continue
            for neighbor in self.graph.neighbors(current):
                if neighbor in self.current_cluster and neighbor not in depths:
                    depths[neighbor] = current_depth + 1
                    queue.append(neighbor)
        return depths

    def do_visualize_cluster(self, arg):
        """Open cluster in Obsidian: VISUALIZE_CLUSTER [max_depth=5]"""
        if not self.current_cluster:
            print("❌ No cluster to visualize")
            return
        max_depth = 5
        if arg:
            try:
                max_depth = int(arg)
            except ValueError:
                print("⚠️ Using default max_depth=5. Provide integer for custom depth.")
        os.makedirs(self.indices_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', self.current_cluster_name)[:50] if self.current_cluster_name else "cluster"
        report_path = os.path.join(self.indices_dir, f"Cluster_Visual_{safe_name}_{timestamp}.md")
        depths = self._compute_node_depths(max_depth)
        def depth_to_color(depth, max_depth):
            normalized = min(depth / max_depth, 1.0)
            r = 1.0
            g = max(0.3, 1.0 - normalized * 0.7)
            b = max(0.3, 1.0 - normalized * 0.7)
            return f"#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}"
        mermaid_lines = [
            "```mermaid",
            "graph LR"
        ]
        for note in self.current_cluster:
            depth = depths.get(note, max_depth)
            color = depth_to_color(depth, max_depth)
            node_id = re.sub(r'[^a-zA-Z0-9_]', '_', note)
            display_name = note if len(note) <= 30 else note[:27] + "..."
            mermaid_lines.append(f"    {node_id}[\"{display_name}\"]:::depth{depth}")
        for note in self.current_cluster:
            for neighbor in self.graph.neighbors(note):
                if neighbor in self.current_cluster and note < neighbor:
                    node_id1 = re.sub(r'[^a-zA-Z0-9_]', '_', note)
                    node_id2 = re.sub(r'[^a-zA-Z0-9_]', '_', neighbor)
                    mermaid_lines.append(f"    {node_id1} --- {node_id2}")
        for depth in range(max_depth + 1):
            color = depth_to_color(depth, max_depth)
            mermaid_lines.append(f"    classDef depth{depth} fill:{color},stroke:#333,stroke-width:2px,color:#000")
        mermaid_lines.append("```")
        report_content = f"""# Cluster Visualization: {self.current_cluster_name}
**Type**: {self.current_cluster_type} | **Notes**: {len(self.current_cluster)} | **Core**: {len(self.core_cluster)}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Core nodes** (depth 0) are shown in red.  
**Related nodes** get lighter colors with increasing depth.

{'\\n'.join(mermaid_lines)}

## Notes in Cluster:
"""
        for note in sorted(self.current_cluster):
            depth = depths.get(note, "N/A")
            report_content += f"- [[{note}]] (Depth: {depth})\n"
        with open(report_path, "w") as f:
            f.write(report_content)
        file_path = f"indices/Cluster_Visual_{safe_name}_{timestamp}.md"
        params = {
            'vault': urllib.parse.quote(self.vault_path, safe=''),
            'file': urllib.parse.quote(file_path, safe='')
        }
        uri = f"obsidian://open?{urllib.parse.urlencode(params)}"
        try:
            if shutil.which('flatpak'):
                result = subprocess.run(
                    ['flatpak', 'list', '--app', '--columns=application'],
                    capture_output=True, text=True
                )
                if 'md.obsidian.Obsidian' in result.stdout:
                    subprocess.Popen([
                        'flatpak', 'run', 'md.obsidian.Obsidian', 
                        f'obsidian://open?{urllib.parse.urlencode(params)}'
                    ])
                    print(f"🔗 Opening via Flatpak: {file_path}")
                else:
                    if sys.platform == 'win32':
                        os.startfile(uri)
                    elif sys.platform == 'darwin':
                        subprocess.Popen(['open', uri])
                    else:
                        subprocess.Popen(['xdg-open', uri])
            else:
                if sys.platform == 'win32':
                    os.startfile(uri)
                elif sys.platform == 'darwin':
                    subprocess.Popen(['open', uri])
                else:
                    subprocess.Popen(['xdg-open', uri])
        except Exception as e:
            print(f"⚠️ Error opening Obsidian: {str(e)}")
            print(f"ℹ️ You can manually open: {uri}")
        print(f"🔗 Created color-coded cluster visualization: {file_path}")
        print("ℹ️ If diagram doesn't render, install Obsidian Mermaid plugin")

    def do_cluster_graph(self, arg):
        """Generate static cluster image: CLUSTER_GRAPH [format=png|jpg]"""
        if not self.current_cluster:
            print("❌ No cluster defined. Use CLUSTER first")
            return
        img_format = "png"
        if arg and arg.split()[0].lower() in ["png", "jpg"]:
            img_format = arg.split()[0].lower()
        G_vis = nx.Graph()
        metadata_fields = ['tags', 'concepts', 'meta_tags', 'meta_keyword']
        cluster_node_id = f"{self.current_cluster_type}_{self.current_cluster_name}"
        G_vis.add_node(cluster_node_id, 
                       label=self.current_cluster_name,
                       type="cluster",
                       group=0,
                       size=30)
        for note in self.current_cluster:
            if note not in self.notes:
                continue
            data = self.notes[note]
            is_core = note in self.core_cluster
            G_vis.add_node(note,
                           label=note,
                           type="note",
                           group=1 if is_core else 2,
                           size=20,
                           path=data['path'])
            G_vis.add_edge(cluster_node_id, note)
            for field in metadata_fields:
                for item in data[field]:
                    clean_item = re.sub(r'[\[\]]', '', item).strip()
                    if not clean_item:
                        continue
                    G_vis.add_node(clean_item,
                                   label=clean_item,
                                   type="metadata",
                                   group=3,
                                   size=15)
                    G_vis.add_edge(note, clean_item)
        plt.figure(figsize=(16, 16), dpi=300)
        shells = [[cluster_node_id]]
        core_nodes = [n for n in self.core_cluster if n in G_vis.nodes]
        expanded_nodes = [n for n in (self.current_cluster - self.core_cluster) if n in G_vis.nodes]
        metadata_nodes = [n for n in G_vis.nodes if G_vis.nodes[n]['type'] == "metadata"]
        if core_nodes: shells.append(core_nodes)
        if expanded_nodes: shells.append(expanded_nodes)
        if metadata_nodes: shells.append(metadata_nodes)
        pos = nx.shell_layout(G_vis, shells)
        node_colors = []
        node_sizes = []
        for node in G_vis.nodes:
            node_type = G_vis.nodes[node]['type']
            if node_type == "cluster":
                node_colors.append('#4fc3f7')  # Blue
                node_sizes.append(2000)
            elif node_type == "note":
                if node in self.core_cluster:
                    node_colors.append('#f44336')  # Red
                    node_sizes.append(800)
                else:
                    node_colors.append('#ff9800')  # Orange
                    node_sizes.append(600)
            else:  # metadata
                node_colors.append('#9c27b0')  # Purple
                node_sizes.append(1200)
        nx.draw_networkx_nodes(
            G_vis, pos,
            node_color=node_colors,
            node_size=node_sizes,
            edgecolors="#222222",
            linewidths=1.0
        )
        nx.draw_networkx_edges(
            G_vis, pos,
            edge_color="#555555",
            alpha=0.6,
            width=1.0
        )
        label_nodes = {node: node for node in G_vis.nodes 
                      if G_vis.nodes[node]['type'] == "cluster" or 
                      (G_vis.nodes[node]['type'] == "note" and node in self.core_cluster)}
        nx.draw_networkx_labels(
            G_vis, pos,
            labels=label_nodes,
            font_size=8,
            font_weight="bold",
            font_color="#ffffff"
        )
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4fc3f7', markersize=10, label='Cluster'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#f44336', markersize=10, label='Core Notes'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#ff9800', markersize=10, label='Expanded Notes'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#9c27b0', markersize=10, label='Metadata')
        ]
        plt.legend(handles=legend_elements, loc='best')
        plt.title(f"Cluster: {self.current_cluster_type} '{self.current_cluster_name}'\n"
                  f"Core Notes: {len(self.core_cluster)} | Expanded: {len(self.current_cluster)-len(self.core_cluster)}",
                  fontsize=14)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', self.current_cluster_name)[:50] if self.current_cluster_name else "cluster"
        filename = f"Cluster_Graph_{safe_name}_{timestamp}.{img_format}"
        filepath = os.path.join(self.graphs_dir, filename)
        plt.savefig(filepath, bbox_inches="tight", dpi=300)
        plt.close()
        print(f"🖼️ Static cluster graph saved to: {filepath}")
        print(f"📊 Core notes: {len(self.core_cluster)} | Expanded: {len(self.current_cluster)-len(self.core_cluster)}")

    def do_cluster_html(self, arg):
        """Generate interactive cluster visualization: CLUSTER_HTML [filename]"""
        if not self.current_cluster:
            print("❌ No cluster defined. Use CLUSTER first")
            return
        default_name = f"cluster_{self.current_cluster_name}.html"
        filename = arg.strip() if arg else default_name
        if not filename.endswith('.html'):
            filename += '.html'
        G_vis = nx.Graph()
        metadata_fields = ['tags', 'concepts', 'meta_tags', 'meta_keyword']
        cluster_node_id = f"{self.current_cluster_type}_{self.current_cluster_name}"
        G_vis.add_node(cluster_node_id, 
                       label=self.current_cluster_name,
                       type="cluster",
                       group=0,
                       size=30)
        for note in self.current_cluster:
            if note not in self.notes:
                continue
            data = self.notes[note]
            is_core = note in self.core_cluster
            G_vis.add_node(note,
                           label=note,
                           type="note",
                           group=1 if is_core else 2,
                           size=20,
                           path=data['path'])
            G_vis.add_edge(cluster_node_id, note)
            for field in metadata_fields:
                for item in data[field]:
                    clean_item = re.sub(r'[\[\]]', '', item).strip()
                    if not clean_item:
                        continue
                    G_vis.add_node(clean_item,
                                   label=clean_item,
                                   type="metadata",
                                   group=3,
                                   size=15)
                    G_vis.add_edge(note, clean_item)
        nodes = []
        links = []
        node_index = {node: idx for idx, node in enumerate(G_vis.nodes)}
        for node, data in G_vis.nodes(data=True):
            node_data = {
                "id": node_index[node],
                "name": data['label'],
                "group": data['group'],
                "type": data['type'],
                "size": data['size']
            }
            if 'path' in data:
                node_data['path'] = data['path']
            nodes.append(node_data)
        for source, target in G_vis.edges():
            links.append({
                "source": node_index[source],
                "target": node_index[target],
                "value": 1
            })
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Knowledge Cluster: {self.current_cluster_name}</title>
    <meta charset="utf-8">
    <style>
        body {{ margin: 0; overflow: hidden; background: #1e1e1e; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                color: #e0e0e0; }}
        #header {{ position: absolute; top: 10px; left: 10px; z-index: 10; 
                  background: rgba(30, 30, 30, 0.85); padding: 15px; 
                  border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); 
                  max-width: 400px; }}
        #title {{ font-size: 1.8em; font-weight: bold; margin-bottom: 10px; color: #4fc3f7; }}
        #stats {{ font-size: 0.9em; margin-bottom: 15px; line-height: 1.4; }}
        #legend {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; }}
        .legend-item {{ display: flex; align-items: center; margin-right: 15px; }}
        .legend-color {{ width: 16px; height: 16px; border-radius: 50%; 
                         margin-right: 5px; border: 1px solid #555; }}
        .legend-cluster {{ background-color: #4fc3f7; }}
        .legend-core {{ background-color: #f44336; }}
        .legend-expanded {{ background-color: #ff9800; }}
        .legend-metadata {{ background-color: #9c27b0; }}
        #graph-container {{ width: 100vw; height: 100vh; }}
        .node {{ stroke: #fff; stroke-width: 1.5px; cursor: pointer; 
                 transition: all 0.3s ease; }}
        .node:hover {{ stroke: #ffeb3b; stroke-width: 3px; filter: brightness(1.2); }}
        .link {{ stroke: #555; stroke-opacity: 0.6; }}
        .node-label {{ font-size: 12px; text-shadow: 0 1px 3px rgba(0,0,0,0.8); 
                       pointer-events: none; font-weight: 600; }}
        .tooltip {{ position: absolute; padding: 8px 12px; 
                   background: rgba(30, 30, 30, 0.9); border: 1px solid #444; 
                   border-radius: 4px; pointer-events: none; font-size: 14px; 
                   max-width: 300px; backdrop-filter: blur(4px); 
                   box-shadow: 0 4px 12px rgba(0,0,0,0.5); }}
    </style>
</head>
<body>
    <div id="header">
        <div id="title">Knowledge Cluster: {self.current_cluster_name}</div>
        <div id="stats">
            <div>Type: {self.current_cluster_type}</div>
            <div>Core Notes: {len(self.core_cluster)}</div>
            <div>Expanded Notes: {len(self.current_cluster) - len(self.core_cluster)}</div>
            <div>Total Nodes: {len(nodes)}</div>
            <div>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        <div id="legend">
            <div class="legend-item"><div class="legend-color legend-cluster"></div>Cluster</div>
            <div class="legend-item"><div class="legend-color legend-core"></div>Core Notes</div>
            <div class="legend-item"><div class="legend-color legend-expanded"></div>Expanded Notes</div>
            <div class="legend-item"><div class="legend-color legend-metadata"></div>Metadata</div>
        </div>
    </div>
    <div id="graph-container"></div>
    
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <script>
        const nodes = {json.dumps(nodes, indent=4)};
        const links = {json.dumps(links, indent=4)};
        const width = window.innerWidth;
        const height = window.innerHeight;
        const svg = d3.select("#graph-container").append("svg")
            .attr("width", width).attr("height", height);
        const tooltip = d3.select("body").append("div")
            .attr("class", "tooltip").style("opacity", 0);
        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id).distance(100))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collide", d3.forceCollide().radius(d => d.size + 5))
            .force("x", d3.forceX().strength(0.05))
            .force("y", d3.forceY().strength(0.05));
        const link = svg.append("g").attr("class", "links")
            .selectAll("line").data(links).enter().append("line")
            .attr("class", "link").attr("stroke-width", d => Math.sqrt(d.value));
        const node = svg.append("g").attr("class", "nodes")
            .selectAll("circle").data(nodes).enter().append("circle")
            .attr("class", "node").attr("r", d => d.size)
            .attr("fill", d => {{
                if (d.type === "cluster") return "#4fc3f7";
                if (d.type === "note") return d.group === 1 ? "#f44336" : "#ff9800";
                return "#9c27b0";
            }})
            .on("mouseover", function(event, d) {{
                tooltip.style("opacity", 0.9)
                    .html(`<strong>${d.name}</strong><br>Type: ${d.type}`)
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 28) + "px");
            }})
            .on("mouseout", () => tooltip.style("opacity", 0))
            .on("click", function(event, d) {{
                if (d.type === "note" && d.path) {{
                    const vaultPath = encodeURIComponent("{self.vault_path}");
                    const filePath = encodeURIComponent(d.path.replace("{self.vault_path}", ""));
                    window.open(`obsidian://open?vault=${{vaultPath}}&file=${{filePath}}`, "_blank");
                }}
            }})
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));
        const label = svg.append("g").attr("class", "labels")
            .selectAll("text").data(nodes).enter().append("text")
            .attr("class", "node-label").attr("text-anchor", "middle")
            .attr("dy", "0.35em").text(d => d.name.length > 20 ? d.name.substring(0, 17) + "..." : d.name)
            .attr("fill", d => d.type === "cluster" ? "#ffffff" : "#e0e0e0");
        simulation.on("tick", () => {{
            link.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
            node.attr("cx", d => d.x).attr("cy", d => d.y);
            label.attr("x", d => d.x).attr("y", d => d.y);
        }});
        function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x; d.fy = d.y;
        }}
        function dragged(event, d) {{ d.fx = event.x; d.fy = event.y; }}
        function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null; d.fy = null;
        }}
        window.addEventListener('resize', () => {{
            const newWidth = window.innerWidth;
            const newHeight = window.innerHeight;
            svg.attr("width", newWidth).attr("height", newHeight);
            simulation.force("center", d3.forceCenter(newWidth / 2, newHeight / 2));
            simulation.alpha(0.3).restart();
        }});
    </script>
</body>
</html>
        """
        html_path = os.path.join(self.graphs_dir, filename)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"🌐 Interactive cluster saved to: {html_path}")
        print("🔗 Opening in web browser...")
        webbrowser.open(f"file://{html_path}")

    def do_chat(self, arg):
        """Start interactive AI chat session about current cluster: CHAT"""
        if not self.current_cluster:
            print("❌ No cluster defined. Use CLUSTER first")
            return
            
        print(f"\n💬 Starting AI chat session using {self.summary_model}")
        print("Type your questions about the cluster. Type 'exit' to end chat.")
        print("Type 'save' to save current chat session and continue.")
        print("ℹ️ Context includes:")
        print(f"- Current cluster: {len(self.current_cluster)} notes")
        print(f"- Full note content for cluster")
        print("- Previous conversation history")
        
        context = self._generate_chat_context()
        history = [
            {"role": "system", "content": "You are a knowledgeable research assistant."},
            {"role": "system", "content": context}
        ]
        self.chat_history = []  # Reset chat history for new session
        
        while True:
            try:
                user_input = input("\nYou: ")
                if user_input.lower() in ['exit', 'quit']:
                    # Save chat history before exiting
                    self._save_chat_session()
                    print("👋 Ending chat session")
                    break
                elif user_input.lower() == 'save':
                    # Save current chat session and continue
                    self._save_chat_session()
                    print("💾 Chat session saved, continuing...")
                    continue
                    
                history.append({"role": "user", "content": user_input})
                self.chat_history.append({"role": "user", "content": user_input})
                
                with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                    for msg in history:
                        if msg['role'] == 'system':
                            f.write(f"# System: {msg['content']}\n\n")
                        elif msg['role'] == 'user':
                            f.write(f"# User: {msg['content']}\n\n")
                    f.write("# Assistant:\n")
                    tmp_path = f.name
                    
                self.PROCESSING = True
                progress_thread = threading.Thread(target=self._show_progress)
                progress_thread.daemon = True
                progress_thread.start()
                
                cmd_str = f"{self.SUMMARY_MODELS[self.summary_model]} < {tmp_path}"
                process = subprocess.Popen(
                    cmd_str,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8'
                )
                stdout, stderr = process.communicate(timeout=3600)
                self.PROCESSING = False
                progress_thread.join(timeout=1)
                os.unlink(tmp_path)
                
                if process.returncode != 0:
                    print(f"❌ Model error: {stderr}")
                    continue
                    
                response = stdout.strip()
                print(f"\nAssistant: {response}")
                history.append({"role": "assistant", "content": response})
                self.chat_history.append({"role": "assistant", "content": response})
                
            except KeyboardInterrupt:
                self.PROCESSING = False
                print("\n🚫 Chat interrupted")
                self._save_chat_session()
                break
            except Exception as e:
                self.PROCESSING = False
                print(f"❌ Error: {str(e)}")

    def _save_chat_session(self):
        """Save the current chat session to summaries directory"""
        if not self.chat_history:
            print("ℹ️ No chat history to save")
            return
            
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', self.current_cluster_name)[:50] if self.current_cluster_name else "cluster"
        chat_path = os.path.join(self.summaries_dir, f"Chat_Session_{safe_name}_{timestamp}.md")
        
        chat_content = f"""# Chat Session: {self.current_cluster_name}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Model**: {self.summary_model}
**Cluster Type**: {self.current_cluster_type}
**Notes in Cluster**: {len(self.current_cluster)}

## Conversation:
"""
        for msg in self.chat_history:
            if msg['role'] == 'user':
                chat_content += f"\n### You:\n{msg['content']}\n"
            elif msg['role'] == 'assistant':
                chat_content += f"\n### Assistant:\n{msg['content']}\n"
                
        with open(chat_path, "w") as f:
            f.write(chat_content)
            
        print(f"💾 Chat session saved to: {chat_path}")

    def _generate_chat_context(self) -> str:
        context = "Current knowledge cluster context:\n\n"
        context += f"- Cluster contains {len(self.current_cluster)} notes\n"
        context += "- Notes in cluster with content previews:\n"
        for note in self.current_cluster:
            if note in self.notes:
                data = self.notes[note]
                context += f"\n## {note}\n"
                context += f"- Tags: {', '.join([f'#{t}' for t in data['tags']])}\n"
                context += f"- Concepts: {', '.join(data['concepts'])}\n"
                if data['summary']:
                    context += f"- Summary: {data['summary']}\n"
                preview = ' '.join(data['content'].split()[:200])
                context += f"- Content Preview: {preview}...\n"
        context += "\nInstructions:\n"
        context += "- Answer user questions using the cluster context\n"
        context += "- For thematic analysis, identify cross-note patterns\n"
        context += "- For taxonomy suggestions, consider tags and concepts\n"
        context += "- For pattern recognition, highlight recurring ideas\n"
        context += "- Be concise but comprehensive in responses\n"
        context += "- Maintain technical accuracy\n"
        return context

    def _parse_output_arg(self, args):
        if '--output' in args:
            idx = args.index('--output')
            if idx + 1 < len(args):
                return args[idx+1].lower()
        return self.output_mode

    def _wrap_file_list(self, file_list):
        terminal_width = shutil.get_terminal_size().columns - 4
        wrapper = wrap(", ".join(file_list), width=terminal_width)
        return "  " + "\n  ".join(wrapper)

    def _display_paginated(self, data, title, formatter, output_mode, header=None):
        print(f"\n{title}")
        if header: print(header)
        print("=" * shutil.get_terminal_size().columns)
        page_size = shutil.get_terminal_size().lines - 6
        current = 0
        while current < len(data):
            end = min(current + page_size, len(data))
            for i in range(current, end):
                if isinstance(data[i], tuple):
                    print(formatter(*data[i]))
                else:
                    print(formatter(data[i]))
                print("-" * shutil.get_terminal_size().columns)
            current = end
            if current < len(data):
                remaining = len(data) - current
                user_input = input(f"Displaying {current}/{len(data)}. Press Enter for more, 'q' to quit: ")
                if user_input.lower() == 'q':
                    break
                print()
            else:
                print(f"Displayed all {len(data)} items")
        if output_mode in ["file", "both"]:
            file_content = title + "\n" + "="*80 + "\n"
            for item in data:
                if isinstance(item, tuple):
                    file_content += formatter(*item) + "\n\n"
                else:
                    file_content += formatter(item) + "\n\n"
            self._write_to_file(title, file_content, title.lower().replace(" ", "_"))

    def _write_to_file(self, title, content, file_prefix):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{file_prefix}_{timestamp}.md".replace(" ", "_")
        file_path = os.path.join(self.indices_dir, filename)
        with open(file_path, "w") as f:
            f.write(content)
        print(f"📝 Report saved to: {file_path}")

    def _generate_prompt(self, content_type: str) -> str:
        prompt = f"Generate a comprehensive {content_type} for these research notes:\n\n"
        for note in self.current_cluster:
            if note not in self.notes:
                continue
            data = self.notes[note]
            prompt += f"# {note}\n"
            if content_type == "summary" and data['summary']:
                prompt += f"{data['summary']}\n\n"
            elif content_type == "deep_summary":
                truncated = ' '.join(data['content'].split()[:500])
                prompt += f"{truncated}\n\n"
        prompt += "\n---\nInstructions: "
        prompt += "Synthesize key themes and connections. " 
        prompt += "Maintain technical accuracy. Structure: Overview -> Key Insights -> Conclusions."
        return prompt

    def _format_time(self, seconds: float) -> str:
        if seconds < 60: return f"{int(seconds)}s"
        elif seconds < 3600: return f"{int(seconds//60)}min {int(seconds%60)}s"
        elif seconds < 86400: return f"{int(seconds//3600)}h {int((seconds%3600)//60)}min"
        else: return f"{int(seconds//86400)}d {int((seconds%86400)//3600)}h"
    
    def _show_progress(self):
        start_time = time.time()
        bar_length = 20
        model_speeds = {"llama3:latest": 0.5, "mixtral:8x7b": 0.2}
        total_words = sum([self.notes[note]['word_count'] 
                          for note in self.current_cluster 
                          if note in self.notes])
        eta = model_speeds[self.summary_model] * total_words if self.summary_model in model_speeds else 300
        while self.PROCESSING:
            elapsed = time.time() - start_time
            progress = min(1.0, elapsed / eta) if eta > 0 else min(1.0, elapsed / 300)
            filled_length = int(progress * bar_length)
            bar = '█' * filled_length + ' ' * (bar_length - filled_length)
            time_left = max(0, eta - elapsed) if eta > 0 else -1
            elapsed_str = self._format_time(elapsed)
            time_left_str = self._format_time(time_left) if time_left >= 0 else "unknown"
            print(f"\r⏱️ Progress: [{bar}] {int(progress*100)}% | "
                  f"Elapsed: {elapsed_str} | ETA: {time_left_str}", 
                  end='', flush=True)
            time.sleep(1)
        print("\r" + " " * shutil.get_terminal_size().columns, end='\r', flush=True)

    def do_help(self, arg):
        """Show available commands: HELP [command]"""
        if arg:
            cmd_func = getattr(self, 'do_' + arg, None)
            if cmd_func and callable(cmd_func):
                print(f"\n{arg.upper()} COMMAND")
                print("-" * 50)
                print(cmd_func.__doc__ or "No documentation available")
                print()
            else:
                print(f"❌ Unknown command: {arg}")
        else:
            print("\nCYBERDECK KNOWLEDGE EXPLORER COMMANDS")
            print("=" * 50)
            print("CLUSTER [type] [name]  - Define note cluster (types: all, tag, concept, meta_tag, meta_keyword)")
            print("COMBINE_CLUSTER [AND|OR] [type] value1,value2 - Combine multiple criteria")
            print("REMOVE [numbers]       - Remove files from cluster by number (e.g., remove 2 or remove 2 5 7)")
            print("SHOW_CLUSTER           - Display current cluster (auto-saves to indices)")
            print("LIST_TAGS [--output]   - List all tags with file relationships")
            print("LIST_CONCEPTS [--output] - List all concepts with file relationships")
            print("LIST_META_TAGS [--output] - List all meta tags with file relationships")
            print("LIST_KEYWORDS [--output] - List all keywords with file relationships")
            print("LIST_CONTENTS [--output] - List all files with metadata")
            print("SUMMARIZE [type]       - Generate AI summary (types: summary, deep) - auto-saves")
            print("MODEL [name]           - Switch NLP model (mixtral:8x7b, llama3:latest)")
            print("BFS_CLUSTER [depth]    - Expand cluster via relationships")
            print("VISUALIZE_CLUSTER [max_depth] - Open color-coded cluster in Obsidian")
            print("CLUSTER_GRAPH [format] - Generate static image of cluster (png/jpg)")
            print("CLUSTER_HTML [filename] - Generate interactive HTML visualization")
            print("CHAT                   - Start interactive AI chat about current cluster - auto-saves on exit")
            print("SET_OUTPUT [mode]      - Set output mode (terminal, file, both)")
            print("HELP [command]         - Show command documentation")
            print("EXIT                   - Quit the explorer")
            print("\nCOMBINE_CLUSTER EXAMPLES:")
            print("  COMBINE_CLUSTER AND tag Cyberdeck,knowledge-management")
            print("  COMBINE_CLUSTER OR tag Cyberdeck,knowledge-management")
            print("  COMBINE_CLUSTER AND concept AI,machine-learning")
            print("\nOUTPUT HANDLING:")
            print("- Default output: terminal")
            print("- Use SET_OUTPUT to change default mode")
            print("- Reports saved in ~/Vault/indices/")
            print("- Summaries saved in ~/Vault/summaries/")
            print("- Static graphs saved in ~/Vault/indices/graphs/")
            print("- SHOW_CLUSTER, SUMMARIZE, and CHAT auto-save regardless of output mode")
            print("=" * 50)

    def do_exit(self, arg):
        """Exit the explorer: EXIT"""
        print("👋 Exiting CYBERDECK KNOWLEDGE EXPLORER")
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AI-Powered Obsidian Knowledge Explorer')
    parser.add_argument('--vault', default='/home/ibo/Vault/', 
                        help='Path to Obsidian vault')
    args = parser.parse_args()
    if not os.path.exists(args.vault):
        print(f"❌ Vault not found at {args.vault}")
    else:
        print("⚠️ Ensure Ollama is installed and models are downloaded:")
        print("  ollama pull mixtral:8x7b")
        print("  ollama pull llama3")
        ObsidianKnowledgeExplorer(args.vault).cmdloop()
```
