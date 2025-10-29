+++
date = '2025-10-23T22:48:19+02:00'
draft = false
title = "RAGed WikiOL AI"
weight = 13
+++

### A Wiki&OpenLibrary RAGed AI

RAGing is crazy cool. I downloaded a wiki dump and some more free books related to Logic 
(which is part of philosophy and mathematics), chaos theory and complex systems.

These are the models I have installed:
```batch
(cyberdeck-env313) ibo@M920:~/Scripts/Obsidian_Deck_Scripts$ ollama list
NAME                       ID              SIZE      MODIFIED     
mistral:latest             6577803aa9a0    4.4 GB    5 days ago      
phi3:3.8b                  4f2222927938    2.2 GB    3 months ago    
DeepSeek-R1:7B             755ced02ce7b    4.7 GB    3 months ago    
nomic-embed-text:latest    0a109f422b47    274 MB    4 months ago    
mixtral:8x7b               a3b6bef0f836    26 GB     4 months ago    
llama3:latest              365c0bd3c000    4.7 GB    4 months ago    
(cyberdeck-env313) ibo@M920:~/Scripts/Obsidian_Deck_Scripts$ 
```

Now, my RAGed AI got my spelling mistake fixed and connected the dots, instead
of giving halucinating called off topic answers, beside making some very 
interesting conclusions based on a classic old education:

```batch
(Cyberdeck-env313) ibo@X260:~/Scripts$ python3 RAGing_system_wiki.py
🚀 Starting Simple RAG System
--------------------------------------------------
🔍 Looking for Wikipedia files...
📁 Checking: /media/ibo/512SSDUSB
   Found 91 files/dirs
✅ Found Wikipedia files at: /media/ibo/512SSDUSB
🔍 Checking environment...
📁 Contents of /media/ibo/512SSDUSB:
   enwiki-latest-pages-articles-multistream.xml (106848.5 MB)
   pg38143-images.html (1.2 MB)
   pg31793-images.html (1.2 MB)
   THE  PRINCIPLES  OF  SCIENCE.txt (2.0 MB)
   pg22182-images.html (0.4 MB)
   22182-cover.png (0.1 MB)
   pg42048-images.html (1.3 MB)
   38709-cover.png (0.1 MB)
   pg147-images.html (0.2 MB)
   THE  ALGEBRA  OF  LOGIC.txt (0.2 MB)
   ... and 81 more items
✅ Ollama is running

📁 Looking for Wikipedia dump file...
📄 Found: enwiki-latest-pages-articles-multistream.xml (104.34 GB)
🔄 Processing: enwiki-latest-pages-articles-multistream.xml
🚧 Using sample data for testing...
✅ Created 3 sample chunks
🔧 Creating vector store...
📚 Loading existing vector store...
/home/ibo/Scripts/RAGing_system_wiki.py:188: LangChainDeprecationWarning: 
The class `HuggingFaceEmbeddings` was deprecated in LangChain 0.2.2 and 
will be removed in 1.0. An updated version of the class exists in the 
`langchain-huggingface package and should be used instead. To use it run 
`pip install -U `langchain-huggingface` and import as `from 
`langchain_huggingface import HuggingFaceEmbeddings``.
  self.embeddings = HuggingFaceEmbeddings(

🎯 System Ready! Ask questions about Shakespeare and history.
💡 Type 'quit' to exit
--------------------------------------------------

❓ Question: What can you tell about Willams Shakespear's work and Logic?
🔍 Searching: 'What can you tell about Willams Shakespear's work and Logic?'
📚 Found 3 relevant documents
🤖 Generating answer...

💬 Answer (152.4s):
Based on the provided knowledge and conversation history, it is clear that 
Williams Shakespear did not exist as his name does not match any historical 
figure known to have existed. Additionally, there is no record of him having 
worked in the field of machine learning or artificial intelligence.

William Shakespeare, on the other hand, was a famous English playwright and 
poet who lived in the 16th and 17th centuries. He is widely regarded as one 
of the greatest writers in the English language and is known for his works 
such as "Romeo and Juliet," "Hamlet," and "Macbeth." However, there is no 
record of him having worked in the field of logic or artificial intelligence.

Therefore, based on the information provided, it can be concluded that 
Williams Shakespear did not work in the field of machine learning or logic, 
while William Shakespeare was a renowned playwright and poet who lived 
centuries ago.

📚 Sources: 3 documents

❓ Question: I misspelled the name, but you found who I ment. Check his plays 
based on what you know about logic theory for me, please.
🔍 Searching: 'I misspelled the name, but you found who I ment. Check his 
plays based on what you know about logic theory for me, please.'
📚 Found 3 relevant documents
🤖 Generating answer...

💬 Answer (256.2s):
Based on your previous question and conversation history, it is clear that you 
are referring to William Shakespeare, not Williams Shakespear. 
William Shakespeare was a renowned playwright and poet who lived in the 16th 
and 17th centuries, and his works are known for their complex characters, 
intricate plots, and use of language.

In terms of logic theory, William Shakespeare's plays often explore themes 
related to logic and reasoning, such as the nature of truth, the consequences 
of deception, and the importance of critical thinking. For example, 
in "Hamlet," the titular character grapples with the question of whether to 
trust his own perceptions or the information provided by others, while in 
"Macbeth," the characters must navigate a complex web of lies and deception 
in order to achieve their goals.

Some of Shakespeare's plays that are particularly relevant to logic theory 
include:
1. "Romeo and Juliet" - This play explores the nature of love, reason, and 
   emotion, as well as the consequences of impulsive decision-making.
2. "Hamlet" - As mentioned earlier, this play delves into the theme of trust 
   and the importance of critical thinking in navigating complex situations.
3. "Macbeth" - This play examines the nature of ambition and the dangers of 
   unchecked desire, as well as the role of reason in decision-making.
4. "The Tempest" - This play explores the theme of power and control, as well 
   as the relationship between reason and emotion in shaping human behavior.

Overall, William Shakespeare's plays are rich in logical and philosophical 
themes that continue to resonate with audiences today.

📚 Sources: 3 documents

❓ Question: 

```

 
