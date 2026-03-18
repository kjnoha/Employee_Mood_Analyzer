/**
 * Employee Emotion Analyzer — Client-Side Logic
 */

// ── Mood Analysis Form ─────────────────────────────────────────────────
const moodForm = document.getElementById('mood-form');
const resultPanel = document.getElementById('result-panel');
const analyzeBtn = document.getElementById('analyze-btn');
const spinner = document.getElementById('spinner');

if (moodForm) {
    moodForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(moodForm);
        const employeeId = formData.get('employee_id')?.trim();
        const textInput = formData.get('text_input')?.trim();

        if (!employeeId || !textInput) {
            showToast('Please fill in both fields.', 'error');
            return;
        }

        analyzeBtn.disabled = true;
        spinner.classList.add('active');
        resultPanel.classList.remove('active');

        try {
            const res = await fetch('/analyze', { method: 'POST', body: formData });
            const data = await res.json();

            if (data.error) {
                showToast(data.error, 'error');
                return;
            }

            renderResult(data.result);
            resultPanel.classList.add('active');
            showToast('Emotion analyzed & logged! ✨', 'success');

            // Refresh charts & feed
            loadCharts();
            loadActivityFeed();

            // Update particle mood
            if (window.updateParticleMood && data.result.category) {
                window.updateParticleMood(data.result.category);
            }
        } catch (err) {
            showToast('Something went wrong. Please retry.', 'error');
            console.error(err);
        } finally {
            analyzeBtn.disabled = false;
            spinner.classList.remove('active');
        }
    });
}


// ── Render Analysis Result ─────────────────────────────────────────────
function renderResult(r) {
    // Emotion header
    document.getElementById('res-emoji').textContent = r.icon;
    document.getElementById('res-emotion').textContent = r.emotion;
    document.getElementById('res-emotion').style.color = r.color;

    const catBadge = document.getElementById('res-category');
    catBadge.textContent = r.category;
    catBadge.className = 'result-category ' + r.category;

    document.getElementById('res-score').textContent = r.score;

    // Sentiment bars
    setSentimentBar('pos', r.sentiment_details.positive);
    setSentimentBar('neg', r.sentiment_details.negative);
    setSentimentBar('neu', r.sentiment_details.neutral);

    // Task priority
    const tp = r.task_priority;
    document.getElementById('tp-priority').textContent = tp.priority.toUpperCase();
    document.getElementById('tp-focus').textContent = tp.focus;
    document.getElementById('tp-time').textContent = tp.time_blocks;

    // Suggestions
    const sugList = document.getElementById('suggestions-list');
    sugList.innerHTML = '';
    r.all_suggestions.forEach(s => {
        const li = document.createElement('li');
        li.textContent = s;
        sugList.appendChild(li);
    });

    // Productivity mini-gauge
    const prodDiv = document.getElementById('result-prod-gauge');
    if (prodDiv && r.productivity) {
        const p = r.productivity;
        const dashLen = (p.score / 100) * 251;  // circumference for r=40
        prodDiv.innerHTML = `
      <svg viewBox="0 0 100 100" width="70" height="70">
        <circle cx="50" cy="50" r="40" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="8"/>
        <circle cx="50" cy="50" r="40" fill="none" stroke="${p.grade_color}" stroke-width="8"
                stroke-dasharray="${dashLen} 251"
                stroke-linecap="round" transform="rotate(-90 50 50)"
                style="transition: stroke-dasharray 1s ease"/>
        <text x="50" y="47" text-anchor="middle" fill="${p.grade_color}"
              font-size="18" font-weight="800" font-family="Inter">${p.score}</text>
        <text x="50" y="62" text-anchor="middle" fill="#94a3b8"
              font-size="8" font-weight="500" font-family="Inter">${p.grade} · ${p.label}</text>
      </svg>
      <div class="mini-gauge-label">Productivity</div>
    `;
    }

    // Streak
    const streakDiv = document.getElementById('result-streak');
    if (streakDiv && r.streak) {
        streakDiv.innerHTML = `${r.streak.emoji} ${r.streak.message}`;
    }

    // Music
    if (r.music) {
        const m = r.music;
        document.getElementById('music-genre').textContent = m.genre;
        document.getElementById('music-vibe').textContent = `"${m.vibe}"`;

        const tracksList = document.getElementById('music-tracks');
        tracksList.innerHTML = '';
        m.tracks.forEach(t => {
            const li = document.createElement('li');
            li.textContent = t;
            tracksList.appendChild(li);
        });

        document.getElementById('music-activity').textContent = m.activity;
    }
}

function setSentimentBar(type, value) {
    const fill = document.querySelector(`.sentiment-bar-fill.${type}`);
    const valEl = document.querySelector(`.sentiment-bar-value.${type}`);
    if (fill) fill.style.width = `${Math.min(value, 100)}%`;
    if (valEl) valEl.textContent = `${value}%`;
}


// ── Charts (Plotly) ────────────────────────────────────────────────────
async function loadCharts() {
    const filterEmp = document.getElementById('chart-filter-emp')?.value || '';

    try {
        const trendRes = await fetch(`/api/trends?days=30${filterEmp ? '&employee_id=' + filterEmp : ''}`);
        const trendData = await trendRes.json();
        renderTrendChart(trendData);
    } catch (e) { console.error('Trend chart error', e); }

    try {
        const distRes = await fetch(`/api/distribution${filterEmp ? '?employee_id=' + filterEmp : ''}`);
        const distData = await distRes.json();
        renderDistributionChart(distData);
    } catch (e) { console.error('Distribution chart error', e); }
}

