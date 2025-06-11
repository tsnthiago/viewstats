## ✅ Objetivo

Deixar o projeto 100% compatível com o README e com a entrega esperada no desafio — incluindo endpoints, arquitetura, classificação com IA e navegação por taxonomia.

---

## ⏱️ Tempo estimado total: 4 a 6 horas (pode ser paralelizado)

---

## 🔥 **PLANO DE IMPLEMENTAÇÃO RÁPIDO**

### 🧱 FASE 1 — Estrutura mínima de pastas (30 min)

> Crie as pastas vazias e arquivos iniciais:

```bash
backend/app/
├── api/
│   ├── search.py
│   ├── taxonomy.py
│   ├── video.py
├── core/
│   ├── config.py
│   └── logger.py
├── models/
│   ├── search.py
│   ├── taxonomy.py
│   ├── video.py
├── utils/
│   └── text_cleaner.py
├── data/
│   └── taxonomy.json
```

> 🔧 Atualize `main.py` para incluir as rotas da pasta `api/`.

---

### 🔍 FASE 2 — Implementar `/search` (1h)

* **Crie `models/search.py`** com:

  ```python
  class SearchRequest(BaseModel):
      query: str
      topic_filter: Optional[str] = None
      top_k: int = 10
  ```

* **Crie `api/search.py` com o endpoint:**

  * Recebe `query`
  * Gera embedding (via `embedding_engine.py`)
  * Aplica filtro se houver (`topics_path`)
  * Busca no Qdrant e retorna resultados

> 🔥 Dica: use o `qdrant_client` com `query_vector` e `filter`

---

### 🌳 FASE 3 — Implementar `/taxonomy` (30 min)

* **Crie `data/taxonomy.json` com estrutura simulada inicialmente**
* **Crie `api/taxonomy.py` com o endpoint GET**

  * Retorna o JSON da árvore para navegação no frontend

---

### 🎥 FASE 4 — Implementar `/video/{id}` e `/channel/{id}` (1h)

* **Crie `api/video.py`**

  * Endpoint `GET /video/{id}` → `client.retrieve()`
  * Endpoint `GET /channel/{id}` → filtra por payload `channel_id`

---

### 🤖 FASE 5 — Classificação com LLM (1h–2h, paralelizável)

* **Crie `services/topic_generator.py`**

  * Função que recebe título + descrição + transcrição
  * Chama OpenAI (ou outro) e retorna tópicos hierárquicos
  * Armazena resultado em `topics_path` no payload

* **Integre isso no pipeline de indexação (no `/qdrant/insert`)**

> Pode usar `OpenAI`, `Mistral` ou `GPT-3.5` com um prompt claro.

---

### 🧠 FASE 6 — Montar e manter a taxonomia (1h)

* **Crie `services/taxonomy_builder.py`**

  * Constrói árvore incremental com base nos `topics_path` dos vídeos
  * Salva em `data/taxonomy.json`

> Pode usar estrutura com `_children` + `_videos` como discutido antes.

---

### 🧪 FASE 7 — Validação, docstrings e OpenAPI (30 min)

* Adicione exemplos de request/response nos schemas Pydantic
* Use `response_model=SearchResult` nos endpoints
* Comente o código com `"""Docstrings"""` nas funções principais

---

### ✅ FASE 8 — Checklist final

| Item                            | Feito? |
| ------------------------------- | ------ |
| Estrutura completa de pastas    | ✅      |
| Todos endpoints do README       | ✅      |
| Embedding + Qdrant funcionando  | ✅      |
| Taxonomia JSON e endpoint ativo | ✅      |
| Classificação IA por vídeo      | ✅      |
| Busca semântica com filtro      | ✅      |
| Schemas Pydantic definidos      | ✅      |
| README atualizado               | ✅      |

---

## 🎁 Extras se sobrar tempo

* Cache da taxonomia em memória
* Indexação de múltiplos vídeos via batch
* Logs estruturados com logger customizado
* Script para exportar tópicos únicos para visualização

---

## ⚙️ Posso te ajudar agora com:

* Esqueleto inicial das pastas com `__init__.py` e arquivos base
* Código do `/search` com integração real com Qdrant
* Prompt para classificação de tópicos com LLM
* Gerador incremental da taxonomia a partir de `topics_path`

Quer que eu comece por onde?
