<div align="center">

# 🤖 Verse AI Knowledge

AI knowledge base for Verse / UEFN — source-grounded prompts, API references, UI tools, RAG and validation.

🇫🇷 Français · 🇬🇧 English · **V22 — Knowledge Integrity & Agent Reliability**

> 🧠 **Règle principale / Core rule:**  
> **Ne jamais inventer une API Verse. / Never invent a Verse API.**

</div>

</div>

---

# 🇫🇷 Français

## ✨ Qu'est-ce que Verse AI Knowledge ?

**Verse AI Knowledge** est une base de connaissances structurée conçue pour aider les IA comme **ChatGPT, Codex, Claude, Gemini** et d'autres modèles capables de lire un dépôt GitHub à générer du code **Verse / UEFN** plus propre, plus fiable et plus maintenable.

Le projet ne “réentraîne” pas directement une IA.

Il lui fournit plutôt :

- 📚 une base de connaissances Verse / UEFN ;
- 🧠 un Master Prompt spécialisé ;
- 🔎 des règles de recherche et de priorité des sources ;
- 🧩 un créateur d'interfaces UI ;
- 🛡️ des règles anti-hallucination ;
- 🧪 des outils de validation statique ;
- 🗂️ des catalogues d'API et de modules ;
- 🔗 de la provenance pour les sources externes ;
- 🧰 des patterns et exemples de projets ;
- 📊 du RAG, de l'Evidence et des outils VerseLab.

---

## 🚨 Règle absolue

> ### ❌ Ne jamais inventer une API Verse.

Une IA utilisant ce dépôt ne doit jamais inventer :

- une classe ;
- une fonction ;
- un événement ;
- un module ;
- une signature ;
- un effet ;
- un import ;
- une propriété Verse.

Si une API exacte n'est pas vérifiable :

```text
TODO(API VERIFY)
```

doit être utilisé à la place d'une API inventée.

---

## 🚀 Démarrage rapide

### 1️⃣ Donne le dépôt à ton IA

```text
https://github.com/ariyo-code/Verse-AI-Knowledge
```

Puis demande-lui de lire en priorité :

```text
AGENTS.md
AI_GUIDE.md
portable/VERSE_AI_MASTER_PROMPT_v21_WITH_UI.txt
knowledge/ROUTING.md
knowledge/api_catalog.json
knowledge/module_catalog.json
```

### 2️⃣ Pour une interface UI

L'IA doit aussi lire :

```text
portable/ui_creator/VERSE_UI_CREATOR_MASTER_PROMPT.txt
portable/ui_creator/COMPONENT_LIBRARY.json
portable/ui_creator/UI_SPEC.schema.json
```

### 3️⃣ Prompt prêt à copier

Le prompt complet à donner à une IA est disponible ici :

```text
PROMPT_AI_CHAT_FR_EN.md
```

---

## 💬 Exemple de demande

```text
=== USER TASK ===

Crée un système complet de garage RP en Verse.

Fonctionnalités :
- véhicules possédés par joueur ;
- persistance ;
- verrouillage / déverrouillage ;
- clés temporaires ;
- menu de garage ;
- un seul véhicule actif par joueur ;
- gestion des respawns ;
- nettoyage à la déconnexion ;
- compatibilité multijoueur.
```

---

## 🧠 Priorité des connaissances

Quand l'IA doit générer du Verse, elle doit suivre cet ordre :

1. 🥇 le code fourni directement par l'utilisateur ;
2. 🥈 le contenu vérifié du dépôt ;
3. 🥉 les API / documentations référencées dans le dépôt ;
4. 📚 les exemples disposant d'une provenance claire ;
5. 🤖 les connaissances générales du modèle uniquement si elles ne contredisent pas le dépôt.

---

## ✅ Statuts de validation

| Statut | Signification |
|---|---|
| 📝 `draft` | Code généré ou écrit, non validé dans UEFN |
| 🔍 `static-checked` | Vérifications statiques du dépôt effectuées |
| 📚 `upstream-verified` | Soutenu par une source upstream fiable |
| 🛠️ `compiled` | Une vraie compilation UEFN existe |
| ✅ `verified` | Compilé et testé fonctionnellement |
| 🌐 `multiplayer-verified` | Testé dans un contexte multijoueur pertinent |

> ⚠️ Une validation statique ne remplace jamais une vraie compilation UEFN.

Tout nouveau code généré commence par défaut avec :

```text
draft
```

---

## 🧩 UI Creator

Le projet contient un système spécialisé pour créer et structurer des interfaces Verse / UEFN.

### Pipeline

```text
Demande / Image / Référence
            ↓
        UI Spec
            ↓
   Hiérarchie composants
            ↓
       État + événements
            ↓
 Implémentation Verse vérifiée
```

