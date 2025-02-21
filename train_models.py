import pandas as pd
import pickle
import joblib
import psycopg2
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
from preprocessing import carregar_dados, preprocessar_dados, dividir_dados

# Conectar ao banco de dados PostgreSQL
def conectar_banco():
    return psycopg2.connect(
        dbname="ml_experimentos",
        user="postgres",
        password="1515",
        host="localhost",
        port="5432"
    )

# Salvar modelo no banco de dados
def salvar_modelo_no_banco(nome, modelo, metrica):
    conn = conectar_banco()
    cur = conn.cursor()
    
    # Serializar modelo para salvar no banco
    modelo_serializado = pickle.dumps(modelo)
    
    # Inserir no banco
    cur.execute("""
        INSERT INTO modelos_ml (nome_modelo, modelo_serializado, metrica)
        VALUES (%s, %s, %s)
    """, (nome, modelo_serializado, metrica))
    
    conn.commit()
    cur.close()
    conn.close()

# Treinar modelo de classificação
def treinar_classificacao():
    df = carregar_dados("iris")
    X, y = preprocessar_dados(df, scaling_method="standard")
    X_train, X_val, X_test, y_train, y_val, y_test = dividir_dados(X, y)

    # Modelos de classificação
    modelos = {
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
        "SVM": SVC(kernel='linear', random_state=42)
    }

    for nome, modelo in modelos.items():
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)
        acuracia = accuracy_score(y_test, y_pred)
        print(f"{nome} - Acurácia: {acuracia:.4f}")

        # Salvar no banco
        salvar_modelo_no_banco(nome, modelo, acuracia)

        # Salvar em arquivo .pkl
        joblib.dump(modelo, f"{nome.lower()}_model.pkl")
        print(f"Modelo {nome} salvo como {nome.lower()}_model.pkl")

# Treinar modelo de regressão
def treinar_regressao():
    df = carregar_dados("california_housing")
    X, y = preprocessar_dados(df, scaling_method="standard")
    X_train, X_val, X_test, y_train, y_val, y_test = dividir_dados(X, y)

    # Modelos de regressão
    modelos = {
        "LinearRegression": LinearRegression(),
        "XGBoost": XGBRegressor(objective="reg:squarederror", n_estimators=100)
    }

    for nome, modelo in modelos.items():
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"{nome} - MSE: {mse:.4f}")

        # Salvar no banco
        salvar_modelo_no_banco(nome, modelo, mse)

        # Salvar em arquivo .pkl
        joblib.dump(modelo, f"{nome.lower()}_model.pkl")
        print(f"Modelo {nome} salvo como {nome.lower()}_model.pkl")

if __name__ == "__main__":
    print("Treinando modelos de classificação...")
    treinar_classificacao()

    print("\nTreinando modelos de regressão...")
    treinar_regressao()
