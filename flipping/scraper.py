#!/usr/bin/env python3
"""
Rastreador de listados inmobiliarios — Valle de Aburrá.

Corre en local (IP residencial). Desde un contenedor en la nube los portales
bloquean por reputación de IP; ver flipping/README.md §Por qué esto se ejecuta en local.

Extracción por heurística de texto en vez de selectores CSS fijos: los portales
cambian su maquetación con frecuencia y los nombres de clase suelen ser hashes
generados. Buscar el patrón "precio + área" dentro de un contenedor sobrevive
mejor a esos cambios que un selector exacto.

Uso:
    python scraper.py --fuente fincaraiz --municipio medellin --max-precio 150000000
    python scraper.py --fuente fincaraiz --municipio bello --debug
"""

import argparse
import csv
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

DATA_DIR = Path(__file__).parent / "data"
CSV_PATH = DATA_DIR / "listados.csv"
CAMPOS = ["fuente", "municipio", "precio", "area_m2", "habitaciones",
          "banos", "sector", "url", "titulo"]

# User-Agent honesto: identifica un Chrome real, que es lo que efectivamente corre.
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

PAUSA_ENTRE_PAGINAS = 2.5  # segundos — cortesía con el servidor

FUENTES = {
    "fincaraiz": {
        "url": ("https://www.fincaraiz.com.co/apartamentos/venta/{municipio}/antioquia"
                "?precioDesde=0&precioHasta={max_precio}&pagina={pagina}"),
        "contenedor": "article, div[class*='listingCard'], div[class*='card']",
    },
    "mercadolibre": {
        "url": ("https://inmuebles.mercadolibre.com.co/apartamentos/venta/antioquia/"
                "{municipio}/_PriceRange_0COP-{max_precio}COP_Desde_{offset}"),
        "contenedor": "div.ui-search-result__wrapper, li.ui-search-layout__item",
    },
    "metrocuadrado": {
        "url": ("https://www.metrocuadrado.com/apartamento/venta/{municipio}/"
                "?search=form&precio=0-{max_precio}&currentPage={pagina}"),
        "contenedor": "div[class*='card'], article",
    },
}

# --- Extractores de campo -------------------------------------------------

RE_PRECIO = re.compile(r"\$\s*([\d][\d.,]{5,})")
RE_AREA = re.compile(r"(\d+(?:[.,]\d+)?)\s*m\s*(?:2|²|<sup>2)", re.I)
RE_HAB = re.compile(r"(\d+)\s*(?:hab|alcob|dormit|habitaci)", re.I)
RE_BANO = re.compile(r"(\d+)\s*ba(?:ñ|n)o", re.I)


def _a_entero(texto):
    """Convierte '150.000.000' o '150,000,000' a int. Formato colombiano: . como miles."""
    limpio = re.sub(r"[.,\s]", "", texto)
    return int(limpio) if limpio.isdigit() else None


def _a_decimal(texto):
    return float(texto.replace(",", "."))


def extraer_de_texto(texto):
    """Saca los campos numéricos del texto plano de una tarjeta de listado."""
    precio = None
    # El precio de venta es el número más alto: descarta administración y cuotas.
    candidatos = [_a_entero(m) for m in RE_PRECIO.findall(texto)]
    candidatos = [c for c in candidatos if c and c > 10_000_000]
    if candidatos:
        precio = max(candidatos)

    area = RE_AREA.search(texto)
    hab = RE_HAB.search(texto)
    bano = RE_BANO.search(texto)

    return {
        "precio": precio,
        "area_m2": _a_decimal(area.group(1)) if area else None,
        "habitaciones": int(hab.group(1)) if hab else None,
        "banos": int(bano.group(1)) if bano else None,
    }


