+++
date = '2025-10-27T09:17:45+01:00'
draft = false
title = 'Folder structures'
weight = 19
+++

Folder structure considerations  
  
RAGing does only need a data dump, because the RAGing creates its own structure readable for the AI.  
  
Folder structures are important for human readability especially, because the RAGing is based on texts. For those mankind developed  
specific forms and structures over the millenniums for a reason.  
  
The Cyberdeck has in particular needs for a clear structure. It's use case combines AI and human behavior. We want to read a text  
while reasoning with the AI about it.  
  
This Thesis is not a Law School Thesis, but Harvard seems to have fixed major parts of that by having announced to bring millions of  
titles from its large libraries to AI training by publishing them.  
  
This is about building with open source LLM models a computer system using both hardware and software most efficient.  
That's why I called it Cyberdeck, being the most powerful tools in Dark Sci-Fi future in which the man-machine link turned  
reality.  
  
DeepSeek suggested a folder structure that does make sense, but not for my personal case in which the sources are more important  
than the librarian classic structure due to the processing pipeline.  
  
The MySQL database combining Obsidian tags with the data dumps and most likely some AI scripts to create a human readable  
Cyberdeck Library Index is coming thereafter.  
  
The Folder Structures  
```black
RAG_Knowledge_Base/
├── main_script.py                 # Main RAG script
├── requirements.txt               # Python dependencies
├── config.yaml                    # Configuration file
├── chroma_db/                     # Vector database (auto-created)
│
├── knowledge_sources/             # All your knowledge sources
│   ├── literature/                # Literary works like your HTML file
│   │   ├── pg348-images.html     # The file you provided
│   │   ├── other_books/
│   │   └── metadata.json         # Optional: metadata about sources
│   │
│   ├── wiki/                      # Wiki content
│   │   ├── philosophy/
│   │   ├── science/
│   │   └── history/
│   │
│   ├── technical/                 # Technical documentation
│   │   ├── programming/
│   │   ├── mathematics/
│   │   └── engineering/
│   │
│   └── personal/                  # Personal notes and documents
│       ├── research_notes/
│       ├── project_docs/
│       └── learning_materials/
│
├── scripts/                       # Utility scripts
│   ├── preprocess_html.py        # Special HTML processing
│   ├── batch_processor.py        # Batch processing
│   └── backup_db.py              # Database backup
│
└── logs/                         # Log files
    ├── rag_system.log
    └── processing.log
```

The Source based structure
```batch
RAG_Pipeline/
├── data_sources/                  # RAW DATA DUMPS (organized by source)
│   ├── wiki_dump/
│   │   └── enwiki-latest-pages.xml
│   ├── open_library/
│   │   ├── literature/
│   │   ├── science/ 
│   │   └── philosophy/
│   ├── web_scraping/
│   │   ├── domain1/
│   │   ├── domain2/
│   │   └── domain3/
│   └── deepseek_chats/
│       ├── conversations/
│       └── obsidian_export/
│
├── processing_scripts/            # SOURCE-SPECIFIC PROCESSORS
│   ├── process_wiki_dump.py
│   ├── process_open_library.py
│   ├── process_web_content.py
│   └── process_chats.py
│
├── unified_knowledge/             # PROCESSED, STRUCTURED DATA
│   ├── chunks/
│   │   ├── wiki/
│   │   ├── books/
│   │   ├── web/
│   │   └── chats/
│   └── metadata.db               # SQLite for structured queries
│
├── vector_store/                  # RAG READY DATA
│   ├── chroma_db/
│   └── embeddings_cache/
│
└── rag_system.py                 # MAIN QUERY INTERFACE
```
Needless to say, that good planning and regular housekeeping of is  
crucial creating Knowledge Systems that lead to success which is  
understanding and learning to progress and evolve.  
