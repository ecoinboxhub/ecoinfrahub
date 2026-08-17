import { useState, useEffect, useRef, useCallback } from 'react'
import { checkHealth, getMetrics, getLanguages, runCalculator, sendChatMessage } from './api'

const SHAPES = {
  area: ['rectangle', 'circle', 'triangle', 'trapezoid'],
  volume: ['cube', 'cylinder', 'sphere', 'cone'],
}

const UNITS_BY_CATEGORY = {
  Length: ['mm', 'cm', 'm', 'km', 'in', 'ft', 'yd', 'mi'],
  Area: ['mm2', 'cm2', 'm2', 'ha', 'km2', 'in2', 'ft2', 'ac'],
  Volume: ['ml', 'l', 'm3', 'gal', 'ft3', 'yd3'],
  Pressure: ['pa', 'kpa', 'mpa', 'bar', 'psi', 'atm'],
  Mass: ['g', 'kg', 't', 'lb'],
  Temperature: ['c', 'f', 'k'],
}

const CALCULATORS = {
  concrete_mix: {
    label: 'Concrete Mix',
    fields: [
      { key: 'cement', label: 'Cement (kg)', type: 'number', default: 350 },
      { key: 'sand', label: 'Sand (kg)', type: 'number', default: 700 },
      { key: 'aggregate', label: 'Aggregate (kg)', type: 'number', default: 1400 },
      { key: 'water', label: 'Water (kg)', type: 'number', default: 175 },
    ],
    results: {
      primary: 'ratio',
      labels: {
        ratio: 'Mix ratio (C:S:A)',
        water_cement_ratio: 'Water–cement ratio',
        total: 'Total material (kg)',
      },
    },
  },
  pavement_thickness: {
    label: 'Pavement Thickness',
    fields: [
      { key: 'cbr', label: 'CBR (%)', type: 'number', default: 15 },
      { key: 'traffic_esa', label: 'Traffic ESA', type: 'number', default: 5000000 },
      { key: 'reliability', label: 'Reliability (%)', type: 'number', default: 90 },
    ],
    results: {
      primary: 'surface_thickness_mm',
      labels: {
        structural_number: 'Structural Number (SN)',
        surface_thickness_mm: 'Surface thickness (mm)',
        base_thickness_mm: 'Base thickness (mm)',
        subbase_thickness_mm: 'Subbase thickness (mm)',
        reliability_percent: 'Reliability (%)',
      },
    },
  },
  drainage: {
    label: 'Drainage Flow',
    fields: [
      { key: 'area_ha', label: 'Area (ha)', type: 'number', default: 50 },
      { key: 'runoff_coefficient', label: 'Runoff Coeff (C)', type: 'number', default: 0.6, step: 0.05 },
      { key: 'rainfall_intensity_mm_hr', label: 'Rainfall (mm/hr)', type: 'number', default: 50 },
    ],
    results: {
      primary: 'peak_flow_m3_s',
      labels: {
        peak_flow_m3_s: 'Peak flow (m³/s)',
        peak_flow_l_s: 'Peak flow (L/s)',
        area_ha: 'Catchment area (ha)',
        runoff_coefficient: 'Runoff coefficient',
      },
    },
  },
  bearing_capacity: {
    label: 'Bearing Capacity',
    fields: [
      { key: 'cohesion', label: 'Cohesion (kPa)', type: 'number', default: 25 },
      { key: 'unit_weight', label: 'Soil Unit Weight (kN/m³)', type: 'number', default: 18 },
      { key: 'phi_deg', label: 'Friction Angle (°)', type: 'number', default: 30 },
      { key: 'width', label: 'Width (m)', type: 'number', default: 1.5 },
      { key: 'depth', label: 'Depth (m)', type: 'number', default: 1.0 },
      { key: 'safety_factor', label: 'Safety Factor', type: 'number', default: 3.0 },
    ],
    results: {
      primary: 'allowable_capacity_kpa',
      labels: {
        cohesion_kpa: 'Cohesion (kPa)',
        phi_deg: 'Friction angle (°)',
        width_m: 'Footing width (m)',
        depth_m: 'Footing depth (m)',
        ultimate_capacity_kpa: 'Ultimate capacity (kPa)',
        allowable_capacity_kpa: 'Allowable capacity (kPa)',
        safety_factor: 'Safety factor',
      },
    },
  },
  traffic_volume: {
    label: 'Traffic Volume',
    fields: [
      { key: 'vehicle_count', label: 'Vehicles counted', type: 'number', default: 120 },
      { key: 'observation_time_minutes', label: 'Observation time (min)', type: 'number', default: 15 },
    ],
    results: {
      primary: 'hourly_volume',
      labels: {
        hourly_volume: 'Hourly volume (veh/hr)',
        daily_estimate: 'Daily estimate (veh/day)',
        vehicle_count: 'Vehicles counted',
        observation_time_minutes: 'Observation time (min)',
      },
    },
  },
  aadt: {
    label: 'AADT (Annual Avg Daily Traffic)',
    fields: [
      { key: 'daily_counts', label: 'Daily counts (comma-separated)', type: 'csv', default: '500, 600, 550' },
      { key: 'adjustment_factor', label: 'Adjustment factor', type: 'number', default: 1.1 },
    ],
    results: {
      primary: 'aadt',
      labels: {
        aadt: 'AADT (veh/day)',
        average_daily_traffic: 'Avg daily traffic',
        total_vehicles: 'Total vehicles',
        days_sampled: 'Days sampled',
        adjustment_factor: 'Adjustment factor',
      },
    },
  },
  earthwork: {
    label: 'Earthwork Volume',
    fields: [
      { key: 'length', label: 'Length (m)', type: 'number', default: 100 },
      { key: 'width', label: 'Width (m)', type: 'number', default: 8 },
      { key: 'depth', label: 'Depth (m)', type: 'number', default: 0.5 },
      { key: 'swell_factor', label: 'Swell factor', type: 'number', default: 1.25 },
    ],
    results: {
      primary: 'bank_volume_m3',
      labels: {
        bank_volume_m3: 'Bank volume (m³)',
        loose_volume_m3: 'Loose volume (m³)',
        compacted_volume_m3: 'Compacted volume (m³)',
        length_m: 'Length (m)',
        width_m: 'Width (m)',
      },
    },
  },
  unit_conversion: {
    label: 'Unit Conversion',
    fields: [
      { key: 'value', label: 'Value', type: 'number', default: 1 },
      { key: 'category', label: 'Category', type: 'select', default: 'Length', options: Object.keys(UNITS_BY_CATEGORY), uiOnly: true },
      { key: 'from_unit', label: 'From unit', type: 'select', default: 'm', depends: 'category', options: UNITS_BY_CATEGORY },
      { key: 'to_unit', label: 'To unit', type: 'select', default: 'ft', depends: 'category', options: UNITS_BY_CATEGORY },
    ],
    results: {
      primary: 'result',
      labels: { result: 'Converted value', category: 'Category' },
    },
  },
  area: {
    label: 'Area',
    fields: [
      { key: 'shape', label: 'Shape', type: 'select', default: 'rectangle', options: SHAPES.area, variant: true },
      { key: 'length', label: 'Length (m)', type: 'number', default: 10, shapes: ['rectangle'] },
      { key: 'width', label: 'Width (m)', type: 'number', default: 5, shapes: ['rectangle'] },
      { key: 'radius', label: 'Radius (m)', type: 'number', default: 3, shapes: ['circle'] },
      { key: 'base', label: 'Base (m)', type: 'number', default: 10, shapes: ['triangle'] },
      { key: 'height', label: 'Height (m)', type: 'number', default: 5, shapes: ['triangle', 'trapezoid'] },
      { key: 'base1', label: 'Base 1 (m)', type: 'number', default: 10, shapes: ['trapezoid'] },
      { key: 'base2', label: 'Base 2 (m)', type: 'number', default: 8, shapes: ['trapezoid'] },
    ],
    results: {
      primary: 'area',
      labels: { area: 'Area', unit: 'Unit', shape: 'Shape' },
    },
  },
  volume: {
    label: 'Volume',
    fields: [
      { key: 'shape', label: 'Shape', type: 'select', default: 'cube', options: SHAPES.volume, variant: true },
      { key: 'side', label: 'Side (m)', type: 'number', default: 3, shapes: ['cube'] },
      { key: 'radius', label: 'Radius (m)', type: 'number', default: 2, shapes: ['cylinder', 'sphere', 'cone'] },
      { key: 'height', label: 'Height (m)', type: 'number', default: 5, shapes: ['cylinder', 'cone'] },
    ],
    results: {
      primary: 'volume',
      labels: { volume: 'Volume', unit: 'Unit', shape: 'Shape' },
    },
  },
  slope: {
    label: 'Slope',
    fields: [
      { key: 'rise', label: 'Rise (m)', type: 'number', default: 1 },
      { key: 'run', label: 'Run (m)', type: 'number', default: 10 },
    ],
    results: {
      primary: 'slope_percent',
      labels: {
        slope_percent: 'Slope (%)',
        slope_degrees: 'Slope (°)',
        slope_ratio: 'Slope ratio (1:X)',
        rise_m: 'Rise (m)',
        run_m: 'Run (m)',
      },
    },
  },
}

