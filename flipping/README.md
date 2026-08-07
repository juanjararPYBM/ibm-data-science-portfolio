# 🏘️ Estudio de Mercado — Flipping Inmobiliario Valle de Aburrá

> **Contexto para una sesión local de Claude Code.** Este archivo lleva todo el análisis
> ya construido para que no haya que repetirlo. Ábrelo primero.
>
> Generado: 2026-08-07 · Presupuesto objetivo: **150M COP solo compra**

---

## 🎯 El encargo

Juan busca su primer *flip*: comprar un inmueble por debajo de mercado, remodelar y revender.
Presupuesto de compra: **150.000.000 COP** (el capital de obra va aparte).
Zona: **Medellín / Valle de Aburrá**. Tipo: apartamento usado, y remate/bancario.

---

## 📊 Lo que ya se estableció

### Precio por m² (venta, 2026)

| Zona | $/m² | Qué compras con 150M |
|---|---|---|
| Medellín (mediana) | 6.700.000 | 22 m² |
| Medellín decil bajo (Robledo, Castilla, Manrique) | ~3.900.000 | 38 m² |
| La Estrella | 4.913.000 | 31 m² |
| Caldas | 3.738.000 | 40 m² |
| Copacabana | 3.559.000 | 42 m² |
| Girardota | 3.480.000 | 43 m² |

Mediana Valle de Aburrá: **3.905.405 $/m²**.
Bello: promedio de listados **330M**, entrada en **135M**.
Camacol Antioquia: el m² creció **12–16%** en estratos medios durante 2025.

### Costos de transacción (ciclo completo)

| Concepto | Quién paga | Tasa |
|---|---|---|
| Derechos notariales | Repartido | ~0,54% |
| Registro + beneficencia | Comprador | 1,7 – 2,0% |
| Retención en la fuente | Vendedor | 1,0% del valor de venta |
| Comisión inmobiliaria | Vendedor | ~3,0% |

**Fricción total del ciclo: ~6–7%.**

### ⚠️ La conclusión que define la estrategia

Con margen objetivo de 13% y fricción de 7%, la regla de compra queda:

```
Compra máxima = (Precio de reventa × 0,80) − Costo de obra
```

Comprando a 150M con 25M de obra, hay que **revender en ~219M**.
En Bello/Copacabana eso son **56–62 m²** — pero 150M en esa misma zona compran **38–43 m²**.

**Los metros no cuadran.** Con este presupuesto el margen **no puede venir de la remodelación**:
tiene que venir de **comprar 25–30% por debajo de mercado**. Es decir, remates y daciones en pago.
La remodelación es el complemento, no el motor.

---

## 🔍 Canales prioritarios

### Remate y dación (donde está el margen)

| Canal | URL |
|---|---|
| Banco Agrario — remates judiciales | https://www.bancoagrario.gov.co/remates-judiciales |
| CISA — activos del Estado | https://inmuebles.cisa.gov.co/PortalComercializacion/ |
| ColSubastas Antioquia | https://colsubastas.com/antioquia |
| Remates Colombia | https://rematescolombia.com/remates |
| Bancolombia Tu360 usados | https://inmobiliariotu360.bancolombia.com/usado |

**Mecánica del remate judicial:** base = **70% del avalúo** (ahí está el descuento estructural).
Para postular se consigna el **40% del avalúo** en la cuenta de depósitos judiciales del juzgado
(casi siempre Banco Agrario).

**Riesgos que hay que evaluar antes de postular:**
- Se compra **sin ver el interior**
- El inmueble puede estar **ocupado** → proceso de entrega/lanzamiento de meses o años, con el capital congelado
- Se heredan **administración y predial atrasados**

> Para un primer flip, la **dación en pago bancaria** (Tu360, Davivienda) es el punto medio sensato:
> menor descuento que el remate judicial, pero inmueble desocupado, escritura limpia y visita permitida.

### Portales comerciales (solo para comparables de precio/m²)

Fincaraíz · Metrocuadrado · MercadoLibre · Properati · Ciencuadras

---

## 🌐 Por qué esto se ejecuta en local

El contenedor remoto de Claude Code web tiene **egress restringido**: solo alcanza Anthropic,
GitHub y registros de paquetes. Todos los portales dan `EGRESS_BLOCKED`.

Además, los portales comerciales filtran por **reputación de IP**: bloquean rangos de datacenter
(Azure/AWS/GCP). Chromium vía Playwright ya produce una huella de navegador auténtica — lo único
que delata a un runner en la nube es la IP.

**Tu conexión residencial en Medellín resuelve ambas capas a la vez.** Por eso este toolkit
corre local.

---

## 🚀 Uso

```bash
# 1. Instalar dependencias (una sola vez)
pip install playwright pandas
playwright install chromium

# 2. Rastrear
python flipping/scraper.py --fuente fincaraiz --municipio medellin --max-precio 150000000
python flipping/scraper.py --fuente fincaraiz --municipio bello    --max-precio 150000000
python flipping/scraper.py --fuente mercadolibre --municipio copacabana --max-precio 150000000

# 3. Analizar y rankear candidatos
python flipping/tamizaje.py --obra-m2 800000 --margen 0.13
```

`scraper.py` acumula en `flipping/data/listados.csv`.
`tamizaje.py` lee ese CSV y produce `flipping/data/candidatos.csv` rankeado por descuento.

### ⚠️ Nota sobre el primer arranque

Este scraper **no pudo probarse** desde el contenedor remoto — los portales estaban bloqueados.
Es una v1 escrita a partir de la estructura conocida de cada sitio. Es probable que en la primera
corrida haga falta **ajustar selectores CSS**. Corre con `--debug` para volcar el HTML y afinar:

```bash
python flipping/scraper.py --fuente fincaraiz --municipio medellin --debug
```

Los portales cambian su maquetación con frecuencia; asume una ronda de ajuste, no un fallo.

### Higiene de rastreo

El scraper usa un User-Agent honesto, limita a ~1 petición cada 2,5 s y respeta paginación
acotada. **No incluye evasión de antibot** (rotación de proxies, spoofing de fingerprint,
resolución de CAPTCHAs) — eso viola los términos de servicio de los portales y crea exposición
legal. Desde una IP residencial no hace falta.

---

## 📌 Estado y siguiente paso

- [x] Análisis de mercado y precios por zona
- [x] Regla de tamizaje calibrada con costos reales
- [x] Canales de remate identificados
- [ ] **Rastreo real de listados** ← requiere sesión local
- [ ] Ranking de candidatos por descuento vs. mediana de zona
- [ ] Visitas y verificación jurídica (certificado de tradición, paz y salvo de administración)
