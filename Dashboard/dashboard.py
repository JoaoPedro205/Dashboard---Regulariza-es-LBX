import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re

# ── Página ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LBX Construtora — Dashboard",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Cores LBX ─────────────────────────────────────────────────────────────────
NAVY, BLUE, BACC   = "#0e1c35", "#2e74d4", "#4a9fe0"
PURPLE, GREEN, RED = "#534AB7", "#1D9E75", "#e05a3a"
GOLD, TEAL         = "#f0a830", "#0F6E56"
COLORS3 = [BLUE, PURPLE, GREEN]
COLORS5 = [BLUE, PURPLE, GREEN, GOLD, RED]

PLOT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="rgba(220,235,255,0.8)", family="Inter, Segoe UI, sans-serif", size=12),
    margin=dict(l=8, r=8, t=44, b=8),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="rgba(220,235,255,0.75)", size=11)),
    title_font=dict(size=14, color="rgba(255,255,255,0.92)", family="Inter, Segoe UI, sans-serif"),
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Base ── */
.stApp {{
  background: linear-gradient(160deg,#0b1628 0%,#0e1c35 45%,#0a1525 100%) !important;
  font-family: Inter, Segoe UI, sans-serif;
}}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
  background: linear-gradient(180deg,#0c1a30 0%,#101e38 100%) !important;
  border-right: 1px solid rgba(74,159,224,0.14) !important;
}}
section[data-testid="stSidebar"] * {{ color:#dceeff !important; }}
section[data-testid="stSidebar"] label {{
  font-size:10px !important; letter-spacing:.1em !important;
  text-transform:uppercase !important; color:rgba(74,159,224,0.85) !important;
}}

/* ── Headings ── */
h1,h2,h3,h4 {{ color:#fff !important; font-family:Inter,sans-serif !important; letter-spacing:.02em; }}

/* ── Section title ── */
.sec {{
  font-size:10px; font-weight:600; letter-spacing:.16em; text-transform:uppercase;
  color:{BACC}; padding-bottom:7px; margin:26px 0 14px;
  border-bottom:1px solid rgba(74,159,224,0.18);
  display:flex; align-items:center; gap:8px;
}}
.sec::before {{
  content:''; width:3px; height:14px;
  background:linear-gradient(180deg,{BLUE},{BACC});
  border-radius:2px; flex-shrink:0;
}}

/* ── KPI cards ── */
.kcard {{
  background:linear-gradient(135deg,rgba(255,255,255,.08) 0%,rgba(255,255,255,.03) 100%);
  border:1px solid rgba(74,159,224,0.2);
  border-radius:14px; padding:18px 14px; text-align:center;
  backdrop-filter:blur(8px); position:relative; overflow:hidden;
}}
.kcard::before {{
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  background:linear-gradient(90deg,{BLUE},{BACC},{PURPLE});
  border-radius:14px 14px 0 0;
}}
.klabel {{ font-size:10px; color:rgba(255,255,255,.42); text-transform:uppercase; letter-spacing:.12em; margin-bottom:8px; font-weight:500; }}
.kval   {{ font-size:28px; font-weight:700; line-height:1; letter-spacing:-.01em; }}
.ksub   {{ font-size:11px; color:rgba(255,255,255,.32); margin-top:5px; }}

/* ── Insight cards ── */
.insight {{
  background:linear-gradient(135deg,rgba(46,116,212,.12) 0%,rgba(255,255,255,.03) 100%);
  border-left:3px solid {BLUE}; border-radius:0 10px 10px 0;
  padding:12px 16px; font-size:12px; color:rgba(255,255,255,.8);
  margin-bottom:10px; line-height:1.7;
}}

/* ── Metric containers ── */
div[data-testid="metric-container"] {{
  background:linear-gradient(135deg,rgba(255,255,255,.07) 0%,rgba(255,255,255,.03) 100%);
  border:1px solid rgba(74,159,224,0.18); border-radius:12px; padding:12px;
}}
div[data-testid="metric-container"] label {{ color:rgba(255,255,255,.5) !important; font-size:11px !important; }}
div[data-testid="metric-container"] div   {{ color:#fff !important; font-weight:600 !important; }}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
  background:rgba(255,255,255,.04); border-radius:10px;
  padding:3px; border:1px solid rgba(74,159,224,0.1); gap:2px;
}}
.stTabs [data-baseweb="tab"] {{
  color:rgba(255,255,255,.5) !important; border-radius:8px;
  font-size:13px; font-weight:500; padding:8px 16px; transition:all .2s;
  font-family:Inter,sans-serif !important;
}}
.stTabs [aria-selected="true"] {{
  color:#fff !important;
  background:linear-gradient(135deg,rgba(46,116,212,.5),rgba(83,74,183,.4)) !important;
  box-shadow:0 2px 14px rgba(46,116,212,.3);
}}

/* ── Chart glass cards ── */
.stPlotlyChart > div {{
  background:linear-gradient(135deg,rgba(255,255,255,.05) 0%,rgba(255,255,255,.02) 100%) !important;
  border:1px solid rgba(74,159,224,0.12) !important;
  border-radius:14px !important; padding:6px !important;
}}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {{
  border:1px solid rgba(74,159,224,0.15) !important;
  border-radius:12px; overflow:hidden;
}}

/* ── Download button ── */
.stDownloadButton > button {{
  background:linear-gradient(135deg,{BLUE},{PURPLE}) !important;
  color:#fff !important; border:none !important; border-radius:8px !important;
  font-weight:600 !important; letter-spacing:.04em !important;
  padding:8px 20px !important; transition:opacity .2s !important;
}}
.stDownloadButton > button:hover {{ opacity:.82 !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width:5px; height:5px; }}
::-webkit-scrollbar-track {{ background:rgba(255,255,255,.03); }}
::-webkit-scrollbar-thumb {{ background:rgba(74,159,224,.28); border-radius:3px; }}
::-webkit-scrollbar-thumb:hover {{ background:rgba(74,159,224,.55); }}

/* ── Mobile ── */
@media(max-width:768px){{
  .main .block-container{{padding:.8rem .6rem 2rem!important;max-width:100%!important;}}
  h1{{font-size:18px!important;}}
  .kcard{{padding:10px!important;}}
  .kval{{font-size:20px!important;}}
  [data-testid="column"]{{width:100%!important;flex:1 1 100%!important;min-width:100%!important;}}
  .stTabs [data-baseweb="tab-list"]{{overflow-x:auto!important;flex-wrap:nowrap!important;}}
  .stTabs [data-baseweb="tab"]{{font-size:11px!important;padding:6px 10px!important;white-space:nowrap;}}
}}
</style>""", unsafe_allow_html=True)
# ── Carregar e tratar dados ───────────────────────────────────────────────────
def _ler_bytes(source):
    """Converte qualquer fonte (path str, UploadedFile, BytesIO) em bytes puros."""
    if isinstance(source, (str, os.PathLike)):
        with open(source, "rb") as f:
            return f.read()
    # UploadedFile ou BytesIO
    if hasattr(source, "getvalue"):
        return source.getvalue()
    source.seek(0)
    return source.read()

@st.cache_data(show_spinner="Carregando dados...", ttl=3600)
def load(raw_bytes: bytes):
    import io
    data = io.BytesIO(raw_bytes)

    # ── Aba Especificação ─────────────────────────────────────────────────────
    try:
        de = pd.read_excel(data, sheet_name="Especificação")
        de.columns = de.columns.str.strip()
        de["Data"]        = pd.to_datetime(de["Data"], errors="coerce")
        de["MesAno"]      = de["Data"].dt.to_period("M").astype(str)
        de["Coordenador"] = de["Coordenador"].fillna("Não informado")
        de["Fornecedor"]  = de["Fornecedor"].fillna("Não informado")
        de["Insumo"]      = de["Insumo"].fillna("Outros")
        de["Obra"]        = de["Obra"].fillna("Não informado")
        de["ValorTotal"]  = pd.to_numeric(de["ValorTotal"], errors="coerce").fillna(0)
        def _cat(t):
            t = str(t).upper()
            if "LOCAC" in t or "ALUGU" in t: return "Locação de Equipamentos"
            if "MATER" in t: return "Materiais"
            if "SERVI" in t: return "Serviços"
            if "FRETE" in t or "TRANS" in t or "CAMIN" in t: return "Fretes e Transportes"
            if "IMPRE" in t or "PLOTA" in t: return "Impressões/Plotagens"
            if "BRITA" in t or "AREIA" in t or "CIMEN" in t or "CONCR" in t: return "Insumos de Construção"
            if "ENGAJ" in t or "ACAO" in t: return "Engajamento"
            if "DESPE" in t: return "Despesas Diversas"
            return "Outros"
        de["CategoriaInsumo"] = de["Insumo"].apply(_cat)
    except Exception:
        de = pd.DataFrame()

    data.seek(0)
    df = pd.read_excel(data, sheet_name=0)
    df.columns = df.columns.str.strip()

    rename = {
        "Para qual obra deseja regularizar um contrato?": "Obra",
        "A solicitação está aprovada?":                   "Aprovada",
        "Essa regularização faz parte da carteira de qual setor?": "Setor",
        "Qual regularização deseja realizar?":            "Tipo",
        "Especifique o motivo da compra ter sido feita diretamente pela obra": "Motivo",
        "Especifique a Categoria:":                       "Categoria",
        "Qual o tipo de contrato?":                       "TipoContrato",
        "Haverá caução ou retenção nesse contrato?":      "Caucao",
        "Condição de pagamento negociada":                "Pagamento",
        "Nome":                                           "Usuario",
        "Hora de início":                                 "Inicio",
        "Hora de conclusão":                              "Fim",
        "Qual o número da Solicitação?":                  "NumSolicitacao",
    }
    # colunas com \xa0
    for col in df.columns:
        clean = col.replace("\xa0", " ").strip()
        if "Credor" in clean and "descrição" in clean.lower():
            rename[col] = "Credor"
            break

    df = df.rename(columns=rename)
    df["Inicio"] = pd.to_datetime(df["Inicio"], errors="coerce")
    df["Fim"]    = pd.to_datetime(df["Fim"],    errors="coerce")
    df["LeadMin"]    = (df["Fim"] - df["Inicio"]).dt.total_seconds() / 60
    df["Ano"]        = df["Inicio"].dt.year
    df["Mes"]        = df["Inicio"].dt.month
    df["MesAno"]     = df["Inicio"].dt.to_period("M").astype(str)
    df["DiaSemana"]  = df["Inicio"].dt.day_name()
    df["HoraDia"]    = df["Inicio"].dt.hour
    df["Semana"]     = df["Inicio"].dt.to_period("W").astype(str)

    # normalizar pagamento
    def norm_pag(v):
        if pd.isna(v): return None
        v = str(v).upper().strip()
        if "TED" in v:    return "TED"
        if "BOLETO" in v or v.startswith("BOL"): return "Boleto"
        if "PIX" in v:    return "PIX"
        if "FATURA" in v: return "Fatura"
        return "Outros"
    df["PagNorm"] = df["Pagamento"].apply(norm_pag)

    # ── Tratar nulos em colunas de filtro para não perder registros ──────────
    df["Setor"]    = df["Setor"].fillna("Não informado")
    df["Usuario"]  = df["Usuario"].fillna("Não identificado")
    df["Categoria"]= df["Categoria"].fillna("Não informado")
    df["Motivo"]   = df["Motivo"].fillna("Não informado")
    df["TipoContrato"] = df["TipoContrato"].fillna("Não informado")
    df["Caucao"]   = df["Caucao"].fillna("Não informado")
    df["PagNorm"]  = df["PagNorm"].fillna("Não informado")

    df["Aprovada_bool"] = df["Aprovada"] == "Sim"
    return df, de

# ── Carregar dados: tenta arquivo local, senão pede upload ──────────────────
import glob, os, io

# Procura qualquer .xlsx na pasta do script (funciona com qualquer nome)
_xlsx_locais = glob.glob(os.path.join(os.path.dirname(__file__) if "__file__" in dir() else ".", "*.xlsx"))
_fonte_local = _xlsx_locais[0] if _xlsx_locais else None

if _fonte_local:
    df, de = load(_ler_bytes(_fonte_local))
else:
    # Arquivo nao encontrado localmente — exibe uploader
    with st.sidebar:
        st.markdown("---")
        st.markdown("### Carregar planilha")
        _upload = st.file_uploader(
            "Selecione o arquivo .xlsx do Forms",
            type=["xlsx"],
            help="Qualquer nome de arquivo é aceito"
        )
    if _upload is None:
        st.markdown(
            "<div style='text-align:center;padding:80px 20px;'>"
            "<p style='color:rgba(255,255,255,.5);font-size:15px;'>"
            "Faça upload da planilha <b>.xlsx</b> no painel lateral.</p>"
            "</div>",
            unsafe_allow_html=True
        )
        st.stop()
    try:
        # Lê os bytes do arquivo enviado pelo usuário
        _bytes = _upload.getvalue()
        if len(_bytes) == 0:
            st.error("O arquivo enviado está vazio. Tente novamente.")
            st.stop()
        df, de = load(_bytes)
    except Exception as e:
        st.error(
            f"**Erro ao processar o arquivo:** {e}\n\n"
            "Causas comuns:\n"
            "- O arquivo não é um `.xlsx` válido\n"
            "- O arquivo está corrompido ou protegido por senha\n"
            "- As colunas não correspondem ao formato esperado do Microsoft Forms"
        )
        st.stop()


# ── Sidebar — Filtros ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<h2 style='color:{BACC}!important;font-size:16px;letter-spacing:.06em;'>⚙ FILTROS</h2>", unsafe_allow_html=True)

    anos = sorted(df["Ano"].dropna().unique().tolist())
    anos_sel = st.multiselect("Ano", anos, default=anos)

    obras_disp = sorted(df["Obra"].dropna().unique())
    obras_sel  = st.multiselect("Obra", obras_disp, default=obras_disp)

    setores_disp = sorted(df["Setor"].dropna().unique())
    setores_sel  = st.multiselect("Setor", setores_disp, default=setores_disp)

    tipos_disp = sorted(df["Tipo"].dropna().unique())
    tipos_sel  = st.multiselect("Tipo", tipos_disp, default=tipos_disp)

    aprov_sel = st.radio("Aprovação", ["Todos", "Aprovadas", "Não aprovadas"], index=0)

    st.markdown("---")
    st.markdown("<span style='font-size:10px;letter-spacing:.1em;color:#4a9fe0;'>💰 GASTOS — FILTROS</span>", unsafe_allow_html=True)
    if not de.empty:
        meses_g_disp = sorted(de["MesAno"].dropna().unique().tolist())
        meses_g_sel  = st.multiselect("Mês (Gastos)", meses_g_disp, default=meses_g_disp)
        coords_disp  = sorted(de["Coordenador"].dropna().unique().tolist())
        coords_sel   = st.multiselect("Coordenador", coords_disp, default=coords_disp)
    else:
        meses_g_sel, coords_sel = [], []
    st.markdown("---")
    st.markdown(f"<span style='font-size:11px;color:rgba(255,255,255,.4);'>Base: {len(df):,} registros</span>", unsafe_allow_html=True)

# ── Filtrar ───────────────────────────────────────────────────────────────────
dff = df[
    df["Ano"].isin(anos_sel) &
    df["Obra"].isin(obras_sel) &
    df["Setor"].isin(setores_sel) &
    df["Tipo"].isin(tipos_sel)
].copy()
if aprov_sel == "Aprovadas":      dff = dff[dff["Aprovada"] == "Sim"]
elif aprov_sel == "Não aprovadas": dff = dff[dff["Aprovada"] == "Não"]

# ── Cabeçalho ─────────────────────────────────────────────────────────────────
st.markdown(
    f"<h1 style='text-align:center;letter-spacing:.08em;font-size:24px;margin-bottom:2px;'>LBX CONSTRUTORA</h1>"
    f"<p style='text-align:center;color:{BACC};letter-spacing:.12em;font-size:11px;margin-top:0;margin-bottom:4px;'>"
    f"DASHBOARD DE REGULARIZAÇÃO · CONTRATOS · ADITIVOS · PEDIDOS DE COMPRA</p>",
    unsafe_allow_html=True
)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊  Visão Geral",
    "🏗️  Obras & Setores",
    "📅  Temporal",
    "👤  Operacional",
    "🔍  Dados Brutos",
    "💰  Gastos por Insumo",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — VISÃO GERAL
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    total      = len(dff)
    aprovadas  = dff["Aprovada_bool"].sum()
    reprov     = total - aprovadas
    pct_aprov  = aprovadas / total * 100 if total > 0 else 0
    lead_med   = dff["LeadMin"].median()
    n_obras    = dff["Obra"].nunique()
    n_usuarios = dff["Usuario"].nunique()

    st.markdown("<div class='sec'>KPIs principais</div>", unsafe_allow_html=True)
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    cards = [
        (c1, "Total",          f"{total:,}",        "solicitações",        BACC),
        (c2, "Aprovadas",      f"{aprovadas:,}",     f"{pct_aprov:.1f}%",   GREEN),
        (c3, "Não aprovadas",  f"{reprov:,}",        f"{100-pct_aprov:.1f}%", RED),
        (c4, "Lead time med.", f"{lead_med:.1f} min","preenchimento",        GOLD),
        (c5, "Obras",          f"{n_obras}",         "empreendimentos",     PURPLE),
        (c6, "Usuários",       f"{n_usuarios}",      "respondentes",        "#4a9fe0"),
    ]
    for col, lbl, val, sub, color in cards:
        col.markdown(
            f"<div class='kcard'><div class='klabel'>{lbl}</div>"
            f"<div class='kval' style='color:{color};'>{val}</div>"
            f"<div class='ksub'>{sub}</div></div>", unsafe_allow_html=True
        )

    st.markdown("<div class='sec'>Mix de regularização</div>", unsafe_allow_html=True)
    mix = dff["Tipo"].value_counts().reset_index()
    mix.columns = ["Tipo","Qtd"]
    mix["Pct"] = (mix["Qtd"]/mix["Qtd"].sum()*100).round(1)

    mc1,mc2,mc3 = st.columns(3)
    for col,(_, row) in zip([mc1,mc2,mc3], mix.iterrows()):
        c = COLORS3[_ % 3]
        col.markdown(
            f"<div class='kcard'><div class='klabel'>{row['Tipo']}</div>"
            f"<div class='kval' style='color:{c};'>{row['Qtd']:,}</div>"
            f"<div class='ksub'>{row['Pct']}% do total</div></div>",
            unsafe_allow_html=True
        )

    st.markdown("<div class='sec'>Aprovação por tipo</div>", unsafe_allow_html=True)
    aprov_tipo = dff.groupby("Tipo").agg(
        Total=("Aprovada_bool","count"),
        Aprovadas=("Aprovada_bool","sum")
    ).reset_index()
    aprov_tipo["Reprovadas"] = aprov_tipo["Total"] - aprov_tipo["Aprovadas"]
    aprov_tipo["Taxa"] = (aprov_tipo["Aprovadas"]/aprov_tipo["Total"]*100).round(1)

    g1, g2 = st.columns([1.4, 1])
    with g1:
        aprov_tipo["PctA"] = (aprov_tipo["Aprovadas"]/aprov_tipo["Total"]*100).round(1)
        aprov_tipo["PctR"] = (aprov_tipo["Reprovadas"]/aprov_tipo["Total"]*100).round(1)
        fig = go.Figure()
        fig.add_bar(name="Aprovadas",    x=aprov_tipo["Tipo"], y=aprov_tipo["Aprovadas"], marker_color=GREEN,
                    text=[f"{v:,} ({p}%)" for v,p in zip(aprov_tipo["Aprovadas"],aprov_tipo["PctA"])],
                    textposition="inside", textfont=dict(color="white",size=10))
        fig.add_bar(name="Não aprovadas",x=aprov_tipo["Tipo"], y=aprov_tipo["Reprovadas"], marker_color=RED,
                    text=[f"{v:,} ({p}%)" for v,p in zip(aprov_tipo["Reprovadas"],aprov_tipo["PctR"])],
                    textposition="inside", textfont=dict(color="white",size=10))
        fig.update_layout(**PLOT, barmode="stack", title="Volume e aprovação por tipo",
                          title_font_color="rgba(255,255,255,.8)")
        st.plotly_chart(fig, use_container_width=True)

    with g2:
        fig2 = px.pie(mix, names="Tipo", values="Qtd", hole=0.58,
                      color_discrete_sequence=COLORS3, title="Distribuição de tipos")
        fig2.update_layout(**PLOT, title_font_color="rgba(255,255,255,.8)")
        fig2.update_traces(textfont_color="white")
        st.plotly_chart(fig2, use_container_width=True)

    # Insights automáticos
    st.markdown("<div class='sec'>Insights automáticos</div>", unsafe_allow_html=True)
    tipo_mais = mix.iloc[0]["Tipo"]
    tipo_pct  = mix.iloc[0]["Pct"]
    obra_top  = dff["Obra"].value_counts().index[0] if total > 0 else "—"
    obra_top_n= dff["Obra"].value_counts().iloc[0] if total > 0 else 0
    worst_obra = dff.groupby("Obra")["Aprovada_bool"].mean().sort_values().index[0] if total > 0 else "—"
    worst_pct  = dff.groupby("Obra")["Aprovada_bool"].mean().sort_values().iloc[0]*100 if total > 0 else 0

    col_i1, col_i2, col_i3 = st.columns(3)
    col_i1.markdown(f"<div class='insight'>O tipo <b>{tipo_mais}</b> representa <b>{tipo_pct}%</b> de todas as solicitações do período selecionado.</div>", unsafe_allow_html=True)
    col_i2.markdown(f"<div class='insight'><b>{obra_top}</b> é a obra mais demandante com <b>{obra_top_n:,}</b> solicitações registradas.</div>", unsafe_allow_html=True)
    col_i3.markdown(f"<div class='insight'><b>{worst_obra}</b> tem a menor taxa de aprovação: apenas <b>{worst_pct:.1f}%</b> das solicitações aprovadas.</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — OBRAS & SETORES
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("<div class='sec'>Volume e taxa de aprovação por obra</div>", unsafe_allow_html=True)

    obra_stats = dff.groupby("Obra").agg(
        Total=("Aprovada_bool","count"),
        Aprovadas=("Aprovada_bool","sum"),
    ).reset_index()
    obra_stats["Taxa%"] = (obra_stats["Aprovadas"]/obra_stats["Total"]*100).round(1)
    obra_stats = obra_stats.sort_values("Total", ascending=True)

    obra_stats["PctA"] = (obra_stats["Aprovadas"]/obra_stats["Total"]*100).round(1)
    obra_stats["PctR"] = ((obra_stats["Total"]-obra_stats["Aprovadas"])/obra_stats["Total"]*100).round(1)
    fig_obras = go.Figure()
    fig_obras.add_bar(name="Aprovadas",    y=obra_stats["Obra"], x=obra_stats["Aprovadas"],
                      orientation="h", marker_color=GREEN,
                      text=[f"{v:,} ({p}%)" for v,p in zip(obra_stats["Aprovadas"],obra_stats["PctA"])],
                      textposition="inside", textfont=dict(color="white",size=9))
    fig_obras.add_bar(name="Não aprovadas",y=obra_stats["Obra"],
                      x=obra_stats["Total"]-obra_stats["Aprovadas"],
                      orientation="h", marker_color=RED,
                      text=[f"{v:,} ({p}%)" for v,p in zip(obra_stats["Total"]-obra_stats["Aprovadas"],obra_stats["PctR"])],
                      textposition="inside", textfont=dict(color="white",size=9))
    fig_obras.update_layout(**PLOT, barmode="stack", height=520,
                            title="Solicitações por obra (aprovadas vs. reprovadas)",
                            xaxis_title="Qtd", yaxis_title="")
    for _, row in obra_stats.iterrows():
        fig_obras.add_annotation(
            y=row["Obra"], x=row["Total"],
            text=f"  {int(row['Total'])} (100%)",
            showarrow=False, xanchor="left",
            font=dict(color="rgba(255,255,255,.8)", size=10, family="Inter"),
        )
    st.plotly_chart(fig_obras, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='sec'>Taxa de aprovação % por obra</div>", unsafe_allow_html=True)
        obra_taxa = obra_stats.sort_values("Taxa%")
        obra_taxa["TextoTaxa"] = obra_taxa.apply(
            lambda r: f"{int(r['Aprovadas'])} aprov. | {r['Taxa%']}%", axis=1)
        fig_taxa = px.bar(obra_taxa, y="Obra", x="Taxa%", orientation="h",
                          color="Taxa%", color_continuous_scale=[[0,RED],[0.5,GOLD],[1,GREEN]],
                          labels={"Taxa%":"Taxa aprovação (%)","Obra":""},
                          title="% aprovação por obra",
                          text=obra_taxa["TextoTaxa"])
        fig_taxa.update_traces(textposition="outside", textfont=dict(color="rgba(255,255,255,.82)",size=10))
        fig_taxa.update_layout(**PLOT, coloraxis_showscale=False)
        st.plotly_chart(fig_taxa, use_container_width=True)

    with col_b:
        st.markdown("<div class='sec'>Distribuição por setor</div>", unsafe_allow_html=True)
        setor_cnt = dff["Setor"].value_counts().reset_index()
        setor_cnt.columns = ["Setor","Qtd"]
        fig_setor = px.pie(setor_cnt, names="Setor", values="Qtd", hole=0.55,
                           color_discrete_sequence=COLORS3, title="Carteira por setor")
        fig_setor.update_layout(**PLOT, title_font_color="rgba(255,255,255,.8)")
        fig_setor.update_traces(textfont_color="white")
        st.plotly_chart(fig_setor, use_container_width=True)

    # ── Mix de tipos por setor — um gráfico por carteira ─────────────────────
    st.markdown("<div class='sec'>Mix de regularização por carteira</div>", unsafe_allow_html=True)
    setores_ativos = [s for s in ["Suprimentos","Obra","Planejamento","Não informado"]
                      if s in dff["Setor"].unique()]
    cores_tipo_map = {
        "Aditivo de Contrato":        BLUE,
        "Pedido de Compra":           PURPLE,
        "Elaboração de Contrato novo":GREEN,
    }
    # Cria uma coluna por setor presente
    colunas_setores = st.columns(len(setores_ativos))
    for col_s, setor in zip(colunas_setores, setores_ativos):
        with col_s:
            dff_setor = dff[dff["Setor"] == setor]
            tipo_setor = dff_setor["Tipo"].value_counts().reset_index()
            tipo_setor.columns = ["Tipo","Qtd"]
            tipo_setor["Pct"] = (tipo_setor["Qtd"] / tipo_setor["Qtd"].sum() * 100).round(1)
            total_setor = len(dff_setor)
            fig_ts = px.pie(
                tipo_setor, names="Tipo", values="Qtd", hole=0.55,
                color="Tipo",
                color_discrete_map=cores_tipo_map,
                title=f"{setor}<br><sup>{total_setor:,} solicitações</sup>",
            )
            fig_ts.update_layout(**PLOT, title_font_color="rgba(255,255,255,.85)",
                                 showlegend=True)
            fig_ts.update_layout(legend=dict(
                                     orientation="v",
                                     font=dict(size=10, color="rgba(255,255,255,0.7)"),
                                     bgcolor="rgba(0,0,0,0)",
                                 ))
            fig_ts.update_traces(
                textfont_color="white",
                textinfo="percent",
                hovertemplate="<b>%{label}</b><br>%{value:,} solicitações<br>%{percent}<extra></extra>",
            )
            st.plotly_chart(fig_ts, use_container_width=True)

    st.markdown("<div class='sec'>Tipo de regularização por obra — todas as obras</div>", unsafe_allow_html=True)
    obra_tipo = dff.groupby(["Obra","Tipo"]).size().reset_index(name="Qtd")
    # Ordenar obras pelo total decrescente para facilitar leitura
    ordem_obras = dff["Obra"].value_counts().index.tolist()
    obra_tipo["Obra"] = pd.Categorical(obra_tipo["Obra"], categories=ordem_obras[::-1], ordered=True)
    obra_tipo = obra_tipo.sort_values("Obra")
    n_obras_total = obra_tipo["Obra"].nunique()
    altura_ot = max(420, n_obras_total * 28)  # altura dinâmica por número de obras
    _tot_ob = obra_tipo.groupby("Obra")["Qtd"].transform("sum")
    obra_tipo["PctTipo"] = (obra_tipo["Qtd"]/_tot_ob*100).round(1)
    obra_tipo["TextoBar"] = obra_tipo.apply(lambda r: f"{r['Qtd']} ({r['PctTipo']}%)", axis=1)
    fig_ot = px.bar(obra_tipo, x="Qtd", y="Obra", color="Tipo",
                    color_discrete_sequence=COLORS3, orientation="h",
                    title=f"Mix de tipos por obra ({n_obras_total} obras)",
                    labels={"Qtd":"Solicitações","Obra":""},
                    text="TextoBar")
    fig_ot.update_traces(textposition="inside", textfont=dict(color="white",size=9))
    fig_ot.update_layout(**PLOT, height=altura_ot, barmode="stack",
                         title_font_color="rgba(255,255,255,.8)")
    fig_ot.update_layout(yaxis=dict(tickfont=dict(size=11)))
    st.plotly_chart(fig_ot, use_container_width=True)

    # Tipo de contrato e caução
    col_tc, col_cau = st.columns(2)
    with col_tc:
        st.markdown("<div class='sec'>Tipo de contrato</div>", unsafe_allow_html=True)
        # Base: apenas Elaboração de Contrato novo
        dff_elab = dff[dff["Tipo"] == "Elaboração de Contrato novo"]
        tc = dff_elab["TipoContrato"].value_counts().reset_index()
        tc.columns = ["Tipo","Qtd"]
        fig_tc = px.pie(tc, names="Tipo", values="Qtd", hole=0.55,
                        color_discrete_sequence=[BLUE, PURPLE],
                        title=f"Normal vs. Spot (base: {len(dff_elab):,} elaborações)")
        fig_tc.update_layout(**PLOT, title_font_color="rgba(255,255,255,.8)")
        fig_tc.update_traces(textfont_color="white")
        st.plotly_chart(fig_tc, use_container_width=True)

    with col_cau:
        st.markdown("<div class='sec'>Caução / Retenção</div>", unsafe_allow_html=True)
        # Base: apenas Elaboração de Contrato novo
        dff_elab = dff[dff["Tipo"] == "Elaboração de Contrato novo"]
        cau = dff_elab["Caucao"].value_counts().reset_index()
        cau.columns = ["Tipo","Qtd"]
        fig_cau = px.pie(cau, names="Tipo", values="Qtd", hole=0.55,
                         color_discrete_sequence=COLORS5,
                         title=f"Caução e retenção nos contratos (base: {len(dff_elab):,} elaborações)")
        fig_cau.update_layout(**PLOT, title_font_color="rgba(255,255,255,.8)")
        fig_cau.update_traces(textfont_color="white")
        st.plotly_chart(fig_cau, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — TEMPORAL
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("<div class='sec'>Evolução mensal por tipo</div>", unsafe_allow_html=True)

    mes_tipo = dff.groupby(["MesAno","Tipo"]).size().reset_index(name="Qtd")
    mes_total = dff.groupby("MesAno").size().reset_index(name="Total")

    _tot_mes = mes_tipo.groupby("MesAno")["Qtd"].transform("sum")
    mes_tipo["PctMes"] = (mes_tipo["Qtd"]/_tot_mes*100).round(1)
    mes_tipo["TextoBar"] = mes_tipo.apply(lambda r: f"{r['Qtd']} ({r['PctMes']}%)", axis=1)
    fig_mt = px.bar(mes_tipo, x="MesAno", y="Qtd", color="Tipo",
                    color_discrete_sequence=COLORS3, barmode="group",
                    labels={"MesAno":"","Qtd":"Solicitações","Tipo":""},
                    title="Solicitações mensais por tipo",
                    text="TextoBar")
    fig_mt.update_traces(textposition="outside", textfont=dict(color="rgba(255,255,255,.75)",size=9))
    # Linha de total mensal sobreposta
    fig_mt.add_scatter(
        x=mes_total["MesAno"],
        y=mes_total["Total"],
        mode="lines+markers+text",
        name="Total do mês",
        line=dict(color=GOLD, width=2.5, dash="dot"),
        marker=dict(size=7, color=GOLD),
        text=mes_total["Total"].astype(str),
        textposition="top center",
        textfont=dict(color=GOLD, size=11),
    )
    fig_mt.update_layout(**PLOT, xaxis_tickangle=-40,
                         title_font_color="rgba(255,255,255,.8)")
    st.plotly_chart(fig_mt, use_container_width=True)

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("<div class='sec'>Aprovadas vs. reprovadas por mês</div>", unsafe_allow_html=True)
        mes_aprov = dff.groupby(["MesAno","Aprovada"]).size().reset_index(name="Qtd")
        _tot_aprov = mes_aprov.groupby("MesAno")["Qtd"].transform("sum")
        mes_aprov["PctMes"] = (mes_aprov["Qtd"]/_tot_aprov*100).round(1)
        mes_aprov["TextoBar"] = mes_aprov.apply(lambda r: f"{r['Qtd']} ({r['PctMes']}%)", axis=1)
        fig_ma = px.bar(mes_aprov, x="MesAno", y="Qtd", color="Aprovada",
                        color_discrete_map={"Sim":GREEN,"Não":RED},
                        labels={"MesAno":"","Qtd":"Qtd","Aprovada":""},
                        title="Aprovação mensal",
                        text="TextoBar")
        fig_ma.update_traces(textposition="inside", textfont=dict(color="white",size=9))
        fig_ma.update_layout(**PLOT, xaxis_tickangle=-40,
                             title_font_color="rgba(255,255,255,.8)")
        st.plotly_chart(fig_ma, use_container_width=True)

    with col_t2:
        st.markdown("<div class='sec'>Volume por dia da semana</div>", unsafe_allow_html=True)
        ordem = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        nomes = ["Segunda","Terça","Quarta","Quinta","Sexta","Sábado","Domingo"]
        dia_cnt = dff["DiaSemana"].value_counts().reindex(ordem, fill_value=0).reset_index()
        dia_cnt.columns = ["Dia","Qtd"]
        dia_cnt["DiaLabel"] = nomes
        dia_cnt["PctDia"] = (dia_cnt["Qtd"]/dia_cnt["Qtd"].sum()*100).round(1)
        dia_cnt["TextoDia"] = dia_cnt.apply(lambda r: f"{r['Qtd']:,} ({r['PctDia']}%)", axis=1)
        fig_dia = px.bar(dia_cnt, x="DiaLabel", y="Qtd",
                         color_discrete_sequence=[BLUE],
                         labels={"DiaLabel":"","Qtd":"Solicitações"},
                         title="Distribuição por dia da semana", text="TextoDia")
        fig_dia.update_traces(textposition="outside", textfont=dict(color="rgba(255,255,255,.82)",size=10))
        fig_dia.update_layout(**PLOT)
        st.plotly_chart(fig_dia, use_container_width=True)

    with col_t1:
        st.markdown("<div class='sec'>Volume por hora do dia</div>", unsafe_allow_html=True)
        hora_cnt = dff["HoraDia"].value_counts().sort_index().reset_index()
        hora_cnt.columns = ["Hora","Qtd"]
        fig_hora = px.area(hora_cnt, x="Hora", y="Qtd",
                           color_discrete_sequence=[BACC],
                           labels={"Hora":"Hora","Qtd":"Solicitações"},
                           title="Pico de preenchimento por hora")
        fig_hora.update_layout(**PLOT, title_font_color="rgba(255,255,255,.8)")
        fig_hora.update_traces(fill="tozeroy", fillcolor=f"rgba(74,159,224,0.2)")
        st.plotly_chart(fig_hora, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — OPERACIONAL
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    col_u1, col_u2 = st.columns(2)

    with col_u1:
        st.markdown("<div class='sec'>Top 15 usuários por volume</div>", unsafe_allow_html=True)
        user_cnt = dff["Usuario"].value_counts().head(15).reset_index()
        user_cnt.columns = ["Usuario","Qtd"]
        user_cnt["PctUser"] = (user_cnt["Qtd"]/user_cnt["Qtd"].sum()*100).round(1)
        user_cnt["TextoUser"] = user_cnt.apply(lambda r: f"{r['Qtd']:,} ({r['PctUser']}%)", axis=1)
        fig_user = px.bar(user_cnt.sort_values("Qtd"), x="Qtd", y="Usuario",
                          orientation="h", color_discrete_sequence=[PURPLE],
                          labels={"Qtd":"Solicitações","Usuario":""},
                          title="Ranking de usuários", text="TextoUser")
        fig_user.update_traces(textposition="outside", textfont=dict(color="rgba(255,255,255,.82)",size=11))
        fig_user.update_layout(**PLOT, height=460)
        st.plotly_chart(fig_user, use_container_width=True)

    with col_u2:
        st.markdown("<div class='sec'>Lead time por usuário (top 10)</div>", unsafe_allow_html=True)
        user_lead = (
            dff.groupby("Usuario")["LeadMin"]
            .agg(["median","count"])
            .reset_index()
        )
        user_lead.columns = ["Usuario","LeadMediano","Total"]
        user_lead = user_lead[user_lead["Total"] >= 5].nlargest(10, "LeadMediano")
        _ul = user_lead.sort_values("LeadMediano").copy()
        _ul_total = _ul["LeadMediano"].sum()
        _ul["TextoLead"] = _ul.apply(lambda r: f"{r['LeadMediano']:.1f} min ({round(r['LeadMediano']/_ul_total*100,1)}%)", axis=1)
        fig_lead = px.bar(_ul, x="LeadMediano", y="Usuario",
                          orientation="h", color_discrete_sequence=[GOLD],
                          labels={"LeadMediano":"Lead time mediano (min)","Usuario":""},
                          title="Usuários com maior tempo de preenchimento",
                          text="TextoLead")
        fig_lead.update_traces(textposition="outside", textfont=dict(color="rgba(255,255,255,.82)",size=11))
        fig_lead.update_layout(**PLOT, height=460)
        st.plotly_chart(fig_lead, use_container_width=True)

    st.markdown("<div class='sec'>Motivos de compra direta pela obra</div>", unsafe_allow_html=True)
    col_m1, col_m2 = st.columns([1.2, 1])

    # Base: apenas Pedido de Compra
    dff_pc_mot = dff[dff["Tipo"] == "Pedido de Compra"]

    with col_m1:
        motivo_cnt = dff_pc_mot["Motivo"].value_counts().reset_index()
        motivo_cnt.columns = ["Motivo","Qtd"]
        motivo_cnt["Pct"] = (motivo_cnt["Qtd"]/motivo_cnt["Qtd"].sum()*100).round(1)
        motivo_cnt["TextoMot"] = motivo_cnt.apply(lambda r: f"{r['Qtd']:,} ({r['Pct']}%)", axis=1)
        fig_mot = px.bar(motivo_cnt.sort_values("Qtd"), x="Qtd", y="Motivo",
                         orientation="h",
                         color="Qtd", color_continuous_scale=[[0,GOLD],[1,RED]],
                         labels={"Qtd":"Ocorrências","Motivo":""},
                         title=f"Motivos de compra direta (base: {len(dff_pc_mot):,} pedidos)",
                         text="TextoMot")
        fig_mot.update_traces(textposition="outside", textfont=dict(color="rgba(255,255,255,.82)",size=11))
        fig_mot.update_layout(**PLOT, coloraxis_showscale=False)
        st.plotly_chart(fig_mot, use_container_width=True)

    with col_m2:
        fig_mot2 = px.pie(motivo_cnt, names="Motivo", values="Qtd", hole=0.52,
                          color_discrete_sequence=COLORS5,
                          title="Proporção dos motivos")
        fig_mot2.update_layout(**PLOT, title_font_color="rgba(255,255,255,.8)")
        fig_mot2.update_traces(textfont_color="white", textinfo="percent")
        st.plotly_chart(fig_mot2, use_container_width=True)

    st.markdown("<div class='sec'>Categorias de pedidos de compra</div>", unsafe_allow_html=True)
    col_c1, col_c2 = st.columns([1.5, 1])

    # Base: apenas Pedido de Compra
    dff_pc_cat = dff[dff["Tipo"] == "Pedido de Compra"]

    with col_c1:
        cat_cnt = dff_pc_cat["Categoria"].value_counts().head(15).reset_index()
        cat_cnt.columns = ["Categoria","Qtd"]
        cat_cnt["PctCat"] = (cat_cnt["Qtd"]/cat_cnt["Qtd"].sum()*100).round(1)
        cat_cnt["TextoCat"] = cat_cnt.apply(lambda r: f"{r['Qtd']:,} ({r['PctCat']}%)", axis=1)
        fig_cat = px.bar(cat_cnt.sort_values("Qtd"), x="Qtd", y="Categoria",
                         orientation="h", color_discrete_sequence=[TEAL],
                         labels={"Qtd":"Ocorrências","Categoria":""},
                         title=f"Top 15 categorias de materiais/serviços (base: {len(dff_pc_cat):,} pedidos)",
                         text="TextoCat")
        fig_cat.update_traces(textposition="outside", textfont=dict(color="rgba(255,255,255,.82)",size=10))
        fig_cat.update_layout(**PLOT, height=440)
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_c2:
        st.markdown("<div class='sec'>Condição de pagamento</div>", unsafe_allow_html=True)
        # Base: apenas Pedido de Compra (mesmo filtro de dff_pc_cat)
        pag_cnt = dff_pc_cat["PagNorm"].value_counts().dropna().reset_index()
        pag_cnt.columns = ["Pagamento","Qtd"]
        fig_pag = px.pie(pag_cnt, names="Pagamento", values="Qtd", hole=0.52,
                         color_discrete_sequence=COLORS5,
                         title=f"Forma de pagamento negociada (base: {len(dff_pc_cat):,} pedidos)")
        fig_pag.update_layout(**PLOT, title_font_color="rgba(255,255,255,.8)")
        fig_pag.update_traces(textfont_color="white")
        st.plotly_chart(fig_pag, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — DADOS BRUTOS
# ─────────────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown("<div class='sec'>Tabela completa de registros filtrados</div>", unsafe_allow_html=True)

    cols_show = [c for c in ["Inicio","Obra","Setor","Tipo","Aprovada","Usuario",
                              "TipoContrato","Caucao","PagNorm","Categoria","Motivo","LeadMin"]
                 if c in dff.columns]
    df_show = dff[cols_show].copy()
    df_show["LeadMin"] = df_show["LeadMin"].round(1)
    df_show = df_show.rename(columns={"LeadMin":"Lead (min)","PagNorm":"Pagamento"})
    df_show["Inicio"] = df_show["Inicio"].dt.strftime("%d/%m/%Y %H:%M")

    col_s1, col_s2, col_s3 = st.columns(3)
    busca_obra = col_s1.selectbox("Filtrar por obra", ["Todas"] + sorted(dff["Obra"].dropna().unique().tolist()))
    busca_tipo = col_s2.selectbox("Filtrar por tipo", ["Todos"] + sorted(dff["Tipo"].dropna().unique().tolist()))
    busca_aprov = col_s3.selectbox("Filtrar aprovação", ["Todos","Sim","Não"])

    df_view = df_show.copy()
    if busca_obra  != "Todas":  df_view = df_view[df_view["Obra"] == busca_obra]
    if busca_tipo  != "Todos":  df_view = df_view[df_view["Tipo"] == busca_tipo]
    if busca_aprov != "Todos":  df_view = df_view[df_view["Aprovada"] == busca_aprov]

    st.markdown(f"<p style='color:rgba(255,255,255,.5);font-size:12px;'>{len(df_view):,} registros exibidos</p>",
                unsafe_allow_html=True)
    st.dataframe(df_view, use_container_width=True, height=500)

    csv = df_view.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Baixar CSV filtrado", csv, "lbx_filtrado.csv", "text/csv")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 6 — GASTOS POR INSUMO, FORNECEDOR E OBRA
# ─────────────────────────────────────────────────────────────────────────────
with tab6:
    if de.empty:
        st.warning("A aba 'Especificação' não foi encontrada na planilha.")
    else:
        de_f = de.copy()
        if meses_g_sel:  de_f = de_f[de_f["MesAno"].isin(meses_g_sel)]
        if coords_sel:   de_f = de_f[de_f["Coordenador"].isin(coords_sel)]

        total_gasto  = de_f["ValorTotal"].sum()
        n_itens      = len(de_f)
        ticket_medio = de_f["ValorTotal"].mean() if n_itens > 0 else 0
        top_forn     = de_f.groupby("Fornecedor")["ValorTotal"].sum().idxmax() if n_itens > 0 else "—"
        top_forn_val = de_f.groupby("Fornecedor")["ValorTotal"].sum().max() if n_itens > 0 else 0

        # ── KPIs ──────────────────────────────────────────────────────────────
        st.markdown("<div class='sec'>KPIs de gastos</div>", unsafe_allow_html=True)
        kg1,kg2,kg3,kg4 = st.columns(4)
        _tf = top_forn[:26]+"…" if len(top_forn)>26 else top_forn
        for col_k,lbl,val,sub,color in [
            (kg1,"Gasto Total",       f"R$ {total_gasto:,.0f}",  "no período",              BACC),
            (kg2,"Itens registrados", f"{n_itens:,}",             "linhas especificação",    GREEN),
            (kg3,"Ticket médio",      f"R$ {ticket_medio:,.0f}", "por item",                GOLD),
            (kg4,"Maior fornecedor",  _tf,                        f"R$ {top_forn_val:,.0f}", RED),
        ]:
            col_k.markdown(
                f"<div class='kcard'><div class='klabel'>{lbl}</div>"
                f"<div class='kval' style='color:{color};font-size:18px;'>{val}</div>"
                f"<div class='ksub'>{sub}</div></div>", unsafe_allow_html=True
            )

        # ══════════════════════════════════════════════════════════════════════
        # GASTO TOTAL POR OBRA
        # ══════════════════════════════════════════════════════════════════════
        st.markdown("<div class='sec'>Gasto total por obra</div>", unsafe_allow_html=True)

        obra_g = (de_f.groupby("Obra")["ValorTotal"].sum()
                  .reset_index()
                  .sort_values("ValorTotal", ascending=True))
        obra_g["Fmt"] = obra_g["ValorTotal"].apply(lambda x: f"R$ {x:,.0f}")
        obra_g["Pct"] = (obra_g["ValorTotal"] / obra_g["ValorTotal"].sum() * 100).round(1)

        col_ob1, col_ob2 = st.columns([1.5, 1])

        with col_ob1:
            fig_obra_bar = go.Figure()
            fig_obra_bar.add_bar(
                x=obra_g["ValorTotal"],
                y=obra_g["Obra"],
                orientation="h",
                marker=dict(
                    color=obra_g["ValorTotal"],
                    colorscale=[
                        [0,   "rgba(46,116,212,0.55)"],
                        [0.4, "rgba(74,159,224,0.80)"],
                        [0.7, "rgba(83,74,183,0.88)"],
                        [1,   "rgba(160,125,224,1.0)"],
                    ],
                    showscale=False,
                ),
                text=obra_g.apply(lambda r: f"{r['Fmt']} ({r['Pct']}%)", axis=1),
                textposition="outside",
                textfont=dict(color="rgba(255,255,255,0.88)", size=11, family="Inter"),
                cliponaxis=False,
            )
            fig_obra_bar.update_layout(
                **PLOT,
                height=max(380, len(obra_g) * 36),
                title=f"Valor gasto por obra — Total: R$ {obra_g['ValorTotal'].sum():,.0f}",
                xaxis_title="Valor Total (R$)",
                yaxis_title="",
            )
            fig_obra_bar.update_layout(xaxis=dict(tickformat=",.0f"))
            st.plotly_chart(fig_obra_bar, use_container_width=True)

        with col_ob2:
            fig_obra_pie = px.pie(
                obra_g.sort_values("ValorTotal", ascending=False),
                names="Obra",
                values="ValorTotal",
                hole=0.52,
                color_discrete_sequence=[
                    BLUE, PURPLE, GREEN, GOLD, RED, TEAL, BACC,
                    "#a07de0", "#f08070", "#4dd4a0", "#f5c060",
                    "#e080c0", "#80c0e0", "#c0e080", "#e0c080", "#8080e0",
                ],
                title="Participação % de cada obra no gasto total",
            )
            fig_obra_pie.update_layout(**PLOT)
            fig_obra_pie.update_traces(
                textfont_color="white",
                textinfo="percent",
                hovertemplate="<b>%{label}</b><br>R$ %{value:,.0f}<br>%{percent}<extra></extra>",
            )
            st.plotly_chart(fig_obra_pie, use_container_width=True)

        # ── Gasto por categoria ────────────────────────────────────────────────
        st.markdown("<div class='sec'>Gasto por categoria de insumo</div>", unsafe_allow_html=True)
        cat_g = de_f.groupby("CategoriaInsumo")["ValorTotal"].sum().reset_index().sort_values("ValorTotal",ascending=True)
        cat_g["Fmt"] = cat_g["ValorTotal"].apply(lambda x: f"R$ {x:,.0f}")
        fig_cat_g = go.Figure()
        fig_cat_g.add_bar(
            x=cat_g["ValorTotal"], y=cat_g["CategoriaInsumo"], orientation="h",
            marker=dict(color=cat_g["ValorTotal"],
                        colorscale=[[0,"rgba(46,116,212,.55)"],[.5,"rgba(74,159,224,.9)"],[1,"rgba(160,125,224,1)"]],
                        showscale=False),
            text=cat_g.apply(lambda r: f"{r['Fmt']} ({round(r['ValorTotal']/cat_g['ValorTotal'].sum()*100,1)}%)", axis=1),
            textposition="outside",
            textfont=dict(color="rgba(255,255,255,.85)",size=11), cliponaxis=False,
        )
        fig_cat_g.update_layout(**PLOT, height=360,
                                title=f"Categorias de insumo — Total: R$ {total_gasto:,.0f}",
                                xaxis_title="Valor Total (R$)")
        fig_cat_g.update_layout(xaxis=dict(tickformat=",.0f"))
        st.plotly_chart(fig_cat_g, use_container_width=True)

        # ── Top 15 fornecedores ────────────────────────────────────────────────
        st.markdown("<div class='sec'>Top 15 empresas por valor gasto</div>", unsafe_allow_html=True)
        forn_g = (de_f.groupby("Fornecedor")["ValorTotal"].sum()
                  .reset_index().nlargest(15,"ValorTotal").sort_values("ValorTotal",ascending=True))
        forn_g["Fmt"]   = forn_g["ValorTotal"].apply(lambda x: f"R$ {x:,.0f}")
        forn_g["Label"] = forn_g["Fornecedor"].str[:45]
        fig_forn = go.Figure()
        fig_forn.add_bar(
            x=forn_g["ValorTotal"], y=forn_g["Label"], orientation="h",
            marker=dict(color=forn_g["ValorTotal"],
                        colorscale=[[0,"rgba(29,158,117,.55)"],[.5,"rgba(29,158,117,.88)"],[1,"rgba(77,212,160,1)"]],
                        showscale=False),
            text=forn_g.apply(lambda r: f"{r['Fmt']} ({round(r['ValorTotal']/forn_g['ValorTotal'].sum()*100,1)}%)", axis=1),
            textposition="outside",
            textfont=dict(color="rgba(255,255,255,.85)",size=11), cliponaxis=False,
        )
        fig_forn.update_layout(**PLOT, height=520,
                               title="Top 15 empresas — maior gasto total",
                               xaxis_title="Valor Total (R$)")
        fig_forn.update_layout(xaxis=dict(tickformat=",.0f"))
        st.plotly_chart(fig_forn, use_container_width=True)

        # ── Heatmap Fornecedor × Obra ──────────────────────────────────────────
        st.markdown("<div class='sec'>Gasto por obra em cada empresa (top 15 fornecedores)</div>", unsafe_allow_html=True)
        top15 = forn_g["Fornecedor"].tolist()
        obra_forn = (de_f[de_f["Fornecedor"].isin(top15)]
                     .groupby(["Fornecedor","Obra"])["ValorTotal"].sum().reset_index())
        obra_forn["FL"] = obra_forn["Fornecedor"].str[:38]
        pivot    = obra_forn.pivot_table(index="FL",columns="Obra",values="ValorTotal",fill_value=0)
        pivot_lbl= obra_forn.pivot_table(index="FL",columns="Obra",
                                          values="ValorTotal",aggfunc="first").fillna(0)
        pivot_txt= [[f"R$ {pivot_lbl.loc[r,c]:,.0f}" if c in pivot_lbl.columns else "—"
                     for c in pivot.columns] for r in pivot.index]
        fig_heat = go.Figure(go.Heatmap(
            z=pivot.values, x=[c[:24] for c in pivot.columns], y=pivot.index.tolist(),
            text=pivot_txt, texttemplate="%{text}",
            textfont=dict(size=9,color="white"),
            colorscale=[[0,"#0b1628"],[.25,"rgba(46,116,212,.5)"],[.7,"rgba(74,159,224,.88)"],[1,"rgba(160,125,224,1)"]],
            showscale=True,
            hovertemplate="<b>%{y}</b><br>%{x}<br>R$ %{z:,.0f}<extra></extra>",
        ))
        fig_heat.update_layout(**PLOT, height=520,
                               title="Mapa de calor — Empresa × Obra (R$)", xaxis_tickangle=-35)
        st.plotly_chart(fig_heat, use_container_width=True)

        # ── Barras empilhadas top 10 fornecedores por obra ─────────────────────
        st.markdown("<div class='sec'>Detalhamento por obra — top 10 empresas</div>", unsafe_allow_html=True)
        top10 = forn_g.nlargest(10,"ValorTotal")["Fornecedor"].tolist()
        of10  = (de_f[de_f["Fornecedor"].isin(top10)]
                 .groupby(["Fornecedor","Obra"])["ValorTotal"].sum().reset_index())
        of10["FL"]  = of10["Fornecedor"].str[:32]
        of10["Fmt"] = of10["ValorTotal"].apply(lambda x: f"R$ {x:,.0f}")
        fig_of = px.bar(of10, x="FL", y="ValorTotal", color="Obra",
                        color_discrete_sequence=[BLUE,PURPLE,GREEN,GOLD,RED,TEAL,BACC,
                                                 "#a07de0","#f08070","#4dd4a0","#f5c060"],
                        barmode="stack",
                        labels={"FL":"Empresa","ValorTotal":"Valor (R$)","Obra":"Obra"},
                        title="Qual obra gastou quanto em cada empresa")
        totais_of = of10.groupby("FL")["ValorTotal"].sum().reset_index()
        _grand_of = totais_of["ValorTotal"].sum()
        for _, row in totais_of.iterrows():
            _pct_of = round(row["ValorTotal"]/_grand_of*100,1) if _grand_of>0 else 0
            fig_of.add_annotation(
                x=row["FL"], y=row["ValorTotal"],
                text=f"R$ {row['ValorTotal']:,.0f} ({_pct_of}%)",
                showarrow=False, yshift=10,
                font=dict(color="rgba(255,255,255,.9)",size=10,family="Inter"),
            )
        fig_of.update_layout(**PLOT, height=480, xaxis_tickangle=-22)
        st.plotly_chart(fig_of, use_container_width=True)

        # ── Coordenador ────────────────────────────────────────────────────────
        st.markdown("<div class='sec'>Gasto por coordenador</div>", unsafe_allow_html=True)
        cg1,cg2 = st.columns([1.4,1])
        coord_g = (de_f.groupby("Coordenador")["ValorTotal"].sum().reset_index()
                   .sort_values("ValorTotal",ascending=True))
        coord_g["Fmt"] = coord_g["ValorTotal"].apply(lambda x: f"R$ {x:,.0f}")
        with cg1:
            fig_crd = go.Figure()
            fig_crd.add_bar(
                x=coord_g["ValorTotal"], y=coord_g["Coordenador"], orientation="h",
                marker=dict(color=coord_g["ValorTotal"],
                            colorscale=[[0,"rgba(240,168,48,.55)"],[1,"rgba(255,200,80,1)"]],
                            showscale=False),
                text=coord_g.apply(lambda r: f"{r['Fmt']} ({round(r['ValorTotal']/coord_g['ValorTotal'].sum()*100,1)}%)", axis=1),
                textposition="outside",
                textfont=dict(color="rgba(255,255,255,.85)",size=11), cliponaxis=False,
            )
            fig_crd.update_layout(**PLOT, height=300, title="Gasto total por coordenador",
                                  xaxis_title="Valor Total (R$)")
            fig_crd.update_layout(xaxis=dict(tickformat=",.0f"))
            st.plotly_chart(fig_crd, use_container_width=True)
        with cg2:
            fig_cp = px.pie(coord_g,names="Coordenador",values="ValorTotal",hole=0.55,
                            color_discrete_sequence=[BLUE,PURPLE,GREEN,GOLD,RED],
                            title="Participação % por coordenador")
            fig_cp.update_layout(**PLOT)
            fig_cp.update_traces(textfont_color="white",textinfo="percent+label",
                                 hovertemplate="<b>%{label}</b><br>R$ %{value:,.0f}<br>%{percent}<extra></extra>")
            st.plotly_chart(fig_cp, use_container_width=True)

        # ── Evolução mensal ────────────────────────────────────────────────────
        st.markdown("<div class='sec'>Evolução mensal dos gastos</div>", unsafe_allow_html=True)
        mes_g   = de_f.groupby(["MesAno","CategoriaInsumo"])["ValorTotal"].sum().reset_index()
        mes_tot = de_f.groupby("MesAno")["ValorTotal"].sum().reset_index()
        fig_mg  = px.bar(mes_g,x="MesAno",y="ValorTotal",color="CategoriaInsumo",
                         color_discrete_sequence=[BLUE,PURPLE,GREEN,GOLD,RED,TEAL,BACC,"#a07de0"],
                         barmode="stack",
                         labels={"MesAno":"","ValorTotal":"Valor (R$)","CategoriaInsumo":"Categoria"},
                         title="Gastos mensais por categoria")
        fig_mg.add_scatter(
            x=mes_tot["MesAno"],y=mes_tot["ValorTotal"],
            mode="lines+markers+text",name="Total do mês",
            line=dict(color=GOLD,width=2.5,dash="dot"),
            marker=dict(size=8,color=GOLD),
            text=mes_tot["ValorTotal"].apply(lambda x: f"R$ {x:,.0f}"),
            textposition="top center",textfont=dict(color=GOLD,size=10),
        )
        fig_mg.update_layout(**PLOT,height=380,xaxis_tickangle=-30)
        st.plotly_chart(fig_mg, use_container_width=True)

        # ── Tabela ─────────────────────────────────────────────────────────────
        with st.expander("📋 Ver dados completos de especificação"):
            de_show = de_f[["MesAno","Obra","Coordenador","Fornecedor",
                            "CategoriaInsumo","Insumo","ValorTotal"]].copy()
            de_show["ValorTotal"] = de_show["ValorTotal"].apply(lambda x: f"R$ {x:,.2f}")
            de_show = de_show.rename(columns={"MesAno":"Mês","CategoriaInsumo":"Categoria",
                                              "Insumo":"Descrição","ValorTotal":"Valor Total"})
            st.dataframe(de_show, use_container_width=True, height=400)
            st.download_button("⬇ Baixar CSV", de_f.to_csv(index=False).encode("utf-8"),
                               "lbx_gastos.csv","text/csv")

# ── Rodapé ────────────────────────────────────────────────────────────────────
st.markdown(
    f"<p style='text-align:center;font-size:10px;color:rgba(255,255,255,.22);margin-top:30px;'>"
    f"LBX CONSTRUTORA · Dashboard de Regularização · Python + Streamlit + Plotly</p>",
    unsafe_allow_html=True
)