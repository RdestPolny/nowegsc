import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

# Konfiguracja strony
st.set_page_config(
    page_title="Google Search Console Dashboard",
    page_icon="📊",
    layout="wide"
)

# Style CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# Funkcje pomocnicze
@st.cache_data
def generate_mock_data():
    """Generuje przykładowe dane dla demonstracji"""
    dates = pd.date_range(start='2024-06-01', end='2025-09-30', freq='W')
    
    data = []
    for i, date in enumerate(dates):
        base_clicks = 400 + np.random.random() * 200
        trend = i * 10
        
        data.append({
            'date': date,
            'clicks': int(base_clicks + trend + np.random.random() * 100),
            'impressions': int((base_clicks + trend) * 25 + np.random.random() * 3000),
            'ctr': 3.5 + np.random.random() * 1.5,
            'position': 9 - (i / len(dates)) * 4
        })
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df

def get_country_data():
    """Zwraca dane o ruchu według krajów"""
    return pd.DataFrame({
        'country': ['Polska', 'USA', 'Niemcy', 'UK', 'Francja'],
        'clicks': [8500, 1200, 950, 720, 580],
        'impressions': [185000, 32000, 28000, 21000, 18500],
        'ctr': [4.59, 3.75, 3.39, 3.43, 3.14]
    })

def get_top_pages():
    """Zwraca najpopularniejsze strony"""
    return pd.DataFrame({
        'page': [
            '/blog/seo-tips-2025',
            '/produkty/kategoria-a',
            '/',
            '/blog/marketing-content',
            '/uslugi',
            '/blog/google-analytics',
            '/kontakt',
            '/o-nas'
        ],
        'clicks': [2100, 1850, 1600, 1320, 1100, 980, 850, 720],
        'impressions': [45000, 42000, 38000, 35000, 28000, 25000, 22000, 19000],
        'ctr': [4.67, 4.40, 4.21, 3.77, 3.93, 3.92, 3.86, 3.79],
        'position': [4.2, 5.1, 3.8, 6.3, 5.8, 7.1, 8.2, 6.9]
    })

def get_top_queries():
    """Zwraca najpopularniejsze zapytania"""
    return pd.DataFrame({
        'query': [
            'optymalizacja seo',
            'marketing internetowy',
            'pozycjonowanie stron',
            'content marketing',
            'analityka google',
            'social media marketing',
            'strategia seo',
            'reklama google ads'
        ],
        'clicks': [1250, 1120, 980, 850, 720, 650, 580, 520],
        'impressions': [28000, 26500, 24000, 21000, 19000, 17500, 15800, 14200],
        'ctr': [4.46, 4.23, 4.08, 4.05, 3.79, 3.71, 3.67, 3.66],
        'position': [4.5, 5.2, 6.1, 5.8, 6.5, 7.2, 7.8, 8.1]
    })

def get_device_data():
    """Zwraca dane o urządzeniach"""
    return pd.DataFrame({
        'device': ['Mobile', 'Desktop', 'Tablet'],
        'clicks': [5800, 4200, 1000],
        'impressions': [135000, 98000, 25000]
    })

def aggregate_by_month(df):
    """Agreguje dane do miesięcy"""
    df_copy = df.copy()
    df_copy['month'] = df_copy['date'].dt.to_period('M')
    
    monthly = df_copy.groupby('month').agg({
        'clicks': 'sum',
        'impressions': 'sum',
        'ctr': 'mean',
        'position': 'mean'
    }).reset_index()
    
    monthly['date'] = monthly['month'].dt.to_timestamp()
    monthly = monthly.drop('month', axis=1)
    
    return monthly

def filter_data_by_period(df, period):
    """Filtruje dane według wybranego okresu"""
    end_date = pd.Timestamp('2025-09-30')
    
    if period == '1month':
        start_date = end_date - timedelta(days=30)
        aggregation = 'day'
    elif period == '3months':
        start_date = end_date - timedelta(days=90)
        aggregation = 'month'
    elif period == '12months':
        start_date = end_date - timedelta(days=365)
        aggregation = 'month'
    elif period == '16months':
        start_date = end_date - timedelta(days=480)
        aggregation = 'month'
    else:
        return df, 'day'
    
    filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    if aggregation == 'month':
        filtered = aggregate_by_month(filtered)
    
    return filtered, aggregation

