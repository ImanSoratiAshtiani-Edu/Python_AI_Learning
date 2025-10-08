import React, { useEffect, useMemo, useRef, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { ChevronDown, ChevronRight, Download, FileJson, Globe, Moon, Plus, Sun, Trash2, Upload, BarChart3, ListChecks } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar, Legend, CartesianGrid } from "recharts";

// ---- Helpers ----
const uid = () => Math.random().toString(36).slice(2) + Date.now().toString(36);
const todayISO = () => new Date().toISOString();
const fmtDateTime = (d, lang) => new Date(d).toLocaleString(lang === 'fa' ? 'fa-IR' : 'en-GB');
const fmtDate = (d, lang) => new Date(d).toLocaleDateString(lang === 'fa' ? 'fa-IR' : 'en-GB');
const startOf = (range) => {
  const now = new Date();
  const d = new Date();
  switch (range) {
    case 'daily': d.setHours(0,0,0,0); return d;
    case 'weekly': {
      const day = (now.getDay() + 6) % 7; // week starts Monday
      d.setDate(now.getDate() - day); d.setHours(0,0,0,0); return d;
    }
    case 'monthly': d.setDate(1); d.setHours(0,0,0,0); return d;
    case '3-monthly': d.setMonth(now.getMonth() - 2, 1); d.setHours(0,0,0,0); return d;
    case 'yearly': d.setMonth(0,1); d.setHours(0,0,0,0); return d;
    case 'all': default: return new Date(0);
  }
};

// ---- i18n strings ----
const TL = {
  en: {
    appTitle: "Study & Tasks Manager",
    categories: "Categories",
    subcategories: "Sub-categories",
    materials: "Materials",
    addCategory: "Add category",
    addSub: "Add sub-category",
    addMaterial: "Add material",
    title: "Title",
    pathUrl: "Local path or URL",
    counter: "Counter",
    lastClick: "Last click",
    actions: "Actions",
    delete: "Delete",
    dashboard: "Dashboard",
    timeRange: "Time range",
    tasks: "Tasks",
    newTask: "New task",
    taskText: "Task description",
    dueDate: "Event date (optional)",
    interval: "Interval",
    none: "None",
    daily: "Daily",
    weekly: "Weekly",
    monthly: "Monthly",
    save: "Save",
    export: "Export JSON",
    import: "Import JSON",
    clearAll: "Clear All",
    expandAll: "Expand All",
    collapseAll: "Collapse All",
    theme: "Theme",
    language: "Language",
    dark: "Dark",
    light: "Light",
    fa: "FA",
    en: "EN",
    visibleNow: "Visible now",
    completed: "Completed",
    history: "History",
    show: "Show",
    hide: "Hide",
    open: "Open",
    clickIt: "Click",
    barTotals: "Totals by material",
    timeSeries: "Usage over time",
    alwaysVisible: "Always visible",
    relevantOnly: "Relevant only",
    expand: "Expand",
    collapse: "Collapse",
  },
  fa: {
    appTitle: "مدیریت مطالعه و کارها",
    categories: "دسته‌ها",
    subcategories: "زیر‌دسته‌ها",
    materials: "مواد آموزشی",
    addCategory: "افزودن دسته",
    addSub: "افزودن زیر‌دسته",
    addMaterial: "افزودن منبع",
    title: "عنوان",
    pathUrl: "مسیر فایل یا آدرس وب",
    counter: "شمارنده",
    lastClick: "آخرین کلیک",
    actions: "اقدامات",
    delete: "حذف",
    dashboard: "داشبورد",
    timeRange: "بازهٔ زمانی",
    tasks: "کارها",
    newTask: "کار جدید",
    taskText: "توضیح کار",
    dueDate: "تاریخ رویداد (اختیاری)",
    interval: "تناوب",
    none: "هیچ‌کدام",
    daily: "روزانه",
    weekly: "هفتگی",
    monthly: "ماهانه",
    save: "ذخیره",
    export: "خروجی JSON",
    import: "ورودی JSON",
    clearAll: "پاکسازی همه",
    expandAll: "گسترش همه",
    collapseAll: "جمع‌کردن همه",
    theme: "پوسته",
    language: "زبان",
    dark: "تیره",
    light: "روشن",
    fa: "فا",
    en: "انگ",
    visibleNow: "قابل نمایش اکنون",
    completed: "انجام‌شده‌ها",
    history: "تاریخچه",
    show: "نمایش",
    hide: "پنهان",
    open: "باز کردن",
    clickIt: "کلیک",
    barTotals: "جمع کلیک‌ها بر اساس منبع",
    timeSeries: "روند استفاده در زمان",
    alwaysVisible: "همیشه قابل مشاهده",
    relevantOnly: "فقط موارد مرتبط",
    expand: "بازکردن",
    collapse: "بستن",
  }
};

