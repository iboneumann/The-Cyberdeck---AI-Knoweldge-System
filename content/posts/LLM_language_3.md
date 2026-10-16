+++
date = '2026-10-16T04:33:57+02:00'
draft = false
title = 'Cyberdeck Architecture - A LLM language-2nd'
weight = 43
+++

# Building a Logic-Capable Specialist LLM: From RAG to a Purpose-Built Encoder

*A field note on expert systems, dense knowledge graphs, and the case for training your own model.*

---

## The starting question

Most conversations about “custom LLMs” collapse into one of three answers:  
  
1. Use RAG.  
2. Fine-tune a pretrained model.  
3. Train from scratch.  
  
The first two are well-trodden. The third is usually dismissed as impractical. But there is a narrow, specific case where from-scratch  
training is not just viable — it is the right tool. This article is about that case, drawn from a real architecture: a headnode that orchestrates  
a cluster of low-cost machines, each hosting small RAG experts over isolated data vaults, with a large “Cortex” model for cross-vault synthesis  
and a hidden from-scratch model enforcing structure and discovering hidden connections.  
  
The core insight is this: **an LLM finds *nearby* things; SQL finds *matching* things; meaning is found by combining both and  
letting a verifier decide.**  
  
---

## Part 1: The three approaches, and where each one breaks

### RAG (Retrieval-Augmented Generation)

RAG connects a pretrained LLM to an external knowledge base. You chunk your documents, embed them, store the vectors, and at query  
time retrieve the closest chunks as context.  
  
**What it does well:**
- Grounds answers in your data.  
- Updates in real time — change the data, change the answers.  
- No training required.  
   
**Where it breaks:**
- The LLM’s world knowledge bleeds in. If your domain uses “attention” differently than the general web, the model may substitute  
its prior.  
- Retrieval is symmetric. Cosine similarity cannot express `A explains B` vs `B explains A`.  
- In a dense knowledge cluster, hub words dominate every vector. Everything looks close to everything else.  
  
### Fine-tuning

Fine-tuning modifies a pretrained model’s weights on your data, usually via LoRA or QLoRA. It teaches style, format, and  
reasoning patterns.  
  
**What it does well:**
- Deep behavioral customization.  
- Much cheaper than pretraining.  
- Can be done on a single consumer GPU for 7B–8B models.  
  
**Where it breaks:**
- Still inherits the base model’s priors.  
- Needs labeled data in instruction/response format.  
- Cannot create new architectural affordances — you get what the base model offers.  
  
### From-scratch training

You initialize a transformer with random weights, train a tokenizer on your corpus, and run the training loop yourself.  
  
**What it does well:**
- You own the weights, the tokenizer, and the architecture.  
- The model’s space is shaped by your domain, not the web.  
- You can design the objective to match your task.  
  
**Where it breaks:**
- You need volume and diversity of data.  
- General language ability does not come for free.  
- At scale, the compute cost is real.  
  
The critical realization: **from-scratch is not one thing.** It is practical for a narrow, formal, validated domain, and impractical  
for a general assistant. The question is not “can I train from scratch?” but “is my domain narrow enough, formal enough, and label-rich  
enough to justify it?”  
  
---
  
## Part 2: The expert system architecture

The system described here has five layers:  
  
```
┌─────────────────────────────────────────────────────────┐
│  Orchestrator (routes questions, merges results)        │
├─────────────────────────────────────────────────────────┤
│  Cortex: large LLM, speculative decoding, 64GB RAM node │
│  Cross-vault synthesis, ambiguity resolution, planning  │
├─────────────────────────────────────────────────────────┤
│  Per-vault RAG experts (small LLMs on office hardware)  │
│  Fast factual lookup within one data silo               │
├─────────────────────────────────────────────────────────┤
│  Built LLM: hidden, background, quality enforcement     │
│  Structural validation, cross-reference scoring         │
├─────────────────────────────────────────────────────────┤
│  Symbolic layer (graph DB, SQL, rule engine, verifier)  │
│  Ground truth. The LLM proposes; the verifier disposes. │
└─────────────────────────────────────────────────────────┘
```
  
The built LLM is not the global brain. Cortex is. The built LLM is the **compiler** — it enforces form, scores candidates, and discovers  
hidden connections. It sits between the symbolic layer and the user, invisible and always on.  
  
### Why the symbolic layer is non-negotiable

