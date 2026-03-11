#!/usr/bin/env python3
"""
token_analytics/deepseek_wrapper.py

Wrapper para llamadas al servidor Deepseek MCP HTTP con registro automático de tokens.
Registra consumo en CSV para análisis de ROI del ecosistema Hipócrates MCP.

Uso:
    from token_analytics.deepseek_wrapper import DeepseekWrapper
    ds = DeepseekWrapper()
    response, meta = ds.call_deepseek("Tu prompt aquí")
    print(f"Tokens usados: {meta['total_tokens']} | Costo: ${meta['cost_usd']}")

Autor: Hipócrates MCP / Sistema Token Analytics
Fecha: 2026-03-11
"""

import os
import csv
import requests
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
DEEPSEEK_API_URL  = "http://localhost:8081/v1/chat/completions"  # Proxy nginx
DOCKER_API_URL    = "http://172.20.0.2:8080/v1/chat/completions" # Docker directo
LOG_FILE          = "token_analytics/deepseek_log.csv"
SESSION_FILE      = "token_analytics/session_counter.txt"

# Costos Deepseek API (USD por 1K tokens)
INPUT_COST_PER_1K  = 0.00014
OUTPUT_COST_PER_1K = 0.00028

# Costos Claude Sonnet estimados (para comparación)
CLAUDE_INPUT_PER_1K  = 0.003
CLAUDE_OUTPUT_PER_1K = 0.015

# Ratio estimado Claude:Deepseek por tipo de tarea
# (cuántos tokens usa Claude vs Deepseek para la misma tarea)
TASK_RATIOS = {
    'GENERATE_CONTENT': 1.8,
    'CODE_REVIEW':      1.5,
    'DATA_ANALYSIS':    1.4,
    'MODEL_TRAINING':   1.6,
    'COMMIT_GITHUB':    2.0,
    'default':          1.6
}


