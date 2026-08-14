# Project Memory & Architectural Overview: MiniChatGPT (Knowledge Search Pro)

## Project Summary
**Knowledge Search Pro** (internally structured as **MiniChatGPT**) is a desktop knowledge base and search application built with Python and Tkinter. It allows users to store, categorize, tag, fuzzy-search, and manage knowledge entries locally.

---

## Directory & File Structure

```
MiniChatGPT/
│
├── main.py                 # Application entry point
├── main.spec               # PyInstaller build specification file
├── requirements.txt        # Third-party Python dependencies (rapidfuzz)
├── memory.md               # Project memory, context, and documentation
│
├── core/                   # Business logic and data management layer
│   ├── __init__.py
│   ├── storage.py          # CRUD manager for knowledge data (JSON & TXT export)
│   ├── search.py           # Multi-field fuzzy search engine using rapidfuzz
│   ├── backup.py          # Automatic timestamped backup & retention manager
│   ├── smart_paste.py      # Smart paste formatter (bolds headings, breaks sentences after full stops with line gaps, extracts metadata)
│
├── ui/                     # Main user interface (Tkinter / TTK)
│   ├── __init__.py
│   ├── main_window.py      # Primary window combining search, results, and answers
│   ├── search_panel.py     # Search input bar component
│   ├── result_panel.py     # Search results list component
│   └── answer_panel.py     # Knowledge entry detail view component
│
├── admin/                  # Admin CRUD interface
│   ├── __init__.py
│   ├── login.py            # Admin login modal window
│   ├── window.py           # Admin main dashboard window
│   ├── form.py             # Entry creation/editing form and treeview
│   └── actions.py          # Actions handler (Save, Update, Delete, Smart Paste)
│
├── data/                   # Active data storage directory
│   ├── config.json         # Application settings and admin credentials
│   ├── knowledge.json      # Primary JSON database for knowledge entries
│   └── knowledge.txt       # Plain-text formatted export of all knowledge
│
└── backups/                # Automatically managed timestamped backups
```

---

## Core Components & Functional Logic

### 1. Data Storage (`core/storage.py`)
- Manages `data/knowledge.json` (primary database) and auto-generates `data/knowledge.txt` on every save.
- Triggers automatic backup creation via `BackupManager` whenever data is saved, updated, or deleted.
- Auto-increments integer IDs (`next_id`).

### 2. Search Engine (`core/search.py`)
- Evaluates queries using multi-field scoring (`title`, `tags`, `keywords`, `category`, `answer`).
- Uses `rapidfuzz.fuzz.ratio` for fuzzy matching, exact match scoring, prefix matching, and phrase bonuses.
- Returns search results sorted descending by relevance score (threshold >= 50).

### 3. Backup System (`core/backup.py`)
- Copies active data files to `backups/` with timestamp suffixes (`YYYYMMDD_HHMMSS`).
- Reads `max_backups` setting from `data/config.json` and automatically cleans up older backups.

### 4. User & Admin Interfaces (`ui/` & `admin/`)
- **Public UI**: Allows non-admin browsing, real-time searching, and viewing full answers.
- **Admin UI**: Password-protected dashboard (`admin_username` / `admin_password` in `data/config.json`) providing full CRUD functionality and Smart Paste clipboard ingestion.

---

## Data Schemas

### Knowledge Item Object (`data/knowledge.json`)
```json
{
  "id": 1,
  "title": "Title of Knowledge Entry",
  "category": "Category Name",
  "keywords": ["keyword1", "keyword2"],
  "tags": ["tag1", "tag2"],
  "answer": "Detailed answer or instructions..."
}
```

### Configuration (`data/config.json`)
```json
{
  "app_name": "Knowledge Search Pro",
  "version": "1.0",
  "theme": "light",
  "admin_username": "admin",
  "admin_password": "admin1",
  "backup_on_save": true,
  "max_backups": 1
}
```

---

## Setup & Running Instructions

### Requirements
- Python 3.8+
- `rapidfuzz` (`pip install -r requirements.txt`)

### Execution
```bash
python main.py
```
