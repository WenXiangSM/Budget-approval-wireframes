/* Section flag control for approver pages. One flag per page. */
(function () {
  var wrap = document.querySelector('[data-flag]');
  if (!wrap) return;
  var btn = document.querySelector('[data-flag-btn]');
  var label = btn.querySelector('span');
  var ta = wrap.querySelector('textarea');
  var text = wrap.querySelector('.flag-text');
  var tab = document.querySelector('.steps li:nth-child(' + wrap.getAttribute('data-section') + ') .flag-mark');
  var saved = wrap.getAttribute('data-state') === 'flagged' ? ta.value : '';

  function set(state) {
    wrap.setAttribute('data-state', state);
    var flagged = state === 'flagged';
    btn.classList.toggle('is-flagged', flagged);
    label.textContent = flagged ? 'Flagged' : 'Flag for edits';
    btn.setAttribute('aria-expanded', state === 'editing');
    if (tab) tab.hidden = !flagged;
    if (flagged) text.textContent = saved;
  }
  function edit() { ta.value = saved; set('editing'); ta.focus(); }

  btn.addEventListener('click', function () {
    if (wrap.getAttribute('data-state') === 'editing') set(saved ? 'flagged' : 'off'); else edit();
  });
  wrap.querySelector('[data-flag-edit]').addEventListener('click', edit);
  wrap.querySelector('[data-flag-remove]').addEventListener('click', function () { saved = ''; ta.value = ''; set('off'); });
  wrap.querySelector('[data-flag-save]').addEventListener('click', function () {
    var v = ta.value.trim();
    if (!v) { ta.focus(); return; }
    saved = v; set('flagged');
  });
  wrap.querySelector('[data-flag-cancel]').addEventListener('click', function () { set(saved ? 'flagged' : 'off'); });

  set(wrap.getAttribute('data-state'));
})();
