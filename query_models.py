import psycopg2

def conectar_banco():
    """Cria uma conexão com o banco de dados PostgreSQL."""
    return psycopg2.connect(
        dbname="ml_experimentos",
        user="postgres",
        password="1515",
        host="localhost",
        port="5432"
    )

def listar_modelos():
    """Lista todos os modelos armazenados no banco."""
    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute("SELECT nome_modelo, metrica FROM modelos_ml;")
    modelos = cur.fetchall()
    conn.close()
    
    print("\nModelos armazenados no banco:")
    for modelo in modelos:
        print(f"Modelo: {modelo[0]} - Métrica: {modelo[1]}")

def melhor_modelo_classificacao():
    """Retorna o modelo de classificação com a maior acurácia."""
    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute("""
        SELECT nome_modelo, metrica FROM modelos_ml 
        WHERE metrica = (SELECT MAX(metrica) FROM modelos_ml);
    """)
    melhor_modelo = cur.fetchone()
    conn.close()
    
    if melhor_modelo:
        print(f"\nMelhor modelo de classificação: {melhor_modelo[0]} - Acurácia: {melhor_modelo[1]}")
    else:
        print("\nNenhum modelo encontrado.")

def melhor_modelo_regressao():
    """Retorna o modelo de regressão com menor RMSE."""
    conn = conectar_banco()
    cur = conn.cursor()
    cur.execute("""
        SELECT nome_modelo, metrica FROM modelos_ml 
        ORDER BY metrica ASC LIMIT 1;
    """)
    melhor_modelo = cur.fetchone()
    conn.close()
    
    if melhor_modelo:
        print(f"\nMelhor modelo de regressão: {melhor_modelo[0]} - RMSE: {melhor_modelo[1]}")
    else:
        print("\nNenhum modelo encontrado.")

if __name__ == "__main__":
    listar_modelos()
    melhor_modelo_classificacao()
    melhor_modelo_regressao()