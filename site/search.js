/* CI Tools 全站搜索 —— 智能匹配（子串 / 子序列 / 同义词）+ 自动补全
   数据来源：search-index.js（由 source/build_search_index.py 生成） */
(function () {
  'use strict';
  var DATA = window.CI_SEARCH_INDEX;
  if (!DATA) return;

  var PAGE = (location.pathname.split('/').pop() || 'index.html');
  var WEIGHT = { zh: 1.0, en: 1.0, tool: 0.62, cmd: 0.74 };
  var RKEY = 'citools-recent';

  /* ---------- 文本归一化与匹配 ---------- */
  function norm(s) {
    if (!s) return '';
    return String(s).toLowerCase()
      .replace(/[\uFF01-\uFF5E]/g, function (c) { return String.fromCharCode(c.charCodeAt(0) - 0xFEE0); })
      .replace(/[\s\u3000·•・_\-–—\/\\|,，.。:：;；'"“”‘’()（）\[\]【】<>《》+→>]/g, '');
  }
  function words(s) {
    return String(s || '').split(/\s+/).map(norm).filter(function (x) { return !!x; });
  }
  function isSubseq(hay, needle) {
    var i = 0;
    for (var j = 0; j < hay.length && i < needle.length; j++) {
      if (hay.charAt(j) === needle.charAt(i)) i++;
    }
    return i === needle.length;
  }
  function fieldScore(hay, needle) {
    if (!hay || !needle) return 0;
    if (hay === needle) return 100;
    var idx = hay.indexOf(needle);
    if (idx === 0) return 88;
    if (idx > 0) return Math.max(36, 70 - idx * 2 - (hay.length - needle.length) * 0.25);
    if (needle.length >= 2 && isSubseq(hay, needle)) return needle.length <= 3 ? 20 : 30;
    return 0;
  }

  /* ---------- 索引扁平化 ---------- */
  var ENTRIES = [];
  (DATA.tools || []).forEach(function (t, i) {
    ENTRIES.push({
      kind: 'tool', file: t.file, anchor: '', tool: t.id, order: i,
      zh: t.zh, en: t.en, subZh: t.desc_zh || '', subEn: t.desc_en || '',
      cmd: t.cmd || '', keys: t.keys || '',
      k: words(t.keys),
      s: {
        zh: norm(t.zh), en: norm(t.en), tool: norm(t.en + ' ' + t.zh),
        cmd: norm(t.cmd), keys: norm(t.keys)
      }
    });
  });
  (DATA.pages || []).forEach(function (p, i) {
    ENTRIES.push({
      kind: 'page', file: p.file, anchor: '', tool: '', order: 100 + i,
      zh: p.zh, en: p.en, subZh: p.sub_zh || '', subEn: p.sub_en || '',
      cmd: '', keys: p.keys || '', k: words(p.keys),
      s: { zh: norm(p.zh), en: norm(p.en), tool: '', cmd: '', keys: norm(p.keys) }
    });
  });
  (DATA.articles || []).forEach(function (a, i) {
    ENTRIES.push({
      kind: 'article', file: a.f, anchor: a.a, tool: a.t || '', order: 200 + i,
      zh: a.zh, en: a.en, subZh: a.tzh || a.t || '', subEn: a.ten || a.t || '',
      cmd: '', keys: '', k: [],
      s: { zh: norm(a.zh), en: norm(a.en), tool: norm((a.tzh || '') + ' ' + (a.ten || '')), cmd: '', keys: '' }
    });
  });

  function scoreEntry(e, tokens) {
    var total = 0;
    for (var i = 0; i < tokens.length; i++) {
      var tk = tokens[i], best = 0;
      for (var f in WEIGHT) {
        if (!e.s[f]) continue;
        var sc = fieldScore(e.s[f], tk) * WEIGHT[f];
        if (sc > best) best = sc;
      }
      if (e.k && e.k.length) {
        var ks = keysScore(e, tk) * 0.92;
        if (ks > best) best = ks;
      }
      if (!best) return 0;
      total += best;
    }
    return total / tokens.length + (tokens.length > 1 ? 4 : 0);
  }

  // 关键词是空格分隔的口语词：整词命中权重最高
  function keysScore(e, tk) {
    var arr = e.k, best = 0;
    for (var i = 0; i < arr.length; i++) {
      var k = arr[i];
      if (!k) continue;
      if (k === tk) return 100;
      if (k.indexOf(tk) === 0) { if (best < 78) best = 78; }
      else if (k.indexOf(tk) >= 0) { if (best < 58) best = 58; }
      else if (tk.length >= 2 && isSubseq(k, tk)) { if (best < 24) best = 24; }
    }
    if (!best && e.s.keys) best = fieldScore(e.s.keys, tk) * 0.7;
    return best;
  }

  function rank(q) {
    var raw = q.trim();
    if (!raw) return null;
    var tokens = raw.split(/\s+/).map(norm).filter(Boolean);
    if (!tokens.length) return null;

    // 先找出与该问句相关的工具，给同工具条目加权
    var toolHits = {};
    ENTRIES.forEach(function (e) {
      if (e.kind !== 'tool') return;
      var sc = scoreEntry(e, tokens);
      if (sc >= 60) toolHits[e.tool] = sc;
    });

    var out = [];
    ENTRIES.forEach(function (e) {
      var sc = scoreEntry(e, tokens);
      if (!sc) return;
      if (e.tool && toolHits[e.tool]) sc += toolHits[e.tool] * 0.22;
      if (e.kind === 'tool') sc += 6;
      sc -= Math.min(6, Math.max(0, (norm(e.zh).length - 24) * 0.12));
      out.push({ e: e, sc: sc, tokens: tokens });
    });
    out.sort(function (a, b) {
      return b.sc - a.sc || a.e.order - b.e.order || a.e.zh.length - b.e.zh.length;
    });
    return out.slice(0, 12);
  }

  /* ---------- 渲染工具 ---------- */
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function hl(text, tokens) {
    text = String(text || '');
    if (!tokens || !tokens.length) return esc(text);
    var lower = text.toLowerCase(), mask = [];
    for (var i = 0; i < text.length; i++) mask[i] = 0;
    tokens.forEach(function (t) {
      if (!t) return;
      var idx = lower.indexOf(t);
      if (idx >= 0) {
        for (var k = 0; k < t.length; k++) mask[idx + k] = 1;
        return;
      }
      var p = 0;
      for (var j = 0; j < lower.length && p < t.length; j++) {
        if (lower.charAt(j) === t.charAt(p)) { mask[j] = 1; p++; }
      }
    });
    var res = '', open = false;
    for (var n = 0; n < text.length; n++) {
      if (mask[n] && !open) { res += '<mark>'; open = true; }
      if (!mask[n] && open) { res += '</mark>'; open = false; }
      res += esc(text.charAt(n));
    }
    return res + (open ? '</mark>' : '');
  }

  function lang() {
    return document.documentElement.getAttribute('data-lang') === 'en' ? 'en' : 'zh';
  }
  var BADGE = {
    zh: { tool: '工具', article: '篇章', page: '页面' },
    en: { tool: 'Tool', article: 'Article', page: 'Page' }
  };

  function itemHTML(e, idx, active, tokens) {
    var L = lang();
    var title = L === 'en' ? (e.en || e.zh) : (e.zh || e.en);
    var sub = '';
    if (e.kind === 'tool') sub = e.cmd || (L === 'en' ? e.subEn : e.subZh);
    else if (e.kind === 'article') sub = L === 'en' ? e.subEn : e.subZh;
    else sub = L === 'en' ? e.subEn : e.subZh;
    return '<li><div class="srch-item" role="option" data-i="' + idx + '" aria-selected="' +
      (active ? 'true' : 'false') + '">' +
      '<span class="srch-badge k-' + e.kind + '">' + BADGE[L][e.kind] + '</span>' +
      '<span class="srch-body"><span class="srch-t">' + hl(title, tokens) + '</span>' +
      (sub ? '<span class="srch-s">' + esc(sub) + '</span>' : '') +
      '</span></div></li>';
  }

  /* ---------- 最近访问 ---------- */
  function recents() {
    try { return JSON.parse(localStorage.getItem(RKEY) || '[]'); } catch (err) { return []; }
  }
  function remember(e) {
    try {
      var list = recents().filter(function (x) { return !(x.file === e.file && x.anchor === e.anchor); });
      list.unshift({ file: e.file, anchor: e.anchor, zh: e.zh, en: e.en, kind: e.kind, cmd: e.cmd || '' });
      localStorage.setItem(RKEY, JSON.stringify(list.slice(0, 6)));
    } catch (err) { /* 隐私模式下忽略 */ }
  }

  /* ---------- DOM ---------- */
  var dock = document.createElement('div');
  dock.className = 'srch-dock';
  dock.innerHTML =
    '<div class="srch">' +
    '<span class="srch-ic">⌕</span>' +
    '<input class="srch-input" id="srchInput" type="search" autocomplete="off" ' +
    'spellcheck="false" role="combobox" aria-expanded="false" aria-controls="srchPanel">' +
    '<kbd class="srch-kbd">Ctrl K</kbd>' +
    '<div class="srch-panel" id="srchPanel" role="listbox" aria-label="搜索结果"></div>' +
    '</div>';

  var main = document.querySelector('main.main') || document.body;
  main.insertBefore(dock, main.firstChild);

  var input = dock.querySelector('#srchInput');
  var panel = dock.querySelector('#srchPanel');
  var items = [];        // 当前可选项（按顺序）
  var active = -1;

  function placeholder() {
    input.placeholder = lang() === 'en'
      ? 'Search commands, tools or features…'
      : '搜索命令、工具或功能…';
    input.setAttribute('aria-label', input.placeholder);
  }
  placeholder();

  function layout() {
    dock.classList.toggle('stuck', dock.getBoundingClientRect().top <= 0 && window.scrollY > 8);
  }
  window.addEventListener('scroll', layout, { passive: true });
  layout();

  function bindItems() {
    panel.querySelectorAll('.srch-item').forEach(function (el) {
      el.addEventListener('mousedown', function (ev) { ev.preventDefault(); });
      el.addEventListener('click', function () { pick(parseInt(el.getAttribute('data-i'), 10)); });
      el.addEventListener('mousemove', function () {
        var i = parseInt(el.getAttribute('data-i'), 10);
        if (i !== active) setActive(i);
      });
    });
  }

  function setActive(i) {
    active = i;
    panel.querySelectorAll('.srch-item').forEach(function (el) {
      var on = parseInt(el.getAttribute('data-i'), 10) === i;
      el.setAttribute('aria-selected', on ? 'true' : 'false');
      if (on && el.scrollIntoView) el.scrollIntoView({ block: 'nearest' });
    });
  }

  function open() {
    panel.classList.add('open');
    input.setAttribute('aria-expanded', 'true');
  }
  function close() {
    panel.classList.remove('open');
    input.setAttribute('aria-expanded', 'false');
    active = -1;
  }

  function renderDefault() {
    var L = lang();
    var tools = ENTRIES.filter(function (e) { return e.kind === 'tool'; });
    var html = '';
    var rec = recents().map(function (r, i) {
      return {
        kind: r.kind || 'tool', file: r.file, anchor: r.anchor || '', tool: '', order: -1 - i,
        zh: r.zh, en: r.en, subZh: '', subEn: '', cmd: r.cmd || '', keys: '', k: [],
        s: { zh: norm(r.zh), en: norm(r.en), tool: '', cmd: '', keys: '' }
      };
    });
    if (rec.length) {
      html += '<div class="srch-sec">' + (L === 'en' ? 'Recent' : '最近查看') + '</div>';
      rec.forEach(function (e, i) { html += itemHTML(e, i, false, null); });
    }
    html += '<div class="srch-sec">' + (L === 'en' ? 'Popular commands' : '常用命令') + '</div>';
    tools.forEach(function (e, i) { html += itemHTML(e, rec.length + i, false, null); });
    panel.innerHTML = '<ul class="srch-list">' + html + '</ul>' +
      '<div class="srch-foot"><span>↑↓ ' + (L === 'en' ? 'navigate' : '选择') + '</span>' +
      '<span>Enter ' + (L === 'en' ? 'open' : '打开') + '</span>' +
      '<span>Esc ' + (L === 'en' ? 'close' : '关闭') + '</span>' +
      '<span class="srch-count">' + tools.length + (L === 'en' ? ' tools · ' : ' 个工具 · ') +
      (DATA.articles || []).length + (L === 'en' ? ' articles' : ' 篇教程') + '</span></div>';
    items = rec.concat(tools);
    active = -1;
    bindItems();
    open();
  }

  function renderResults(res, tokens) {
    var L = lang();
    if (!res.length) {
      var q = esc(input.value.trim());
      panel.innerHTML = '<div class="srch-empty">' + (L === 'en'
        ? 'No match for <b>' + q + '</b>.<br>Try a tool name, e.g. <b>quantities</b>, <b>keynotes</b>.'
        : '没有找到与 <b>' + q + '</b> 相关的内容。<br>试试工具名，如 <b>算量</b>、<b>注释</b>、<b>镜像</b>。') +
        '</div>';
      items = [];
      active = -1;
      open();
      return;
    }
    var html = '<div class="srch-sec">' + (L === 'en' ? 'Results' : '搜索结果') + '</div>';
    res.forEach(function (r, i) { html += itemHTML(r.e, i, i === 0, tokens); });
    panel.innerHTML = '<ul class="srch-list">' + html + '</ul>' +
      '<div class="srch-foot"><span>↑↓ ' + (L === 'en' ? 'navigate' : '选择') + '</span>' +
      '<span>Enter ' + (L === 'en' ? 'open' : '打开') + '</span>' +
      '<span>Esc ' + (L === 'en' ? 'close' : '关闭') + '</span>' +
      '<span class="srch-count">' + res.length + (L === 'en' ? ' results' : ' 条结果') + '</span></div>';
    items = res.map(function (r) { return r.e; });
    active = 0;
    bindItems();
    open();
  }

  function run() {
    var q = input.value;
    if (!q.trim()) { renderDefault(); return; }
    var res = rank(q);
    renderResults(res || [], res && res.length ? res[0].tokens : null);
  }

  function go(e) {
    remember(e);
    close();
    var url = e.file + (e.anchor ? '#' + e.anchor : '');
    if (e.file === PAGE) {
      if (e.anchor) {
        var el = document.getElementById(e.anchor);
        if (el) {
          el.scrollIntoView({ behavior: 'smooth', block: 'start' });
          try { history.replaceState(null, '', '#' + e.anchor); } catch (err) { location.hash = e.anchor; }
        }
      }
      input.blur();
      return;
    }
    location.href = url;
  }

  function pick(i) {
    var e = items[i];
    if (e) go(e);
  }

  /* ---------- 事件 ---------- */
  var timer = null;
  input.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(run, 70);
  });
  input.addEventListener('focus', function () { run(); });
  input.addEventListener('keydown', function (ev) {
    var k = ev.key;
    if (k === 'ArrowDown' || k === 'ArrowUp') {
      if (!items.length) return;
      ev.preventDefault();
      var n = items.length;
      var next = k === 'ArrowDown' ? (active + 1) % n : (active - 1 + n) % n;
      setActive(next);
    } else if (k === 'Enter') {
      if (active >= 0 && items[active]) { ev.preventDefault(); go(items[active]); }
    } else if (k === 'Escape') {
      close();
      input.blur();
    } else if (k === 'Tab') {
      close();
    }
  });

  document.addEventListener('mousedown', function (ev) {
    if (!dock.contains(ev.target)) close();
  });

  document.addEventListener('keydown', function (ev) {
    var tag = (ev.target.tagName || '').toLowerCase();
    var typing = tag === 'input' || tag === 'textarea' || ev.target.isContentEditable;
    if ((ev.ctrlKey || ev.metaKey) && ev.key.toLowerCase() === 'k') {
      ev.preventDefault();
      input.focus();
      input.select();
    } else if (ev.key === '/' && !typing) {
      ev.preventDefault();
      input.focus();
    }
  });

  // 语言切换后刷新占位符与面板
  new MutationObserver(function () {
    placeholder();
    if (panel.classList.contains('open')) run();
  }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-lang'] });
})();
