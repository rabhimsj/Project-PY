import { useState, type FormEvent } from 'react'
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import {
  ArrowUpRight,
  BookOpen,
  BrainCircuit,
  Briefcase,
  CalendarCheck2,
  CheckCircle2,
  GraduationCap,
  LayoutDashboard,
  MessageSquareText,
  NotebookPen,
  Sparkles,
  Upload,
  UserRound,
} from 'lucide-react'
import { NavLink, Route, Routes } from 'react-router-dom'

const overviewCards = [
  { label: 'Attendance', value: '87.4%', delta: '+4.1%', icon: CalendarCheck2, accent: 'bg-emerald-500/10 text-emerald-600' },
  { label: 'Average Marks', value: '86.8%', delta: '+3.2%', icon: BookOpen, accent: 'bg-blue-500/10 text-blue-600' },
  { label: 'Study Plan', value: '7 days', delta: 'On track', icon: NotebookPen, accent: 'bg-violet-500/10 text-violet-600' },
  { label: 'Career Readiness', value: '72%', delta: 'Strong', icon: Briefcase, accent: 'bg-amber-500/10 text-amber-600' },
]

const attendanceData = [
  { name: 'Jan', value: 75 },
  { name: 'Feb', value: 78 },
  { name: 'Mar', value: 81 },
  { name: 'Apr', value: 84 },
  { name: 'May', value: 87 },
  { name: 'Jun', value: 89 },
]

const marksData = [
  { name: 'AI', score: 92 },
  { name: 'DBMS', score: 84 },
  { name: 'DSA', score: 88 },
  { name: 'OS', score: 79 },
  { name: 'Math', score: 91 },
]

const pieData = [
  { name: 'Strong', value: 52 },
  { name: 'Moderate', value: 33 },
  { name: 'Needs work', value: 15 },
]

const chartColors = ['#22c55e', '#3b82f6', '#f59e0b']

const messages = [
  { from: 'AI', text: 'Your latest revision notes show strong understanding of graph theory. Revise dynamic programming with 2 timed drills today.' },
  { from: 'You', text: 'Give me a quick summary of my SQL revision plan and expected exam questions.' },
]

const docs = [
  { name: 'DBMS_Notes.pdf', type: 'Study material', status: 'Indexed' },
  { name: 'AI_Revision.txt', type: 'Lecture notes', status: 'Ready' },
  { name: 'Placement_Resume.pdf', type: 'Career file', status: 'Analyzed' },
]

const studyPlan = [
  { day: 'Mon', topic: 'DSA Practice', hours: '2.5h' },
  { day: 'Tue', topic: 'DBMS Revision', hours: '2h' },
  { day: 'Wed', topic: 'AI Concepts', hours: '3h' },
  { day: 'Thu', topic: 'Mock Quiz', hours: '2h' },
  { day: 'Fri', topic: 'Interview Prep', hours: '1.5h' },
]

const sidebarItems = [
  { label: 'Dashboard', to: '/', icon: LayoutDashboard },
  { label: 'AI Chat', to: '/ai-chat', icon: MessageSquareText },
  { label: 'Documents', to: '/documents', icon: Upload },
  { label: 'Study Plan', to: '/study-plan', icon: NotebookPen },
  { label: 'Career', to: '/career', icon: Briefcase },
  { label: 'Profile', to: '/profile', icon: UserRound },
]

function PageHeader({ title, subtitle, actions }: { title: string; subtitle: string; actions?: React.ReactNode }) {
  return (
    <header className="mb-6 flex flex-col gap-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="text-sm text-slate-500">Welcome back</p>
        <h2 className="text-2xl font-semibold text-slate-900">{title}</h2>
        <p className="text-sm text-slate-500">{subtitle}</p>
      </div>
      {actions}
    </header>
  )
}

