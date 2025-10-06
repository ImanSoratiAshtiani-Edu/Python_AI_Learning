# app.py
"""
Modern Git Commit Helper (FastAPI + Tailwind, single-file)
- Shows `git status --porcelain=1 -uall`
- For .py files: previews content, offers Copy buttons and an auto-generated Copilot/ChatGPT prompt
- Commit editor with "Commit & Next"; also "Skip" to move forward
- For non-.py files: "Open in Explorer" (server-side) and a chore(...) commit template
- Push button (origin main by default)

Usage:
  1) pip install fastapi uvicorn[standard]
  2) python app.py
  3) Open http://127.0.0.1:8000

Tested on Windows 10/11, Python 3.10+
"""

from __future__ import annotations

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any

from fastapi import FastAPI, Query, Body, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# ----------------------------- Config -----------------------------
REPO_PATH = Path(r"D:\git\Python_AI_Learning").resolve()
BRANCH = "main"
MAX_FILE_BYTES = 800_000  # cap for preview
# ------------------------------------------------------------------

app = FastAPI(title="Modern Git Commit Helper")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"]
)

# ----------------------------- Utilities -----------------------------

def run_git(args: List[str]) -> str:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=str(REPO_PATH),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=False,
            check=False,
        )
        return proc.stdout.strip()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Git not found in PATH")


def safe_path(rel_path: str) -> Path:
    # Normalize and ensure the path stays within the repo
    p = (REPO_PATH / rel_path).resolve()
    if not str(p).startswith(str(REPO_PATH)):
        raise HTTPException(status_code=400, detail="Path traversal detected")
    return p


def get_status_files() -> List[Dict[str, Any]]:
    out = run_git(["status", "--porcelain=1", "-uall"]) or ""
    lines = [ln for ln in out.splitlines() if ln.strip()]
    items: List[Dict[str, Any]] = []
    for l in lines:
        # e.g. "?? path/to/file" or " M path" or "A  file"
        status = l[:2].strip()
        rel = l[3:].strip()
        full = (REPO_PATH / rel).resolve()
        is_py = full.suffix.lower() == ".py"
        items.append({
            "status": status,
            "rel": rel.replace("\\", "/"),
            "is_py": is_py,
            "ext": full.suffix.lower(),

            "exists": full.exists(),
        })
    return items


def read_file_preview(p: Path) -> str:
    if not p.exists() or not p.is_file():
        return ""
    try:
        data = p.read_bytes()
        return data[:MAX_FILE_BYTES].decode("utf-8", errors="replace")
    except Exception:
        try:
            return p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return ""


def build_commit_template(rel: str, text: str) -> str:
    scope = Path(rel).parent.as_posix() or "root"
    type_ = "feat"
    low = rel.lower()
    if any(k in low for k in ("readme", ".md", "docs")):
        type_ = "docs"
    elif any(k in low for k in ("fix", "bug")):
        type_ = "fix"
    elif any(k in low for k in ("test", "_test.py")):
        type_ = "test"

    # very light parsing
    imports = []
    defs = []
    classes = []
    for line in text.splitlines()[:2000]:  # only scan first 2k lines
        ls = line.strip()
        if ls.startswith("import ") or ls.startswith("from "):
            imports.append(ls)
        elif ls.startswith("def "):
            name = ls.split("def ", 1)[1].split("(", 1)[0]
            defs.append(f"{name}()")
        elif ls.startswith("class "):
            name = ls.split("class ", 1)[1].split("(")[0].split(":")[0].strip()
            classes.append(name)

    bullets = []
    if imports:
        bullets.append("- imports: " + ", ".join(imports[:6]))
    if classes:
        bullets.append("- classes: " + ", ".join(classes[:6]))
    if defs:
        bullets.append("- functions: " + ", ".join(defs[:8]))
    bullets.append("- educational notes: explain key methods, theory, and practical usage")
    bullets.append("- include examples and edge cases (where relevant)")

    short = f"Add/organize {Path(rel).name} with clear, educational structure"
    body = "\n".join(bullets)
    return f"""
{type_}({scope}): {short}

{body}
""".strip()