function renderTrendChart(data) {
    const container = document.getElementById('trend-chart');
    if (!container) return;

    if (!data || data.length === 0) {
        container.innerHTML = '<div class="empty-state"><div class="empty-icon">📈</div><p>No trend data yet. Log some moods first!</p></div>';
        return;
    }

    const trace = {
        x: data.map(d => d.date),
        y: data.map(d => d.avg_score),
        type: 'scatter',
        mode: 'lines+markers',
        fill: 'tozeroy',
        line: { color: '#6366f1', width: 3, shape: 'spline' },
        marker: {
            color: data.map(d => d.avg_score >= 0 ? '#10b981' : '#f43f5e'),
            size: 8,
        },
        fillcolor: 'rgba(99, 102, 241, 0.08)',
        hovertemplate: '<b>%{x}</b><br>Avg Score: %{y:.2f}<br>Entries: %{text}<extra></extra>',
        text: data.map(d => d.count),
    };

    const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { family: 'Inter', color: '#94a3b8', size: 12 },
        margin: { l: 40, r: 16, t: 10, b: 40 },
        xaxis: {
            gridcolor: 'rgba(255,255,255,0.04)',
            linecolor: 'rgba(255,255,255,0.04)',
            tickfont: { size: 10 },
        },
        yaxis: {
            gridcolor: 'rgba(255,255,255,0.04)',
            linecolor: 'rgba(255,255,255,0.04)',
            range: [-1, 1],
            tickfont: { size: 10 },
            zeroline: true,
            zerolinecolor: 'rgba(255,255,255,0.08)',
        },
        hoverlabel: {
            bgcolor: '#1e293b',
            font: { color: '#f1f5f9', family: 'Inter' },
            bordercolor: 'rgba(255,255,255,0.1)',
        },
    };

    Plotly.newPlot(container, [trace], layout, { responsive: true, displayModeBar: false });
}

function renderDistributionChart(data) {
    const container = document.getElementById('distribution-chart');
    if (!container) return;

    if (!data.labels || data.labels.length === 0) {
        container.innerHTML = '<div class="empty-state"><div class="empty-icon">🍩</div><p>No distribution data yet.</p></div>';
        return;
    }

    const labelsWithIcons = data.labels.map((l, i) => `${data.icons[i]} ${l}`);

    const trace = {
        labels: labelsWithIcons,
        values: data.values,
        type: 'pie',
        hole: 0.55,
        marker: {
            colors: data.colors,
            line: { color: '#0a0e1a', width: 2 },
        },
        textposition: 'outside',
        textfont: { family: 'Inter', size: 11, color: '#94a3b8' },
        hovertemplate: '<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>',
        sort: false,
    };

    const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { family: 'Inter', color: '#94a3b8', size: 12 },
        margin: { l: 10, r: 10, t: 10, b: 10 },
        showlegend: false,
        hoverlabel: {
            bgcolor: '#1e293b',
            font: { color: '#f1f5f9', family: 'Inter' },
            bordercolor: 'rgba(255,255,255,0.1)',
        },
        annotations: [{
            text: `<b>${data.values.reduce((a, b) => a + b, 0)}</b><br>entries`,
            font: { size: 14, color: '#f1f5f9', family: 'Inter' },
            showarrow: false,
        }],
    };

    Plotly.newPlot(container, [trace], layout, { responsive: true, displayModeBar: false });
}


// ── Activity Feed ──────────────────────────────────────────────────────
async function loadActivityFeed() {
    const feedList = document.getElementById('feed-list');
    if (!feedList) return;

    try {
        const res = await fetch('/api/logs');
        const entries = await res.json();

        if (entries.length === 0) {
            feedList.innerHTML = '<div class="empty-state"><div class="empty-icon">📝</div><p>No entries yet.</p></div>';
            return;
        }

        feedList.innerHTML = entries.slice(0, 20).map(e => `
      <div class="feed-item">
        <div class="feed-icon" style="background: ${e.color}15;">
          ${e.icon}
        </div>
        <div class="feed-content">
          <div class="feed-text">${escapeHtml(truncate(e.text_input, 60))}</div>
          <div class="feed-meta">
            <strong>${escapeHtml(e.employee_id)}</strong> · ${e.emotion} · ${formatTimestamp(e.timestamp)}
          </div>
        </div>
        <div class="feed-score" style="color: ${e.color};">
          ${e.score >= 0 ? '+' : ''}${e.score}
          <div class="score-label">score</div>
        </div>
      </div>
    `).join('');
    } catch (err) {
        console.error('Feed load error', err);
    }
}


// ── Toast Notification ─────────────────────────────────────────────────
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    setTimeout(() => toast.classList.remove('show'), 3500);
}


// ── Helpers ────────────────────────────────────────────────────────────
function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str || '';
    return div.innerHTML;
}

function truncate(str, len) {
    if (!str) return '';
    return str.length > len ? str.substring(0, len) + '…' : str;
}

function formatTimestamp(ts) {
    if (!ts) return '';
    try {
        const d = new Date(ts);
        const now = new Date();
        const diff = now - d;
        if (diff < 60000) return 'Just now';
        if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    } catch {
        return ts;
    }
}


// ── Chart Filter ───────────────────────────────────────────────────────
const chartFilter = document.getElementById('chart-filter-emp');
if (chartFilter) {
    chartFilter.addEventListener('change', () => loadCharts());
}


// ── Init ───────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    loadCharts();
    loadActivityFeed();
});