function DashboardPage() {
  return (
    <>
      <PageHeader
        title="Student dashboard"
        subtitle="Overview of your academic progress"
        actions={
          <div className="flex items-center gap-3">
            <button className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm font-medium text-slate-700">
              This week
            </button>
            <button className="flex items-center gap-2 rounded-xl bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500">
              <Sparkles className="h-4 w-4" />
              Generate AI plan
            </button>
          </div>
        }
      />

      <div className="mb-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {overviewCards.map(({ label, value, delta, icon: Icon, accent }) => (
          <div key={label} className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
            <div className="mb-4 flex items-center justify-between">
              <div className={`rounded-xl p-2 ${accent}`}>
                <Icon className="h-5 w-5" />
              </div>
              <span className="text-xs font-semibold text-emerald-600">{delta}</span>
            </div>
            <p className="text-sm text-slate-500">{label}</p>
            <p className="mt-2 text-3xl font-bold text-slate-900">{value}</p>
          </div>
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.5fr_1fr]">
        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-slate-900">Attendance trend</h3>
              <p className="text-sm text-slate-500">Strong consistency across the last 6 months</p>
            </div>
            <div className="rounded-xl bg-emerald-50 px-2.5 py-1.5 text-xs font-semibold text-emerald-700">+12% from last term</div>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={attendanceData}>
                <defs>
                  <linearGradient id="attendanceFill" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="5%" stopColor="#22c55e" stopOpacity={0.5} />
                    <stop offset="95%" stopColor="#22c55e" stopOpacity={0.08} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="name" tickLine={false} axisLine={false} />
                <YAxis tickLine={false} axisLine={false} domain={[60, 100]} />
                <Tooltip />
                <Area type="monotone" dataKey="value" stroke="#16a34a" strokeWidth={3} fill="url(#attendanceFill)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-slate-900">Academic balance</h3>
              <p className="text-sm text-slate-500">Subject performance snapshot</p>
            </div>
            <CheckCircle2 className="h-5 w-5 text-emerald-500" />
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} dataKey="value" innerRadius={52} outerRadius={78} paddingAngle={4}>
                  {pieData.map((entry, index) => (
                    <Cell key={entry.name} fill={chartColors[index]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-2 space-y-2 text-sm text-slate-600">
            {pieData.map((item, index) => (
              <div key={item.name} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: chartColors[index] }} />
                  {item.name}
                </div>
                <span className="font-medium">{item.value}%</span>
              </div>
            ))}
          </div>
        </section>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[1.3fr_1fr]">
        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-slate-900">Recent marks</h3>
              <p className="text-sm text-slate-500">Performance and subject scores</p>
            </div>
            <button className="flex items-center gap-1 text-sm font-medium text-indigo-600">
              View analytics <ArrowUpRight className="h-4 w-4" />
            </button>
          </div>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={marksData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="name" tickLine={false} axisLine={false} />
                <YAxis domain={[0, 100]} tickLine={false} axisLine={false} />
                <Tooltip />
                <Bar dataKey="score" radius={[8, 8, 0, 0]} fill="#6366f1" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-slate-900">AI assistant</h3>
              <p className="text-sm text-slate-500">Latest academic guidance</p>
            </div>
            <BrainCircuit className="h-5 w-5 text-indigo-600" />
          </div>
          <div className="space-y-3">
            {messages.map((message, index) => (
              <div key={index} className={`rounded-xl p-3 text-sm ${message.from === 'AI' ? 'bg-indigo-50 text-slate-700' : 'bg-slate-100 text-slate-700'}`}>
                <span className="mb-1 block font-semibold text-slate-900">{message.from}</span>
                {message.text}
              </div>
            ))}
          </div>
          <div className="mt-4 flex gap-2">
            <input
              value="Ask about the revision plan"
              readOnly
              className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-500"
            />
            <button className="rounded-xl bg-indigo-600 px-3 py-2 text-sm font-semibold text-white">Send</button>
          </div>
        </section>
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-slate-900">Uploaded documents</h3>
              <p className="text-sm text-slate-500">Indexed and ready for RAG search</p>
            </div>
            <button className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-1.5 text-sm font-medium text-slate-700">Upload</button>
          </div>
          <div className="space-y-3">
            {docs.map((doc) => (
              <div key={doc.name} className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50 p-3">
                <div>
                  <p className="font-medium text-slate-800">{doc.name}</p>
                  <p className="text-xs text-slate-500">{doc.type}</p>
                </div>
                <span className="rounded-full bg-emerald-100 px-2.5 py-1 text-xs font-semibold text-emerald-700">{doc.status}</span>
              </div>
            ))}
          </div>
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-slate-900">Weekly study plan</h3>
              <p className="text-sm text-slate-500">Personalized revision schedule</p>
            </div>
            <GraduationCap className="h-5 w-5 text-cyan-600" />
          </div>
          <div className="space-y-3">
            {studyPlan.map((item) => (
              <div key={item.day} className="flex items-center justify-between rounded-xl border border-slate-200 bg-slate-50 p-3">
                <div>
                  <p className="font-medium text-slate-800">{item.day}</p>
                  <p className="text-xs text-slate-500">{item.topic}</p>
                </div>
                <span className="rounded-full bg-cyan-100 px-2.5 py-1 text-xs font-semibold text-cyan-700">{item.hours}</span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </>
  )
}

function ChatPage() {
  const [chatMessages, setChatMessages] = useState<Array<{from: string, text: string}>>([])
  const [input, setInput] = useState('Explain dynamic programming with an exam-focused approach')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    const trimmed = input.trim()
    if (!trimmed || isLoading) return

    const userMessage = { from: 'You', text: trimmed }
    setChatMessages((previous) => [...previous, userMessage])
    setInput('')
    setError('')
    setIsLoading(true)

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: trimmed, conversation_id: null }),
      })

      if (!response.ok) {
        const data = await response.json().catch(() => ({}))
        throw new Error(data.detail || 'Unable to get a response from the AI assistant.')
      }

      const data = await response.json()
      const aiText = data.response || data.reply || data.message || data.answer || "No response received"

      setChatMessages((previous) => [...previous, { from: 'AI', text: aiText }])
    } catch (fetchError) {
      setError(fetchError instanceof Error ? fetchError.message : 'Failed to reach the AI assistant.')
      setChatMessages((previous) => [...previous, { from: 'AI', text: 'Sorry, I could not reach the CampusMind AI backend right now. Please try again.' }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      <PageHeader title="AI Chat" subtitle="Ask academic questions and get contextual guidance" />
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="space-y-3">
          {chatMessages.map((message, index) => (
            <div key={`${message.from}-${index}`} className={`rounded-xl p-3 text-sm ${message.from === 'AI' ? 'bg-indigo-50 text-slate-700' : 'bg-slate-100 text-slate-700'}`}>
              <span className="mb-1 block font-semibold text-slate-900">{message.from}</span>
              {message.text}
            </div>
          ))}
        </div>

        {error && <p className="mt-4 rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}

        <form onSubmit={handleSubmit} className="mt-6 flex gap-2">
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Ask about your studies, attendance, career growth, or revision plan"
            className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700 outline-none ring-0 placeholder:text-slate-400 focus:border-indigo-300"
          />
          <button
            type="submit"
            disabled={isLoading}
            className="rounded-xl bg-indigo-600 px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-indigo-400"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </div>
    </>
  )
}

function DocumentsPage() {
  return (
    <>
      <PageHeader title="Documents" subtitle="Upload and manage your study materials" actions={<button className="rounded-xl bg-indigo-600 px-4 py-2 text-sm font-semibold text-white">Upload file</button>} />
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {docs.map((doc) => (
          <div key={doc.name} className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
            <div className="mb-3 flex items-center justify-between">
              <Upload className="h-5 w-5 text-indigo-600" />
              <span className="rounded-full bg-emerald-100 px-2.5 py-1 text-xs font-semibold text-emerald-700">{doc.status}</span>
            </div>
            <p className="font-medium text-slate-800">{doc.name}</p>
            <p className="mt-1 text-sm text-slate-500">{doc.type}</p>
          </div>
        ))}
      </div>
    </>
  )
}

function StudyPlanPage() {
  return (
    <>
      <PageHeader title="Study Plan" subtitle="Your weekly revision roadmap" />
      <div className="space-y-3">
        {studyPlan.map((item) => (
          <div key={item.day} className="flex items-center justify-between rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
            <div>
              <p className="font-semibold text-slate-800">{item.day}</p>
              <p className="text-sm text-slate-500">{item.topic}</p>
            </div>
            <span className="rounded-full bg-cyan-100 px-2.5 py-1 text-xs font-semibold text-cyan-700">{item.hours}</span>
          </div>
        ))}
      </div>
    </>
  )
}

function CareerPage() {
  return (
    <>
      <PageHeader title="Career" subtitle="Career readiness and placement support" />
      <div className="grid gap-6 md:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Skill gap analysis</h3>
          <ul className="mt-4 space-y-2 text-sm text-slate-600">
            <li>• SQL and system design are strengths</li>
            <li>• Data structures needs more timed practice</li>
            <li>• Resume formatting can be improved</li>
          </ul>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-900">Recommended roadmap</h3>
          <ul className="mt-4 space-y-2 text-sm text-slate-600">
            <li>• 3 mock interviews this month</li>
            <li>• 2 project improvements</li>
            <li>• AI/ML fundamental revision</li>
          </ul>
        </div>
      </div>
    </>
  )
}

function ProfilePage() {
  return (
    <>
      <PageHeader title="Profile" subtitle="Academic profile and personal details" />
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-center gap-4">
          <div className="flex h-14 w-14 items-center justify-center rounded-full bg-indigo-100 text-lg font-bold text-indigo-600">S</div>
          <div>
            <h3 className="text-xl font-semibold text-slate-900">Demo Student</h3>
            <p className="text-sm text-slate-500">B.Tech Computer Science • Semester 6</p>
          </div>
        </div>
        <div className="mt-6 grid gap-4 md:grid-cols-2 text-sm text-slate-600">
          <div className="rounded-xl bg-slate-50 p-3">Branch: CSE</div>
          <div className="rounded-xl bg-slate-50 p-3">Target role: Software Engineer</div>
          <div className="rounded-xl bg-slate-50 p-3">Skills: Python, React, SQL</div>
          <div className="rounded-xl bg-slate-50 p-3">Interests: AI, Data Structures, ML</div>
        </div>
      </div>
    </>
  )
}

function App() {
  return (
    <div className="min-h-screen bg-slate-100 text-slate-800">
      <div className="flex min-h-screen flex-col lg:flex-row">
        <aside className="w-full border-b border-slate-200 bg-slate-900 p-5 text-white lg:w-72 lg:border-b-0 lg:border-r">
          <div className="mb-8 flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400">
              <BrainCircuit className="h-5 w-5" />
            </div>
            <div>
              <h1 className="text-lg font-semibold">CampusMind AI</h1>
              <p className="text-xs text-slate-300">Student Success Suite</p>
            </div>
          </div>

          <nav className="space-y-2">
            {sidebarItems.map(({ label, to, icon: Icon }) => (
              <NavLink
                key={label}
                to={to}
                end={to === '/'}
                className={({ isActive }) =>
                  `flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-sm font-medium transition ${
                    isActive ? 'bg-white/10 text-white' : 'text-slate-300 hover:bg-white/5 hover:text-white'
                  }`
                }
              >
                <Icon className="h-4 w-4" />
                {label}
              </NavLink>
            ))}
          </nav>

          <div className="mt-8 rounded-2xl border border-slate-700 bg-slate-800/80 p-4">
            <div className="mb-3 flex items-center gap-2 text-cyan-300">
              <Sparkles className="h-4 w-4" />
              <span className="text-sm font-medium">AI Insight</span>
            </div>
            <p className="text-sm text-slate-300">
              Focus on SQL and algorithmic revision this week to improve exam confidence and placement readiness.
            </p>
          </div>
        </aside>

        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/ai-chat" element={<ChatPage />} />
            <Route path="/documents" element={<DocumentsPage />} />
            <Route path="/study-plan" element={<StudyPlanPage />} />
            <Route path="/career" element={<CareerPage />} />
            <Route path="/profile" element={<ProfilePage />} />
          </Routes>
        </main>
      </div>
    </div>
  )
}

export default App
