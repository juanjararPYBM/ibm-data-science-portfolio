#!/usr/bin/env python3
"""
token_analytics/daily_close.py

Cierre contable diario automático — Token Analytics / Hipócrates MCP
Ejecución: 12:00am COT (UTC-5) via Windows Task Scheduler

Flujo:
  1. Lee deepseek_log.csv y filtra entradas del día
  2. Calcula totales: tokens, costos, ahorro vs Claude
  3. Lee TOKEN_LOG.md desde GitHub API
  4. Agrega sección CIERRE CONTABLE al final
  5. Pushea TOKEN_LOG.md actualizado a GitHub
  6. Registra en daily_close.log
"""

import os
import sys
import csv
import base64
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Tuple
import requests

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
REPO_OWNER      = "juanjararPYBM"
REPO_NAME       = "ibm-data-science-portfolio"
TOKEN_LOG_PATH  = "TOKEN_LOG.md"
DEEPSEEK_LOG    = Path(__file__).parent / "deepseek_log.csv"
LOG_FILE        = Path(__file__).parent / "daily_close.log"

# Costos por 1K tokens (USD)
CLAUDE_INPUT_PER_1K   = 0.003
CLAUDE_OUTPUT_PER_1K  = 0.015
DEEPSEEK_INPUT_PER_1K = 0.00014
DEEPSEEK_OUT_PER_1K   = 0.00028

# ─── LOGGING ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger(__name__)