# Inicjalizacja session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'selected_site' not in st.session_state:
    st.session_state.selected_site = None
if 'period' not in st.session_state:
    st.session_state.period = '3months'

# Strona logowania
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center;'>📊 Google Search Console Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Połącz się z GSC, aby zobaczyć swoje dane analityczne</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🔐 Połącz z Google", use_container_width=True, type="primary"):
            st.session_state.authenticated = True
            st.rerun()
        
        st.info("🔒 Ta aplikacja używa OAuth 2.0 do bezpiecznego połączenia z GSC")

# Wybór witryny
elif st.session_state.selected_site is None:
    st.title("📂 Wybierz witrynę")
    
    sites = ['https://example.com', 'https://blog.example.com']
    
    for site in sites:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### 🌐 {site}")
            st.caption("Kliknij przycisk, aby zobaczyć dane")
        with col2:
            if st.button("Wybierz", key=site, use_container_width=True):
                st.session_state.selected_site = site
                st.rerun()

# Dashboard główny
else:
    # Pobierz dane
    data = generate_mock_data()
    
    # Nagłówek
    st.title("📊 Dashboard Google Search Console")
    st.markdown(f"**Witryna:** {st.session_state.selected_site}")
    
    # Przyciski wyboru okresu
    st.markdown("### 📅 Wybierz okres")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Ostatni miesiąc", use_container_width=True, 
                    type="primary" if st.session_state.period == '1month' else "secondary"):
            st.session_state.period = '1month'
            st.rerun()
    
    with col2:
        if st.button("Kwartał (3 msc)", use_container_width=True,
                    type="primary" if st.session_state.period == '3months' else "secondary"):
            st.session_state.period = '3months'
            st.rerun()
    
    with col3:
        if st.button("Ostatnie 12 msc", use_container_width=True,
                    type="primary" if st.session_state.period == '12months' else "secondary"):
            st.session_state.period = '12months'
            st.rerun()
    
    with col4:
        if st.button("Ostatnie 16 msc", use_container_width=True,
                    type="primary" if st.session_state.period == '16months' else "secondary"):
            st.session_state.period = '16months'
            st.rerun()
    
    # Filtruj dane
    filtered_data, aggregation = filter_data_by_period(data, st.session_state.period)
    
    # Własny zakres dat
    st.markdown("### 🗓️ Lub wybierz własny zakres")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        start_date = st.date_input("Data początkowa", value=filtered_data['date'].min())
    with col2:
        end_date = st.date_input("Data końcowa", value=filtered_data['date'].max())
    with col3:
        custom_agg = st.selectbox("Agregacja", ["Dziennie", "Miesięcznie"])
    
    if st.button("Zastosuj własny zakres"):
        filtered_data = data[(data['date'] >= pd.Timestamp(start_date)) & 
                            (data['date'] <= pd.Timestamp(end_date))]
        if custom_agg == "Miesięcznie":
            filtered_data = aggregate_by_month(filtered_data)
        aggregation = 'day' if custom_agg == "Dziennie" else 'month'
    
    st.divider()
    
    # Metryki
    total_clicks = int(filtered_data['clicks'].sum())
    total_impressions = int(filtered_data['impressions'].sum())
    avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    avg_position = filtered_data['position'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🖱️ Kliknięcia w okresie",
            value=f"{total_clicks:,}",
            delta="+12.5%"
        )
    
    with col2:
        st.metric(
            label="👁️ Wyświetlenia w okresie",
            value=f"{total_impressions:,}",
            delta="+8.3%"
        )
    
    with col3:
        st.metric(
            label="📈 Średnie CTR",
            value=f"{avg_ctr:.2f}%",
            delta="+5.2%"
        )
    
    with col4:
        st.metric(
            label="📍 Średnia pozycja",
            value=f"{avg_position:.1f}",
            delta="-8.5%",
            delta_color="inverse"
        )
    
    st.divider()
    
    # Wykres: Ruch w czasie
    st.markdown(f"### 📊 Ruch w czasie ({'miesięcznie' if aggregation == 'month' else 'dziennie'})")
    
    fig_traffic = go.Figure()
    fig_traffic.add_trace(go.Scatter(
        x=filtered_data['date'],
        y=filtered_data['clicks'],
        name='Kliknięcia',
        line=dict(color='#3b82f6', width=3),
        yaxis='y'
    ))
    fig_traffic.add_trace(go.Scatter(
        x=filtered_data['date'],
        y=filtered_data['impressions'],
        name='Wyświetlenia',
        line=dict(color='#10b981', width=3),
        yaxis='y2'
    ))
    
    fig_traffic.update_layout(
        height=400,
        hovermode='x unified',
        yaxis=dict(title='Kliknięcia', side='left'),
        yaxis2=dict(title='Wyświetlenia', side='right', overlaying='y'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    st.plotly_chart(fig_traffic, use_container_width=True)
    
    # Wykres: CTR i Pozycja
    st.markdown(f"### 📈 CTR i Pozycja w czasie ({'miesięcznie' if aggregation == 'month' else 'dziennie'})")
    
    fig_metrics = go.Figure()
    fig_metrics.add_trace(go.Scatter(
        x=filtered_data['date'],
        y=filtered_data['ctr'],
        name='CTR (%)',
        line=dict(color='#f59e0b', width=3),
        yaxis='y'
    ))
    fig_metrics.add_trace(go.Scatter(
        x=filtered_data['date'],
        y=filtered_data['position'],
        name='Pozycja',
        line=dict(color='#ef4444', width=3),
        yaxis='y2'
    ))
    
    fig_metrics.update_layout(
        height=400,
        hovermode='x unified',
        yaxis=dict(title='CTR (%)', side='left'),
        yaxis2=dict(title='Pozycja (średnia)', side='right', overlaying='y', autorange='reversed'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    st.plotly_chart(fig_metrics, use_container_width=True)
    
    st.divider()
    
    # Sekcja z krajami i urządzeniami
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌍 Ruch według krajów")
        country_data = get_country_data()
        
        fig_countries = px.bar(
            country_data,
            x='clicks',
            y='country',
            orientation='h',
            color='clicks',
            color_continuous_scale='Blues',
            text='clicks'
        )
        fig_countries.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig_countries.update_layout(height=400, showlegend=False, xaxis_title='Kliknięcia')
        
        st.plotly_chart(fig_countries, use_container_width=True)
    
    with col2:
        st.markdown("### 📱 Ruch według urządzeń")
        device_data = get_device_data()
        
        fig_devices = px.pie(
            device_data,
            values='clicks',
            names='device',
            color_discrete_sequence=['#3b82f6', '#10b981', '#f59e0b']
        )
        fig_devices.update_traces(textposition='inside', textinfo='percent+label')
        fig_devices.update_layout(height=400)
        
        st.plotly_chart(fig_devices, use_container_width=True)
    
    st.divider()
    
    # Tabele
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔗 Najpopularniejsze strony")
        top_pages = get_top_pages()
        st.dataframe(
            top_pages.style.format({
                'clicks': '{:,}',
                'impressions': '{:,}',
                'ctr': '{:.2f}%',
                'position': '{:.1f}'
            }),
            hide_index=True,
            use_container_width=True,
            height=400
        )
    
    with col2:
        st.markdown("### 🔍 Najpopularniejsze zapytania")
        top_queries = get_top_queries()
        st.dataframe(
            top_queries.style.format({
                'clicks': '{:,}',
                'impressions': '{:,}',
                'ctr': '{:.2f}%',
                'position': '{:.1f}'
            }),
            hide_index=True,
            use_container_width=True,
            height=400
        )
    
    # Sidebar z dodatkowymi opcjami
    with st.sidebar:
        st.markdown("### ⚙️ Opcje")
        st.markdown(f"**Aktualny okres:** {st.session_state.period}")
        st.markdown(f"**Agregacja:** {aggregation}")
        
        st.divider()
        
        if st.button("🔄 Odśwież dane", use_container_width=True):
            st.rerun()
        
        if st.button("🚪 Wyloguj", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.selected_site = None
            st.rerun()
        
        st.divider()
        st.caption("📊 Google Search Console Dashboard")
        st.caption("Wersja 1.0 - Streamlit")
