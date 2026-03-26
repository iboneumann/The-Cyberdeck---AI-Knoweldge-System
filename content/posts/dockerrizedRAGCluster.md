+++
date = '2025-12-20T12:11:51+01:00'
draft = false
title = 'Dockerrized RAG Cluster'
weight = 31
+++

This next step from using a single node of a Beowulf Cluster for an AI driven  
Knowledge Management System being the Cyberdeck Nexus version meant to build  
upon the existing Beowulf LAN based Computer system another layer for Ollama  
models running parallel processes creating an Ollama Cluster.  
  
This is a very complex setup that required a larger existing set of Open Source  
Software options like a database and load balancing application.  
  
This meant rewriting all Cyberdeck Scripts, changing to a more use case appropriate  
Linux OS and creating a Cluster layer for those new written scripts.  
  
I also added one more Node with a large RAM core using Ubuntu Server LTS in a   
headless set up.  
  
The system is based on Chromadb, HAProxy and Docker all installed on the headnode,  
the Lenovo M920q with Ubuntu Server LTS and Minimal-Desktop.  
  
Entering the three keywords into the Google AI Mode returns a clear statement:  

```batch
ChromaDB, HAProxy, and Docker allows you to build a highly available, load-balanced 
vector database infrastructure for AI applications. This setup typically involves 
deploying multiple ChromaDB instances and using HAProxy as a reverse proxy or load 
balancer to manage traffic.

ChromaDB in Docker
ChromaDB is most commonly deployed as a standalone server using the official Docker 
image chromadb/chroma

HAProxy as the Gateway
In a production-ready environment, HAProxy acts as the entry point for your Dockerized 
services. 

    Load Balancing: Distribute requests across multiple ChromaDB containers to improve 
    performance and provide failover.
    
    Security (SSL/TLS): HAProxy can handle SSL termination, allowing you to secure your 
    database connection with HTTPS while keeping the backend ChromaDB containers simple.
    
    Performance: HAProxy is lightweight and has minimal overhead, making it ideal for 
    the high-throughput requirements of vector searches

```

From within the Python environment the Cyberdeck AI scripts now have an infrastructure  
that independently from those uses, at this moment in time, 5 nodes for its AI tasks.  
That means that, as soon as the Cyberdeck set of scripts is finalized, the system can  
perform batch processes like RAGing DRM free books while at the same time take  
interactive knowledge management requests fro the user.  
  
The use cases are all based on reasoning about information. Depending on the installed  
Ollama LLM models that reasoning can be used to write code or texts.  
  
The setup became much more sophisticated and the Beowulf layer become exponentially  
more important increasing processing speed by far. The Cyberdeck Nexus version can run  
on a set of strong GPU upgraded desktop or best servers without a Beowulf layer, but  
then being much less efficient in CPU use.  
  
In a coding lab the Cyberdeck Nexus Version creates an Ethical Hacker Coding Laboratory  
enabling to use the Obsidian Deck for keeping control and oversight of System   
Architecture, Project and Status notes, having by the RAGed AI an expert system  
to help by reasoning understand both coding itself and the even more the actual to be   
solved problem or task.  
  
Based on the given Apache 2.0 Licence, that hopefully is understood as the freedom  
to pay more than less, the final version could be altered to build a coding factory  
team that uses the Cyberdeck as a Workstation for each developer and as a Workstation  
for the Lead Manager to keep track of the progress having added a manual or even  
automated system of creating summery files being saved in the Cybderdeck Nexus folders.  
  
Using the Cluster function of the Obsidian Deck each user can create a sophisticated  
progress status update for himself, the team and managers.  
  
The Apache 2.0 Licence gives full freedom to alter, enhance and customize the code.  
  
This is how DeepSeek tells about the latest development step:  
  