def build_copilot_prompt(rel: str, text: str) -> str:
    return f"""
You are GitCopilot. Read this Python file and propose a concise, multi-line Conventional Commit in English that:
- uses type(scope): short description
- subject line <= 72 chars, imperative mood
- bullet points summarizing educational topics (theory/methods/practice)

File name: {rel}

<FILE_CONTENT_START>
{text}
<FILE_CONTENT_END>
""".strip()

# ----------------------------- API -----------------------------

@app.get("/", response_class=HTMLResponse)
async def index() -> str:
    return INDEX_HTML


@app.get("/api/status")
async def api_status() -> JSONResponse:
    return JSONResponse(get_status_files())


@app.get("/api/file")
async def api_file(path: str = Query(...)) -> JSONResponse:
    p = safe_path(path)
    is_py = p.suffix.lower() == ".py"
    text = read_file_preview(p) if is_py else ""
    commit_tmpl = build_commit_template(path, text) if is_py else (
        f"chore({Path(path).parent.as_posix() or 'root'}): add {Path(path).name}\n\n- describe what this asset contains\n- why it is added and how it is used\n- reference related notebooks or code if applicable"
    )
    prompt = build_copilot_prompt(path, text) if is_py else ""
    return JSONResponse({
        "rel": path,
        "exists": p.exists(),
        "is_py": is_py,
        "text": text,
        "commit_template": commit_tmpl,
        "prompt": prompt,
    })


@app.post("/api/commit")
async def api_commit(payload: Dict[str, Any] = Body(...)) -> JSONResponse:
    path = payload.get("path")
    message = payload.get("message", "").strip()
    if not path or not message:
        raise HTTPException(status_code=400, detail="path and message are required")
    p = safe_path(path)
    if not p.exists():
        raise HTTPException(status_code=404, detail="file not found")

    add_out = run_git(["add", "--", path])
    # write temp file for multi-line commit
    tmp = Path(os.getenv("TEMP", str(REPO_PATH))) / "_git_helper_commit_msg.txt"
    tmp.write_text(message, encoding="utf-8")
    com_out = run_git(["commit", "-F", str(tmp)])
    try:
        tmp.unlink(missing_ok=True)
    except Exception:
        pass
    return JSONResponse({"added": path, "git_add": add_out, "git_commit": com_out})


@app.post("/api/push")
async def api_push() -> JSONResponse:
    out = run_git(["push", "origin", BRANCH])
    return JSONResponse({"push": out})