function fieldVisible(field, values) {
  if (field.variant) return true
  if (field.shapes) {
    return Boolean(values.shape && field.shapes.includes(values.shape))
  }
  return true
}

function CalcPanel({ calc, values, onFieldChange, onCalculate, result }) {
  const primaryLabel = calc.results?.labels?.[calc.results?.primary]
  const hasError = result && result.error
  return (
    <div className="calc-panel">
      {calc.fields.map(f => {
        if (!fieldVisible(f, values)) return null
        const opts = f.depends ? ((f.options && f.options[values[f.depends]]) || []) : (Array.isArray(f.options) ? f.options : [])
        return (
          <div key={f.key} className="calc-field">
            <label>{f.label}</label>
            {f.type === 'select' ? (
              <select
                value={values[f.key] ?? f.default}
                onChange={e => onFieldChange(f.key, e.target.value)}
              >
                {opts.map(o => <option key={o} value={o}>{o}</option>)}
              </select>
            ) : (
              <input
                type={f.type === 'number' ? 'number' : 'text'}
                value={values[f.key] ?? f.default}
                step={f.step}
                onChange={e => onFieldChange(f.key, e.target.value)}
              />
            )}
          </div>
        )
      })}
      <button className="calc-btn-small" onClick={() => onCalculate()}>Calculate</button>
      {result && (
        hasError ? (
          <div className="calc-result calc-error">{result.error}</div>
        ) : (
          <div className="calc-result">
            {result[calc.results?.primary] !== undefined && (
              <div className="calc-result-primary">{primaryLabel}: <strong>{result[calc.results.primary]}{result.unit ? ` ${result.unit}` : ''}</strong></div>
            )}
            <div className="calc-result-rows">
              {Object.entries(result)
                .filter(([k]) => k !== calc.results?.primary && calc.results?.labels?.[k])
                .map(([k, v]) => (
                  <div key={k} className="calc-result-row">
                    <span>{calc.results.labels[k]}</span>
                    <span>{v}</span>
                  </div>
                ))}
            </div>
            {result.formula && (
              <div className="calc-working">
                <div className="calc-working-sec"><span className="cw-label">Formula</span><div className="cw-code">{result.formula}</div></div>
                {result.variables && Object.keys(result.variables).length > 0 && (
                  <div className="calc-working-sec">
                    <span className="cw-label">Variables</span>
                    <div className="cw-rows">
                      {Object.entries(result.variables).map(([k, v]) => (
                        <div key={k} className="cw-row">
                          <span className="cw-var">{k} = {v.value} {v.unit || ''}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                {Array.isArray(result.given) && result.given.length > 0 && (
                  <div className="calc-working-sec">
                    <span className="cw-label">Given</span>
                    <div className="cw-rows">
                      {result.given.map((g, i) => <div key={i} className="cw-row">{g}</div>)}
                    </div>
                  </div>
                )}
                {result.substitution && (
                  <div className="calc-working-sec"><span className="cw-label">Substitution</span><div className="cw-code">{result.substitution}</div></div>
                )}
                {Array.isArray(result.working) && result.working.length > 0 && (
                  <div className="calc-working-sec">
                    <span className="cw-label">Working</span>
                    <div className="cw-rows">
                      {result.working.map((w, i) => <div key={i} className="cw-row">{w}</div>)}
                    </div>
                  </div>
                )}
                {result.explanation && (
                  <div className="calc-working-sec"><span className="cw-label">Engineering Note</span><div className="cw-note">{result.explanation}</div></div>
                )}
              </div>
            )}
          </div>
        )
      )}
    </div>
  )
}

function ProgressBar({ tokens, maxTokens, startTime }) {
  const elapsed = (performance.now() - (startTime || performance.now())) / 1000
  const tps = elapsed > 0 ? (tokens / elapsed).toFixed(1) : '--'
  const pct = Math.min(100, (tokens / maxTokens) * 100)
  return (
    <div className="stream-progress">
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${pct}%` }} />
      </div>
      <div className="progress-info">
        {tokens} / {maxTokens} tokens · {elapsed.toFixed(1)}s · {tps} tok/s
      </div>
    </div>
  )
}

function Message({ msg }) {
  const isError = msg.role === 'error'
  return (
    <div className={`msg ${isError ? 'error' : msg.role}`}>
      <div className="msg-content">{msg.content}</div>
      {msg.sources && msg.sources.length > 0 && (
        <div className="msg-sources">
          <span className="src-label">Sources:</span>
          {msg.sources.map((s, i) => (
            <span key={i} className="src-badge" title={`Relevance: ${s.relevance}`}>{s.source}</span>
          ))}
        </div>
      )}
      {msg.meta && <div className="msg-meta">{msg.meta}</div>}
    </div>
  )
}

const MAX_TOKENS = 768

export default function App() {
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('ecoinframind-theme')
    return saved !== null ? saved === 'dark' : true
  })

  useEffect(() => {
    localStorage.setItem('ecoinframind-theme', darkMode ? 'dark' : 'light')
  }, [darkMode])

  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [streamText, setStreamText] = useState('')
  const [streamTokens, setStreamTokens] = useState(0)
  const [streamTick, setStreamTick] = useState(0)
  const [status, setStatus] = useState({ online: false, modelLoaded: false })
  const [metrics, setMetrics] = useState({})
  const [languages, setLanguages] = useState([])
  const [language, setLanguage] = useState('english')
  const [openCalc, setOpenCalc] = useState(null)
  const [calcValues, setCalcValues] = useState({})
  const [calcResults, setCalcResults] = useState({})
  const messagesEnd = useRef(null)
  const inputRef = useRef(null)
  const streamStartRef = useRef(null)

  const scrollBottom = useCallback(() => {
    setTimeout(() => messagesEnd.current?.scrollIntoView({ behavior: 'smooth' }), 50)
  }, [])

  useEffect(() => {
    const h = setInterval(async () => {
      try {
        const d = await checkHealth()
        setStatus({ online: true, modelLoaded: d.model_loaded })
      } catch { setStatus({ online: false, modelLoaded: false }) }
    }, 5000)
    const m = setInterval(async () => {
      try { setMetrics(await getMetrics()) } catch {}
    }, 10000)
    checkHealth().then(d => setStatus({ online: true, modelLoaded: d.model_loaded })).catch(() => {})
    getLanguages().then(d => setLanguages(d.languages || [])).catch(() => {})
    return () => { clearInterval(h); clearInterval(m) }
  }, [])

  useEffect(() => { scrollBottom() }, [messages, streamText, streamTick, scrollBottom])

  useEffect(() => {
    if (!loading) return
    const id = setInterval(() => setStreamTick(t => t + 1), 1000)
    return () => clearInterval(id)
  }, [loading])

  async function handleSend() {
    const text = input.trim()
    if (!text || loading) return
    setInput('')
    setLoading(true)
    setStreamText('')

    const userMsg = { role: 'user', content: text }
    const history = messages.map(m => ({ role: m.role, content: m.content }))
    setMessages(prev => [...prev, userMsg])

    const t0 = performance.now()
    streamStartRef.current = t0
    setStreamTokens(0)
    let pendingSources = null
    try {
      await sendChatMessage(
        text,
        history,
        language,
        full => {
          setStreamText(full)
          setStreamTokens(Math.ceil(full.length / 4))
        },
        (meta, fullText) => {
          const elapsed = ((performance.now() - t0) / 1000).toFixed(1)
          setMessages(prev => [...prev,
            { role: 'assistant', content: fullText, meta: `${meta.tokens} tokens · ${elapsed}s · CPU ${meta.cpu}% · RAM ${meta.ram} GB`, sources: meta.sources || pendingSources || [] }
          ])
          setStreamText('')
        },
        sources => { pendingSources = sources }
      )
    } catch (e) {
      const errMsg = e.message.startsWith('HTTP') ? `Backend error: ${e.message}` : e.message
      setMessages(prev => [...prev, { role: 'error', content: errMsg }])
    }
    setLoading(false)
    setStreamText('')
    setStreamTokens(0)
    inputRef.current?.focus()
  }

  function handleCalcSelect(name) {
    setOpenCalc(openCalc === name ? null : name)
    const calc = CALCULATORS[name]
    if (calc && !calcValues[name]) {
      const vals = {}
      calc.fields.forEach(f => {
        const v = Array.isArray(f.options) ? (f.default ?? f.options[0]) : f.default
        vals[f.key] = v
      })
      if (name === 'unit_conversion') {
        vals.from_unit = UNITS_BY_CATEGORY[vals.category][0]
        vals.to_unit = UNITS_BY_CATEGORY[vals.category][1]
      }
      setCalcValues(prev => ({ ...prev, [name]: vals }))
    }
  }

  function handleCalcField(name, key, value) {
    setCalcValues(prev => {
      const v = { ...prev[name], [key]: value }
      if (name === 'unit_conversion' && key === 'category') {
        v.from_unit = UNITS_BY_CATEGORY[value][0]
        v.to_unit = UNITS_BY_CATEGORY[value][1]
      }
      return { ...prev, [name]: v }
    })
  }

  async function handleCalculate(calc, values) {
    const parsed = {}
    calc.fields.forEach(f => {
      if (f.uiOnly) return
      const raw = values[f.key] ?? f.default
      const sendKey = f.key2 || f.key
      if (f.type === 'csv') {
        parsed[sendKey] = String(raw).split(',').map(s => parseFloat(s.trim())).filter(n => !Number.isNaN(n))
      } else if (f.type === 'number') {
        const n = parseFloat(raw)
        parsed[sendKey] = Number.isNaN(n) ? null : n
      } else {
        parsed[sendKey] = String(raw)
      }
    })
    try {
      const r = await runCalculator(calc.name, parsed)
      setCalcResults(prev => ({ ...prev, [calc.name]: r.result }))
    } catch (e) {
      setCalcResults(prev => ({ ...prev, [calc.name]: { error: e.message } }))
    }
  }

  const name = openCalc
  const activeCalc = name ? CALCULATORS[name] : null
  const offlineBanner = !status.online && messages.length > 0

  return (
    <div className={`app ${darkMode ? 'dark' : 'light'}`}>
      <aside className="sidebar">
        <div className="sidebar-header">
          <div>
            <h1>EcoInfraMind AI</h1>
            <p className="subtitle">Offline Engineering AI</p>
          </div>
          <button className="theme-toggle" onClick={() => setDarkMode(d => !d)} title={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}>
            {darkMode ? '\u2600' : '\u263E'}
          </button>
        </div>
        <div className={`status ${status.online ? 'green' : 'red'}`}>
          <span className={`dot ${status.online ? 'green' : 'red'}`} />
          {status.online ? `Online${status.modelLoaded ? ' · Model Loaded' : ''}` : 'Connecting...'}
        </div>

        <div className="section-label">Language</div>
        <div className="lang-selector">
          {languages.map(lang => (
            <button
              key={lang}
              className={`lang-btn ${language === lang ? 'active' : ''}`}
              onClick={() => setLanguage(lang)}
            >
              {lang.charAt(0).toUpperCase() + lang.slice(1)}
            </button>
          ))}
        </div>

        <div className="section-label">Calculators</div>
        {Object.entries(CALCULATORS).map(([key, calc]) => (
          <div key={key}>
            <button
              className={`calc-btn ${openCalc === key ? 'active' : ''}`}
              onClick={() => handleCalcSelect(key)}
            >
              {calc.label}
            </button>
          </div>
        ))}

        <div className="metrics">
          <div>CPU: {metrics.cpu_percent?.toFixed(1) ?? '--'}%</div>
          <div>RAM: {metrics.ram_gb?.toFixed(2) ?? '--'} GB</div>
          <div>Model: {metrics.model_loaded ? 'Loaded' : 'Not loaded'}</div>
          <div>Knowledge: {metrics.knowledge_stats?.total_chunks ?? '--'} chunks</div>
        </div>
      </aside>

      <main className="main">
        <header className="header">
          <span>Chat</span>
          <button className="clear-btn" onClick={() => setMessages([])}>Clear</button>
        </header>

        <div className="messages">
          {offlineBanner && (
            <div className="banner banner-error">
              Connection lost — backend unreachable. Check if the server is running on port 8432.
            </div>
          )}
          {messages.map((msg, i) => (
            <Message key={i} msg={msg} />
          ))}
          {loading && streamText && (
            <div className="msg assistant">
              <div className="msg-content">{streamText}</div>
              <ProgressBar tokens={streamTokens} maxTokens={MAX_TOKENS} startTime={streamStartRef.current} />
            </div>
          )}
          {loading && !streamText && (
            <div className="msg assistant">
              <div className="typing"><span></span><span></span><span></span></div>
            </div>
          )}
          <div ref={messagesEnd} />
        </div>

        <div className="input-area">
          <div className="input-row">
            <textarea
              ref={inputRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend() } }}
              placeholder="Ask an engineering question..."
              rows={1}
            />
            <button onClick={handleSend} disabled={loading || !input.trim()}>Send</button>
          </div>
        </div>
      </main>

      {activeCalc && (
        <aside className="calc-sidebar">
          <div className="calc-header">
            <h3>{activeCalc.label}</h3>
            <button className="close-btn" onClick={() => setOpenCalc(null)}>×</button>
          </div>
          <CalcPanel
            calc={{ ...activeCalc, name }}
            values={calcValues[name] || {}}
            onFieldChange={(key, val) => handleCalcField(name, key, val)}
            onCalculate={() => handleCalculate({ ...activeCalc, name }, calcValues[name] || {})}
            result={calcResults[name]}
          />
        </aside>
      )}
    </div>
  )
}