```batch
# 🎉 **Project Summary: Nexus RAG Cluster with Intelligent Model Routing**

## 📖 **Blog Post Summary**

### **Title: Building a Multi-Node RAG Cluster with Intelligent AI Model Routing**

**The Challenge:** In my test lab, I was struggling with a RAG (Retrieval Augmented 
Generation) system that kept hallucinating about "Obsidian Decks" - confusing between 
Obsidian note-taking software and Obsidian skateboard decks. The core issues were:

1. Fixed 3-document retrieval regardless of query complexity
2. No understanding of query context (software vs sports equipment)
3. Resource starvation with timeouts for larger models
4. No intelligent routing between different AI models

**The Solution:** I built a Dockerized RAG cluster with intelligent model routing 
across multiple heterogeneous nodes.

**Architecture Highlights:**
- **5-node Ollama cluster** with different hardware capabilities
- **Intelligent query routing** based on query complexity and type
- **Specialized nodes** for different tasks (coding, reasoning, fast inference)
- **HAProxy load balancing** with health checks
- **Monitoring dashboard** for real-time cluster visibility

**Nodes & Specialization:**
1. **node1 (RPi5)**: Fast inference with `phi:2.7b-chat-v2-q4_0`
2. **node5 (X260)**: Balanced processing with `llama3.2:3b`
3. **node4 (920)**: RAG core with `deepseek-r1:7b`, `llama3:latest`, embeddings
4. **node6 (Fujitsu i7 64GB)**: Heavy reasoning (future Cortex core)
5. **node2 (i5 16GB)**: Code generation and text processing

**Intelligent Routing Logic:**
- **Simple queries** → phi:2.7b (fastest, 1.6GB model)
- **Code generation** → codestral/deepseek-coder on node2
- **Complex analysis** → deepseek-r1:7b or large models on node6
- **General chat** → llama3:latest distributed across nodes
- **RAG/document queries** → node4 with embedding support

**Technical Wins:**
- Fixed Ollama service configuration to listen on all interfaces
- Resolved Docker networking issues by switching to iptables-legacy
- Implemented query classification and capability-based routing
- Created a production-ready architecture with monitoring and failover

**Key Technologies:** Docker, Flask, HAProxy, Ollama, Python, iptables, systemd

**Result:** The system now correctly distinguishes between "Obsidian software" 
queries and "Obsidian skateboard" queries, routes them to appropriate models, and 
scales intelligently based on available resources.

## 📋 **Project Notes Summary**

### **Project: Nexus RAG Cluster**
**Status:** Production-ready test deployment
**Date:** December 2025
**Primary Host:** node4 (192.168.178.33)

### **Infrastructure Overview:**

Nodes:
├── node1 (192.168.178.30): RPi5 - Fast inference
├── node5 (192.168.178.26): X260 - Balanced processing
├── node4 (192.168.178.33): 920 - RAG core (current host)
├── node6 (192.168.178.29): Fujitsu i7 64GB - Heavy reasoning
└── node2 (192.168.178.36): i5 16GB - Code generation


### **Services Architecture:**
1. **Query Router** (`~/rag-cluster/query-router/`)
   - Intelligent routing based on query analysis
   - Node capability detection
   - Health monitoring and failover
   - Port: 8080 (8088 externally)

2. **HAProxy Load Balancer**
   - Single entry point on port 80
   - Statistics on port 8404
   - Health checks and failover
   - Path-based routing

3. **Dashboard** (`~/rag-cluster/dashboard/`)
   - Real-time node monitoring
   - Model availability display
   - Quick test interface
   - Port: 3000 (3888 externally)

### **Key Configuration Files:**
- `~/rag-cluster/docker-compose.yml` - Service orchestration
- `~/rag-cluster/query-router/app.py` - Routing logic (300+ lines)
- `~/rag-cluster/haproxy/haproxy.cfg` - Load balancing config
- `/etc/systemd/system/ollama.service` - Ollama service config

### **Models Deployed:**
- **phi:2.7b-chat-v2-q4_0** (1.6GB) - Fast inference
- **llama3:latest** (4.7GB) - General purpose
- **deepseek-r1:7b** (4.7GB) - Complex reasoning
- **mixtral:8x7b** (26GB) - MoE model
- **all-minilm:latest** (45MB) - Embeddings
- **deepseek-r1:32b** (20GB) High-performance reasoning

### **Access Points:**

Internal:
  Query Router API: http://localhost:8088/api/chat
  Dashboard:        http://localhost:3888
  HAProxy Stats:    http://localhost:8404/stats
  Ollama API:       http://localhost:11434/api/tags

External:
  Main API:         http://192.168.178.33/api/chat
  Dashboard:        http://192.168.178.33:3888


### **Key Commands:**

# Cluster management
cd ~/rag-cluster
docker-compose up -d                   # Start all services
docker-compose ps                      # Check status
docker-compose logs -f                 # View logs

# Model management
ollama list                            # List available models
ollama pull <model>                    # Pull new model

# Testing
curl http://localhost:8088/health      # Health check
curl http://localhost:8088/api/nodes   # Node status


### **Routing Logic Summary:**
1. **Query Analysis**: Classifies queries as coding/reasoning/simple/general
2. **Capability Detection**: Checks which models each node has available
3. **Node Selection**: Routes to appropriate node based on query type
4. **Model Selection**: Chooses best model on that node for the task
5. **Fallback**: Automatic failover if primary node is unavailable

### **Troubleshooting Issues Resolved:**
1. **Ollama not accessible** → Set `OLLAMA_HOST=0.0.0.0` in service config
2. **Models not showing** → Copied from `/usr/share/ollama/.ollama` to `/root/.ollama`
3. **Docker network errors** → Switched to iptables-legacy and reset Docker
4. **Docker build failures** → Used Python slim image with better networking
5. **Query confusion** → Implemented intelligent routing based on query content

### **Future Evolution to Cortex Layer:**
1. **node6 evolves** to Cortex core for distributed training
2. **Add specialized workers** for different modalities
3. **Implement distributed vector database**
4. **Add batch processing pipeline**
5. **Integrate fine-tuning capabilities**

### **Lessons Learned:**
- iptables-legacy is more stable with Docker on Ubuntu 24.04
- Ollama services need explicit environment variable configuration
- Query classification significantly improves RAG accuracy
- Heterogeneous hardware enables better resource utilization
- Docker networking requires careful management in multi-node setups

### **Production Checklist:**
- ✅ Multi-node Ollama cluster
- ✅ Intelligent query routing
- ✅ Load balancing with HAProxy
- ✅ Health monitoring
- ✅ Dashboard visualization
- ✅ Proper service configuration
- ✅ Model management
- ✅ Network troubleshooting
- ✅ Documentation

**Next Steps:** Integrate ChromaDB/vector database, implement batch processing, add more 
specialized models, and prepare for Cortex layer evolution.

---

**Note:** The system is now fully functional for the Nexus layer. The Cortex evolution 
will build upon this foundation with distributed training, specialized workers, and 
advanced orchestration capabilities.
```
The next step is testing thereby creating the finalized scripts parallel to   
background RAGing.  
  