@app.post("/api/open_explorer")
async def api_open_explorer(payload: Dict[str, Any] = Body(...)) -> JSONResponse:
    path = payload.get("path")
    if not path:
        raise HTTPException(status_code=400, detail="path is required")
    p = safe_path(path)
    if not p.exists():
        raise HTTPException(status_code=404, detail="file not found")
    try:
        subprocess.Popen(["explorer.exe", f"/select,{str(p)}"])  # pragma: no cover
        return JSONResponse({"status": "ok"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------- Frontend (HTML+JS) -----------------------------
INDEX_HTML = """
<!DOCTYPE html>
<html lang=\"en\" class=\"h-full\" >
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Modern Git Commit Helper</title>
  <script>
  // Tailwind: dark mode بر مبنای کلاس
  window.tailwind = { config: { darkMode: 'class' } };
</script>
<script>
  // اعمال اولیه‌ی تم قبل از paint
  (function () {
    try {
      const saved = localStorage.getItem('theme'); // 'dark' | 'light' | null
      const sys = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const useDark = saved ? (saved === 'dark') : sys;
      document.documentElement.classList.toggle('dark', useDark);
    } catch {}
  })();
</script>
<script src="https://cdn.tailwindcss.com"></script>
<script>
  (function(){
    function init(){
      const btn = document.getElementById('themeBtn');
      if(!btn) return; // اگر دکمه نبود، بی‌صدا خروج

      function syncBtn(){
        const isDark = document.documentElement.classList.contains('dark');
        btn.textContent = isDark ? '☀' : '☾';
        btn.setAttribute('aria-pressed', String(isDark));
        btn.title = isDark ? 'Switch to light' : 'Switch to dark';
      }
      function applyTheme(dark){
        document.documentElement.classList.toggle('dark', dark);
        localStorage.setItem('theme', dark ? 'dark' : 'light');
        syncBtn();
      }

      // رویداد کلیک
      btn.addEventListener('click', ()=> {
        applyTheme(!document.documentElement.classList.contains('dark'));
      });

      // همگام‌سازی اولیه دکمه با وضعیت فعلی
      syncBtn();

      // اگر کاربر ترجیح ذخیره نکرده، با تغییر تم سیستم همگام شود
      const mq = window.matchMedia('(prefers-color-scheme: dark)');
      (mq.addEventListener ? mq.addEventListener : mq.addListener)
        .call(mq, e => { if (!localStorage.getItem('theme')) applyTheme(e.matches); });
    }

    // تضمین اجرا بعد از ساخته‌شدن DOM (اسکریپت در head است)
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', init, { once: true });
    } else {
      init();
    }
  })();
</script>

  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\"/>
  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin/>
  <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap\" rel=\"stylesheet\"/>
  <style>
    :root { color-scheme: light dark; }
    body { font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Helvetica Neue', Arial, 'Apple Color Emoji','Segoe UI Emoji'; }
    .glass { backdrop-filter: blur(8px); background: rgba(255,255,255,0.7); }
    .dark .glass { background: rgba(17,24,39,0.6); }
    .status-pill { @apply inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium; }
    .pill-qq { @apply bg-brand-50 text-brand-700; }    /* ?? */
    .pill-mod { @apply bg-warn/10 text-warn; }        /* M */
    .pill-add { @apply bg-accent/10 text-accent; }    /* A */
    .pill-del { @apply bg-danger/10 text-danger; }    /* D */
  </style>
</head>
<body class=\"bg-gradient-to-br from-brand-50 to-white dark:from-slate-900 dark:to-slate-950 min-h-screen text-slate-800 dark:text-slate-100\">
  <div class=\"max-w-7xl mx-auto p-6 space-y-6\">
    <!-- Header -->
    <header class=\"rounded-3xl shadow-lg glass dark:shadow-black/30 px-6 py-5 flex items-center justify-between\">
      <div class=\"space-y-1\">
        <h1 class=\"text-2xl font-bold tracking-tight\">Modern Git Commit Helper</h1>
        <p class=\"text-sm text-slate-500 dark:text-slate-400\">Repo: {repo}</p>
      </div>
      <div class=\"flex items-center gap-2\">
        <div class=\"hidden sm:flex gap-2\">
          <button class=\"px-3 py-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow hover:shadow-md transition\" onclick=\"fetchStatus()\">Refresh <span class=\"ml-2 text-xs text-slate-500\">(R)</span></button>
          <button class=\"px-3 py-2 rounded-xl bg-brand-600 text-white shadow hover:bg-brand-700 transition\" onclick=\"doPush()\">Push origin {branch} <span class=\"ml-2 text-xs text-brand-200\">(P)</span></button>
        </div>
        <button id=\"themeBtn\" class=\"px-3 py-2 rounded-xl bg-slate-900 text-white dark:bg-white dark:text-slate-900 shadow\" title=\"Toggle theme\" aria-label=\"Toggle theme\">☾</button>
      </div>
    </header>

    <!-- Filters / legend -->
    <section class=\"grid grid-cols-1 lg:grid-cols-3 gap-3\">
      <div class=\"col-span-2 rounded-2xl bg-white/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow p-3\">
        <div class=\"flex items-center gap-2\">
          <select id=\"search\" class=\"w-full px-3 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 focus:outline-none focus:ring-2 focus:ring-brand-400 font-mono text-sm\"><option value=\"all\">Folder Path: All</option></select>
          <select id=\"kindFilter\" class=\"px-3 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-sm\">
            <option value=\"all\">All</option>
            <option value=\"python\">Python</option>
            <option value=\"other\">Other</option>
          </select>
          <select id=\"statusFilter\" class=\"px-3 py-2 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-sm\">
            <option value=\"all\">All Status</option>
            <option value=\"??\">Untracked (??)</option>
            <option value=\"M\">Modified (M)</option>
            <option value=\"A\">Added (A)</option>
            <option value=\"D\">Deleted (D)</option>
          </select>
        </div>
      </div>
      <div class=\"rounded-2xl bg-white/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow p-3 text-sm\">
        <div class=\"flex items-center gap-3 flex-wrap\">
          <span class=\"text-slate-500 dark:text-slate-400\">Shortcuts: R refresh, P push, J/K next/prev, C commit, E explorer, / search</span>
        </div>
      </div>
    </section>

    <!-- Table -->
    <section class=\"rounded-3xl bg-white/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow overflow-hidden\">
      <div class=\"px-4 py-3 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between\">
        <div class=\"font-semibold\">Changes & Untracked (<span id=\"count\">0</span>)</div>
        <div class=\"text-sm text-slate-500 dark:text-slate-400\" id=\"indexLabel\">–</div>
      </div>
      <div class=\"overflow-auto max-h-[300px]\">
        <table class=\"min-w-full\">
          <thead class=\"bg-slate-50 dark:bg-slate-800 sticky top-0 z-10 text-left\">
            <tr>
              <th class=\"px-3 py-2 text-xs font-semibold text-slate-500\">Status</th>
              <th class=\"px-3 py-2 text-xs font-semibold text-slate-500\">Path</th>
              <th class=\"px-3 py-2 text-xs font-semibold text-slate-500\">Kind</th>
            </tr>
          </thead>
          <tbody id=\"files-body\"></tbody>
        </table>
      </div>
      <div class=\"px-4 py-3 border-t border-slate-200 dark:border-slate-800 text-sm text-slate-700 dark:text-slate-300\">Selected: <span class=\"font-mono\" id=\"relPath\">–</span></div>
    </section>

    <!-- Detail -->
    <section id=\"detail\"></section>
  </div>

  <!-- Toast -->
  <div id=\"toast\" class=\"fixed bottom-5 left-1/2 -translate-x-1/2 px-4 py-2 rounded-xl bg-slate-900 text-white text-sm shadow-lg hidden\">Copied</div>

  <script>
    const state = { files: [], idx: 0, current: null, raw: [] };
    // Parent folder helpers for the dropdown (reusing id='search')
    function getParentFolder(rel){
      const i = rel.lastIndexOf('/');
      return i >= 0 ? rel.slice(0, i) : ''; // root is ''
    }

    function collectParents(){
      const set = new Set();
      (state.raw || []).forEach(f => { set.add(getParentFolder(f.rel)); });
      return Array.from(set).sort((a,b)=> a.localeCompare(b));
    }

 function populateSearchDropdown(){
  const sel = document.getElementById('search');
  if(!sel) return;

  const parents = collectParents();

  let opts = '<option value="all">All Folders</option>';  // ← مهم: تعریف اولیه
  const hasRoot = (state.raw || []).some(f => !f.rel.includes('/'));
  if (hasRoot) opts += '<option value="">root</option>';

  parents.filter(p => p !== '').forEach(p => {
    opts += '<option value="' + escapeHtml(p) + '">' + escapeHtml(p) + '</option>';
  });

  sel.innerHTML = opts;
}

// === File extension dropdown (kindFilter) ===
function collectExtensions(){
  const set = new Set();
  (state.raw || []).forEach(f => {
    const ext = (f.ext || '').toLowerCase();
    set.add(ext);
  });
  const arr = Array.from(set);
  arr.sort((a,b)=> {
    if(a==='' && b==='') return 0;
    if(a==='') return 1;
    if(b==='') return -1;
    return a.localeCompare(b);
  });
  return arr;
}
function collectStatuses(){
  const set = new Set();
  (state.raw || []).forEach(f => {
    if (f.status) set.add(f.status);
  });
  // ترتیب پیشنهادی
  const order = ['staged','modified','renamed','deleted','untracked','ignored','conflict','unknown'];
  const arr = Array.from(set);
  arr.sort((a,b)=>{
    const ia = order.indexOf(a); const ib = order.indexOf(b);
    if (ia === -1 && ib === -1) return a.localeCompare(b);
    if (ia === -1) return 1;
    if (ib === -1) return -1;
    return ia - ib;
  });
  return arr;
}

function populateStatusDropdown(){
  const sel = document.getElementById('statusFilter');  // ← sel تعریف شد
  if(!sel) return;

  const stats = collectStatuses();

  let opts = '<option value="all">All Status</option>';     // ← opts تعریف شد (برچسب پیش‌فرض)
  stats.forEach(s => {
    opts += '<option value="' + escapeHtml(s) + '">' + escapeHtml(s) + '</option>';
  });

  sel.innerHTML = opts;
}

function populateKindDropdown(){
  const sel = document.getElementById('kindFilter');  // ← تعریف sel
  if(!sel) return;

  const exts = collectExtensions();

  let opts = '<option value="all">All Files</option>'; // ← تعریف opts
  exts.forEach(ext => {
    const label = ext ? ext : '(no ext)';
    const val = ext || '__noext__';
    opts += '<option value="' + escapeHtml(val) + '">' + escapeHtml(label) + '</option>';
  });

  sel.innerHTML = opts;
}


    // Theme toggle (persist)
    const root = document.documentElement;
    const themeBtn = () => document.getElementById('themeBtn');
    function applyTheme(mode){
      if(mode==='dark'){ root.classList.add('dark'); localStorage.setItem('theme','dark'); themeBtn().textContent='☀'; }
      else { root.classList.remove('dark'); localStorage.setItem('theme','light'); themeBtn().textContent='☾'; }
    }
    (function(){ applyTheme(localStorage.getItem('theme')|| (matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light')); })();
    document.addEventListener('click', (e)=>{ if(e.target.id==='themeBtn'){ applyTheme(root.classList.contains('dark')?'light':'dark'); }});

    async function fetchStatus(){
      const r = await fetch('/api/status');
      state.raw = await r.json();
      state.files = state.raw; // default
      state.idx = 0;
      populateSearchDropdown();
      populateKindDropdown();
      populateStatusDropdown()
      renderFilesTable();
      if (state.files.length) selectIndex(0); else renderEmpty();
    }

    function filterData(){
      const p = document.getElementById('search').value; // selected parent folder
      const k = document.getElementById('kindFilter').value;
      const s = document.getElementById('statusFilter').value;
      state.files = state.raw.filter(f=>{
        const ext = (f.ext || '').toLowerCase();
        const sel = (k === '__noext__') ? '' : (k || '');
        const okK = (k==='all') || (ext === sel);
        const okS = (s==='all') || (f.status===s || f.status.startsWith(s));
        const okP = (p==='all') || (p==='' && !f.rel.includes('/')) || f.rel===p || f.rel.startsWith(p + '/');
        return okP && okK && okS;
      });
      renderFilesTable();
      if(state.files.length){ state.idx = 0; selectIndex(0);} else { renderEmpty(); }
   
    }

    document.addEventListener('input', (e)=>{
      if(['search','kindFilter','statusFilter'].includes(e.target.id)) filterData();
    });

    document.addEventListener('keydown', (e)=>{
      if(e.key==='/' && !e.ctrlKey){ e.preventDefault(); document.getElementById('search').focus(); }
      if(e.key.toLowerCase()==='r'){ fetchStatus(); }
      if(e.key.toLowerCase()==='p'){ doPush(); }
      if(e.key.toLowerCase()==='j'){ nextFile(); }
      if(e.key.toLowerCase()==='k'){ prevFile(); }
      if(e.key.toLowerCase()==='c'){ doCommit(); }
      if(e.key.toLowerCase()==='e'){ openExplorer(); }
      if(e.ctrlKey && e.key==='/'){ document.getElementById('search').focus(); }
    });

    function renderFilesTable(){
      const tbody = document.getElementById('files-body');
      tbody.innerHTML = '';
      document.getElementById('count').textContent = state.files.length;
      state.files.forEach((f, i) => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-50 dark:hover:bg-slate-800/60 cursor-pointer';
        tr.onclick = () => selectIndex(i);
        const pill = badgeFor(f.status);
        tr.innerHTML = `
          <td class=\"px-3 py-2 text-sm\">${pill}</td>
          <td class=\"px-3 py-2 text-sm font-mono\">${escapeHtml(f.rel)}</td>
          <td class=\"px-3 py-2 text-sm\">${(f.ext||'').startsWith('.') ? f.ext.slice(1) : (f.ext||'—')}</td>
        `;
        tbody.appendChild(tr);
      });
    }

    function badgeFor(status){
      const s = status.trim();
      if(s==='??') return `<span class=\"status-pill pill-qq\">?? new</span>`;
      if(s==='M')  return `<span class=\"status-pill pill-mod\">M modified</span>`;
      if(s==='A')  return `<span class=\"status-pill pill-add\">A added</span>`;
      if(s==='D')  return `<span class=\"status-pill pill-del\">D deleted</span>`;
      return `<span class=\"status-pill bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300\">${escapeHtml(s)}</span>`;
    }

    async function selectIndex(i){
      state.idx = i; const file = state.files[i];
      document.getElementById('indexLabel').textContent = `File ${i+1} / ${state.files.length}`;
      document.getElementById('relPath').textContent = file.rel;
      const r = await fetch(`/api/file?path=${encodeURIComponent(file.rel)}`);
      const data = await r.json(); state.current = data; renderDetail();
    }

    function renderEmpty(){
      document.getElementById('detail').innerHTML = `<div class=\"p-6 text-slate-500\">No changes / untracked files found.</div>`;
    }

    function copyText(txt){ navigator.clipboard.writeText(txt||'').then(()=> toast('Copied to clipboard')); }

    function toast(msg){
      const t = document.getElementById('toast'); t.textContent = msg; t.classList.remove('hidden');
      setTimeout(()=> t.classList.add('hidden'), 1400);
    }

    function nextFile(){ if(!state.files.length) return; const ni = Math.min(state.files.length-1, state.idx+1); selectIndex(ni); }
    function prevFile(){ if(!state.files.length) return; const pi = Math.max(0, state.idx-1); selectIndex(pi); }

    async function doCommit(){
      const box = document.getElementById('commitBox');
      const msg = (box?.value || '').trim();
      if(!msg){ toast('Write a commit message first'); box?.focus(); return; }
      const path = state.current?.rel; if(!path){ toast('No file selected'); return; }
      const r = await fetch('/api/commit', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ path, message: msg }) });
      if(!r.ok){ const e = await r.json(); toast('Error: ' + e.detail); return; }
      toast('Committed: ' + path);
      await fetchStatus();
      if (state.files.length) selectIndex(Math.min(state.idx, state.files.length-1)); else renderEmpty();
    }

    async function doPush(){ const r = await fetch('/api/push', { method:'POST'}); const d = await r.json(); toast('Push done'); console.log(d.push); }

    async function openExplorer(){ const path = state.current?.rel; if(!path) return; const r = await fetch('/api/open_explorer', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ path }) }); if(r.ok) toast('Explorer opened'); else toast('Cannot open Explorer'); }

    function renderDetail(){
      const d = state.current; if(!d) return; const isPy = d.is_py;
      const actions = isPy ? `<div class=\"space-x-2\">
          <button class=\"px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800\" onclick=\"copyText(state.current.text)\">Copy file</button>
          <button class=\"px-3 py-1.5 rounded-xl bg-slate-900 text-white dark:bg-white dark:text-slate-900\" onclick=\"copyText(state.current.prompt)\">Copy prompt</button>
        </div>` : `<button class=\"px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800\" onclick=\"openExplorer()\">Open in Explorer (E)</button>`;

      const fileCard = isPy ? `
        <div class=\"rounded-2xl bg-white/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow p-4\">
          <div class=\"flex items-center justify-between mb-2\">
            <h3 class=\"text-lg font-semibold\">Preview</h3>
            ${actions}
          </div>
          <pre class=\"text-sm overflow-auto max-h-[360px] bg-slate-50 dark:bg-slate-800 rounded-xl p-3\"><code>${escapeHtml(d.text)}</code></pre>
        </div>`
      : `
        <div class=\"rounded-2xl bg-white/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow p-4\">
          <div class=\"flex items-center justify-between mb-2\">
            <h3 class=\"text-lg font-semibold\">Non-.py asset</h3>
            ${actions}
          </div>
          <p class=\"text-slate-600 dark:text-slate-400 text-sm\">Use the chore(...) template below and adjust notes as needed.</p>
        </div>`;

      const commitCard = `
        <div class=\"rounded-2xl bg-white/80 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 shadow p-4\">
          <div class=\"flex items-center justify-between mb-2\">
            <h3 class=\"text-lg font-semibold\">Commit message</h3>
            <div class=\"space-x-2\">
              <button class=\"px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800\" onclick=\"copyText(document.getElementById('commitBox').value)\">Copy commit</button>
              <button class=\"px-3 py-1.5 rounded-xl bg-brand-600 text-white hover:bg-brand-700 transition\" onclick=\"doCommit()\">Commit & Next (C)</button>
            </div>
          </div>
          <textarea id=\"commitBox\" class=\"w-full h-48 p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white/70 dark:bg-slate-900/40 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-brand-400\" spellcheck=\"false\">${d.commit_template}</textarea>
          <div class=\"mt-2 flex items-center gap-2\">
            <button class=\"px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800\" onclick=\"prevFile()\">Prev (K)</button>
            <button class=\"px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800\" onclick=\"nextFile()\">Next (J)</button>
          </div>
        </div>`;

      document.getElementById('detail').innerHTML = `<div class=\"grid grid-cols-1 xl:grid-cols-2 gap-6\">${fileCard}${commitCard}</div>`;
    }

    function escapeHtml(s){ return (s||'').replace(/[&<>\\"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\\"':'&quot;'}[c])); }

    window.addEventListener('DOMContentLoaded', () => { fetchStatus(); document.getElementById('search').addEventListener('keydown', e=>{ if(e.key==='Escape'){ e.target.blur(); }}); });
  </script>

<script>
  (function(){
    const btn = document.getElementById('themeBtn');
    if(!btn) return;

    function syncBtn(){
      const isDark = document.documentElement.classList.contains('dark');
      btn.textContent = isDark ? '☀' : '☾';
      btn.setAttribute('aria-pressed', String(isDark));
    }
    function applyTheme(dark){
      document.documentElement.classList.toggle('dark', dark);
      localStorage.setItem('theme', dark ? 'dark' : 'light');
      syncBtn();
    }
    btn.addEventListener('click', ()=>{
      applyTheme(!document.documentElement.classList.contains('dark'));
    });
    syncBtn();
  })();
</script>
</body>


</html>
""".replace("{repo}", str(REPO_PATH)).replace("{branch}", BRANCH)


if __name__ == "__main__":
    # Run: python app.py
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="127.0.0.1", port=port)
