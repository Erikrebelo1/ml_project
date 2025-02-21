import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from evaluate_models import avaliar_classificacao, avaliar_regressao
from io import StringIO
import sys

def capturar_saida(func):
    """Executa uma função e captura sua saída do console."""
    buffer = StringIO()
    sys.stdout = buffer
    func()
    sys.stdout = sys.__stdout__
    return buffer.getvalue()

def extrair_metricas(saida):
    """Extrai métricas da saída do console e retorna um dicionário."""
    metricas = []
    linhas = saida.strip().split('\n')
    for linha in linhas:
        partes = linha.split(" - ")
        if len(partes) == 2:
            nome, valor = partes[0], partes[1]
            valores = [float(x.split(": ")[1]) for x in valor.split(", ")]
            metricas.append([nome] + valores)
    return metricas

def gerar_relatorio():
    """Gera relatório comparativo de modelos de ML."""
    print("Gerando relatório comparativo...")
    
    # Capturar e processar métricas dos modelos
    classificacao_saida = capturar_saida(avaliar_classificacao)
    regressao_saida = capturar_saida(avaliar_regressao)
    
    classificacao_metricas = extrair_metricas(classificacao_saida)
    regressao_metricas = extrair_metricas(regressao_saida)
    
    df_classificacao = pd.DataFrame(classificacao_metricas, columns=["Modelo", "Acurácia"])
    df_regressao = pd.DataFrame(regressao_metricas, columns=["Modelo", "RMSE", "R²"])
    
    print("\nTabela de Classificação:")
    print(df_classificacao)
    print("\nTabela de Regressão:")
    print(df_regressao)
    
    # Criar gráficos comparativos
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    sns.barplot(x="Acurácia", y="Modelo", data=df_classificacao, hue="Modelo", palette="Blues_r", legend=False)

    plt.title("Comparação de Acurácia - Classificação")
    
    plt.subplot(1, 2, 2)
    df_regressao_melt = df_regressao.melt(id_vars=["Modelo"], var_name="Métrica", value_name="Valor")
    sns.barplot(x="Valor", y="Modelo", hue="Métrica", data=df_regressao_melt, palette="coolwarm")
    plt.title("Comparação de RMSE e R² - Regressão")
    
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    gerar_relatorio()