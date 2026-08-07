#!/usr/bin/env python3
"""
Modelo de suscripción (underwriting) para flipping — Valle de Aburrá.

Lee flipping/data/listados.csv, calcula el precio por m² de cada inmueble contra
la mediana de su zona, y descarta lo que no deja margen después de costos reales.

Premisa del estudio: con tope de compra de 150M en el Valle de Aburrá, el margen
NO puede venir de la remodelación — tiene que venir de comprar por debajo de
mercado. Por eso el ranking es por DESCUENTO, no por precio absoluto.

Uso:
    python tamizaje.py --obra-m2 800000 --margen 0.13
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"
CSV_ENTRADA = DATA_DIR / "listados.csv"
CSV_SALIDA = DATA_DIR / "candidatos.csv"

# Costos de transacción reales en Colombia 2026 (ver README §Costos).
COSTO_COMPRA = 0.023   # registro + beneficencia (1,7-2,0%) + mitad de notariales (0,27%)
COSTO_VENTA = 0.0427   # comisión 3% + retención en la fuente 1% + mitad notariales 0,27%

# Mediana de $/m² por municipio — respaldo cuando no hay muestra propia suficiente.
# Fuente: Habi / Lonja de Medellín y Antioquia, 2026.
MEDIANA_REFERENCIA = {
    "medellin": 6_700_000,
    "envigado": 6_200_000,
    "sabaneta": 5_800_000,
    "itagui": 4_900_000,
    "la estrella": 4_913_000,
    "bello": 4_100_000,
    "caldas": 3_738_000,
    "copacabana": 3_559_000,
    "girardota": 3_480_000,
    "barbosa": 3_300_000,
}

MUESTRA_MINIMA = 5  # listados necesarios para confiar en una mediana propia


def compra_maxima(reventa, obra, margen):
    """
    Precio máximo de compra que todavía deja el margen objetivo.

    Inversión  = P·(1+c_compra) + Obra
    Neto venta = R·(1−c_venta)
    Exigimos:    Neto ≥ Inversión·(1+margen)

        P ≤ [ R·(1−c_venta)/(1+margen) − Obra ] / (1+c_compra)
    """
    return (reventa * (1 - COSTO_VENTA) / (1 + margen) - obra) / (1 + COSTO_COMPRA)


def medianas_por_zona(df, usar_propia):
    """
    Mediana de $/m² por municipio.

    Por defecto usa la referencia de mercado (Lonja/Habi), NO la muestra propia.

    Razón — sesgo de selección: el scraper filtra listados a ≤150M, así que la
    muestra está recortada por abajo y su mediana queda por debajo de la mediana
    real del mercado. Calcular el descuento contra esa mediana sesgada lo
    subestima sistemáticamente, y hace parecer caro un inmueble que sí está
    barato. La referencia externa no tiene ese recorte.

    --mediana-propia solo es válido si se rastreó SIN tope de precio.
    """
    propias = df.groupby("municipio_norm")["precio_m2"].agg(["median", "count"])
    medianas = {}

    for municipio, fila in propias.iterrows():
        clave = str(municipio).strip().lower()
        n = int(fila["count"])

        if usar_propia and n >= MUESTRA_MINIMA:
            medianas[clave] = (fila["median"], f"muestra propia (n={n})")
        elif clave in MEDIANA_REFERENCIA:
            medianas[clave] = (MEDIANA_REFERENCIA[clave], "referencia de mercado")
        elif n >= MUESTRA_MINIMA:
            medianas[clave] = (fila["median"], f"⚠ muestra propia sesgada (n={n})")
        else:
            medianas[clave] = (None, f"sin referencia (n={n})")

    return medianas


def main():
    ap = argparse.ArgumentParser(description="Tamizaje de candidatos para flipping")
    ap.add_argument("--obra-m2", type=int, default=800_000,
                    help="Costo de remodelación por m². Cosmética 500-800k, integral 800k-1.5M")
    ap.add_argument("--margen", type=float, default=0.13,
                    help="Margen neto objetivo sobre la inversión total (0.13 = 13%%)")
    ap.add_argument("--uplift", type=float, default=0.0,
                    help="Sobreprecio sobre la mediana tras remodelar (0.10 = 10%%). "
                         "Conservador: 0. La mediana ya refleja inmuebles en buen estado.")
    ap.add_argument("--tope-compra", type=int, default=150_000_000,
                    help="Presupuesto máximo de compra. Descarta lo que no alcanza.")
    ap.add_argument("--mediana-propia", action="store_true",
                    help="Usar la mediana de la muestra rastreada en vez de la referencia. "
                         "SOLO válido si se rastreó sin tope de precio (ver docstring).")
    ap.add_argument("--top", type=int, default=25)
    args = ap.parse_args()

    if not CSV_ENTRADA.exists():
        print(f"No existe {CSV_ENTRADA}. Corre primero scraper.py.")
        return 1

    df = pd.read_csv(CSV_ENTRADA)
    df = df.dropna(subset=["precio", "area_m2"])
    df = df[(df["area_m2"] > 15) & (df["area_m2"] < 400)]  # descarta parqueaderos y errores
    df = df[df["precio"] > 20_000_000]

    if df.empty:
        print("Sin listados válidos tras el filtrado.")
        return 1

    df["precio_m2"] = df["precio"] / df["area_m2"]
    df["municipio_norm"] = df["municipio"].astype(str).str.strip().str.lower()

    medianas = medianas_por_zona(df, args.mediana_propia)
    df["mediana_zona"] = df["municipio_norm"].map(lambda m: medianas.get(m, (None, ""))[0])
    df["origen_mediana"] = df["municipio_norm"].map(lambda m: medianas.get(m, (None, ""))[1])
    df = df.dropna(subset=["mediana_zona"])

    # El presupuesto es una restricción dura: lo que no alcanza, no es candidato.
    sobre_presupuesto = int((df["precio"] > args.tope_compra).sum())
    df = df[df["precio"] <= args.tope_compra]
    if df.empty:
        print(f"Ningún listado por debajo del tope de ${args.tope_compra:,}.")
        return 1

    # Valoración
    df["valor_mercado"] = df["area_m2"] * df["mediana_zona"]
    df["descuento"] = 1 - (df["precio"] / df["valor_mercado"])
    df["costo_obra"] = df["area_m2"] * args.obra_m2
    df["reventa_esperada"] = df["valor_mercado"] * (1 + args.uplift)
    df["compra_max"] = compra_maxima(df["reventa_esperada"], df["costo_obra"], args.margen)
    df["holgura"] = df["compra_max"] - df["precio"]
    df["viable"] = df["holgura"] > 0

    # Margen real que dejaría comprando al precio de lista
    inversion = df["precio"] * (1 + COSTO_COMPRA) + df["costo_obra"]
    neto = df["reventa_esperada"] * (1 - COSTO_VENTA)
    df["margen_real"] = (neto - inversion) / inversion

    df = df.sort_values("descuento", ascending=False)

    # --- Informe ---
    print(f"\n{'='*74}")
    print(f"TAMIZAJE — obra ${args.obra_m2:,}/m² · margen objetivo {args.margen:.0%}"
          f" · uplift {args.uplift:.0%}")
    print(f"{'='*74}\n")

    print(f"Listados analizados : {len(df)}  (tope ${args.tope_compra:,})")
    print(f"Sobre presupuesto   : {sobre_presupuesto} descartados")
    print(f"Viables             : {int(df['viable'].sum())} "
          f"({df['viable'].mean():.0%})\n")

    print("Mediana $/m² por municipio:")
    for municipio, (valor, origen) in sorted(medianas.items()):
        print(f"  {municipio:<16} ${valor:>12,.0f}   [{origen}]")

    viables = df[df["viable"]].head(args.top)

    if viables.empty:
        print("\n" + "-" * 74)
        print("NINGÚN CANDIDATO VIABLE en el mercado abierto.")
        print("-" * 74)
        print("Es el resultado esperado, no un fallo del modelo: a precio de lista")
        print("los portales no dejan margen tras costos. El margen está en comprar")
        print("bajo mercado — remates y daciones en pago. Ver README §Canales.\n")
        print(f"Mejores descuentos observados (aún insuficientes):\n")
        muestra = df.head(10)
    else:
        print(f"\n{'-'*74}")
        print(f"TOP {len(viables)} CANDIDATOS (ordenados por descuento)")
        print(f"{'-'*74}\n")
        muestra = viables

    for _, r in muestra.iterrows():
        print(f"  ${r['precio']:>12,.0f}  {r['area_m2']:>5.0f} m²  "
              f"${r['precio_m2']:>10,.0f}/m²  {r['municipio']:<12} "
              f"desc {r['descuento']:>6.1%}  margen {r['margen_real']:>6.1%}")
        if r["titulo"]:
            print(f"      {str(r['titulo'])[:70]}")
        if isinstance(r["url"], str) and r["url"]:
            print(f"      {r['url']}")
        print()

    columnas = ["fuente", "municipio", "sector", "precio", "area_m2", "precio_m2",
                "mediana_zona", "valor_mercado", "descuento", "costo_obra",
                "compra_max", "holgura", "margen_real", "viable", "url", "titulo"]
    df[columnas].to_csv(CSV_SALIDA, index=False)
    print(f"Detalle completo → {CSV_SALIDA}")

    print("\nRecordatorio: el descuento es una señal, no una conclusión. Antes de")
    print("ofertar hay que verificar certificado de tradición, paz y salvo de")
    print("administración y predial, y estado real del inmueble.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
