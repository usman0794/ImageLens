import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

const lineDot = { r: 5 }
const activeLineDot = { r: 7 }
const barRadius = [10, 10, 0, 0]

function DashboardCharts({ searchesOverTime = [], topCategories = [] }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <section className="glass-panel p-5">
        <h2 className="mb-5 text-lg font-black">Searches over time</h2>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={searchesOverTime}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,.25)" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="searches" stroke="#3386ff" strokeWidth={3} dot={lineDot} activeDot={activeLineDot} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>

      <section className="glass-panel p-5">
        <h2 className="mb-5 text-lg font-black">Top categories</h2>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={topCategories}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,.25)" />
              <XAxis dataKey="category" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#3386ff" radius={barRadius} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>
    </div>
  )
}

export default DashboardCharts