class DeepseekWrapper:
    """Wrapper para Deepseek API con registro automático de tokens."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key no encontrada. Establece la variable de entorno DEEPSEEK_API_KEY."
            )
        self.session_id = self._get_next_session_id()
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self._init_log_file()
        print(f"[TOKEN ANALYTICS] Sesión iniciada: {self.session_id}")

    # ── GESTIÓN DE SESIÓN ─────────────────────────────────────────────────────

    def _get_next_session_id(self) -> str:
        """Genera session_id autoincremental."""
        try:
            if os.path.exists(SESSION_FILE):
                with open(SESSION_FILE, 'r') as f:
                    counter = int(f.read().strip())
            else:
                counter = self._get_last_session_counter()
            counter += 1
            os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
            with open(SESSION_FILE, 'w') as f:
                f.write(str(counter))
            return f"SES-{counter:03d}"
        except Exception:
            return f"SES-{int(datetime.now().timestamp()) % 999:03d}"

    def _get_last_session_counter(self) -> int:
        """Lee el último número de sesión del CSV."""
        try:
            if not os.path.exists(LOG_FILE):
                return 0
            with open(LOG_FILE, 'r') as f:
                rows = list(csv.DictReader(f))
            if not rows:
                return 0
            match = re.search(r'SES-(\d+)', rows[-1].get('session_id', ''))
            return int(match.group(1)) if match else 0
        except Exception:
            return 0

    def _init_log_file(self):
        """Crea el CSV con headers si no existe."""
        if not os.path.exists(LOG_FILE):
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
            with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow([
                    'timestamp', 'session_id', 'task_type', 'model',
                    'prompt_tokens', 'completion_tokens', 'total_tokens',
                    'cost_usd', 'claude_equiv_tokens', 'claude_equiv_cost_usd',
                    'savings_tokens', 'savings_usd', 'task_description'
                ])

    # ── DETECCIÓN DE TAREA ────────────────────────────────────────────────────

    def detect_task_type(self, prompt: str) -> str:
        """Detecta el tipo de tarea basado en keywords del prompt."""
        p = prompt.lower()
        patterns = {
            'GENERATE_CONTENT': [r'genera', r'crea', r'escribe', r'implementa', r'desarrolla'],
            'CODE_REVIEW':      [r'revisa', r'analiza.*c[oó]dig', r'debug', r'error.*c[oó]dig', r'fix'],
            'DATA_ANALYSIS':    [r'analiza.*datos', r'\beda\b', r'estad[ií]stic', r'visuali', r'pandas', r'seaborn'],
            'MODEL_TRAINING':   [r'entrena', r'modelo.*ml', r'sklearn', r'xgboost', r'random.?forest', r'logistic'],
            'COMMIT_GITHUB':    [r'commit', r'push', r'github', r'repositori'],
        }
        for task_type, pats in patterns.items():
            if any(re.search(pat, p) for pat in pats):
                return task_type
        return 'GENERATE_CONTENT'

    # ── CÁLCULO DE COSTOS ─────────────────────────────────────────────────────

    def calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Calcula costo real Deepseek en USD."""
        return round(
            (prompt_tokens / 1000) * INPUT_COST_PER_1K +
            (completion_tokens / 1000) * OUTPUT_COST_PER_1K, 6
        )

    def estimate_claude_equivalent(self, total_tokens: int, task_type: str) -> Dict:
        """Estima cuánto habría costado la misma tarea en Claude."""
        ratio = TASK_RATIOS.get(task_type, TASK_RATIOS['default'])
        claude_tokens = int(total_tokens * ratio)
        # Asumimos 60% input / 40% output para Claude
        claude_input  = int(claude_tokens * 0.6)
        claude_output = int(claude_tokens * 0.4)
        claude_cost   = round(
            (claude_input / 1000) * CLAUDE_INPUT_PER_1K +
            (claude_output / 1000) * CLAUDE_OUTPUT_PER_1K, 6
        )
        return {'tokens': claude_tokens, 'cost_usd': claude_cost}

    # ── LOGGING ───────────────────────────────────────────────────────────────

    def log_usage(self, task_type: str, model: str, prompt_tokens: int,
                  completion_tokens: int, task_description: str):
        """Registra una entrada en el CSV de log."""
        total_tokens = prompt_tokens + completion_tokens
        cost_usd     = self.calculate_cost(prompt_tokens, completion_tokens)
        claude_equiv = self.estimate_claude_equivalent(total_tokens, task_type)
        savings      = {
            'tokens': claude_equiv['tokens'] - total_tokens,
            'usd':    round(claude_equiv['cost_usd'] - cost_usd, 6)
        }
        row = {
            'timestamp':           datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'session_id':          self.session_id,
            'task_type':           task_type,
            'model':               model,
            'prompt_tokens':       prompt_tokens,
            'completion_tokens':   completion_tokens,
            'total_tokens':        total_tokens,
            'cost_usd':            cost_usd,
            'claude_equiv_tokens': claude_equiv['tokens'],
            'claude_equiv_cost_usd': claude_equiv['cost_usd'],
            'savings_tokens':      savings['tokens'],
            'savings_usd':         savings['usd'],
            'task_description':    task_description[:200]
        }
        with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
            csv.DictWriter(f, fieldnames=row.keys()).writerow(row)
        print(f"[TOKEN LOG] {task_type} | {total_tokens:,} tokens | "
              f"${cost_usd:.5f} | ahorro vs Claude: {savings['tokens']:,} tokens")

    # ── LLAMADA PRINCIPAL ─────────────────────────────────────────────────────

    def call_deepseek(self, prompt: str, model: str = "deepseek-chat",
                      max_tokens: int = 2000, system_prompt: str = "",
                      task_description: str = "") -> Tuple[str, Dict]:
        """
        Llama a Deepseek y registra el uso de tokens.

        Returns:
            (response_text, metadata_dict)
        """
        task_type = self.detect_task_type(prompt)
        messages  = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {"model": model, "messages": messages, "max_tokens": max_tokens}
        response = None

        for url in [DEEPSEEK_API_URL, DOCKER_API_URL]:
            try:
                r = requests.post(url, headers=self.headers, json=payload, timeout=60)
                r.raise_for_status()
                response = r
                break
            except requests.exceptions.RequestException as e:
                print(f"[DEEPSEEK] Fallo en {url}: {e}")

        if response is None:
            raise ConnectionError("No se pudo conectar a ningún endpoint Deepseek.")

        result        = response.json()
        response_text = result['choices'][0]['message']['content']
        usage         = result.get('usage', {})
        prompt_tokens = usage.get('prompt_tokens', int(len(prompt.split()) * 1.3))
        comp_tokens   = usage.get('completion_tokens', int(len(response_text.split()) * 1.3))

        desc = task_description or (prompt[:100] + '...' if len(prompt) > 100 else prompt)
        self.log_usage(task_type, model, prompt_tokens, comp_tokens, desc)

        return response_text, {
            'task_type':         task_type,
            'model':             model,
            'prompt_tokens':     prompt_tokens,
            'completion_tokens': comp_tokens,
            'total_tokens':      prompt_tokens + comp_tokens,
            'cost_usd':          self.calculate_cost(prompt_tokens, comp_tokens),
            'session_id':        self.session_id
        }

    # ── RESUMEN DE SESIÓN ─────────────────────────────────────────────────────

    def get_session_summary(self, session_id: Optional[str] = None) -> Dict:
        """Genera resumen completo de una sesión."""
        target = session_id or self.session_id
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                rows = [r for r in csv.DictReader(f) if r['session_id'] == target]
        except FileNotFoundError:
            return {"error": "Log file no encontrado"}

        if not rows:
            return {"error": f"Sin datos para sesión {target}"}

        def _sum(field): return sum(int(r[field]) for r in rows)
        def _sumf(field): return sum(float(r[field]) for r in rows)

        by_type = {}
        for r in rows:
            t = r['task_type']
            by_type.setdefault(t, {'count': 0, 'tokens': 0, 'cost': 0.0, 'savings': 0.0})
            by_type[t]['count']   += 1
            by_type[t]['tokens']  += int(r['total_tokens'])
            by_type[t]['cost']    += float(r['cost_usd'])
            by_type[t]['savings'] += float(r['savings_usd'])

        total_tokens  = _sum('total_tokens')
        total_cost    = _sumf('cost_usd')
        total_savings = _sumf('savings_usd')

        return {
            'session_id':          target,
            'total_tasks':         len(rows),
            'total_prompt_tokens': _sum('prompt_tokens'),
            'total_comp_tokens':   _sum('completion_tokens'),
            'total_tokens':        total_tokens,
            'total_cost_usd':      round(total_cost, 6),
            'total_savings_usd':   round(total_savings, 6),
            'savings_pct':         round(total_savings / (total_cost + total_savings) * 100, 1)
                                   if (total_cost + total_savings) > 0 else 0,
            'tasks_by_type':       by_type,
            'first_task':          rows[0]['timestamp'],
            'last_task':           rows[-1]['timestamp'],
        }

    def print_session_report(self, session_id: Optional[str] = None):
        """Imprime resumen legible de sesión."""
        s = self.get_session_summary(session_id)
        if 'error' in s:
            print(f"Error: {s['error']}"); return

        sep = '=' * 65
        print(f"\n{sep}")
        print(f"  REPORTE SESIÓN: {s['session_id']}")
        print(f"  {s['first_task']}  →  {s['last_task']}")
        print(sep)
        print(f"  Tareas:          {s['total_tasks']}")
        print(f"  Tokens totales:  {s['total_tokens']:>10,}")
        print(f"  Costo real:      ${s['total_cost_usd']:>10.5f}")
        print(f"  Ahorro vs Claude: ${s['total_savings_usd']:>9.5f}  ({s['savings_pct']}%)")
        print(f"\n  Desglose por tipo:")
        print(f"  {'Tipo':<22} {'#':>3} {'Tokens':>10} {'Costo':>10} {'Ahorro':>10}")
        print(f"  {'-'*58}")
        for t, d in s['tasks_by_type'].items():
            print(f"  {t:<22} {d['count']:>3} {d['tokens']:>10,} "
                  f"${d['cost']:>9.5f} ${d['savings']:>9.5f}")
        print(sep + "\n")


# ─── USO DIRECTO ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Deepseek Wrapper — Token Analytics v1.0")
    print(f"Log: {LOG_FILE}")
    try:
        ds = DeepseekWrapper()
        resp, meta = ds.call_deepseek(
            "Di hola y confirma que el sistema de monitoreo de tokens está activo.",
            max_tokens=100
        )
        print(f"Respuesta: {resp}")
        ds.print_session_report()
    except Exception as e:
        print(f"Error: {e}")