class DailyClose:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        if not self.github_token:
            log.error("GITHUB_TOKEN no encontrado en variables de entorno")
            sys.exit(1)

        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        # Fecha actual en hora Colombia (UTC-5)
        self.now_cot   = datetime.utcnow() - timedelta(hours=5)
        self.today_str = self.now_cot.strftime("%Y-%m-%d")
        self.day_start = datetime(self.now_cot.year, self.now_cot.month, self.now_cot.day)
        self.day_end   = self.day_start + timedelta(days=1)

        log.info(f"Cierre contable iniciado para {self.today_str} (hora COT)")

    # ── LECTURA CSV ────────────────────────────────────────────────────────────

    def read_deepseek_log(self) -> list:
        """Lee deepseek_log.csv y retorna filas del día actual."""
        if not DEEPSEEK_LOG.exists():
            log.warning(f"deepseek_log.csv no encontrado: {DEEPSEEK_LOG}")
            return []

        rows_today = []
        try:
            with open(DEEPSEEK_LOG, 'r', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    try:
                        ts = datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S")
                        if self.day_start <= ts < self.day_end:
                            rows_today.append(row)
                    except (ValueError, KeyError):
                        continue
        except Exception as e:
            log.error(f"Error leyendo deepseek_log.csv: {e}")

        log.info(f"Entradas Deepseek del día: {len(rows_today)}")
        return rows_today

    # ── CÁLCULO DE TOTALES ─────────────────────────────────────────────────────

    def calculate_totals(self, rows: list) -> Dict:
        """Calcula totales del día a partir de las filas del CSV."""
        if not rows:
            return {
                'deepseek_tokens': 0, 'deepseek_cost': 0.0,
                'claude_equiv_tokens': 0, 'claude_equiv_cost': 0.0,
                'savings_tokens': 0, 'savings_usd': 0.0,
                'savings_pct': 0.0, 'tasks': 0
            }

        ds_tokens    = sum(int(r.get('total_tokens', 0)) for r in rows)
        ds_cost      = sum(float(r.get('cost_usd', 0)) for r in rows)
        cl_tokens    = sum(int(r.get('claude_equiv_tokens', 0)) for r in rows)
        cl_cost      = sum(float(r.get('claude_equiv_cost_usd', 0)) for r in rows)
        sv_tokens    = cl_tokens - ds_tokens
        sv_usd       = cl_cost - ds_cost
        sv_pct       = round(sv_usd / cl_cost * 100, 1) if cl_cost > 0 else 0.0

        return {
            'deepseek_tokens':    ds_tokens,
            'deepseek_cost':      round(ds_cost, 5),
            'claude_equiv_tokens': cl_tokens,
            'claude_equiv_cost':  round(cl_cost, 5),
            'savings_tokens':     sv_tokens,
            'savings_usd':        round(sv_usd, 5),
            'savings_pct':        sv_pct,
            'tasks':              len(rows)
        }

    # ── GITHUB API ─────────────────────────────────────────────────────────────

    def get_token_log(self) -> Tuple[str, str]:
        """Lee TOKEN_LOG.md desde GitHub y retorna (contenido, sha)."""
        url = (f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
               f"/contents/{TOKEN_LOG_PATH}")
        resp = requests.get(url, headers=self.headers, timeout=30)
        resp.raise_for_status()
        data    = resp.json()
        content = base64.b64decode(data['content']).decode('utf-8')
        log.info(f"TOKEN_LOG.md leído — SHA: {data['sha'][:8]}")
        return content, data['sha']

    def push_token_log(self, content: str, sha: str) -> bool:
        """Actualiza TOKEN_LOG.md en GitHub via API."""
        url = (f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
               f"/contents/{TOKEN_LOG_PATH}")
        payload = {
            "message": f"🔒 Cierre contable automático — {self.today_str} [Token Analytics Bot]",
            "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
            "sha":     sha,
            "committer": {
                "name":  "Token Analytics Bot",
                "email": "token-analytics@hipocrates-mcp.local"
            }
        }
        resp = requests.put(url, headers=self.headers, json=payload, timeout=30)
        if resp.status_code in (200, 201):
            commit_sha = resp.json()['commit']['sha']
            log.info(f"TOKEN_LOG.md actualizado — commit {commit_sha[:8]}")
            return True
        else:
            log.error(f"Error al pushear TOKEN_LOG.md: {resp.status_code} {resp.text[:200]}")
            return False

    # ── GENERACIÓN DEL BLOQUE DE CIERRE ───────────────────────────────────────

    def _next_session_id(self, content: str) -> str:
        """Determina el próximo número de sesión leyendo cierres anteriores."""
        import re
        nums = re.findall(r'CIERRE CONTABLE — SES-0*(\d+)', content)
        return f"SES-{(max(int(n) for n in nums) + 1):03d}" if nums else "SES-001"

    def build_closure_block(self, content: str, totals: Dict) -> str:
        """Construye el bloque markdown de cierre contable."""
        ses = self._next_session_id(content)
        ts  = f"{self.today_str} 00:00 COT"

        return (
            f"\n---\n"
            f"\n### CIERRE CONTABLE — {ses} — {ts}\n"
            f"| Métrica | Valor |\n"
            f"|---------|-------|\n"
            f"| Total tokens Claude estimados | {totals['claude_equiv_tokens']:,} |\n"
            f"| Total tokens Deepseek (real) | {totals['deepseek_tokens']:,} |\n"
            f"| Costo real Deepseek (USD) | ${totals['deepseek_cost']:.5f} |\n"
            f"| Ahorro vs Claude (tokens) | {totals['savings_tokens']:,} |\n"
            f"| Ahorro vs Claude (USD) | ${totals['savings_usd']:.5f} |\n"
            f"| Ahorro % | {totals['savings_pct']:.1f}% |\n"
            f"| Tareas delegadas a Deepseek | {totals['tasks']} |\n"
            f"| Hora de cierre | {ts} |\n"
        )

    # ── ORQUESTACIÓN ──────────────────────────────────────────────────────────

    def run(self):
        log.info("=" * 55)
        log.info(f"CIERRE CONTABLE — {self.today_str}")
        log.info("=" * 55)

        rows   = self.read_deepseek_log()
        totals = self.calculate_totals(rows)

        log.info(f"Tokens Deepseek:   {totals['deepseek_tokens']:>8,}")
        log.info(f"Tokens Claude est: {totals['claude_equiv_tokens']:>8,}")
        log.info(f"Ahorro:            {totals['savings_pct']:>7.1f}%  (${totals['savings_usd']:.5f})")

        content, sha = self.get_token_log()
        block        = self.build_closure_block(content, totals)
        updated      = content.rstrip() + block

        ok = self.push_token_log(updated, sha)

        if ok:
            log.info("✅ CIERRE COMPLETADO")
        else:
            log.error("❌ CIERRE FALLÓ")
            sys.exit(1)


if __name__ == "__main__":
    try:
        DailyClose().run()
    except Exception as e:
        log.error(f"Error inesperado: {e}", exc_info=True)
        sys.exit(1)
