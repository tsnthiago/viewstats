# ViewStats Video Data Processor

> **Nota:** Esta pasta (`viewstats/`) é um módulo de scripts dentro de um projeto maior. Todos os scripts, dados e artefatos aqui são autocontidos e independentes do restante do repositório.

## Visão Geral

Este pipeline processa dados de vídeos a partir de um CSV, extrai metadados estruturados e hierárquicos usando LLMs (Google Gemini), gera taxonomias, mapeia vídeos para tópicos e indexa tudo em um banco vetorial Qdrant para busca semântica. O pipeline é tolerante a falhas, modular e salva checkpoints em todas as etapas críticas.

## Estrutura da Pasta
```
viewstats/
│
├── main.py                # Orquestra todo o pipeline (entrada única)
├── config.py              # Configurações globais
├── data_handler.py        # Carregamento e preparação dos dados
├── llm_processor.py       # Prompt e processamento LLM
├── result_handler.py      # Merge e salvamento dos resultados
├── taxonomy_builder.py    # Consolidação e geração da taxonomia mestra
├── taxonomy_mapper.py     # Mapeamento de vídeos para IDs da taxonomia
├── indexer.py             # Indexação vetorial no Qdrant
├── embedding_service.py   # Geração de embeddings via OpenAI
├── requirements.txt       # Dependências Python
├── .gitignore             # Ignora dados, input, .env e caches
├── data/
│   ├── processed_videos.json     # Saída dos metadados dos vídeos
│   ├── draft_taxonomy.json       # Taxonomia bruta (intermediário)
│   ├── canonical_taxonomy.json   # Taxonomia refinada pelo LLM
│   ├── master_taxonomy.json      # Taxonomia mestra final (cópia da canônica)
│   ├── video_to_taxonomy_map.json # Mapeamento de vídeos para IDs da taxonomia
│   └── indexed_ytids.json        # Checkpoint de vídeos já indexados
└── input/
    └── input.csv                # Arquivo de entrada
```

## Requisitos
- Python 3.8+
- google-genai
- pandas
- tqdm
- python-dotenv
- qdrant-client
- sentence-transformers
- openai
- matplotlib (opcional)
- seaborn (opcional)

## Variáveis de Ambiente
Crie um arquivo `.env` com:
```
GOOGLE_API_KEY=...
OPENAI_API_KEY=...
INTERNAL_API_KEY=...
```
Essas variáveis são necessárias para acessar as APIs do Google Gemini, OpenAI (embeddings) e para upload automático da taxonomia.

## .gitignore
O projeto ignora automaticamente arquivos de dados, input, variáveis de ambiente e caches:
```
__pycache__/
.env
/input
*.env
/data
```

## Instalação
1. **Clone o repositório:**
   ```bash
   git clone <your-repo-url>
   cd viewstats
   ```
2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Prepare seus dados:**
   - Coloque seu CSV de entrada em `input/input.csv` (ou ajuste o caminho em `config.py`).

4. **Configure as variáveis de ambiente:**
   - Crie um arquivo `.env` na raiz da pasta `viewstats` com suas chaves:
     ```env
     GOOGLE_API_KEY=your_google_api_key_here
     OPENAI_API_KEY=your_openai_api_key_here
     INTERNAL_API_KEY=your_internal_api_key_here
     ```

## Uso
Execute o pipeline completo com:
```bash
python main.py
```

O pipeline irá:
1. Carregar e limpar os dados de entrada
2. Processar cada vídeo com o LLM, extraindo:
   - `description`: descrição resumida e detalhada
   - `named_entities`: entidades nomeadas (ex: pessoas, marcas, organizações)
   - `intention`: intenção principal do vídeo (ex: tutorial, review, entretenimento)
   - `hierarchical_topics`: lista de caminhos hierárquicos (ex: "tecnologia > hardware > montagem de pc")
3. Salvar os metadados em `data/processed_videos.json`
4. Gerar uma taxonomia bruta (draft) a partir dos caminhos extraídos, salva em `data/draft_taxonomy.json`
5. Refinar a taxonomia bruta usando o LLM em duas passadas restritivas (merge/re-parent, sem invenção de tópicos), gerando `data/canonical_taxonomy.json`
6. Salvar a taxonomia final para uso externo em `data/master_taxonomy.json` (cópia da canônica)
7. Mapear cada vídeo para os IDs da taxonomia canônica, gerando `data/video_to_taxonomy_map.json`
8. Indexar todos os vídeos no Qdrant, criando vetores de embedding (usando OpenAI `text-embedding-3-small`) e payloads filtráveis
9. Exibir um **relatório final** com o total de tokens, custo estimado (8 casas decimais) e tempo de execução de cada etapa LLM
10. Fazer upload automático da taxonomia final para um endpoint externo, se `INTERNAL_API_KEY` estiver definida.

### Artefatos de saída
- `data/processed_videos.json`: Metadados extraídos de cada vídeo.
- `data/draft_taxonomy.json`: Taxonomia bruta, agregada programaticamente dos caminhos.
- `data/canonical_taxonomy.json`: Taxonomia refinada pelo LLM, apenas com merges e re-parenting, sem tópicos inventados.
- `data/master_taxonomy.json`: Taxonomia final para consumo externo (cópia da canônica).
- `data/video_to_taxonomy_map.json`: Mapeamento de cada vídeo para os IDs da taxonomia canônica.
- `data/indexed_ytids.json`: Lista de vídeos já indexados no Qdrant (checkpoint).

