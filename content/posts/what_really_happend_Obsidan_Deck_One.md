+++
date = '2025-10-23T17:44:13+02:00'
draft = false
title = "Obsidian Deck reality"
weight = 4
+++

### What really happend - Obsidan Deck
The RAGed AI gave a good plan based on what it was taught on.  
RAGing means teaching an AI model with knowledge. This is  
different from searching with an AI model through a database  
of notes containing a solution. RAGed the AI reasons and does  
not just look up by searching for Keywords.  
  
In the end of the Day does the Obsidian Deck have no  
SQL database at this moment, neither has the Cyberdeck which  
would control, manage and execute file operations over the  
LAN Computers.  
  
This is about a living project using old refurbished Office  
Lenovo i7 and i5 hardware combined with RaspberryPi SBCs.  
  
The Obsidian Deck is functional.  
  
This is the pipeline that turns DeepSeek Chats into an  
Obsidian Vault:  
  
1st: AIparser10.py  
  
2nd: filename_generator.py  
  
3rd: convert_to_obsidian.py  
  
Final AI Shell: Obsidian-Deck.py  
  
Each is a Python script executed in a Python 3.13 environment.  
The AI parser is Version 10 and uses a locally installed Llama  
model on a currently just 16GB RAM i7 M920 tiny (max 32GB) to  
create a useful tag based structure for at this moment about  
600 DeepSeek chats.  
  
Using a Firefox extension to download .html files of the  
DeepSeek chat they need better naming than a time stamp which  
is done by the filename_generator.py. Finally the pipelines  
last script converts the md files into Obsidian md files and  
saves them into the Obsidian Vault.  
  
The Obsidian-Deck.py is at this point not RAGed, but uses a set  
of commands to structure the large Vault for better understanding  
of the content being able to summaries the based on tags defined  
Obsidian nodes Cluster.  
  
Sometimes reading the manual helps to understand what  
something does:  

```bash
## The Obsidian Deck Manual
AI Knowledge Explorer Manual
Quick Start Guide

1. Basic Setup
Start the explorer:  python3 obsidian-deck.py --vault /path/to/your/vault

If using default location
  python obsidian-deck.py


AUTO-SAVE FEATURES
Always Saved (Regardless of Output Mode)
    show_cluster → ~/Vault/indices/Cluster_Report_*.md
    summarize → ~/Vault/summaries/Summary_*.md
    chat → ~/Vault/summaries/Chat_Session_*.md (on exit)

Optional Saving

    all list_* commands with --output file or --output both

    Visualizations to ~/Vault/indices/graphs/

2. Essential Commands You Were Trying
Define a cluster first: obsidian> cluster tag Obsidian
Works with any cluster type
  cluster tag "multi word tag"
  cluster concept "complex concept name"

  Then summarize:
  
  obsidian> summarize summary
  or
  obsidian> summarize deep

For chat:
obsidian> chat

---

🔍 cluster MANAGEMENT
Define a Cluster
Multi-word cluster names supported!:
cluster tag Cyberdeck knowledge-management
cluster concept artificial-intelligence
cluster all research-project

View Current Cluster
show_cluster  # Auto-saves to ~/Vault/indices/

Remove Files from Cluster
 Remove single file
remove 2

 Remove multiple files
remove 2 5 7

 Shows numbered list first for reference
Expand Cluster

BFS_cluster 3                # Expand via links to depth 3

 Complete Command Reference
 📁 cluster MANAGEMENT
Define a note cluster:
cluster [type] [name]
Types: `tag`, `concept`, `meta_tag`, `meta_keyword`, `all`

Examples:
cluster tag Obsidian         # All notes with #Obsidian tag
cluster concept machine_learning
cluster meta_tag important

combine_cluster AND tag Cyberdeck,knowledge-management
combine_cluster OR tag Cyberdeck,knowledge-management


Show current cluster:
show_cluster


Expand cluster relationships:
BFS_cluster [depth]          # Default depth=2


 📊 LISTING & INDEXING
List all tags:
list_tags [--output TERMINAL|FILE|BOTH]


List all concepts:
list_concepts [--output TERMINAL|FILE|BOTH]


List all files with metadata:
list_content [--output TERMINAL|FILE|BOTH]


 🤖 AI SUMMARIZATION
Generate summaries:
summarize summary            # Quick summary using existing note summaries
summarize deep               # Deep analysis using full note content


Switch AI models:
model llama3:latest          # Faster, good for most tasks
model mixtral:8x7b           # More powerful, slower


Interactive chat about cluster:
chat


 🎨 VISUALIZATION
Open in Obsidian:
visualize_cluster [max_depth]# Default depth=5


Generate static image:
cluster_GRAPH png            # or jpg


Interactive web visualization:
cluster_HTML my_cluster.html


 ⚙️ OUTPUT CONTROL
 OBSIDIAN DECK QUICK REFERENCE - ALL COMMANDS LOWERCASE

 BASIC WORKFLOW:
cluster tag Obsidian         # Define cluster by tag
show_cluster                 # View current cluster  
summarize deep               # AI analysis (or 'summary' for quick version)

 cluster TYPES:
cluster tag <tagname>        # By hashtag
cluster concept <concept>    # By concept 
cluster meta_tag <metatag>   # By meta tag
cluster meta_keyword <keyword> # By keyword

 LISTING COMMANDS:
list_tags                    # All tags
list_concepts                # All concepts  
list_meta_tags               # All meta tags
list_keywords                # All keywords
list_contents                # All files with metadata

 VISUALIZATION UNDER CONSTRUCTION:
visualize_cluster           # Open in Obsidian
cluster_graph png           # Static image (png/jpg)
cluster_html my_viz.html    # Interactive web viz

 AI FEATURES:
summarize summary           # Quick summary
summarize deep              # Deep analysis
chat                        # Interactive chat about cluster
model llama3:latest         # Switch AI model

 UTILITIES:
set_output terminal         # terminal/file/both
help                        # Show all commands
exit                        # Quit

NO DASHES NEEDED - JUST SPACES!
 WRONG: summarize --deep
 RIGHT: summarize deep

EXAMPLE WORKFLOW:
cluster tag AI
show_cluster  
summarize deep
visualize_cluster
```
