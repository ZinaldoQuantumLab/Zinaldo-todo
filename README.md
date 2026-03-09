# ⚛ Zinaldo Quantum Lab — Task Manager

Interface web avancée de gestion de tâches construite avec **Python + Flask**.

---

## 🚀 Installation

```bash
# 1. Cloner / décompresser le projet
cd zinaldo-todo

# 2. Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
python app.py
```

Ouvrir le navigateur sur → **http://localhost:5000**

---

## ✨ Fonctionnalités

| Fonctionnalité | Détail |
|---|---|
| ➕ Créer une tâche | Titre, description, priorité, catégorie, date d'échéance, tags, sous-tâches |
| ✏️ Modifier | Édition complète de toute tâche existante |
| ✓ Compléter | Toggle rapide directement sur la carte |
| 🗑️ Supprimer | Suppression individuelle avec confirmation |
| 🔍 Recherche | Recherche en temps réel titre + description |
| 🏷️ Filtres | Par statut, priorité, catégorie |
| ☑️ Actions en lot | Sélectionner → Terminer / Rouvrir / Supprimer |
| 📊 Statistiques | Total, complétées, en retard, barre de progression |
| 🏷 Tags | Tags personnalisés sur chaque tâche |
| 📋 Sous-tâches | Checklists imbriquées avec barre de progression |
| 🔃 Tri | Par date, priorité, échéance |
| 💾 Persistance | Données stockées en JSON (tasks.json) |

---

## 🗂️ Structure du projet

```
zinaldo-todo/
├── app.py              ← Serveur Flask + API REST
├── tasks.json          ← Données persistantes (auto-créé)
├── requirements.txt
├── README.md
└── templates/
    └── index.html      ← Interface complète (HTML + CSS + JS)
```

---

## 🔌 API REST

| Méthode | Route | Description |
|---|---|---|
| GET | `/api/tasks` | Lister les tâches (filtres via query params) |
| POST | `/api/tasks` | Créer une tâche |
| PUT | `/api/tasks/<id>` | Modifier une tâche |
| DELETE | `/api/tasks/<id>` | Supprimer une tâche |
| POST | `/api/tasks/bulk` | Action en lot |
| GET | `/api/stats` | Statistiques globales |

**Query params pour GET /api/tasks :**
- `status` : `all` | `active` | `completed`
- `priority` : `high` | `medium` | `low`
- `category` : nom de la catégorie
- `search` : terme de recherche

---

## 🎨 Stack Technique

- **Backend** : Python 3.10+ / Flask 3.x
- **Frontend** : HTML5 + CSS3 + JavaScript Vanilla
- **Fonts** : Syne (Google Fonts) + JetBrains Mono
- **Persistance** : JSON file (facilement migrable vers SQLite/PostgreSQL)

---

*Zinaldo Quantum Lab © 2025*
