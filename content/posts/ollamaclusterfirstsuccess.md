+++
date = '2025-12-25T19:32:50+01:00'
draft = false
title = 'Ollama Cluster first success'
weight = 33
+++

Using two ports at the HAProxy server I have managed to now run two raging
scripts in parallel next to each other using the same set of 6 nodes all
having a single Ollama instance running. 

At this time they only used the same model simultaniously dedicated 
to RAGing.

Eventually, this set up will handle complex routing between dedicated
Expert AIs.

(/images/parallelRAGprocessing.png)
