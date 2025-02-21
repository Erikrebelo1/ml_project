import joblib
import numpy as np
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
from preprocessing import carregar_dados, preprocessar_dados, dividir_dados

def avaliar_classificacao():
    print("Avaliando modelos de classificação...")
    df = carregar_dados("iris")  # Podemos mudar para outro dataset
    X, y = preprocessar_dados(df, scaling_method="standard")
    _, _, X_test, _, _, y_test = dividir_dados(X, y)
    
    modelos = {
        "RandomForest": joblib.load("randomforest_model.pkl"),
        "SVM": joblib.load("svm_model.pkl")
    }
    
    for nome, modelo in modelos.items():
        y_pred = modelo.predict(X_test)
        acuracia = accuracy_score(y_test, y_pred)
        print(f"{nome} - Acurácia: {acuracia:.4f}")

def avaliar_regressao():
    print("\nAvaliando modelos de regressão...")
    df = carregar_dados("california_housing")  # Podemos mudar para outro dataset
    X, y = preprocessar_dados(df, scaling_method="standard")
    _, _, X_test, _, _, y_test = dividir_dados(X, y)
    
    modelos = {
        "LinearRegression": joblib.load("linearregression_model.pkl"),
        "XGBoost": joblib.load("xgboost_model.pkl")
    }
    
    for nome, modelo in modelos.items():
        y_pred = modelo.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        print(f"{nome} - RMSE: {rmse:.4f}, R²: {r2:.4f}")

if __name__ == "__main__":
    avaliar_classificacao()
    avaliar_regressao()