def rastrear(fuente, municipio, max_precio, paginas, debug):
    cfg = FUENTES[fuente]
    resultados = []

    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=not debug)
        ctx = navegador.new_context(user_agent=UA, locale="es-CO",
                                    viewport={"width": 1440, "height": 2200})
        pagina = ctx.new_page()

        for n in range(1, paginas + 1):
            url = cfg["url"].format(municipio=municipio, max_precio=max_precio,
                                    pagina=n, offset=(n - 1) * 48 + 1)
            print(f"  [{n}/{paginas}] {url}")

            try:
                resp = pagina.goto(url, wait_until="domcontentloaded", timeout=60000)
                if resp and resp.status >= 400:
                    print(f"      HTTP {resp.status} — el portal rechazó la petición.")
                    if resp.status == 403:
                        print("      403 = bloqueo por antibot. ¿Estás en IP residencial?")
                    break
            except Exception as e:
                print(f"      Error de navegación: {type(e).__name__}")
                break

            pagina.wait_for_timeout(3500)
            # Scroll para disparar la carga diferida de tarjetas.
            for _ in range(8):
                pagina.mouse.wheel(0, 2500)
                pagina.wait_for_timeout(700)

            if debug:
                volcado = DATA_DIR / f"debug_{fuente}_{municipio}_p{n}.html"
                volcado.write_text(pagina.content(), encoding="utf-8")
                print(f"      HTML volcado en {volcado}")

            tarjetas = pagina.query_selector_all(cfg["contenedor"])
            encontradas = 0

            for tarjeta in tarjetas:
                try:
                    texto = tarjeta.inner_text()
                except Exception:
                    continue
                if not texto or "m" not in texto.lower():
                    continue

                campos = extraer_de_texto(texto)
                if not campos["precio"] or not campos["area_m2"]:
                    continue
                if campos["precio"] > max_precio:
                    continue

                enlace = tarjeta.query_selector("a[href]")
                href = enlace.get_attribute("href") if enlace else None
                if href and href.startswith("/"):
                    origen = re.match(r"https?://[^/]+", url).group(0)
                    href = origen + href

                lineas = [l.strip() for l in texto.split("\n") if l.strip()]
                resultados.append({
                    "fuente": fuente,
                    "municipio": municipio,
                    **campos,
                    "sector": next((l for l in lineas if not RE_PRECIO.search(l)
                                    and 3 < len(l) < 60), ""),
                    "url": href or "",
                    "titulo": lineas[0][:120] if lineas else "",
                })
                encontradas += 1

            print(f"      {encontradas} listados extraídos")
            if encontradas == 0:
                print("      Sin resultados: probablemente los selectores cambiaron.")
                print("      Corre con --debug y revisa el HTML volcado.")
                break

            time.sleep(PAUSA_ENTRE_PAGINAS)

        navegador.close()

    return resultados


def guardar(filas):
    """Añade al CSV acumulado, evitando duplicados por URL."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    vistos = set()

    if CSV_PATH.exists():
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            vistos = {r["url"] for r in csv.DictReader(f) if r.get("url")}

    nuevas = [f for f in filas if not f["url"] or f["url"] not in vistos]
    escribir_cabecera = not CSV_PATH.exists()

    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        if escribir_cabecera:
            w.writeheader()
        w.writerows(nuevas)

    return len(nuevas)


def main():
    ap = argparse.ArgumentParser(description="Rastreador de listados — Valle de Aburrá")
    ap.add_argument("--fuente", required=True, choices=sorted(FUENTES))
    ap.add_argument("--municipio", required=True,
                    help="medellin, bello, itagui, envigado, copacabana, girardota, caldas...")
    ap.add_argument("--max-precio", type=int, default=150_000_000)
    ap.add_argument("--paginas", type=int, default=5)
    ap.add_argument("--debug", action="store_true",
                    help="Navegador visible y volcado de HTML para ajustar selectores")
    args = ap.parse_args()

    print(f"\nRastreando {args.fuente} · {args.municipio} · tope ${args.max_precio:,}\n")
    filas = rastrear(args.fuente, args.municipio, args.max_precio,
                     args.paginas, args.debug)

    if not filas:
        print("\nNo se extrajo nada. Revisa el diagnóstico de arriba.")
        return 1

    nuevas = guardar(filas)
    print(f"\n{len(filas)} listados extraídos · {nuevas} nuevos → {CSV_PATH}")
    print("Siguiente paso: python flipping/tamizaje.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
