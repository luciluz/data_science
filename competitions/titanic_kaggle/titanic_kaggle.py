#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sobrevivientes del Titanic

@author: luci
"""
#%%
import pandas as pd
import numpy as np
#%%
# Cargamos datos
df_train = pd.read_csv("train.csv")
df_test = pd.read_csv("test.csv")

# este se guarda para la predicción
test_ids = df_test['PassengerId']
#%%
## Procesamiento de la data

# Cambio los datos de sexo por números
df_train['Sex'].replace(['female','male'],[0,1],inplace=True)
df_test['Sex'].replace(['female','male'],[0,1],inplace=True)

# Cambio datos de embarque en números
df_train['Embarked'].replace(['Q','S','C'],[0,1,2],inplace=True)
df_test['Embarked'].replace(['Q','S','C'],[0,1,2],inplace=True)

# Reemplazo datos faltantes en edad por su media
print(df_train['Age'].mean())
print(df_test['Age'].mean())
promedio = 30
df_train['Age'] = df_train['Age'].replace(np.nan , promedio)
df_test['Age'] = df_test['Age'].replace(np.nan , promedio)
#%%
# Valor faltante solo en Fare del pasajero 1044
# le ponemos 10 ya que es de tercera clase
df_test.loc[df_test['PassengerId'] == 1044, 'Fare'] = 10

# Buscar la fila correspondiente al pasajero con PassengerId 1044
passenger_1044 = df_test.loc[df_test['PassengerId'] == 1044]

# Imprimir la fila
print(passenger_1044)
#%%
# Creo grupos de edad
bins = [0, 8, 15, 18, 25, 40, 60, 100]
names = [1, 2, 3, 4, 5, 6, 7]
df_train['Age'] = pd.cut(df_train['Age'], bins, labels = names)
df_test['Age'] = pd.cut(df_test['Age'], bins, labels = names)

# Creo grupos en Fare
bins = [0,10,30,50,100,600]
names = [1, 2, 3, 4, 5]
df_train['Fare'] = pd.cut(df_train['Fare'], bins, labels = names)
df_test['Fare'] = pd.cut(df_train['Fare'], bins, labels = names)

# Se elimina columna Cabin porque tiene muchos datos perdidos
df_train.drop(['Cabin'], axis=1, inplace=True)
df_test.drop(['Cabin'], axis=1, inplace=True)

# Elimino columnas innecesarias
df_train = df_train.drop(['PassengerId','Name','Ticket'], axis=1)
df_test = df_test.drop(['PassengerId','Name','Ticket'], axis=1)

# Se eliminan las filas con datos faltantes (sólo en train)
df_train.dropna(axis=0, how='any', inplace=True)

# Verifico los datos
print(pd.isnull(df_train).sum())
print(pd.isnull(df_test).sum())

print(df_train.shape)
print(df_test.shape)

print(df_train.head())
print(df_test.head())

#%% Algoritmos de ML

# Divido conjunto de datos en conjunto de entrenamiento y pruebas
from sklearn.model_selection import train_test_split
y = df_train['Survived']
X = df_train.drop(['Survived'], axis=1)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

## Regresión Logística
from sklearn.linear_model import LogisticRegression

clf = LogisticRegression(random_state=0, max_iter=1000).fit(X_train, y_train)

predictions = clf.predict(X_val)
from sklearn.metrics import accuracy_score
res_rl = round(accuracy_score(y_val, predictions),2)
print('Precisión Regresión Logística:')
print(res_rl)

## K Neighbors
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors= 3)
knn.fit(X_train, y_train)
Y_pred = knn.predict(X_val)
res_knn = round(knn.score(X_train, y_train),2)
print('Precisión vecinos más cercanos')
print(res_knn)

## Árbol de decisión
from sklearn.tree import DecisionTreeClassifier

# Inicializar y ajustar el modelo de árbol de decisión
tree_model = DecisionTreeClassifier(random_state=42)
tree_model.fit(X_train, y_train)

# Realizar predicciones en el conjunto de prueba
predictions = tree_model.predict(X_val)

# Evaluar la precisión del modelo
res_tree = round(accuracy_score(y_val, predictions),2)
print('Precisión del modelo de árbol de decisión:')
print(res_tree)

#%%
# Creo tabla con los rendimientos
dicc = [{'Algoritmo': 'Regresión Logística', 'Precisión': res_rl},
        {'Algoritmo': 'K nearest neighbors', 'Precisión': res_knn},
        {'Algoritmo': 'Árbol de decisión', 'Precisión': res_tree}]
rendimientos = pd.DataFrame(dicc)
print(rendimientos)