// ---- Data shapes ----
// Material: {id, title, url, clicks, lastClickedAt, history:[{ts}]}
// Sub: {id, name, materials: Material[]}
// Category: {id, name, subs: Sub[]}
// Task: {id, text, date?: ISO, interval?: 'daily'|'weekly'|'monthly', completedAt?: ISO, lastDoneAt?: ISO, always?: boolean}

const DEFAULT_DATA = {
  categories: [
    { id: uid(), name: "Python-AI", subs: [
      { id: uid(), name: "Grammar / Basics", materials: [] },
      { id: uid(), name: "NumPy / Pandas", materials: [] }
    ]},
    { id: uid(), name: "Italian language", subs: [
      { id: uid(), name: "Vocabulary", materials: [] }
    ]}
  ],
  tasks: [
    { id: uid(), text: "Review NumPy indexing", interval: 'weekly', lastDoneAt: null },
    { id: uid(), text: "Italian verbs practice", interval: 'daily', lastDoneAt: null },
    { id: uid(), text: "Read 10 pages of AI book", date: null }
  ]
};

const STORAGE_KEY = 'studyAppDataV1';
const THEME_KEY = 'studyAppTheme';
const LANG_KEY = 'studyAppLang';

// ---- Root App ----
export default function App() {
  const [data, setData] = useState(() => {
    try { const raw = localStorage.getItem(STORAGE_KEY); return raw ? JSON.parse(raw) : DEFAULT_DATA; } catch { return DEFAULT_DATA; }
  });
  const [lang, setLang] = useState(() => localStorage.getItem(LANG_KEY) || 'en');
  const [dark, setDark] = useState(() => (localStorage.getItem(THEME_KEY) || 'dark') === 'dark');
  const [expanded, setExpanded] = useState({ cats:true, dash:true, tasks:true });
  const t = TL[lang];

	// --- Apply or remove dark mode class on root ---
useEffect(() => {
  const root = window.document.documentElement;
  if (dark) {
    root.classList.add('dark');
  } else {
    root.classList.remove('dark');
  }
}, [dark]);


  useEffect(() => { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); }, [data]);
  useEffect(() => { localStorage.setItem(THEME_KEY, dark ? 'dark' : 'light'); }, [dark]);
  useEffect(() => { localStorage.setItem(LANG_KEY, lang); }, [lang]);

return (
  <>
    <div
      className={
        "min-h-screen transition-colors duration-300 " +
        (dark
          ? "bg-background-dark text-text-dark"
          : "bg-background-light text-text-light")
      }
    >
      <div className="container mx-auto px-3 py-4 max-w-6xl">
        <Header
          lang={lang}
          setLang={setLang}
          dark={dark}
          setDark={setDark}
          t={t}
        />

        {/* Categories & Materials */}
        <SectionCard
          title={t.categories}
          icon={<ChevronDown className="w-4 h-4" />}
          expanded={expanded.cats}
          onToggle={() => setExpanded((s) => ({ ...s, cats: !s.cats }))}
        >
          <CategoryManager data={data} setData={setData} t={t} lang={lang} />
        </SectionCard>

        {/* Dashboard */}
        <SectionCard
          title={t.dashboard}
          icon={<BarChart3 className="w-4 h-4" />}
          expanded={expanded.dash}
          onToggle={() => setExpanded((s) => ({ ...s, dash: !s.dash }))}
        >
          <Dashboard data={data} t={t} lang={lang} />
        </SectionCard>

        {/* Tasks */}
        <SectionCard
          title={t.tasks}
          icon={<ListChecks className="w-4 h-4" />}
          expanded={expanded.tasks}
          onToggle={() => setExpanded((s) => ({ ...s, tasks: !s.tasks }))}
        >
          <TasksSection data={data} setData={setData} t={t} lang={lang} />
        </SectionCard>

        {/* Import / Export */}
        <ImportExport data={data} setData={setData} t={t} />
      </div>
    </div>

    {/* 🎨 استایل Material - با JSX معتبر */}
    <style>{`
      .bg-card {
        border: 1px solid rgba(0,0,0,0.1);
        border-radius: 1rem;
        box-shadow: 0 3px 8px rgba(0,0,0,0.12);
        background-color: #ffffff;
        transition: all 0.3s ease;
      }
      .dark .bg-card {
        background-color: #1e293b;
        border-color: rgba(255,255,255,0.1);
        box-shadow: 0 3px 8px rgba(255,255,255,0.05);
      }
      .bg-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(0,0,0,0.15);
      }
      .bg-primary {
        background-color: #2563eb;
        color: white;
        border-radius: 0.75rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        transition: all 0.2s ease;
      }
      .bg-primary:hover {
        background-color: #1e40af;
      }
    `}</style>
  </>
);
}
function Header({ lang, setLang, dark, setDark, t }){
  return (
    <div className="flex items-center justify-between gap-3 mb-4">
      <h1 className="text-2xl font-semibold tracking-tight">{t.appTitle}</h1>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <Globe className="w-4 h-4"/>
          <Select value={lang} onValueChange={setLang}>
            <SelectTrigger className="w-[120px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="en">EN</SelectItem>
              <SelectItem value="fa">FA</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="flex items-center gap-2">
          <Sun className="w-4 h-4"/>
          <Switch checked={dark} onCheckedChange={setDark} />
          <Moon className="w-4 h-4"/>
        </div>
      </div>
    </div>
  );
}

