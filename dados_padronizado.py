import pandas as pd
import numpy as np

# Carrega a planilha
df = pd.read_excel("Base_despadronizada.xlsx", dtype=str)

# Padroniza a coluna "sexo"
sexo_map = {
    'm': 'Masculino', 'masc': 'Masculino', 'masculino': 'Masculino',
    'f': 'Feminino', 'fem': 'Feminino', 'feminino': 'Feminino'
}
df['sexo'] = df['sexo'].str.lower().map(sexo_map)

# Função para corrigir notas 
def corrigir_nota(valor):
    if pd.isna(valor):
        return np.nan

    if isinstance(valor, pd.Timestamp):
        return float(f"{valor.month}.{valor.day}")

    try:
        data = pd.to_datetime(valor, errors='coerce', dayfirst=True)
        if not pd.isna(data):
            return float(f"{data.month}.{data.day}")
    except:
        pass

    try:
        return float(str(valor).replace(",", "."))
    except:
        return np.nan

# Aplicar correção nas colunas de notas
df['nota_matematica'] = df['nota_matematica'].apply(corrigir_nota)
df['nota_portugues'] = df['nota_portugues'].apply(corrigir_nota)
df['frequencia'] = pd.to_numeric(df['frequencia'], errors='coerce')

# Calcular a média
df['media'] = (df['nota_matematica'] + df['nota_portugues'] + (df['frequencia'] / 10)) / 3

# Criar a coluna "aprovado"
df['aprovado'] = df['media'].apply(lambda x: 'Sim' if x >= 7 else 'Não')

# Arredondar as notas para uma casa decimal
df['nota_matematica'] = df['nota_matematica'].round(1)
df['nota_portugues'] = df['nota_portugues'].round(1)
df['media'] = df['media'].round(2)

# Salvar o resultado criando um novo arquivo xlsx 
print(df['aprovado'].value_counts(normalize=True) * 100)

#df.to_excel("Base_Padronizada_Completa.xlsx", index=False)
