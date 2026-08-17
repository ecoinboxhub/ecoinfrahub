const API = '/api/v1'

function cleanText(text) {
  text = text.replace(/^#+\s*/gm, '')
  text = text.replace(/\*\*(.*?)\*\*/g, '$1')
  text = text.replace(/\*(.*?)\*/g, '$1')
  text = text.replace(/__(.*?)__/g, '$1')
  text = text.replace(/_(.*?)_/g, '$1')
  text = text.replace(/`(.*?)`/g, '$1')
  text = text.replace(/~~(.*?)~~/g, '$1')
  text = text.replace(/\[(.*?)\]\(.*?\)/g, '$1')
  text = text.replace(/\n{3,}/g, '\n\n')
  return text.trim()
}

export async function checkHealth() {
  const r = await fetch(`${API}/health`)
  return r.json()
}

export async function getMetrics() {
  const r = await fetch(`${API}/metrics`)
  return r.json()
}

export async function getLanguages() {
  const r = await fetch(`${API}/languages`)
  return r.json()
}

export async function getKnowledgeStats() {
  const r = await fetch(`${API}/knowledge/stats`)
  return r.json()
}

export async function runCalculator(name, params) {
  const r = await fetch(`${API}/calculator`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ calculator: name, params }),
  })
  if (!r.ok) {
    let detail = `HTTP ${r.status}`
    try { const j = await r.json(); detail = j.detail || detail } catch {}
    throw new Error(detail)
  }
  return r.json()
}

export async function sendChatMessage(message, history = [], language = 'english', onToken, onMeta, onSources) {
  const r = await fetch(`${API}/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, history, language }),
  })
  if (!r.ok) {
    let detail = `HTTP ${r.status}`
    try { const j = await r.json(); detail = j.detail || detail } catch {}
    throw new Error(detail)
  }
  const reader = r.body.getReader()
  const decoder = new TextDecoder()
  let full = ''
  let sources = null
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    const chunk = decoder.decode(value, { stream: true })
    for (const line of chunk.split('\n')) {
      if (!line.startsWith('data: ')) continue
      const data = line.slice(6).trim()
      if (data === '[DONE]') continue
      try {
        const parsed = JSON.parse(data)
        if (parsed.token) {
          full += parsed.token
          onToken?.(cleanText(full))
        }
        if (parsed.sources && !parsed.meta) {
          sources = parsed.sources
          onSources?.(parsed.sources)
        }
        if (parsed.meta) {
          onMeta?.(parsed.meta, cleanText(full))
        }
      } catch {}
    }
  }
  return { full: cleanText(full), sources }
}