function SectionCard({ title, icon, children, expanded, onToggle }){
  return (
    <Card className="mb-4 border-slate-200 dark:border-slate-800">
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-100 dark:border-slate-800">
        <div className="flex items-center gap-2"><span>{icon}</span><h2 className="font-medium">{title}</h2></div>
        <Button variant="ghost" size="sm" onClick={onToggle} className="gap-1">
          {expanded ? <ChevronDown className="w-4 h-4"/> : <ChevronRight className="w-4 h-4"/>}
          {expanded ? 'Collapse' : 'Expand'}
        </Button>
      </div>
      {expanded && <CardContent className="p-4">{children}</CardContent>}
    </Card>
  );
}

// ---- Category & Material management ----
function CategoryManager({ data, setData, t, lang }){
  const [newCat, setNewCat] = useState("");

  const addCategory = () => {
    if (!newCat.trim()) return;
    setData(d => ({...d, categories: [...d.categories, { id: uid(), name: newCat.trim(), subs: [] }]}));
    setNewCat("");
  };

  const deleteCategory = (cid) => {
    setData(d => ({...d, categories: d.categories.filter(c => c.id !== cid)}));
  };

  const addSub = (cid, name) => {
    if (!name.trim()) return;
    setData(d => ({...d, categories: d.categories.map(c => c.id===cid?{...c, subs:[...c.subs, {id: uid(), name: name.trim(), materials: []}]}:c)}));
  };

  const deleteSub = (cid, sid) => {
    setData(d => ({...d, categories: d.categories.map(c => c.id===cid?{...c, subs: c.subs.filter(s=>s.id!==sid)}:c)}));
  };

  return (
    <div className="space-y-4">
      <div className="flex gap-2">
        <Input placeholder={t.addCategory} value={newCat} onChange={e=>setNewCat(e.target.value)} />
        <Button onClick={addCategory} className="shrink-0"><Plus className="w-4 h-4 mr-1"/>{t.addCategory}</Button>
      </div>

      <div className="space-y-3">
        {data.categories.map(cat => (
          <CategoryItem key={cat.id} cat={cat} onDelete={()=>deleteCategory(cat.id)} onAddSub={addSub} onDeleteSub={deleteSub} data={data} setData={setData} t={t} lang={lang} />
        ))}
      </div>
    </div>
  );
}