No purely learned system reliably separates meaningful from coincidental relations at scale. The state of the art is:  
  
- **Embeddings + graph + metadata** to rank candidates.  
- **Symbolic checks** to eliminate what is provably wrong.  
- **User verification** to resolve the rest.  
- **Logging** to train the next iteration.  
  
If you let the LLM be the final judge, you get confident coincidences.  
  
---
  
## Part 3: The hidden-connection problem

This is the heart of the architecture. The question:  
  
> Given a file, what other files in this corpus are semantically close but structurally far?  
  
SQL cannot answer this. It matches strings, not concepts. `LIKE '%attention%'` finds the word, not the idea.  
  
A general embedding model can approximate it, but it wastes capacity on world knowledge you do not need. It blurs the discriminative tail.  
  
The query you actually want is a **three-condition conjunction**:  
  
1. **Graph distance is large** — the two files are in different cores, far apart in the link graph.  
2. **Embedding distance is small** — their vectors are close in your trained space.  
3. **Shared vocabulary is tail, not hub** — the similarity comes from discriminative terms, not common words.  
  
That conjunction is the signal. It is also, not coincidentally, the shape of a **long-range link** in a small-world network. The vault has  
those links sparsely; the model finds candidates for new ones.  
  
### The residual failure modes

Even in a closed domain, three problems remain:  
  
**Polysemy inside the domain.** Two files both use “attention” — one about transformer attention, one about visual attention. Same vault.  
Close in vector space. Coincidental.  
  
**Hub saturation.** In a tightly connected cluster, a handful of hub words dominate every file’s vector. Everything starts looking close to everything else.  
The knot becomes a blur precisely where the vault is richest.  
  
**Symmetric flattening.** Cosine similarity is symmetric. Meaning is not. `A explains B` is not `B explains A`.  
  
### The graph is the signal the vectors lack

The Obsidian structure — a dense knot with cores connected to each other — carries information the embedding space cannot:  
  
- **Explicit links** are ground-truth positive pairs.  
- **Backlinks, tags, folder placement** are weaker labels.  
- **Graph distance** is orthogonal to embedding distance. Two files can be graph-distant and embedding-close — that is exactly the query.  
- **Community structure** gives you the scale at which a relation should be evaluated.  
  
The training signal is the graph itself. Every link is a positive. Every rejected suggestion is a negative. This is why from-scratch is  
viable here: you have labels that general models do not.  
  
---

## Part 4: The dictionary and the index

### The dedicated dictionary

In a transformer, the dictionary is the **embedding matrix** — one row per token. You can make it explicitly domain-shaped in three ways:  
  
**1. Custom tokenizer.** Train BPE or Unigram on your corpus, not on general text. A general tokenizer fragments your terms into pieces  
the model must reassemble. A domain tokenizer gives each term its own token and its own learned vector. This is the single largest  
win for a closed domain.  
  
**2. Explicit lexical anchors.** Reserve token slots for graph concepts: link types, tags, folder names, entity IDs, schema fields.  
The model then has first-class representations for structural vocabulary.  
  
**3. Hub down-weighting.** Weight tokens by inverse document frequency before the model sees them. Common terms contribute less.  
The tail carries the discriminative signal.  
  
### The dedicated index

Three layers, queried together:  
  
**Vector index (HNSW or IVF).** Approximate nearest neighbors over file-level or chunk-level embeddings. Fast, CPU-only, one node.  
  
**Graph index.** The Obsidian link graph, backlinks, tags, folders. Exact structural distance and typed relations.  
  
**Lexical index.** Inverted index over the tail vocabulary only. BM25 or similar. Catches exact matches the vector index ranks low.  
  
A pair that scores high on all three is a strong hidden connection. A pair that scores high only on the vector index is a candidate  
for the scorer.  
  
---

## Part 5: The training objective

You are not training a generative LLM. You are training a **contrastive encoder** whose space is shaped by the graph.  
  
**Positives:** existing links, backlinks, user-accepted suggestions, files in the same core.  
  
**Negatives:** random pairs, user-rejected suggestions, files in distant cores.  
  
**Hard negatives:** graph-distant pairs that are embedding-close but user-rejected. These are the most valuable examples in the entire dataset.  
  
**Weighted loss:** down-weight hubs via IDF or SIF so the gradient flows to the tail.  
  
### Why the user-verification loop matters

