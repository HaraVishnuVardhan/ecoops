# 🌱 EcoOps 2.0
 
### Confidence-Aware Campus Sustainability Agent
 
> **We don't just optimize — we know when NOT to optimize.**
 
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-orange)](https://langchain-ai.github.io/langgraph/)
[![MCP](https://img.shields.io/badge/MCP-FastMCP-purple)](https://modelcontextprotocol.io/)
[![RAG](https://img.shields.io/badge/RAG-ChromaDB-yellow)](https://www.trychroma.com/)
[![LLM](https://img.shields.io/badge/LLM-Llama%203.2-lightgrey)](https://ollama.com/)
 
EcoOps 2.0 is an agentic AI system for campus sustainability operations. It detects abnormal energy, water, and waste consumption, grounds its analysis in campus policy documents, calculates confidence scores, and safely decides whether to **recommend**, **monitor**, or **escalate** — always keeping a human in the loop.
 
---
 
## 🎯 Problem
 
Campus facilities teams often notice unusual resource consumption, but an anomaly doesn't always mean something is wrong. A sudden spike could be caused by:
 
- Campus events
- Normal operational changes
- Sensor uncertainty
- Actual infrastructure problems
Automatically changing operations based on an anomaly alone can lead to unsafe or incorrect decisions. EcoOps investigates these anomalies intelligently while keeping humans in control of any real-world action.
 
---
 
## 🏆 Track
 
**Sustainability, Smart Infrastructure & Future Communities**
 
---
 
## ⚙️ System Design
 
```
                    ┌─────────────────┐
                    │  React Frontend │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │     FastAPI     │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │    LangGraph    │
                    │   Orchestrator  │
                    └────────┬────────┘
                             ↓
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
        ┌──────────┐   ┌──────────┐   ┌────────────┐
        │ Anomaly  │   │   RAG    │   │ Historical │
        │ MCP Tool │   │ ChromaDB │   │  MCP Tool  │
        └──────────┘   └──────────┘   └────────────┘
              └──────────────┼──────────────┘
                             ↓
                    ┌─────────────────┐
                    │   Confidence    │
                    │     Scoring     │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │  Safety Router  │
                    └───────┬─────────┘
                            ↓
             ┌──────────────┼──────────────┐
             ↓              ↓              ↓
        RECOMMEND        MONITOR        ESCALATE
             ↓              ↓              ↓
          Llama          Llama        MCP Alert
        + Ollama       + Ollama       → Human
```
 
---
 
## ✨ Features
 
- Multi-step agentic workflow using **LangGraph**
- Real tool integration using **FastMCP**
- RAG grounding using **ChromaDB**
- Confidence-aware safety decisions
- RECOMMEND / MONITOR / ESCALATE routing
- Human escalation for unsafe or uncertain cases
- Local LLM inference using **Llama 3.2** + **Ollama**
- Full audit trail for every system decision
- Resilience against tool, RAG, and LLM failures
---
 
## 🏗️ Architecture
 
| Component       | Technology         |
|-----------------|---------------------|
| Frontend        | React + Vite        |
| Backend         | FastAPI             |
| Orchestration   | LangGraph           |
| Tool Layer      | FastMCP / MCP        |
| Vector Store    | ChromaDB            |
| Grounding       | RAG                 |
| LLM             | Llama 3.2 3B         |
| Local Runtime   | Ollama               |
 
---
 
## 🛡️ Confidence & Safety
 
**The LLM does not make the final safety decision.**
 
EcoOps calculates a confidence score from three signals:
 
- Anomaly / data confidence
- Policy retrieval confidence
- Historical / context confidence
A deterministic **safety router** then decides the outcome:
 
| Condition                  | Decision       |
|-----------------------------|----------------|
| Confidence ≥ 0.80           | 🟢 RECOMMEND   |
| Confidence 0.50 – 0.79      | 🟡 MONITOR     |
| Confidence < 0.50           | 🔴 ESCALATE    |
| Extreme anomaly             | 🔴 ESCALATE    |
| Required tool failure       | 🔴 ESCALATE    |
 
Extreme anomalies are always blocked from automatic optimization. Operational changes always require human approval.
 
---
 
## 📚 RAG Grounding
 
EcoOps retrieves the relevant policy document for each detected anomaly type:
 
- Energy anomaly → `energy_policy.txt`
- Water anomaly → `water_policy.txt`
- Waste anomaly → `waste_policy.txt`
Policies live under:
 
```
rag/
└── documents/
    ├── energy_policy.txt
    ├── water_policy.txt
    └── waste_policy.txt
```
 
> These are synthetic demonstration policies created for the hackathon.
 
---
 
## 🧪 Demo Scenarios
 
| Location          | Resource | Change | Context            | Result       |
|--------------------|----------|--------|---------------------|--------------|
| Academic Block A    | Energy   | +15%   | Normal operations   | 🟡 MONITOR   |
| Hostel C            | Water    | +35%   | Campus event        | 🟡 MONITOR   |
| Chemistry Lab       | Energy   | +383%  | 2:47 AM              | 🔴 ESCALATE  |
 
### Chemistry Lab Example
 
The system detects an extreme energy anomaly:
 
- **Current:** 28,000
- **Baseline:** 5,800
- **Increase:** ~383%
- **Time:** 2:47 AM
Because the anomaly is extreme, the safety router blocks automatic optimization and creates an MCP facilities alert for human review.
 
---
 
## 📁 Project Structure
 
```
ecoops/
├── agents/
│   ├── graph.py
│   ├── nodes.py
│   ├── router.py
│   └── state.py
├── backend/
│   └── main.py
├── mcp_tools/
│   ├── client.py
│   ├── server.py
│   └── tools.py
├── rag/
│   ├── documents/
│   ├── ingest.py
│   ├── retriever.py
│   └── llm.py
├── frontend/
├── test_mcp.py
├── test_graph.py
├── test_scenarios.py
├── requirements.txt
└── README.md
```
 
---
 
## 🚀 Quick Start
 
### Prerequisites
 
- Python 3.10+
- Node.js
- [Ollama](https://ollama.com/)
- Git
Pull the required model:
 
```bash
ollama pull llama3.2:3b
```
 
### 1. Start the MCP Server
 
```bash
cd C:\Users\vv510\OneDrive\eccops
.venv\Scripts\activate
python -m mcp_tools.server
```
 
### 2. Start the FastAPI Backend
 
Open a second terminal:
 
```bash
cd C:\Users\vv510\OneDrive\eccops
.venv\Scripts\activate
uvicorn backend.main:app --reload --port 8080
```
 
### 3. Start the React Frontend
 
Open a third terminal:
 
```bash
cd C:\Users\vv510\OneDrive\eccops\frontend
npm run dev
```
 
Then open [http://localhost:5173](http://localhost:5173)
 
### 4. Run Tests
 
```bash
cd C:\Users\vv510\OneDrive\eccops
.venv\Scripts\activate
python test_scenarios.py
```
 
---
 
## 🔍 Why It's Agentic
 
EcoOps is not a single LLM prompt. **LangGraph** coordinates multiple specialized processing steps, **MCP** provides tool access, **RAG** provides external grounding, and a confidence-based router conditionally determines the next action.
 
The LLM generates guidance — deterministic safety logic controls whether the system is allowed to recommend an action.
 
---
 
## 🔐 Safety Principle
 
> **We don't just optimize — we know when NOT to optimize.**
 
EcoOps never automatically changes campus operations. It can recommend, monitor, or escalate, while keeping humans in control.
 
---
 
## 🎥 Demo Video
 
📺 [Watch the demo on YouTube](https://youtu.be/U_8r7RdN0_4)
 
## 🔗 Repository
 
[github.com/HaraVishnuVardhan/ecoops](https://github.com/HaraVishnuVardhan/ecoops)
 

