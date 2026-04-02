import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import glob

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Olist Analytics · Power Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── THEME / CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

  /* ── Global reset — Streamlit modern selectors ── */
  html, body { background-color: #0f1117 !important; }
  
  [data-testid="stAppViewContainer"],
  [data-testid="stMain"],
  [data-testid="stMainBlockContainer"],
  .main, .stApp, section.main,
  [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: #0f1117 !important;
    color: #e2e8f0 !important;
  }

  /* Inputs, selects, textareas */
  .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div,
  .stMultiSelect div[data-baseweb="select"] > div {
    background-color: #161b2e !important;
    color: #e2e8f0 !important;
    border-color: #1e2540 !important;
  }

  /* Streamlit default text overrides */
  p, span, div, label, h1, h2, h3, h4, li {
    color: #e2e8f0;
  }

  /* ── Hide streamlit chrome ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stToolbar"] { display: none !important; }
a[href*="github.com"] { display: none !important; }
.stToolbar { display: none !important; }
.block-container { padding: 1.5rem 2rem 2rem 2rem !important; max-width: 100% !important; }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: #13151f !important;
    border-right: 1px solid #1e2130;
  }
  [data-testid="stSidebar"] * { color: #94a3b8 !important; }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stMultiSelect label { color: #64748b !important; font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; }

  /* ── Page title ── */
  .dash-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 28px;
    letter-spacing: -0.02em;
    color: #f1f5f9;
    line-height: 1;
  }
  .dash-subtitle {
    font-size: 13px;
    color: #475569;
    margin-top: 4px;
    font-weight: 300;
  }
  .dash-badge {
    display: inline-block;
    background: #1e3a5f;
    color: #60a5fa;
    font-size: 10px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-left: 8px;
    vertical-align: middle;
  }

  /* ── KPI cards ── */
  .kpi-card {
    background: #161b2e;
    border: 1px solid #1e2540;
    border-radius: 12px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
  }
  .kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 12px 12px 0 0;
  }
  .kpi-card.blue::before  { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
  .kpi-card.green::before { background: linear-gradient(90deg, #10b981, #34d399); }
  .kpi-card.amber::before { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
  .kpi-card.rose::before  { background: linear-gradient(90deg, #f43f5e, #fb7185); }
  .kpi-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #475569;
    font-weight: 500;
  }
  .kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #f1f5f9;
    line-height: 1.1;
    margin: 6px 0 2px 0;
  }
  .kpi-delta-up   { font-size: 12px; color: #34d399; }
  .kpi-delta-down { font-size: 12px; color: #fb7185; }
  .kpi-icon {
    position: absolute;
    right: 18px; top: 18px;
    font-size: 22px;
    opacity: 0.25;
  }

  /* ── Section header ── */
  .section-header {
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 24px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1e2540;
  }

  /* ── Chart container ── */
  .chart-box {
    background: #161b2e;
    border: 1px solid #1e2540;
    border-radius: 12px;
    padding: 20px;
  }
  .chart-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 4px;
  }
  .chart-sub {
    font-size: 11px;
    color: #334155;
    margin-bottom: 14px;
  }

  /* ── Table ── */
  .styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }
  .styled-table th {
    background: #0f1117;
    color: #475569;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid #1e2540;
  }
  .styled-table td {
    padding: 10px 14px;
    border-bottom: 1px solid #1a2035;
    color: #cbd5e1;
  }
  .styled-table tr:hover td { background: #1a2035; }

  /* ── SQL chip ── */
  .sql-chip {
    display: inline-block;
    background: #0d1f3c;
    border: 1px solid #1e3a5f;
    border-radius: 6px;
    padding: 2px 8px;
    font-family: 'Courier New', monospace;
    font-size: 11px;
    color: #60a5fa;
  }

  /* ── Divider ── */
  hr { border-color: #1e2540; margin: 24px 0; }

  /* ── Plotly override ── */
  .js-plotly-plot .plotly .modebar { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ─── PLOTLY THEME ─────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#94a3b8", size=12),
    xaxis=dict(gridcolor="#1e2540", zerolinecolor="#1e2540", tickfont=dict(size=11)),
    yaxis=dict(gridcolor="#1e2540", zerolinecolor="#1e2540", tickfont=dict(size=11)),
    margin=dict(t=10, b=40, l=40, r=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    colorway=["#3b82f6","#10b981","#f59e0b","#f43f5e","#8b5cf6","#06b6d4","#ec4899"],
)

def pl(**overrides):
    merged = {**PLOTLY_LAYOUT, **overrides}
    return merged

# ─── TRADUÇÃO DE CATEGORIAS PT-BR ─────────────────────────────────────────────
CATEGORY_PT = {
    "bed_bath_table": "Cama, Mesa & Banho",
    "health_beauty": "Saúde & Beleza",
    "sports_leisure": "Esporte & Lazer",
    "furniture_decor": "Móveis & Decoração",
    "computers_accessories": "Informática & Acessórios",
    "housewares": "Utilidades Domésticas",
    "watches_gifts": "Relógios & Presentes",
    "telephony": "Telefonia",
    "garden_tools": "Jardim & Ferramentas",
    "auto": "Automotivo",
    "toys": "Brinquedos",
    "cool_stuff": "Artigos Legais",
    "perfumery": "Perfumaria",
    "baby": "Bebê",
    "electronics": "Eletrônicos",
    "fashion_bags_accessories": "Bolsas & Acessórios",
    "office_furniture": "Móveis de Escritório",
    "stationery": "Papelaria",
    "food_drink": "Alimentos & Bebidas",
    "construction_tools_safety": "Ferramentas & Segurança",
    "small_appliances": "Pequenos Eletrodomésticos",
    "consoles_games": "Consoles & Games",
    "audio": "Áudio",
    "fashion_shoes": "Calçados",
    "pet_shop": "Pet Shop",
    "market_place": "Marketplace",
    "luggage_accessories": "Malas & Acessórios",
    "industry_commerce_and_business": "Indústria & Comércio",
    "musical_instruments": "Instrumentos Musicais",
    "books_general_interest": "Livros (Geral)",
    "books_technical": "Livros Técnicos",
    "books_imported": "Livros Importados",
    "dvds_blu_ray": "DVDs & Blu-Ray",
    "cds_dvds_musicals": "CDs & DVDs Musicais",
    "arts_and_craftmanship": "Artesanato",
    "art": "Arte",
    "diapers_and_hygiene": "Fraldas & Higiene",
    "fashion_male_clothing": "Roupas Masculinas",
    "fashion_female_clothing": "Roupas Femininas",
    "fashion_underwear_beach": "Roupas Íntimas & Praia",
    "fashion_sport": "Moda Esportiva",
    "kitchen_dining_laundry_garden_furniture": "Cozinha, Lavanderia & Jardim",
    "flowers": "Flores",
    "food": "Alimentos",
    "drinks": "Bebidas",
    "home_appliances": "Eletrodomésticos",
    "home_appliances_2": "Eletrodomésticos 2",
    "home_comfort": "Conforto Residencial",
    "home_comfort_2": "Conforto Residencial 2",
    "home_construction": "Construção",
    "la_cuisine": "Cozinha Gourmet",
    "christmas_supplies": "Artigos de Natal",
    "party_supplies": "Artigos para Festas",
    "signaling_and_security": "Sinalização & Segurança",
    "tablets_printing_image": "Tablets & Fotografia",
    "fixed_telephony": "Telefonia Fixa",
    "portable_kitchen_food_processors": "Processadores de Alimento",
    "air_conditioning": "Ar Condicionado",
    "furniture_bedroom": "Móveis de Quarto",
    "furniture_living_room": "Sala de Estar",
    "furniture_mattress_and_upholstery": "Colchões & Estofados",
    "construction_tools_lights": "Iluminação & Construção",
    "construction_tools_construction": "Ferramentas de Construção",
    "construction_tools_garden": "Ferramentas de Jardim",
    "costruction_tools_tools": "Ferramentas Gerais",
    "agro_industry_and_commerce": "Agronegócio & Comércio",
    "not_defined": "Não Definido",
}

def traduz_categoria(nome):
    if not nome or nome == "N/A":
        return "Não Definido"
    pt = CATEGORY_PT.get(nome)
    if pt:
        return pt
    # fallback: substitui _ por espaço e capitaliza
    return nome.replace("_", " ").title()


@st.cache_resource(show_spinner=False)
def load_database():
    conn = sqlite3.connect(":memory:", check_same_thread=False)

    csv_map = {
        "orders":        "olist_orders_dataset.csv",
        "order_items":   "olist_order_items_dataset.csv",
        "customers":     "olist_customers_dataset.csv",
        "products":      "olist_products_dataset.csv",
        "sellers":       "olist_sellers_dataset.csv",
        "payments":      "olist_order_payments_dataset.csv",
        "reviews":       "olist_order_reviews_dataset.csv",
        "categories":    "product_category_name_translation.csv",
    }

    # Diretório do script (funciona como main.py ou dashboard.py)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CWD = os.getcwd()

    loaded = []
    for table, fname in csv_map.items():
        paths = [
            os.path.join(BASE_DIR, fname),
            os.path.join(BASE_DIR, "archive", fname),
            os.path.join(BASE_DIR, "data", fname),
            os.path.join(CWD, fname),
            os.path.join(CWD, "archive", fname),
        ]
        for p in paths:
            if os.path.exists(p):
                df = pd.read_csv(p)
                df.to_sql(table, conn, if_exists="replace", index=False)
                loaded.append(table)
                break

    return conn, loaded

def q(conn, sql: str) -> pd.DataFrame:
    return pd.read_sql_query(sql, conn)

with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0 24px 0;'>
      <div style='font-family:Syne,sans-serif; font-size:18px; font-weight:800; color:#f1f5f9;'>📦 Olist</div>
      <div style='font-size:11px; color:#334155; margin-top:2px;'>Painel Analítico</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**📁 Página**")
    page = st.selectbox("", ["📊 Visão Geral", "🗺️ Geográfico", "📦 Produtos", "⭐ Reviews", "🗃️ SQL Explorer"], label_visibility="collapsed")
    
    st.markdown("<hr style='border-color:#1e2540; margin: 16px 0;'>", unsafe_allow_html=True)
    st.markdown("**🔍 Filtros**")

    conn, loaded_tables = load_database()

    if "orders" in loaded_tables:
        years_df = q(conn, "SELECT DISTINCT substr(order_purchase_timestamp, 1, 4) as yr FROM orders WHERE yr IS NOT NULL ORDER BY yr DESC")
        years = ["Todos"] + years_df["yr"].tolist()
        sel_year = st.selectbox("Ano", years)
    else:
        sel_year = "Todos"

    if "customers" in loaded_tables:
        states_df = q(conn, "SELECT DISTINCT customer_state FROM customers ORDER BY customer_state")
        sel_states = st.multiselect("Estado", states_df["customer_state"].tolist(), default=[])
    else:
        sel_states = []

    st.markdown("<hr style='border-color:#1e2540; margin: 16px 0;'>", unsafe_allow_html=True)
    
    # Status das tabelas carregadas
    st.markdown("<div style='font-size:10px; color:#475569; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;'>Tabelas carregadas</div>", unsafe_allow_html=True)
    all_tables = ["orders","order_items","customers","products","sellers","payments","reviews","categories"]
    for t in all_tables:
        icon = "✅" if t in loaded_tables else "❌"
        st.markdown(f"<div style='font-size:11px; color:{'#34d399' if t in loaded_tables else '#ef4444'}; margin-bottom:2px;'>{icon} {t}</div>", unsafe_allow_html=True)

    if not loaded_tables:
        st.error("Nenhum CSV encontrado.\nExecute na pasta com os arquivos Olist.")

year_filter = f"AND substr(o.order_purchase_timestamp,1,4) = '{sel_year}'" if sel_year != "Todos" else ""
state_list  = "','".join(sel_states)
state_filter = f"AND c.customer_state IN ('{state_list}')" if sel_states else ""

if page == "📊 Visão Geral":

    # Header
    col_title, col_info = st.columns([3, 1])
    with col_title:
        st.markdown("""
        <div class='dash-title'>Visão Geral <span class='dash-badge'>Live · SQLite</span></div>
        <div class='dash-subtitle'>E-commerce brasileiro · Dataset Olist · Análise completa com SQL</div>
        """, unsafe_allow_html=True)

    if "orders" in loaded_tables and "payments" in loaded_tables:
        kpi_sql = f"""
            SELECT
                COUNT(DISTINCT o.order_id)                         AS total_pedidos,
                ROUND(SUM(p.payment_value), 2)                     AS receita_total,
                ROUND(AVG(p.payment_value), 2)                     AS ticket_medio,
                COUNT(DISTINCT o.customer_id)                      AS clientes_unicos
            FROM orders o
            JOIN payments p ON o.order_id = p.order_id
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE o.order_status = 'delivered'
            {year_filter} {state_filter}
        """
        kpi = q(conn, kpi_sql).iloc[0]

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class='kpi-card blue'>
              <div class='kpi-icon'>📦</div>
              <div class='kpi-label'>Total de Pedidos</div>
              <div class='kpi-value'>{int(kpi.total_pedidos):,}</div>
              <div class='kpi-delta-up'>▲ entregues com sucesso</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            receita_fmt = f"R$ {kpi.receita_total/1e6:.1f}M" if kpi.receita_total > 1e6 else f"R$ {kpi.receita_total:,.0f}"
            st.markdown(f"""
            <div class='kpi-card green'>
              <div class='kpi-icon'>💰</div>
              <div class='kpi-label'>Receita Total</div>
              <div class='kpi-value'>{receita_fmt}</div>
              <div class='kpi-delta-up'>▲ pedidos entregues</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class='kpi-card amber'>
              <div class='kpi-icon'>🎯</div>
              <div class='kpi-label'>Ticket Médio</div>
              <div class='kpi-value'>R$ {kpi.ticket_medio:.2f}</div>
              <div class='kpi-delta-up'>▲ por transação</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
            <div class='kpi-card rose'>
              <div class='kpi-icon'>👥</div>
              <div class='kpi-label'>Clientes Únicos</div>
              <div class='kpi-value'>{int(kpi.clientes_unicos):,}</div>
              <div class='kpi-delta-up'>▲ compradores distintos</div>
            </div>""", unsafe_allow_html=True)

    # ── Receita por mês + Status ──────────────────────────────────────────────
    st.markdown("<div class='section-header'>Receita & Status</div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        if "orders" in loaded_tables and "payments" in loaded_tables:
            monthly_sql = f"""
                SELECT
                    substr(o.order_purchase_timestamp, 1, 7) AS mes,
                    ROUND(SUM(p.payment_value), 2)           AS receita
                FROM orders o
                JOIN payments p ON o.order_id = p.order_id
                JOIN customers c ON o.customer_id = c.customer_id
                WHERE o.order_status = 'delivered'
                {year_filter} {state_filter}
                GROUP BY mes
                ORDER BY mes
            """
            df_monthly = q(conn, monthly_sql)
            if not df_monthly.empty:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df_monthly["mes"], y=df_monthly["receita"],
                    fill="tozeroy", line=dict(color="#3b82f6", width=2.5),
                    fillcolor="rgba(59,130,246,0.12)",
                    name="Receita Mensal",
                    hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>"
                ))
                fig.update_layout(**pl(height=280))
                st.markdown("<div class='chart-box'><div class='chart-title'>Receita Mensal</div><div class='chart-sub'>Soma de pagamentos por mês · pedidos entregues</div>", unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        if "orders" in loaded_tables:
            status_sql = f"""
                SELECT o.order_status AS status, COUNT(*) AS total
                FROM orders o
                JOIN customers c ON o.customer_id = c.customer_id
                WHERE 1=1 {year_filter} {state_filter}
                GROUP BY o.order_status
                ORDER BY total DESC
            """
            df_status = q(conn, status_sql)
            if not df_status.empty:
                STATUS_PT = {
                    "delivered":"Entregue","shipped":"Enviado","canceled":"Cancelado",
                    "invoiced":"Faturado","processing":"Processando",
                    "approved":"Aprovado","unavailable":"Indisponível","created":"Criado"
                }
                df_status["status_pt"] = df_status["status"].map(lambda x: STATUS_PT.get(x, x))
                colors = ["#3b82f6","#10b981","#f59e0b","#f43f5e","#8b5cf6","#06b6d4","#ec4899","#64748b"]
                fig2 = go.Figure(go.Pie(
                    labels=df_status["status_pt"], values=df_status["total"],
                    hole=0.6,
                    marker=dict(colors=colors, line=dict(color="#161b2e", width=2)),
                    textinfo="none",
                    hoverinfo="label+percent+value",
                    hovertemplate="<b>%{label}</b><br>%{value:,} pedidos (%{percent})<extra></extra>"
                ))
                fig2.update_layout(**pl(
                    height=280,
                    legend=dict(orientation="v", x=1, y=0.5, font=dict(size=10)),
                    annotations=[dict(text=f"<b>{df_status['total'].sum():,}</b><br><span style='font-size:9px'>total</span>",
                                      x=0.5, y=0.5, showarrow=False, font=dict(size=14, color="#f1f5f9"))]))
                st.markdown("<div class='chart-box'><div class='chart-title'>Status dos Pedidos</div><div class='chart-sub'>Distribuição por status</div>", unsafe_allow_html=True)
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Categorias & Pagamentos</div>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        if all(t in loaded_tables for t in ["order_items","products","categories","payments"]):
            cat_sql = f"""
                SELECT
                    COALESCE(cat.product_category_name_english, p.product_category_name, 'N/A') AS categoria,
                    ROUND(SUM(pay.payment_value), 2) AS receita,
                    COUNT(DISTINCT oi.order_id)       AS pedidos
                FROM order_items oi
                JOIN orders o   ON oi.order_id   = o.order_id
                JOIN products p ON oi.product_id = p.product_id
                JOIN payments pay ON o.order_id  = pay.order_id
                JOIN customers c ON o.customer_id = c.customer_id
                LEFT JOIN categories cat ON p.product_category_name = cat.product_category_name
                WHERE o.order_status = 'delivered'
                {year_filter} {state_filter}
                GROUP BY categoria
                ORDER BY receita DESC
                LIMIT 10
            """
            df_cat = q(conn, cat_sql)
            if not df_cat.empty:
                df_cat["categoria"] = df_cat["categoria"].apply(traduz_categoria)
                fig3 = go.Figure(go.Bar(
                    y=df_cat["categoria"][::-1], x=df_cat["receita"][::-1],
                    orientation="h",
                    marker=dict(color=df_cat["receita"][::-1], colorscale=[[0,"#1e3a5f"],[1,"#3b82f6"]]),
                    hovertemplate="<b>%{y}</b><br>R$ %{x:,.2f}<extra></extra>"
                ))
                fig3.update_layout(**pl(height=320))
                st.markdown("<div class='chart-box'><div class='chart-title'>Top 10 Categorias por Receita</div><div class='chart-sub'>Valor total de pagamentos por categoria</div>", unsafe_allow_html=True)
                st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
                st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        if "payments" in loaded_tables:
            pay_sql = f"""
                SELECT
                    p.payment_type                    AS tipo,
                    COUNT(*)                          AS transacoes,
                    ROUND(SUM(p.payment_value), 2)    AS valor_total
                FROM payments p
                JOIN orders o ON p.order_id = o.order_id
                JOIN customers c ON o.customer_id = c.customer_id
                WHERE 1=1 {year_filter} {state_filter}
                GROUP BY tipo ORDER BY valor_total DESC
            """
            df_pay = q(conn, pay_sql)
            if not df_pay.empty:
                PAY_PT = {"credit_card":"Cartão de Crédito","boleto":"Boleto","voucher":"Voucher","debit_card":"Cartão de Débito","not_defined":"N/D"}
                df_pay["tipo_pt"] = df_pay["tipo"].map(lambda x: PAY_PT.get(x, x))
                fig4 = go.Figure(go.Bar(
                    x=df_pay["tipo_pt"], y=df_pay["valor_total"],
                    marker=dict(color=["#3b82f6","#10b981","#f59e0b","#f43f5e","#8b5cf6"],
                                line=dict(color="#161b2e", width=1)),
                    hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>"
                ))
                fig4.update_layout(**pl(height=320))
                st.markdown("<div class='chart-box'><div class='chart-title'>Formas de Pagamento</div><div class='chart-sub'>Valor total por método de pagamento</div>", unsafe_allow_html=True)
                st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
                st.markdown("</div>", unsafe_allow_html=True)

elif page == "🗺️ Geográfico":
    st.markdown("<div class='dash-title'>Análise Geográfica</div><div class='dash-subtitle'>Distribuição de pedidos e receita por estado brasileiro</div>", unsafe_allow_html=True)

    if all(t in loaded_tables for t in ["orders","customers","payments"]):
        geo_sql = f"""
            SELECT
                c.customer_state                      AS estado,
                COUNT(DISTINCT o.order_id)            AS pedidos,
                COUNT(DISTINCT o.customer_id)         AS clientes,
                ROUND(SUM(p.payment_value), 2)        AS receita,
                ROUND(AVG(p.payment_value), 2)        AS ticket_medio
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN payments p  ON o.order_id    = p.order_id
            WHERE o.order_status = 'delivered' {year_filter}
            GROUP BY c.customer_state
            ORDER BY receita DESC
        """
        df_geo = q(conn, geo_sql)

        if not df_geo.empty:
            c1, c2 = st.columns(2)
            with c1:
                fig_bar = px.bar(df_geo, x="estado", y="receita",
                    color="receita", color_continuous_scale=["#1e3a5f","#3b82f6"],
                    labels={"estado":"Estado","receita":"Receita (R$)"},
                    hover_data={"pedidos":True,"ticket_medio":True})
                fig_bar.update_layout(**pl(height=380, coloraxis_showscale=False))
                st.markdown("<div class='chart-box'><div class='chart-title'>Receita por Estado</div><div class='chart-sub'>Estados ordenados por valor total</div>", unsafe_allow_html=True)
                st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
                st.markdown("</div>", unsafe_allow_html=True)

            with c2:
                fig_scatter = px.scatter(df_geo, x="pedidos", y="ticket_medio",
                    size="receita", color="receita", text="estado",
                    color_continuous_scale=["#1e3a5f","#10b981"],
                    labels={"pedidos":"Nº de Pedidos","ticket_medio":"Ticket Médio (R$)"})
                fig_scatter.update_traces(textposition="top center", textfont=dict(size=9, color="#94a3b8"))
                fig_scatter.update_layout(**pl(height=380, coloraxis_showscale=False))
                st.markdown("<div class='chart-box'><div class='chart-title'>Volume vs Ticket Médio</div><div class='chart-sub'>Tamanho do ponto = receita total</div>", unsafe_allow_html=True)
                st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})
                st.markdown("</div>", unsafe_allow_html=True)

            # Tabela completa
            st.markdown("<div class='section-header'>Ranking Completo por Estado</div>", unsafe_allow_html=True)
            df_geo["receita_fmt"]  = df_geo["receita"].apply(lambda x: f"R$ {x:,.2f}")
            df_geo["ticket_fmt"]   = df_geo["ticket_medio"].apply(lambda x: f"R$ {x:,.2f}")
            df_geo["pedidos_fmt"]  = df_geo["pedidos"].apply(lambda x: f"{x:,}")
            df_show = df_geo[["estado","pedidos_fmt","clientes","receita_fmt","ticket_fmt"]].rename(columns={
                "estado":"Estado","pedidos_fmt":"Pedidos","clientes":"Clientes","receita_fmt":"Receita Total","ticket_fmt":"Ticket Médio"})
            
            rows = ""
            for i, row in df_show.iterrows():
                rows += f"<tr>{''.join(f'<td>{v}</td>' for v in row.values)}</tr>"
            st.markdown(f"""
            <div class='chart-box'>
              <table class='styled-table'>
                <thead><tr>{''.join(f'<th>{c}</th>' for c in df_show.columns)}</tr></thead>
                <tbody>{rows}</tbody>
              </table>
            </div>""", unsafe_allow_html=True)

elif page == "📦 Produtos":
    st.markdown("<div class='dash-title'>Análise de Produtos</div><div class='dash-subtitle'>Performance por categoria, vendedor e ticket</div>", unsafe_allow_html=True)

    if all(t in loaded_tables for t in ["order_items","products","sellers","payments","orders"]):
        
        # Heatmap: Categorias × Meses
        heat_sql = """
            SELECT
                COALESCE(cat.product_category_name_english, p.product_category_name) AS categoria,
                substr(o.order_purchase_timestamp, 1, 7) AS mes,
                COUNT(oi.order_item_id) AS qty
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            JOIN products p ON oi.product_id = p.product_id
            LEFT JOIN categories cat ON p.product_category_name = cat.product_category_name
            WHERE o.order_status = 'delivered'
            GROUP BY categoria, mes
            ORDER BY mes
        """
        if "categories" in loaded_tables:
            df_heat = q(conn, heat_sql)
        else:
            df_heat = pd.DataFrame()

        if not df_heat.empty:
            pivot = df_heat.pivot_table(index="categoria", columns="mes", values="qty", fill_value=0)
            top_cats = pivot.sum(axis=1).nlargest(12).index
            pivot_top = pivot.loc[top_cats]
            pivot_top.index = [traduz_categoria(c) for c in pivot_top.index]

            fig_heat = go.Figure(go.Heatmap(
                z=pivot_top.values, x=pivot_top.columns.tolist(), y=pivot_top.index.tolist(),
                colorscale=[[0,"#0f1117"],[0.5,"#1e3a5f"],[1,"#3b82f6"]],
                hovertemplate="<b>%{y}</b><br>%{x}<br>%{z} itens vendidos<extra></extra>"
            ))
            fig_heat.update_layout(**pl(height=380))
            st.markdown("<div class='chart-box'><div class='chart-title'>Heatmap: Vendas por Categoria × Mês</div><div class='chart-sub'>Top 12 categorias · intensidade = nº de itens vendidos</div>", unsafe_allow_html=True)
            st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

        # Top Sellers
        st.markdown("<div class='section-header'>Top Vendedores</div>", unsafe_allow_html=True)
        seller_sql = f"""
            SELECT
                s.seller_state                          AS estado,
                s.seller_city                           AS cidade,
                COUNT(DISTINCT oi.order_id)             AS pedidos,
                ROUND(SUM(oi.price), 2)                 AS receita,
                ROUND(AVG(oi.price), 2)                 AS preco_medio
            FROM order_items oi
            JOIN sellers s  ON oi.seller_id  = s.seller_id
            JOIN orders o   ON oi.order_id   = o.order_id
            WHERE o.order_status = 'delivered' {year_filter}
            GROUP BY s.seller_id
            ORDER BY receita DESC
            LIMIT 15
        """
        df_sellers = q(conn, seller_sql)
        if not df_sellers.empty:
            df_sellers["receita_fmt"] = df_sellers["receita"].apply(lambda x: f"R$ {x:,.2f}")
            df_sellers["preco_fmt"]   = df_sellers["preco_medio"].apply(lambda x: f"R$ {x:,.2f}")
            rows = ""
            for i, row in df_sellers[["estado","cidade","pedidos","receita_fmt","preco_fmt"]].iterrows():
                rows += f"<tr>{''.join(f'<td>{v}</td>' for v in row.values)}</tr>"
            headers = ["Estado","Cidade","Pedidos","Receita Total","Preço Médio"]
            st.markdown(f"""
            <div class='chart-box'>
              <table class='styled-table'>
                <thead><tr>{''.join(f'<th>{c}</th>' for c in headers)}</tr></thead>
                <tbody>{rows}</tbody>
              </table>
            </div>""", unsafe_allow_html=True)

elif page == "⭐ Reviews":
    st.markdown("<div class='dash-title'>Análise de Reviews</div><div class='dash-subtitle'>Satisfação dos clientes e NPS por categoria</div>", unsafe_allow_html=True)

    if all(t in loaded_tables for t in ["reviews","orders","order_items","products"]):

        c1, c2, c3 = st.columns(3)
        kpi_rev = q(conn, """
            SELECT
                ROUND(AVG(review_score), 2)           AS nota_media,
                COUNT(*)                              AS total_reviews,
                SUM(CASE WHEN review_score >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_positivo
            FROM reviews
        """).iloc[0]

        with c1:
            st.markdown(f"<div class='kpi-card blue'><div class='kpi-icon'>⭐</div><div class='kpi-label'>Nota Média</div><div class='kpi-value'>{kpi_rev.nota_media:.2f}</div><div class='kpi-delta-up'>▲ de 5.0 possíveis</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='kpi-card green'><div class='kpi-icon'>💬</div><div class='kpi-label'>Total de Reviews</div><div class='kpi-value'>{int(kpi_rev.total_reviews):,}</div><div class='kpi-delta-up'>▲ avaliações coletadas</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='kpi-card amber'><div class='kpi-icon'>😊</div><div class='kpi-label'>Avaliações Positivas</div><div class='kpi-value'>{kpi_rev.pct_positivo:.1f}%</div><div class='kpi-delta-up'>▲ notas 4 ou 5</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='section-header'>Distribuição de Notas</div>", unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            dist_sql = "SELECT review_score AS nota, COUNT(*) AS qty FROM reviews GROUP BY nota ORDER BY nota"
            df_dist = q(conn, dist_sql)
            colors_rev = {1:"#f43f5e", 2:"#fb923c", 3:"#f59e0b", 4:"#34d399", 5:"#3b82f6"}
            fig_rev = go.Figure(go.Bar(
                x=df_dist["nota"].astype(str), y=df_dist["qty"],
                marker_color=[colors_rev.get(n,"#475569") for n in df_dist["nota"]],
                hovertemplate="Nota %{x}<br>%{y:,} avaliações<extra></extra>"
            ))
            fig_rev.update_layout(**pl(height=300))
            st.markdown("<div class='chart-box'><div class='chart-title'>Distribuição de Notas</div><div class='chart-sub'>Contagem por pontuação (1–5)</div>", unsafe_allow_html=True)
            st.plotly_chart(fig_rev, use_container_width=True, config={"displayModeBar": False})
            st.markdown("</div>", unsafe_allow_html=True)

        with col_b:
            cat_rev_sql = """
                SELECT
                    COALESCE(cat.product_category_name_english, p.product_category_name) AS categoria,
                    ROUND(AVG(r.review_score), 2) AS nota_media,
                    COUNT(r.review_id)            AS total_reviews
                FROM reviews r
                JOIN orders o     ON r.order_id    = o.order_id
                JOIN order_items oi ON o.order_id  = oi.order_id
                JOIN products p    ON oi.product_id = p.product_id
                LEFT JOIN categories cat ON p.product_category_name = cat.product_category_name
                GROUP BY categoria
                HAVING total_reviews > 50
                ORDER BY nota_media DESC
                LIMIT 10
            """ if "categories" in loaded_tables else ""
            
            if cat_rev_sql:
                df_cat_rev = q(conn, cat_rev_sql)
                if not df_cat_rev.empty:
                    df_cat_rev["categoria"] = df_cat_rev["categoria"].apply(traduz_categoria)
                    fig_cr = go.Figure(go.Bar(
                        y=df_cat_rev["categoria"][::-1], x=df_cat_rev["nota_media"][::-1],
                        orientation="h",
                        marker=dict(color=df_cat_rev["nota_media"][::-1], colorscale=[[0,"#f43f5e"],[0.5,"#f59e0b"],[1,"#10b981"]]),
                        hovertemplate="<b>%{y}</b><br>Nota: %{x:.2f}<extra></extra>"
                    ))
                    fig_cr.update_layout(**pl(height=300))
                    st.markdown("<div class='chart-box'><div class='chart-title'>Nota Média por Categoria</div><div class='chart-sub'>Top 10 · mín. 50 avaliações</div>", unsafe_allow_html=True)
                    st.plotly_chart(fig_cr, use_container_width=True, config={"displayModeBar": False})
                    st.markdown("</div>", unsafe_allow_html=True)

elif page == "🗃️ SQL Explorer":
    st.markdown("<div class='dash-title'>SQL Explorer</div><div class='dash-subtitle'>Execute queries diretamente no banco SQLite in-memory</div>", unsafe_allow_html=True)

    # Schema
    st.markdown("<div class='section-header'>Schema do Banco</div>", unsafe_allow_html=True)
    schema_cols = st.columns(4)
    schemas = {
        "orders": ["order_id","customer_id","order_status","order_purchase_timestamp","order_delivered_customer_date"],
        "order_items": ["order_id","order_item_id","product_id","seller_id","price","freight_value"],
        "customers": ["customer_id","customer_unique_id","customer_zip_code_prefix","customer_city","customer_state"],
        "payments": ["order_id","payment_sequential","payment_type","payment_installments","payment_value"],
        "products": ["product_id","product_category_name","product_name_lenght","product_weight_g"],
        "sellers": ["seller_id","seller_zip_code_prefix","seller_city","seller_state"],
        "reviews": ["review_id","order_id","review_score","review_comment_title","review_creation_date"],
        "categories": ["product_category_name","product_category_name_english"],
    }
    for i, (table, cols) in enumerate(schemas.items()):
        with schema_cols[i % 4]:
            icon = "✅" if table in loaded_tables else "❌"
            cols_html = "".join(f"<div style='font-size:10px; color:#475569; padding:1px 0; font-family:monospace;'>· {c}</div>" for c in cols)
            st.markdown(f"""
            <div style='background:#0f1117; border:1px solid #1e2540; border-radius:8px; padding:12px; margin-bottom:8px;'>
              <div style='font-size:12px; font-weight:700; color:#60a5fa; margin-bottom:6px;'>{icon} {table}</div>
              {cols_html}
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Queries de Exemplo</div>", unsafe_allow_html=True)
    examples = {
        "Top 10 cidades por receita": """SELECT c.customer_city, c.customer_state,
       COUNT(DISTINCT o.order_id) AS pedidos,
       ROUND(SUM(p.payment_value), 2) AS receita
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN payments p ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_city, c.customer_state
ORDER BY receita DESC
LIMIT 10""",
        "Tempo médio de entrega por estado": """SELECT c.customer_state AS estado,
       ROUND(AVG(
         julianday(o.order_delivered_customer_date) -
         julianday(o.order_purchase_timestamp)
       ), 1) AS dias_medio_entrega,
       COUNT(*) AS pedidos
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY c.customer_state
ORDER BY dias_medio_entrega""",
        "Categorias com maior churn (nota < 3)": """SELECT
  COALESCE(cat.product_category_name_english, p.product_category_name) AS categoria,
  COUNT(CASE WHEN r.review_score <= 2 THEN 1 END) AS reviews_negativas,
  COUNT(*) AS total_reviews,
  ROUND(COUNT(CASE WHEN r.review_score <= 2 THEN 1 END)*100.0/COUNT(*),1) AS pct_negativo
FROM reviews r
JOIN orders o ON r.order_id = o.order_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN categories cat ON p.product_category_name = cat.product_category_name
GROUP BY categoria
HAVING total_reviews > 100
ORDER BY pct_negativo DESC
LIMIT 10""",
    }

    selected_example = st.selectbox("Carregar exemplo:", ["(personalizar)"] + list(examples.keys()))
    
    default_query = examples[selected_example] if selected_example != "(personalizar)" else "SELECT * FROM orders LIMIT 10"
    
    user_query = st.text_area("Query SQL:", value=default_query, height=160,
        help="Execute qualquer SELECT no banco Olist")

    col_run, col_exp = st.columns([1, 5])
    with col_run:
        run = st.button("▶ Executar", type="primary")

    if run or selected_example != "(personalizar)":
        try:
            df_result = q(conn, user_query)
            st.success(f"✅ {len(df_result):,} linha(s) retornadas")
            if not df_result.empty:
                rows = ""
                for _, row in df_result.head(200).iterrows():
                    rows += f"<tr>{''.join(f'<td>{v}</td>' for v in row.values)}</tr>"
                headers_html = "".join(f"<th>{c}</th>" for c in df_result.columns)
                st.markdown(f"""
                <div class='chart-box' style='overflow-x:auto;'>
                  <table class='styled-table'>
                    <thead><tr>{headers_html}</tr></thead>
                    <tbody>{rows}</tbody>
                  </table>
                </div>""", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Erro SQL: {e}")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 32px 0 8px 0; color:#1e2540; font-size:11px;'>
  Desenvolvido com <strong style='color:#3b82f6;'>Streamlit</strong> · 
  SQLite in-memory · 
  Dataset: <strong style='color:#3b82f6;'>Olist E-Commerce Brasileiro</strong> · 
  Plotly · Python
</div>
""", unsafe_allow_html=True)