Il inclut :

- 🧱 bibliothèque logique de composants ;
- 🧾 schéma UI structuré ;
- 🎨 création d'interface ;
- ♻️ refonte d'interface ;
- 🖼️ génération depuis une référence visuelle ;
- 🔗 planification des événements ;
- 📱 responsive design ;
- 🧹 refactorisation ;
- 🛡️ règles anti-hallucination des widgets Verse.

Dossier :

```text
portable/ui_creator/
```

---

## 🧠 Master Prompt Verse

Le fichier principal est :

```text
portable/VERSE_AI_MASTER_PROMPT_v21_WITH_UI.txt
```

Il couvre notamment :

- 📦 imports et modules ;
- ⚠️ failure contexts ;
- ⚙️ effets et signatures ;
- 👤 état joueur ;
- 🔄 lifecycle ;
- ⏳ concurrence et tâches async ;
- 🧹 cleanup ;
- 💾 persistance ;
- 🚗 véhicules ;
- 👥 équipes ;
- 🎮 Creative Devices ;
- 🌐 multijoueur ;
- 🧩 UI ;
- 🏗️ architecture maintenable ;
- 🧪 vérification avant réponse.

---

## 🔎 Base de connaissances

Les fichiers principaux sont :

```text
knowledge/ROUTING.md
knowledge/api_catalog.json
knowledge/module_catalog.json
knowledge/index.json
```

---

## 🧪 RAG, Evidence & VerseLab

Le projet contient également plusieurs systèmes de recherche, d'analyse et de validation :

```text
rag/
curation/
verification/
reports/
lab/
benchmark/
benchmarks/
tests/
tools/
```

🎯 Objectif : récupérer les meilleures preuves disponibles avant de produire du code.

---

## 📂 Structure du projet

```text
Verse-AI-Knowledge/
├── 📁 .github/
├── 📁 benchmark/
├── 📁 benchmarks/
├── 📁 bridge/
├── 📁 curation/
├── 📁 dependencies/
├── 📁 docs/
├── 📁 errors/
├── 📁 examples/
├── 📁 external/
├── 📁 knowledge/
├── 📁 lab/
├── 📁 maintenance/
├── 📁 mcp/
├── 📁 portable/
│   └── 📁 ui_creator/
├── 📁 projects/
├── 📁 prompts/
├── 📁 rag/
├── 📁 reports/
├── 📁 schemas/
├── 📁 staging/
├── 📁 systems/
├── 📁 templates/
├── 📁 tests/
├── 📁 tools/
├── 📁 verification/
├── 📄 AGENTS.md
├── 📄 AI_GUIDE.md
├── 📄 README.md
├── 📄 README_FR.md
├── 📄 README_EN.md
├── 📄 SECURITY.md
├── 📄 LICENSE.md
├── 📄 THIRD_PARTY_NOTICES.md
├── 📄 VERSION.md
└── 📄 manifest.json
```

---

## 🔐 Sécurité

Ne publie jamais :

- 🔑 clés API ;
- 🎮 identifiants Epic Games ;
- 🤖 token Discord ;
- 🗄️ URL de base de données contenant des identifiants ;
- 🔒 mots de passe ;
- 📄 fichiers `.env` privés ;
- 🪪 tokens d'authentification ;
- 🔐 clés SSH privées.

Voir :

```text
SECURITY.md
```

---

## 📜 Licence

**Verse AI Knowledge n'est pas un projet open-source sauf si le propriétaire du dépôt change explicitement sa licence.**

Les conditions applicables au contenu original du projet sont définies dans :

```text
LICENSE.md
```

Le fait que le dépôt soit public ne donne pas automatiquement le droit de :

- redistribuer le projet ;
- republier le ZIP ;
- créer un mirror public ;
- revendre le projet ;
- republier une copie substantielle ;
- supprimer les mentions de copyright ou de provenance.

Les contenus tiers conservent leurs propres licences.

Voir :

```text
THIRD_PARTY_NOTICES.md
```

---

## ⚠️ Disclaimer

Verse, Unreal Editor for Fortnite, Fortnite, Epic Games ainsi que les marques et technologies associées appartiennent à leurs propriétaires respectifs.

**Verse AI Knowledge est un projet indépendant et n'est ni affilié, ni approuvé, ni sponsorisé par Epic Games.**

Le code généré par une IA peut contenir des erreurs.  
Pour un projet important, compile et teste toujours le code dans UEFN.

---

<div align="center">

# 🧠 Verse AI Knowledge v22

### 🇫🇷 Du Verse basé sur des sources, pas sur des API inventées.  
### 🇬🇧 Source-grounded Verse generation. No invented APIs.

⭐ If this project helps you, consider starring the repository.

</div>