Every accepted vault is a positive example. Every rejected vault is a negative. Every edited vault is a preference pair. Every question the  
vault later answers well is reinforcement.  
  
The user is not just a gate — they are the labeler. That is the only reason a hidden synthesizer is viable.  
  
### The feedback loop risk

If the built LLM proposes vaults, small experts answer user questions, and the built LLM trains on the resulting logs, the system can converge  
 on its own biases. You need at least one of:  
  
- A held-out set of real, messy, out-of-distribution questions.  
- Periodic sampling of rejected vaults for re-review.  
- A symbolic or statistical check that the vault distribution is not collapsing.  
- Cortex as an independent critic that does not train on the same loop.  
  
---

## Part 6: What the built LLM is actually for

Four roles, in order of fit:  
  
| Role | What it does | Why from-scratch fits |  
|---|---|---|
| **Structural enforcer**                  | Validates schema, types, references, grammar. Hidden, background, always on. | Formal, validatable, high-volume, repetitive.                       |  
| **Pair scorer**                          | Takes two files or concepts, outputs relation type and confidence. | Trained on graph labels. Hard negatives teach the key distinction.            |  
| **Candidate proposer**                   | Generates likely cross-references across vaults. High recall, some coincidences. | Verification is downstream. Proposer does not need to be right. |  
| **Draft model for speculative decoding** | Acts as the fast draft model for Cortex. | If trained on Cortex’s domain outputs, it accelerates inference.                                        |  
  
The built LLM is not a judge. It is a proposer and a scorer. The symbolic layer and the user decide truth.  
  
---

## Part 7: What to build first
  
**1. Tokenizer.** Domain BPE, 16k–32k vocab, special tokens for graph structure.  
  
**2. Encoder.** Small transformer, 6–12 layers, 384–768 dim, context 256–512. Bidirectional or causal; for retrieval, bidirectional is usually better.  
  
**3. Training data from the graph.** Positives from links. Negatives from random and rejected pairs. Hard negatives from graph-distant embedding-close rejects.  
  
**4. IDF/SIF weighting** on the input side before the model sees tokens.  
  
**5. Vector index** over the trained embeddings. HNSW, one node, no GPU.  
  
**6. Query layer** that joins vector index, graph index, and lexical index.  
  
**7. Scorer** — a small head or a separate classifier that takes a candidate pair and outputs meaningful vs coincidental with a rationale.  
  
**8. User loop** that logs accept/reject and feeds back into training.  
  
Start with the encoder. It is the model that does what SQL cannot and what a general embedding model does poorly. Everything else is orchestration around it.  
  
---

## Part 8: The honest ceiling

This works well when:  
  
- The vault is large enough to train a tokenizer and encoder meaningfully — thousands of files, not dozens.  
- The graph has enough links to generate training signal — hundreds to thousands of positive pairs.  
- The domain is closed enough that your vocabulary does not need general-world knowledge.  
- You are willing to run the user-verification loop and log the labels.  
  
It works poorly when the vault is tiny, the graph is sparse, or the domain overlaps heavily with general knowledge. In those cases, a fine-tuned general  
embedding model plus a small classifier will beat a from-scratch encoder, because you do not have enough signal to shape a new space.  
  
But if your vault is dense, your graph is rich, and your vocabulary is yours, then a from-scratch encoder with a dedicated dictionary and a dedicated  
index is not just viable — it is the right tool.  
  
---

## Closing: the brain observation is not just a metaphor
  
A dense knot with cores connected to each other is **small-world network topology**. Clusters, hubs, long-range links. The connectome has the same shape.  
  
Two consequences follow:  
  
1. **Local structure is already dense.** Intra-knot relations are mostly redundant. The model does not need to learn them; the knot already encodes them.  
2. **Long-range links carry the meaning.** Inter-core connections are sparse, expensive, and informative. They are where the vault thinks.  
  
So the built LLM should be trained to predict **long-range links**. The local ones are free. This is link prediction on the sparse backbone, and it is a  
 much smaller, more tractable problem than “understand the whole vault.”  
  
The vector space tells you what is *near*. The graph tells you what is *connected*. Meaning is what happens when those two disagree — graph-distant but  
 embedding-close. That disagreement is your signal. Everything else is noise.  
  
---

*This article is a design note, not a benchmark. The architecture described is one instance of a broader pattern: narrow, formal, label-rich domains are  
 where from-scratch training earns its place. The general assistant is a different problem, solved by different tools.*  
  
