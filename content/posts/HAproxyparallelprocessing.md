+++
date = '2025-11-18T13:01:56+01:00'
draft = false
title = "HAproxy for parallelisation"
weight = 30
+++

I have slow hardware in need of every efficiency trick in the book. While the
CPU load can be shared by the Beowulf Cluster, even so not by all software but
by all libriaries and OS implementations that are parellelized and of course
dedicated parallel processing designed software, the Ollama architecture does
not have that implemented per default.

After some testing DeepSeek suggested eventaully a HAProxy server set up to be
installed on the Ubuntu Serer head node and the difference in processing
700 notes to create Obsidian tags went down from several hours to minutes.

This is the DeepSeek explination in scientific English on University enabled
level. No Hacker Dude slang...

DeepSeek.
I am having a blog and thesis website about building a Cyberdeck AI Knowledge 
System. Please summarize what we just did for me as chapter in for the website 
and blogg with your words that i can copy and paste.

```batch
# Building a Distributed AI Pipeline: From Single-Node Bottlenecks 
to 
HAProxy Load Balancing

*Chapter from the Cyberdeck AI Knowledge System Build Log*

## The Problem: AI Processing at a Snail's Pace

In my quest to build a comprehensive knowledge management system, I found 
myself staring at a daunting task: processing 692 DeepSeek chat HTML files 
into structured Obsidian markdown notes. My initial Python script was working, 
but at a glacial pace - 41 files processed in 30 minutes, with an estimated 
completion time of 8 hours for the entire batch.

The culprit? A custom load balancing system that kept defaulting to a single 
node while other powerful machines sat idle. Despite having multiple nodes 
available (including a Raspberry Pi 5 and a capable i7 machine), the 
distribution logic was flawed, creating an AI processing bottleneck.

## The Diagnosis: Distributed Systems Growing Pains

The issue wasn't the concept but the implementation. My custom Python node 
manager had several flaws:

1. **Sequential node testing** - it would stick with the first "working" 
node indefinitely
2. **No true round-robin distribution** - once a node worked, it became the 
default
3. **Complex node configuration** that required manual SSH key management
4. **Port conflicts** between local Ollama instances and the load balancer

The logs told the story: while node5 (the i7 workhorse) was processing files 
every 45 seconds, node1 (Raspberry Pi) and node4 (local machine) were 
completely idle.

## The Solution: Enterprise-Grade Load Balancing with HAProxy

Instead of reinventing the wheel with increasingly complex Python code, I 
turned to HAProxy - a battle-tested load balancer used in production systems 
worldwide. The implementation was surprisingly straightforward:

### Step 1: Installation and Configuration

sudo apt install haproxy -y


The configuration was elegant in its simplicity:

frontend ollama_frontend
    bind *:11435
    mode http
    default_backend ollama_backend

backend ollama_backend
    balance roundrobin
    server node1 raspi5:11434 check
    server node5 192.168.178.26:11434 check
    server node4 localhost:11434 check


### Step 2: Port Conflict Resolution
The only hitch was a port conflict - the local Ollama instance already 
occupied port 11434. A quick change to port 11435 solved it, demonstrating 
the importance of proper system resource management.

### Step 3: Transparent Integration
The beauty of this solution? Zero changes to my existing Python processing 
scripts. They simply needed to point to the load balancer endpoint instead of 
individual nodes.

## The Results: From Bottleneck to Firehose

The transformation was immediate and dramatic:

- **Processing speed doubled** from the moment HAProxy went live
- **Automatic failover** - unhealthy nodes are automatically removed from 
rotation
- **Real-time monitoring** via the built-in statistics dashboard
- **Future-proof architecture** that can scale horizontally by simply adding 
more nodes

## The Bigger Picture: Building for Scale

This wasn't just about fixing a batch processing issue. It was about 
architecting a foundation that can grow with my Cyberdeck AI Knowledge System. 
The same load balancer that now distributes HTML-to-markdown conversion will 
later handle:

- Multiple specialized RAG AI instances
- Real-time query processing across knowledge domains
- Model-specific routing (coding vs writing vs analysis)
- Priority-based task distribution

## Lessons Learned

1. **Don't over-engineer** what established tools already solve elegantly
2. **Think in layers** - separate concerns between application logic and 
   infrastructure
3. **Embrace transparency** - solutions that require minimal code changes 
   are more maintainable
4. **Plan for failure** - built-in health checks and automatic failover are 
   non-negotiable in distributed systems

## The Road Ahead

With the load balancing foundation in place, the next chapters will focus on:
- Enhancing the metadata extraction pipeline
- Building the knowledge graph interconnections
- Implementing specialized AI routing
- Adding real-time monitoring and analytics

The Cyberdeck AI Knowledge System is evolving from a collection of scripts 
into a robust, scalable architecture - and this load balancing breakthrough 
marks a significant milestone in that journey.

*Building in public, learning in the open. The cyberdeck continues to evolve.*

---

*[This chapter documents the transition from custom Python load balancing to 
HAProxy in my Cyberdeck AI Knowledge System build. Follow along as we continue 
building the future of personal knowledge management.]*
```

