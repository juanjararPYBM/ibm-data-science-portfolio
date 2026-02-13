# ============================================================
# LAB MÓDULO 1 - VERSIÓN HEALTH
# Dataset: Medical Appointment No Shows
# Objetivo: Exploración inicial de datos médicos
# ============================================================
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
import pandas as pd

import numpy as np

# Cargar el dataset
df = pd.read_csv(r'C:\Users\user\OneDrive\Desktop\VScode\Curso python\KaggleV2-May-2016.csv')


# 1. PRIMER VISTAZO (como el lab de IBM)
print("=" * 50)
print("1. FORMA DEL DATASET")
print("=" * 50)
print(f"Filas: {df.shape[0]}")
print(f"Columnas: {df.shape[1]}")

print("\n" + "=" * 50)
print("2. PRIMERAS 5 FILAS")
print("=" * 50)
print(df.head())

print("\n" + "=" * 50)
print("3. INFORMACIÓN DE COLUMNAS")
print("=" * 50)
print(df.info())

print("\n" + "=" * 50)
print("4. ESTADÍSTICAS BÁSICAS")
print("=" * 50)
resumen = df.describe()
print(resumen[['Age', 'Scholarship','Hipertension','Diabetes','Alcoholism','SMS_received']])
nulos= df.isnull().sum()        # cuántos nulos por columna
nulosPER= df.isna().mean() * 100   # porcentaje de nulos
print(nulos)
print(nulosPER)
