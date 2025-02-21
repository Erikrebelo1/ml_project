import psycopg2

# Configurações do banco
DB_HOST = "localhost"
DB_NAME = "ml_experimentos"
DB_USER = "postgres"
DB_PASSWORD = "1515"  # minha sena senha do PostgreSQL

def conectar():
    """Estabelece a conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("✅ Conexão bem-sucedida!")
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return None

# Testando a conexão 
if __name__ == "__main__":
    conn = conectar()
    if conn:
        conn.close()
