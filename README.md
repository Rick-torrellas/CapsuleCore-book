# Capsule Core book

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Version](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Rick-torrellas/CapsuleCore-book/badges/version.json)
[![CI CD](https://github.com/Rick-torrellas/CapsuleCore-book/actions/workflows/main.yaml/badge.svg)](https://github.com/Rick-torrellas/CapsuleCore-book/actions/workflows/main.yaml)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Download](https://img.shields.io/github/v/release/Rick-torrellas/CapsuleCore-book?label=Download&color=orange)](https://github.com/Rick-torrellas/CapsuleCore-book/releases)
[![Ask DeepWiki](https://img.shields.io/badge/DeepWiki-Documentation-blue?logo=gitbook&logoColor=white)](https://deepwiki.com/Rick-torrellas/CapsuleCore-book)

---

## Installation

Ensure you have your environment ready (recommended to use uv or pip):

```bash
pip install capsulecore-book
```

## usage

```python
from CapsuleCore_book import JSONLexicon, Codex

lexicon = JSONLexicon(storage_path="./my_knowledge_base.json")
codex = Codex(lexicon)

entry1 = codex.create_entry(
    title="Atomic Habits 3",
    content="Small changes lead to remarkable results.",
    tags=["productivity", "books"]
)

entry2 = codex.create_entry(
    title="The Power of Habit 3",
    content="Habits are the compound interest of self-improvement.",
    tags=["productivity", "books"]
)

codex.create_relation(entry1.id, entry2.id, relation_type="related_to")
```