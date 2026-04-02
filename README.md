# 📦 Olist Analytics Dashboard

> Dashboard de analytics estilo Power BI construído do zero com Python, SQL e Streamlit — sem licença, sem limite, 100% editável.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-in--memory-003B57?style=flat-square&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/licença-MIT-22c55e?style=flat-square)

---

## 🌐 Demo ao vivo

**[👉 Acessar o dashboard](https://olist-analytics.streamlit.app/)**

> A plataforma hiberna o app após períodos de inatividade. Se aparecer uma tela com emoji de sono, clique no botão amarelo e aguarde alguns segundos.

---

## 📸 Visão geral

O projeto usa o dataset público da **Olist** (maior e-commerce marketplace brasileiro) com mais de **100 mil pedidos reais** distribuídos em 8 tabelas relacionais.

Todos os dados são carregados em um banco **SQLite in-memory** via `sqlite3` e consultados com SQL puro, sem ORM, sem abstração, sem custo de infraestrutura.

---

## 🗂️ Páginas

| Página | Conteúdo |
|---|---|
| 📊 **Visão Geral** | KPIs de receita, pedidos, ticket médio e clientes únicos · receita mensal · status dos pedidos · top categorias · formas de pagamento |
| 🗺️ **Geográfico** | Receita e volume de pedidos por estado · gráfico de dispersão volume × ticket médio · ranking completo |
| 📦 **Produtos** | Heatmap de vendas por categoria × mês · top 15 vendedores por receita |
| ⭐ **Reviews** | NPS · distribuição de notas (1–5) · nota média e % de avaliações negativas por categoria |
| 🗃️ **SQL Explorer** | Execute qualquer `SELECT` ao vivo no banco · 3 queries de exemplo prontas · schema completo das tabelas |

Todas as páginas têm **filtros dinâmicos por ano e estado** que injetam cláusulas `WHERE` nas queries SQL em tempo real.

---

## 🛠️ Stack

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.10+ |
| Interface | Streamlit |
| Banco de dados | SQLite (in-memory via `sqlite3`) |
| Visualizações | Plotly Express & Graph Objects |
| Estilo | CSS customizado com tema dark |
| Dataset | Olist Brazilian E-Commerce (Kaggle) |

---

## 🚀 Rodando localmente

### 1. Clone o repositório

```bash
git clone https://github.com/aguinirpretti/Olist-Analytics.git
cd Olist-Analytics
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Baixe o dataset

Acesse: [kaggle.com/datasets/olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

Extraia o ZIP na **mesma pasta** do `main.py`. Você precisa dos seguintes arquivos:

```
olist_orders_dataset.csv
olist_order_items_dataset.csv
olist_customers_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
product_category_name_translation.csv
```

### 5. Rode

```bash
streamlit run main.py
```

Acesse **http://localhost:8501** no navegador.

---

## 📁 Estrutura do projeto

```
.
├── main.py                  # Aplicação principal
├── requirements.txt         # Dependências Python
├── .streamlit/
│   └── config.toml          # Configuração do tema dark
└── README.md
```

> Os arquivos CSV do dataset **não são versionados** (tamanho e licença Kaggle). Siga as instruções acima para baixá-los.

---

## 🧠 Como funciona

```
CSVs do Olist
     │
     ▼
pandas.read_csv()
     │
     ▼
SQLite in-memory  ←──── sqlite3.connect(":memory:")
     │
     ▼
Queries SQL puras  ←──── JOINs entre 8 tabelas
     │
     ▼
DataFrames pandas
     │
     ▼
Plotly (gráficos)  +  CSS customizado
     │
     ▼
Streamlit (interface web)
```

Não há servidor de banco de dados externo, tudo roda na memória RAM durante a sessão. Na primeira carga os CSVs são indexados pelo `@st.cache_resource`, então as consultas subsequentes são instantâneas.

---

## 📦 Dependências

```
streamlit>=1.32.0
pandas>=2.0.0
plotly>=5.18.0
```

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---

## 🙋 Autor

Feito por **[Aguinir Pretti Junior](https://www.linkedin.com/in/aguinirpjr/)** · [LinkedIn](https://linkedin.com/in/aguinirpjr)
