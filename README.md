<p align="center">
  <img src="011-logo-svg.svg" alt="TypeTwo AI Logo" width="200">
</p>

# typetwo ai: Autonomous Agent for Drug Discovery

Retrieve, verify, and analyze drug and medical data from specialized databases.

## Beta Preview

The AI agent is currently in beta. You can test the live version here:
[beta.typetwo.ai](https://beta.typetwo.ai/).

## Overview  

This system enables natural language search over relational drug and medical databases, currently supporting *ChEMBL 35*. Users can input queries in plain English, and the AI:  

- Interprets the request and generates a valid SQL query.  
- Executes the query on the database.  
- Analyzes the retrieved results to check for relevance and completeness.  
- If results are unsatisfactory, it refines the query and repeats the process until an accurate response is obtained.

```mermaid
graph TB
    User[User/UI] -->|Asks question| Orchestrator[🧠 Orchestrator Agent]
    
    subgraph Agent Loop
        Writer["📝 Writer Agent"]
        Checker[🕵️ Checker Agent]
        Database[(Database)]
    end
    
    Orchestrator -->|Gives instructions| Writer
    Writer -->|Executes SQL query| Database
    Database -->|Returns results| Checker
    Checker -->|Results bad| Writer
    Checker -->|Results good| User
```

## Tech Stack

- **Frontend:** React + TypeScript + Vite  
- **Backend:** Python + Flask  
- **LLMs:** Gemini 2.0, Claude 3.5 with tools/function calling
- **Database:** Google Cloud SQL (currently hosting ChEMBL 35)  
- **Deployment:** Google Cloud (App Engine, Cloud Build)


## Project Links  

- **Project Website:** [https://typetwo.ai/](https://typetwo.ai/)  
- **Beta Deployment:** [https://beta.typetwo.ai/](https://beta.typetwo.ai/)

<details>
  <summary>Agent Schema</summary>
  ```mermaid
  sequenceDiagram
    participant App
    participant Orchestrator
    participant Writer as Query Writer
    participant Checker as Query Checker
    participant DB as Database

    App-->>Orchestrator: User Query
    Orchestrator-->>App: QTAAOTF Answer
    App-->>Writer: Query Instructions
    Writer-->>App: Query
    App-->>DB: Query
    DB-->>App: Search Results
    App-->>Checker: Search Results
    
    Checker-->>App: Check Results
    
    alt Results Not Satisfactory
        App-->>Writer: Rewrite Query with New Instructions
    else Results Good
        App-)App: Return Results
    end
  ```