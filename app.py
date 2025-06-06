import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Definir o título do app
st.header('Análise Financeira')

# Carregar o dataset
df = pd.read_csv('MS_FinancialSample.csv', delimiter=';')

# Limpar os nomes das colunas removendo espaços
df.columns = df.columns.str.strip()

# Limpeza dos dados na coluna 'Sales'
df['Sales'] = df['Sales'].astype(str)
df['Sales'] = df['Sales'].replace({'\$': '', '\.': ''}, regex=True)
df['Sales'] = df['Sales'].str.replace(',', '.')
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')

# Agrupando os dados por país e segmento
seg_by_country = df.groupby(['Country', 'Segment'])['Sales'].sum().reset_index()

# Criando o gráfico
plt.figure(figsize=(10, 6))  # Tamanho da figura

# Plotando as barras para cada segmento
for i, segment in enumerate(seg_by_country['Segment'].unique()):
    segment_data = seg_by_country[seg_by_country['Segment'] == segment]
    plt.bar(segment_data['Country'] + ' ' + segment, segment_data['Sales'], label=segment)

# Títulos e labels
plt.title('Total Vendas por País e Segmento', fontsize=16)
plt.xlabel('País e Segmento', fontsize=12)
plt.ylabel('Total Vendas ( USD)', fontsize=12)
plt.xticks(rotation=90)  # Rotaciona os labels do eixo X para melhorar a leitura

# Formatação monetária no eixo Y
formatter = FuncFormatter(lambda x, pos: f'${x:,.0f}')
plt.gca().yaxis.set_major_formatter(formatter)

# Ajuste do layout para não cortar as labels
plt.tight_layout()

# Ajustar limites do eixo Y
y_max = seg_by_country['Sales'].max()  # Valor máximo da coluna de vendas
y_min = 0  # Definir valor mínimo (pode ser ajustado conforme necessário)
plt.ylim(y_min, y_max * 1.1)  # Aumenta o limite superior em 10% para dar uma margem visual

# Legenda
plt.legend(title='Segment')

# Exibindo o gráfico no Streamlit
st.pyplot(plt)