+++
date = '2025-10-23T22:12:39+02:00'
draft = false
title = "The AI RAGing Script"
weight = 10
+++

```batch
#!/usr/bin/env python3
import ollama
import json
import os
import numpy as np
import sys
sys.path.append('/home/ibo/Scripts')
# Now you can import your module
from obsidian_loader import ObsidianLoader
from datetime import datetime

class EnhancedRAGSystem:
    def __init__(self, 
                 chat_model="deepseek-r1:7b",
                 embedding_model="nomic-embed-text",
                 obsidian_path="/media/ibo/512SSDUSB/Obsidian/",
                 chat_history_path="media/ibo/512SSDUSB/ollama_chat_history/",
                 vector_db_path="./rag_vector_db/"):
        
        self.chat_model = chat_model
        self.embedding_model = embedding_model
        self.obsidian_path = obsidian_path
        self.chat_history_path = chat_history_path
        self.vector_db_path = vector_db_path
        self.knowledge_base = []
        
        # Create directories
        os.makedirs(self.vector_db_path, exist_ok=True)
        
        # Initialize components
        self.obsidian_loader = ObsidianLoader(obsidian_path)
        self.vector_db_file = os.path.join(self.vector_db_path, 
"enhanced_knowledge_base.json")
        
        # Load knowledge base
        self.load_knowledge_base()
        
        print(f"Enhanced RAG System Initialized")
        print(f"  - Obsidian notes loaded from: {obsidian_path}")
        print(f"  - Knowledge items: {len(self.knowledge_base)}")
    
    def get_embedding(self, text):
        """Get embeddings using Ollama"""
        try:
            response = ollama.embeddings(model=self.embedding_model, 
prompt=text)
            return response['embedding']
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return [0.0] * 384
    
    def load_obsidian_knowledge(self):
        """Load and process Obsidian notes"""
        print("Loading Obsidian notes...")
        notes = self.obsidian_loader.load_obsidian_notes()
        chunks = self.obsidian_loader.extract_conversation_chunks(notes)
        
        for i, chunk in enumerate(chunks):
            item = {
                'content': chunk,
                'source': 'obsidian',
                'timestamp': datetime.now().isoformat(),
                'embedding': self.get_embedding(chunk),
                'type': 'chat_turn' if len(chunk) < 1000 else 'content_chunk'
            }
            self.knowledge_base.append(item)
        
        print(f"✓ Added {len(chunks)} chunks from Obsidian notes")
    
    def load_chat_history(self):
        """Load existing Ollama chat history"""
        print("Loading Ollama chat history...")
        import glob
        
        chat_files = glob.glob(os.path.join(self.chat_history_path, 
"chat_session_*.json"))
        
        for file_path in chat_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for message in data.get('messages', []):
                    if message['role'] == 'user':
                        item = {
                            'content': message['content'],
                            'source': os.path.basename(file_path),
                            'timestamp': data.get('timestamp', ''),
                            'embedding': self.get_embedding(message['content']),
                            'type': 'user_query'
                        }
                        self.knowledge_base.append(item)
                
                print(f"✓ Loaded {os.path.basename(file_path)}")
                
            except Exception as e:
                print(f"✗ Error loading {file_path}: {e}")
    
    def load_knowledge_base(self):
        """Load or create the complete knowledge base"""
        if os.path.exists(self.vector_db_file):
            try:
                with open(self.vector_db_file, 'r', encoding='utf-8') as f:
                    self.knowledge_base = json.load(f)
                print(f"✓ Loaded existing knowledge base with {len(self.knowledge
_base)} items")
            except Exception as e:
                print(f"Error loading knowledge base: {e}")
                self.knowledge_base = []
        else:
            # First time - load from all sources
            self.load_obsidian_knowledge()
            self.load_chat_history()
            self.save_knowledge_base()
    
    def save_knowledge_base(self):
        """Save knowledge base to file"""
        try:
            with open(self.vector_db_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
            print("✓ Knowledge base saved")
        except Exception as e:
            print(f"Error saving knowledge base: {e}")
    
    def cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors"""
        if not vec1 or not vec2:
            return 0.0
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return dot_product / (norm1 * norm2)
    
    def find_relevant_context(self, query, top_k=5):
        """Find most relevant context using vector similarity"""
        if not self.knowledge_base:
            return []
        
        query_embedding = self.get_embedding(query)
        similarities = []
        
        for item in self.knowledge_base:
            similarity = self.cosine_similarity(query_embedding, item['embedding'])
            similarities.append((similarity, item))
        
        # Sort by similarity and return top results
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [item for score, item in similarities[:top_k] if score > 0.3]
    
    def ask_question(self, question, use_context=True):
        """Ask a question using the enhanced RAG system"""
        if use_context:
            context_items = self.find_relevant_context(question)
            
            if context_items:
                context_text = "\n".join([
                    f"[From {item['source']}] {item['content']}"
                    for item in context_items
                ])
                
                prompt = f"""Based on my previous conversations and notes:

{context_text}

Current question: {question}

Please provide an answer that builds upon my existing knowledge and 
previous discussions:"""
            else:
                prompt = question
        else:
            prompt = question
        
        # Get response from DeepSeek R1
        try:
            response = ollama.chat(
                model=self.chat_model,
                messages=[{"role": "user", "content": prompt}],
                stream=False
            )
            return response['message']['content']
        except Exception as e:
            return f"Error getting response: {str(e)}"
    
    def interactive_chat(self):
        """Interactive chat mode"""
        print("\n" + "="*60)
        print("Enhanced RAG Chat System Ready!")
        print("I'll use your Obsidian notes AND chat history to help you.")
        print("Commands: 'quit', 'refresh', 'context on/off', 'sources'")
        print("="*60)
        
        context_enabled = True
        
        while True:
            try:
                question = input("\nYou: ").strip()
                
                if question.lower() in ['quit', 'exit']:
                    break
                elif question.lower() == 'refresh':
                    self.load_obsidian_knowledge()
                    self.load_chat_history()
                    self.save_knowledge_base()
                    print("✓ Knowledge base refreshed!")
                    continue
                elif question.lower() == 'context off':
                    context_enabled = False
                    print("✓ Context disabled - using raw model responses")
                    continue
                elif question.lower() == 'context on':
                    context_enabled = True
                    print("✓ Context enabled - using your knowledge base")
                    continue
                elif question.lower() == 'sources':
                    print(f"Knowledge sources: {len(self.knowledge_base)} items")
                    sources = {}
                    for item in self.knowledge_base:
                        source = item['source']
                        sources[source] = sources.get(source, 0) + 1
                    for source, count in sources.items():
                        print(f"  - {source}: {count} items")
                    continue
                elif not question:
                    continue
                
                print("Assistant: Thinking...")
                response = self.ask_question(question, use_context=context_enabled)
                print(f"Assistant: {response}")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    # Check if Ollama is running
    try:
        models = ollama.list()
        print("✓ Connected to Ollama")
    except Exception as e:
        print(f"Error: Cannot connect to Ollama - {e}")
        print("Make sure Ollama is running: ollama serve")
        return
    
    # Initialize enhanced RAG system
    rag = EnhancedRAGSystem()
    
    # Start interactive chat
    rag.interactive_chat()

if __name__ == "__main__":
    main()
```
