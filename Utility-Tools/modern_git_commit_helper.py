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
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Modern Git Commit Helper</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    const state = {
      files: [],
      idx: 0,
      current: null,
    };

    async function fetchStatus() {
      const r = await fetch('/api/status');
      state.files = await r.json();
      state.idx = 0;
      renderFilesTable();
      if (state.files.length) selectIndex(0);
      else renderEmpty();
    }

    function renderFilesTable() {
      const tbody = document.getElementById('files-body');
      tbody.innerHTML = '';
      state.files.forEach((f, i) => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-gray-50 cursor-pointer';
        tr.onclick = () => selectIndex(i);
        tr.innerHTML = `
          <td class="px-3 py-2 text-sm">${f.status}</td>
          <td class="px-3 py-2 text-sm font-mono">${f.rel}</td>
          <td class="px-3 py-2 text-sm">${f.is_py ? 'python' : 'other'}</td>
        `;
        tbody.appendChild(tr);
      });
      document.getElementById('count').textContent = state.files.length;
    }

    async function selectIndex(i) {
      state.idx = i;
      const file = state.files[i];
      document.getElementById('indexLabel').textContent = `File ${i+1} / ${state.files.length}`;
      document.getElementById('relPath').textContent = file.rel;
      const r = await fetch(`/api/file?path=${encodeURIComponent(file.rel)}`);
      const data = await r.json();
      state.current = data;
      renderDetail();
    }

    function renderEmpty(){
      document.getElementById('detail').innerHTML = `
        <div class="p-6 text-gray-500">No changes / untracked files found.</div>`;
    }

    function copyText(txt){
      navigator.clipboard.writeText(txt).then(()=>{
        toast('Copied to clipboard');
      });
    }

    function toast(msg){
      const t = document.getElementById('toast');
      t.textContent = msg; t.classList.remove('hidden');
      setTimeout(()=>t.classList.add('hidden'), 1400);
    }

    function nextFile(){
      if (!state.files.length) return;
      const ni = Math.min(state.files.length - 1, state.idx + 1);
      selectIndex(ni);
    }

    function prevFile(){
      if (!state.files.length) return;
      const pi = Math.max(0, state.idx - 1);
      selectIndex(pi);
    }

    async function doCommit(){
      const msg = (document.getElementById('commitBox').value || '').trim();
      if (!msg) { toast('Write a commit message first'); return; }
      const path = state.current?.rel;
      const r = await fetch('/api/commit', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path, message: msg })
      });
      if (!r.ok) { const e = await r.json(); toast('Error: ' + e.detail); return; }
      const data = await r.json();
      toast('Committed: ' + path);
      await fetchStatus();
      // stay on same index if possible
      if (state.files.length) {
        selectIndex(Math.min(state.idx, state.files.length-1));
      } else { renderEmpty(); }
    }

    async function doPush(){
      const r = await fetch('/api/push', { method: 'POST' });
      const data = await r.json();
      toast('Push done');
      console.log(data.push);
    }

    async function openExplorer(){
      const path = state.current?.rel; if (!path) return;
      const r = await fetch('/api/open_explorer', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ path })
      });
      if (r.ok) toast('Explorer opened'); else toast('Cannot open Explorer');
    }

    function renderDetail(){
      const d = state.current; if (!d) return;
      const isPy = d.is_py;
      const fileCard = isPy ? `
        <div class="bg-white rounded-2xl shadow p-4">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-lg font-semibold">Preview</h3>
            <div class="space-x-2">
              <button class="px-3 py-1.5 rounded-xl bg-gray-100" onclick="copyText(state.current.text)">Copy file</button>
              <button class="px-3 py-1.5 rounded-xl bg-gray-100" onclick="copyText(state.current.prompt)">Copy prompt (Copilot/ChatGPT)</button>
            </div>
          </div>
          <pre class="text-sm overflow-auto max-h-[360px] bg-gray-50 rounded-xl p-3"><code>${escapeHtml(d.text)}</code></pre>
        </div>
      ` : `
        <div class="bg-white rounded-2xl shadow p-4">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-lg font-semibold">Non-.py asset</h3>
            <button class="px-3 py-1.5 rounded-xl bg-gray-100" onclick="openExplorer()">Open in Explorer</button>
          </div>
          <p class="text-gray-600 text-sm">Use the chore(...) template below and adjust notes as needed.</p>
        </div>`;

      const commitCard = `
        <div class="bg-white rounded-2xl shadow p-4">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-lg font-semibold">Commit message</h3>
            <div class="space-x-2">
              <button class="px-3 py-1.5 rounded-xl bg-gray-100" onclick="copyText(document.getElementById('commitBox').value)">Copy commit</button>
              <button class="px-3 py-1.5 rounded-xl bg-black text-white" onclick="doCommit()">Commit & Next</button>
            </div>
          </div>
          <textarea id="commitBox" class="w-full h-48 p-3 rounded-xl border border-gray-200 font-mono text-sm" spellcheck="false">${d.commit_template}</textarea>
          <div class="mt-2 flex items-center gap-2">
            <button class="px-3 py-1.5 rounded-xl bg-gray-100" onclick="prevFile()">Prev</button>
            <button class="px-3 py-1.5 rounded-xl bg-gray-100" onclick="nextFile()">Next</button>
          </div>
        </div>
      `;

      document.getElementById('detail').innerHTML = `
        <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">${fileCard}${commitCard}</div>
      `;
    }

    function escapeHtml(s){
      return (s||'').replace(/[&<>\"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]));
    }

    window.addEventListener('DOMContentLoaded', fetchStatus);
  </script>
</head>
<body class="bg-gray-100 min-h-screen">
  <div class="max-w-7xl mx-auto p-6 space-y-6">
    <header class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold">Modern Git Commit Helper</h1>
        <p class="text-gray-600 text-sm">Repo: {repo}</p>
      </div>
      <div class="flex items-center gap-2">
        <button class="px-3 py-2 rounded-xl bg-white shadow" onclick="fetchStatus()">Refresh</button>
        <button class="px-3 py-2 rounded-xl bg-black text-white shadow" onclick="doPush()">Push origin {branch}</button>
      </div>
    </header>

    <section class="bg-white rounded-2xl shadow overflow-hidden">
      <div class="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
        <div class="font-semibold">Changes & Untracked (<span id="count">0</span>)</div>
        <div class="text-sm text-gray-500" id="indexLabel">–</div>
      </div>
      <div class="overflow-auto max-h-[260px]">
        <table class="min-w-full">
          <thead class="bg-gray-50 text-left">
            <tr>
              <th class="px-3 py-2 text-xs font-semibold text-gray-500">Status</th>
              <th class="px-3 py-2 text-xs font-semibold text-gray-500">Path</th>
              <th class="px-3 py-2 text-xs font-semibold text-gray-500">Kind</th>
            </tr>
          </thead>
          <tbody id="files-body"></tbody>
        </table>
      </div>
      <div class="px-4 py-3 border-t border-gray-100 text-sm text-gray-700">Selected: <span class="font-mono" id="relPath">–</span></div>
    </section>

    <section id="detail"></section>
  </div>

  <div id="toast" class="fixed bottom-4 left-1/2 -translate-x-1/2 px-3 py-2 bg-black text-white text-sm rounded-xl shadow hidden">Copied</div>
</body>
</html>
""".replace("{repo}", str(REPO_PATH)).replace("{branch}", BRANCH)


if __name__ == "__main__":
    # Run: python app.py
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="127.0.0.1", port=port)
