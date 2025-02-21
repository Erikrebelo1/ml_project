import pandas as pd
from sklearn.datasets import load_iris, load_breast_cancer, fetch_california_housing

# Função para carregar e pré-processar o dataset
def carregar_dados(dataset_name="iris"):
    if dataset_name == "iris":
        data = load_iris()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df['target'] = data.target
    elif dataset_name == "breast_cancer":
        data = load_breast_cancer()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df['target'] = data.target
    elif dataset_name == "california_housing":  # Suporte para "California Housing"
        data = fetch_california_housing(as_frame=True)
        df = data.frame
        # Renomeia a coluna alvo para "target" para padronizar com os demais datasets
        df = df.rename(columns={"MedHouseVal": "target"})
    else:
        raise ValueError("Dataset não reconhecido")
    
    return df

# Função para pré-processar os dados (exemplo: normalização ou padronização)
def preprocessar_dados(df, scaling_method="standard"):
    X = df.drop('target', axis=1)
    y = df['target']
    
    if scaling_method == "standard":
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
    
    return X, y

# Função para dividir os dados em treinamento, validação e teste
def dividir_dados(X, y, test_size=0.2, val_size=0.1):
    from sklearn.model_selection import train_test_split
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=test_size, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=val_size / (1 - test_size), random_state=42)
    return X_train, X_val, X_test, y_train, y_val, y_test

if __name__ == "__main__":
    # Exemplo de uso:
    df = carregar_dados("california_housing")
    print("Colunas do dataset:", df.columns.tolist())