function CategoryItem({ cat, onDelete, onAddSub, onDeleteSub, data, setData, t, lang }){
  const [subName, setSubName] = useState("");
  const [open, setOpen] = useState(true);

  const addMaterialAtRoot = (title, url) => {
    if (!title.trim()) return;
    const mat = { id: uid(), title: title.trim(), url: url?.trim()||"", clicks: 0, lastClickedAt: null, history: [] };
    setData(d => ({...d, categories: d.categories.map(c=> c.id===cat.id?{...c, subs: c.subs.length?c.subs:[{id: uid(), name: "General", materials: []}],
      // if no subs, attach to implicit 'General'
      subs: c.subs.length? c.subs: [{id: uid(), name: "General", materials: []}] }: c)}));
  };

  return (
    <div className="rounded-2xl border p-3 border-slate-200 dark:border-slate-800">
      <div className="flex items-center justify-between">
        <div className="font-medium">{cat.name}</div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={()=>setOpen(o=>!o)}>{open?TL[lang].collapse:TL[lang].expand}</Button>
          <Button variant="destructive" size="sm" onClick={onDelete}><Trash2 className="w-4 h-4"/></Button>
        </div>
      </div>
      {open && (
        <div className="mt-3 space-y-3">
          <div className="flex gap-2">
            <Input placeholder={t.addSub} value={subName} onChange={e=>setSubName(e.target.value)} />
            <Button onClick={()=>{ onAddSub(cat.id, subName); setSubName(""); }}><Plus className="w-4 h-4 mr-1"/>{t.addSub}</Button>
          </div>
          <div className="grid md:grid-cols-2 gap-3">
            {(cat.subs.length?cat.subs:[{id:"__root__", name:"General", materials: []}]).map(sub => (
              <SubCategoryItem key={sub.id} catId={cat.id} sub={sub} onDeleteSub={onDeleteSub} data={data} setData={setData} t={t} lang={lang} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function SubCategoryItem({ catId, sub, onDeleteSub, data, setData, t, lang }){
  const [title, setTitle] = useState("");
  const [url, setUrl] = useState("");

  const addMat = () => {
    if (!title.trim()) return;
    const mat = { id: uid(), title: title.trim(), url: url.trim(), clicks: 0, lastClickedAt: null, history: [] };
    setData(d => ({...d, categories: d.categories.map(c => c.id===catId?{...c, subs: c.subs.map(s => s.id===sub.id?{...s, materials:[...s.materials, mat]}:s)}:c)}));
    setTitle(""); setUrl("");
  };

  const deleteMat = (mid) => {
    setData(d => ({...d, categories: d.categories.map(c => c.id===catId?{...c, subs: c.subs.map(s => s.id===sub.id?{...s, materials: s.materials.filter(m=>m.id!==mid)}:s)}:c)}));
  };

  const clickMat = (mid) => {
    const now = todayISO();
    setData(d => ({...d, categories: d.categories.map(c => c.id===catId?{...c, subs: c.subs.map(s => s.id===sub.id?{...s, materials: s.materials.map(m=> m.id===mid?{...m, clicks:(m.clicks||0)+1, lastClickedAt: now, history:[...m.history, {ts: now}]}:m)}:s)}:c)}));
  };

  return (
    <div className="border rounded-xl p-3 border-slate-200 dark:border-slate-800">
      <div className="flex items-center justify-between mb-2">
        <div className="font-medium">{sub.name}</div>
        {sub.id!=="__root__" && (
          <Button variant="destructive" size="sm" onClick={()=>onDeleteSub(catId, sub.id)}><Trash2 className="w-4 h-4"/></Button>
        )}
      </div>
      <div className="flex flex-col sm:flex-row gap-2 mb-3">
        <Input placeholder={t.title} value={title} onChange={e=>setTitle(e.target.value)} />
        <Input placeholder={t.pathUrl} value={url} onChange={e=>setUrl(e.target.value)} />
        <Button onClick={addMat} className="shrink-0"><Plus className="w-4 h-4 mr-1"/>{t.addMaterial}</Button>
      </div>
      <div className="space-y-2">
        {sub.materials.length===0 && <div className="text-sm text-slate-500">No materials yet.</div>}
        {sub.materials.map(m => (
          <div key={m.id} className="flex items-center justify-between gap-2 rounded-lg border px-3 py-2 hover:bg-slate-50 dark:hover:bg-slate-900 border-slate-200 dark:border-slate-800">
            <div className="min-w-0">
              <div className="truncate font-medium">{m.title}</div>
              <div className="text-xs text-slate-500 break-all">
                {m.url && <a className="underline" href={m.url} target="_blank" rel="noreferrer">{m.url}</a>}
              </div>
              <div className="text-xs mt-1">[{m.lastClickedAt?fmtDateTime(m.lastClickedAt, lang):'-'} : {m.clicks||0}]</div>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" onClick={()=>clickMat(m.id)}>{TL[lang].clickIt}</Button>
              {m.url && <Button variant="secondary" size="sm" asChild><a href={m.url} target="_blank" rel="noreferrer">{TL[lang].open}</a></Button>}
              <Button variant="destructive" size="sm" onClick={()=>deleteMat(m.id)}><Trash2 className="w-4 h-4"/></Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ---- Dashboard ----
function Dashboard({ data, t, lang }){
  const [range, setRange] = useState('monthly');
  const start = useMemo(()=>startOf(range), [range]);

  // Flatten material history
  const events = useMemo(() => {
    const arr = [];
    for (const c of data.categories) {
      for (const s of c.subs) {
        for (const m of s.materials) {
          for (const h of (m.history||[])) {
            const ts = new Date(h.ts);
            if (ts >= start) {
              arr.push({ ts, cat: c.name, sub: s.name, matId: m.id, title: m.title });
            }
          }
        }
      }
    }
    return arr.sort((a,b)=>a.ts-b.ts);
  }, [data, start]);

  // Group by day for line chart
  const series = useMemo(() => {
    const map = new Map(); // key: yyyy-mm-dd
    for (const e of events) {
      const d = e.ts.toISOString().slice(0,10);
      const key = d+"|"+e.title;
      map.set(key, (map.get(key)||0)+1);
    }
    // Build dataset per title (stacked lines as separate series labels in legend)
    const days = [...new Set(events.map(e=>e.ts.toISOString().slice(0,10)))].sort();
    const titles = [...new Set(events.map(e=>e.title))];
    const rows = days.map(day => {
      const row = { day };
      for (const t of titles) row[t] = 0;
      for (const t2 of titles) {
        const k = day+"|"+t2; if (map.has(k)) row[t2] = map.get(k);
      }
      return row;
    });
    return { rows, titles };
  }, [events]);

  // Totals per material for bar chart
  const totals = useMemo(()=>{
    const map = new Map();
    for (const e of events) {
      map.set(e.title, (map.get(e.title)||0)+1);
    }
    return [...map.entries()].map(([title, count])=>({ title, count }));
  }, [events]);

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <Label className="text-sm">{t.timeRange}</Label>
        <Tabs value={range} onValueChange={setRange} className="w-full">
          <TabsList className="flex flex-wrap">
            {['daily','weekly','monthly','3-monthly','yearly','all'].map(key => (
              <TabsTrigger key={key} value={key} className="capitalize">{key}</TabsTrigger>
            ))}
          </TabsList>
        </Tabs>
      </div>

      <div className="grid lg:grid-cols-2 gap-4">
        <Card className="border-slate-200 dark:border-slate-800">
          <CardContent className="p-3">
            <div className="font-medium mb-2">{t.timeSeries}</div>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={series.rows} margin={{top:10,right:10,left:0,bottom:10}}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="day" tick={{fontSize:12}}/>
                  <YAxis allowDecimals={false}/>
                  <Tooltip />
                  <Legend />
                  {series.titles.map(name => (
                    <Line key={name} type="monotone" dataKey={name} dot={false} />
                  ))}
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card className="border-slate-200 dark:border-slate-800">
          <CardContent className="p-3">
            <div className="font-medium mb-2">{t.barTotals}</div>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={totals} margin={{top:10,right:10,left:0,bottom:10}}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="title" tick={{fontSize:12}} interval={0} angle={-20} textAnchor="end" height={70}/>
                  <YAxis allowDecimals={false}/>
                  <Tooltip />
                  <Bar dataKey="count" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

// ---- Tasks ----
function isDue(task, now=new Date()){
  if (task.completedAt && (!task.interval && !task.date)) return false; // completed one-off
  const last = task.lastDoneAt ? new Date(task.lastDoneAt) : null;
  if (task.interval){
    // due if never done, or last < start of interval
    const d = new Date(now);
    if (task.interval==='daily') d.setHours(0,0,0,0);
    if (task.interval==='weekly') { const tmp = new Date(now); const dow=(tmp.getDay()+6)%7; d.setDate(tmp.getDate()-dow); d.setHours(0,0,0,0); }
    if (task.interval==='monthly') { d.setDate(1); d.setHours(0,0,0,0); }
    return !last || last < d;
  }
  if (task.date){
    const due = new Date(task.date);
    return due.toDateString() === now.toDateString() || due < now; // show on day and if overdue
  }
  return true; // always visible
}

function TasksSection({ data, setData, t, lang }){
  const [text, setText] = useState("");
  const [date, setDate] = useState("");
  const [interval, setInterval] = useState("none");

  const addTask = () => {
    if (!text.trim()) return;
    const task = { id: uid(), text: text.trim(), date: date? new Date(date).toISOString(): null, interval: interval==='none'? null: interval, completedAt: null, lastDoneAt: null };
    setData(d=>({...d, tasks:[...d.tasks, task]}));
    setText(""); setDate(""); setInterval("none");
  };

  const toggleDone = (id) => {
    setData(d=>({...d, tasks: d.tasks.map(tk => tk.id===id ? ({...tk, completedAt: tk.completedAt? null : todayISO(), lastDoneAt: todayISO()}) : tk)}));
  };

  const removeTask = (id) => setData(d=>({...d, tasks: d.tasks.filter(tk=>tk.id!==id)}));

  const now = new Date();
  const current = data.tasks.filter(tk => isDue(tk, now));
  const history = data.tasks.filter(tk => !isDue(tk, now));

  return (
    <div className="space-y-4">
      <div className="grid md:grid-cols-4 gap-2">
        <Input className="md:col-span-2" placeholder={t.taskText} value={text} onChange={e=>setText(e.target.value)} />
        <Input type="date" value={date} onChange={e=>setDate(e.target.value)} title={t.dueDate} />
        <Select value={interval} onValueChange={setInterval}>
          <SelectTrigger>
            <SelectValue placeholder={t.interval} />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="none">{t.none}</SelectItem>
            <SelectItem value="daily">{t.daily}</SelectItem>
            <SelectItem value="weekly">{t.weekly}</SelectItem>
            <SelectItem value="monthly">{t.monthly}</SelectItem>
          </SelectContent>
        </Select>
      </div>
      <div className="flex gap-2">
        <Button onClick={addTask}><Plus className="w-4 h-4 mr-1"/>{t.newTask}</Button>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <Card className="border-slate-200 dark:border-slate-800">
          <CardContent className="p-3 space-y-2">
            <div className="font-medium">{t.visibleNow}</div>
            {current.length===0 && <div className="text-sm text-slate-500">—</div>}
            {current.map(task => (
              <TaskRow key={task.id} task={task} lang={lang} t={t} onToggle={()=>toggleDone(task.id)} onRemove={()=>removeTask(task.id)} />
            ))}
          </CardContent>
        </Card>
        <Card className="border-slate-200 dark:border-slate-800">
          <CardContent className="p-3 space-y-2">
            <div className="font-medium">{t.history}</div>
            {history.length===0 && <div className="text-sm text-slate-500">—</div>}
            {history.map(task => (
              <TaskRow key={task.id} task={task} lang={lang} t={t} onToggle={()=>toggleDone(task.id)} onRemove={()=>removeTask(task.id)} />
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function TaskRow({ task, t, lang, onToggle, onRemove }){
  const dueLabel = task.date ? fmtDate(task.date, lang) : (task.interval ? TL[lang][task.interval] : TL[lang].alwaysVisible);
  return (
    <div className="flex items-center justify-between gap-2 rounded-lg border px-3 py-2 border-slate-200 dark:border-slate-800">
      <div className="min-w-0">
        <div className="truncate">{task.text}</div>
        <div className="text-xs text-slate-500">{dueLabel}</div>
      </div>
      <div className="flex items-center gap-2">
        <label className="flex items-center gap-2 text-sm">
          <input type="checkbox" className="w-4 h-4" checked={!!task.completedAt && !task.interval && !task.date ? true : false} onChange={onToggle} />
          <span>{t.completed}</span>
        </label>
        <Button variant="destructive" size="sm" onClick={onRemove}><Trash2 className="w-4 h-4"/></Button>
      </div>
    </div>
  );
}

// ---- Import / Export ----
function ImportExport({ data, setData, t }){
  const fileRef = useRef(null);

  const exportJSON = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], {type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'study_app_data.json'; a.click();
    URL.revokeObjectURL(url);
  };

  const importJSON = (file) => {
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const obj = JSON.parse(reader.result);
        if (obj && obj.categories && obj.tasks) setData(obj);
      } catch (e) { alert('Invalid JSON'); }
    };
    reader.readAsText(file);
  };

  const clearAll = () => {
    if (confirm('Clear all data?')) setData(DEFAULT_DATA);
  };

  return (
    <div className="flex flex-wrap items-center gap-2 mt-4">
      <Button onClick={exportJSON} variant="outline" className="gap-2"><Download className="w-4 h-4"/>{t.export}</Button>
      <input type="file" accept="application/json" hidden ref={fileRef} onChange={e=>{ const f=e.target.files?.[0]; if (f) importJSON(f); e.target.value=''; }} />
      <Button onClick={()=>fileRef.current?.click()} variant="outline" className="gap-2"><Upload className="w-4 h-4"/>{t.import}</Button>
      <Button onClick={clearAll} variant="destructive" className="gap-2"><Trash2 className="w-4 h-4"/>{t.clearAll}</Button>
    </div>
  );
}