### Indexação e Busca no Qdrant
- Todos os vídeos são indexados na coleção Qdrant `videos_viewstats`.
- Cada ponto contém:
  - Um vetor de embedding (`title` + `description_llm`, via OpenAI)
  - Payload: `yt_id`, `title`, `description_llm`, `intention`, `named_entities` (apenas nomes), `taxonomy_ids`
- Suporta busca semântica (por similaridade de texto) e filtragem por tópicos da taxonomia.
- A coleção é criada automaticamente se não existir.

### Tolerância a Falhas e Checkpoints
- O pipeline salva checkpoints intermediários em todas as etapas críticas (processamento LLM, mapeamento, indexação).
- Permite retomar o processamento sem perder progresso já realizado.
- Todos os artefatos intermediários e finais são salvos em `data/` (ignorado pelo git).

### Logs e Auditoria de Custo
- O pipeline exibe logs limpos e detalhados para cada etapa crítica.
- Para cada chamada ao LLM (processamento de vídeos e refinamento de taxonomia), são exibidos:
  - Tokens usados
  - Custo estimado (8 casas decimais)
  - Tempo de execução
- Ao final, um **relatório consolidado** mostra o total de tokens, custo e tempo de cada etapa e do pipeline completo.
- Isso permite auditoria precisa e otimização do uso do LLM.

## Configuração e Parametrização

Todas as opções principais do pipeline estão centralizadas em `config.py`, incluindo:
- Caminhos de entrada/saída
- Modelos LLM para cada etapa (`LLM_MODEL_VIDEO`, `LLM_MODEL_TAXONOMY`)
- Custos por milhão de tokens para input/output de cada modelo (`LLM_VIDEO_INPUT_COST_PER_M`, etc.)
- Limite mínimo e **máximo** de caracteres do transcript enviado ao LLM (`TRANSCRIPT_MIN_LENGTH`, `TRANSCRIPT_MAX_CHARS`)
- Limite de concorrência
- Parâmetros do Qdrant (`QDRANT_URL`, `QDRANT_COLLECTION_NAME`, `EMBEDDING_MODEL`, `EMBEDDING_MODEL_OPENAI`)
- Custos de embeddings OpenAI (`EMBEDDING_COST_PER_M_TOKENS`)

**Exemplo:**
```python
class Config:
    TRANSCRIPT_MAX_CHARS = 4000  # Limite máximo de caracteres do transcript enviado ao LLM
    LLM_MODEL_VIDEO = "gemini-2.0-flash-lite"
    LLM_MODEL_TAXONOMY = "gemini-2.0-flash-lite"
    LLM_VIDEO_INPUT_COST_PER_M = 0.075
    LLM_VIDEO_OUTPUT_COST_PER_M = 0.30
    LLM_TAXONOMY_INPUT_COST_PER_M = 0.075
    LLM_TAXONOMY_OUTPUT_COST_PER_M = 0.30
    QDRANT_URL = "http://147.79.111.195:6333"
    QDRANT_COLLECTION_NAME = "videos_viewstats"
    EMBEDDING_MODEL = 'text-embedding-3-small'
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBEDDING_MODEL_OPENAI = "text-embedding-3-small"
    EMBEDDING_COST_PER_M_TOKENS = 0.02
    ...
```

## Estratégia de Processamento de Transcript
- O transcript de cada vídeo é extraído e limpo.
- **Apenas os primeiros `TRANSCRIPT_MAX_CHARS` caracteres** são enviados ao LLM para garantir performance e evitar estouro de contexto.
- O valor é facilmente ajustável no `config.py`.

## Estratégia de Refinamento de Taxonomia (Duas Passadas)
- **Primeira passada:** O LLM recebe a lista de categorias do topo e retorna uma lista canônica, podendo mesclar categorias semelhantes.
- **Segunda passada:** Para cada categoria canônica, o pipeline **agrega todas as sub-árvores** das categorias originais do draft que foram fundidas nela (por similaridade de nome, substrings, singular/plural). Só então envia esse bloco agregado para o LLM refinar, garantindo que nenhuma informação é perdida.
- Isso torna o refinamento robusto mesmo quando múltiplas categorias do draft são mescladas em uma só canônica.

## Indexação Vetorial e Busca Semântica
- O script indexa todos os vídeos no Qdrant, criando vetores de embedding (usando OpenAI `text-embedding-3-small`) e payloads ricos para filtragem.
- Suporta busca semântica (por similaridade de texto) e busca por tópicos (filtrando por taxonomy_ids).
- A coleção é criada automaticamente se não existir.

## Auditoria de Custos
- O custo de cada chamada ao LLM é calculado separadamente para tokens de input e output, usando os valores definidos no `config.py` para cada modelo.
- Os logs e relatórios finais detalham tokens, custos (com 8 casas decimais) e tempo de execução de cada etapa.