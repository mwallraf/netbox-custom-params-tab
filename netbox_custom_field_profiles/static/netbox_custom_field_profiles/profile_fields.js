(() => {
  function initialize() {
    const select = document.getElementById('id_selected_fields');
    const order = document.getElementById('id_field_order');
    const mode = document.getElementById('id_field_mode');
    const list = document.getElementById('profile-ordered-fields');
    const status = document.getElementById('profile-order-status');
    if (!select || !order || !mode || !list || list.dataset.initialized) return;
    list.dataset.initialized = 'true';
    let ids = [];
    try { ids = JSON.parse(order.value || '[]').map(String); } catch (_) { /* Server shows malformed payload error. */ }
    let dragged = null;
    const chosen = () => Array.from(select.selectedOptions).map(option => option.value);
    const synchronize = () => { order.value = JSON.stringify(ids.map(Number)); };
    function move(id, index, control) {
      const current = ids.indexOf(id);
      ids.splice(current, 1);
      ids.splice(Math.max(0, Math.min(index, ids.length)), 0, id);
      render();
      const row = Array.from(list.children).find(item => item.dataset.fieldId === id);
      const target = row?.querySelector(`[data-control="${control}"]`);
      (target?.disabled ? row.querySelector('[data-control="handle"]') : target)?.focus();
      status.textContent = `Field moved to position ${ids.indexOf(id) + 1} of ${ids.length}.`;
    }
    function render() {
      const selected = chosen();
      ids = ids.filter(id => selected.includes(id));
      selected.forEach(id => { if (!ids.includes(id)) ids.push(id); });
      list.replaceChildren();
      ids.forEach((id, index) => {
        const option = Array.from(select.options).find(item => item.value === id);
        const row = document.createElement('li');
        row.className = 'list-group-item d-flex gap-2 align-items-center';
        row.dataset.fieldId = id;
        const handle = document.createElement('button');
        handle.type = 'button'; handle.textContent = '↕'; handle.className = 'btn btn-outline-secondary';
        handle.draggable = true; handle.dataset.control = 'handle';
        handle.setAttribute('aria-label', `Drag ${option.textContent}`);
        handle.addEventListener('dragstart', event => {
          dragged = id; event.dataTransfer.setData('text/plain', id); event.dataTransfer.effectAllowed = 'move';
        });
        handle.addEventListener('dragend', () => { dragged = null; });
        row.addEventListener('dragover', event => { if (dragged !== null) event.preventDefault(); });
        row.addEventListener('drop', event => {
          if (dragged !== null && ids.includes(dragged)) { event.preventDefault(); move(dragged, index, 'handle'); }
        });
        row.append(handle);
        const label = document.createElement('span'); label.textContent = option.textContent; label.className = 'me-auto'; row.append(label);
        [['up', 'Move up', -1], ['down', 'Move down', 1]].forEach(([key, text, delta]) => {
          const button = document.createElement('button'); button.type = 'button'; button.textContent = text;
          button.className = 'btn btn-outline-secondary btn-sm'; button.dataset.control = key;
          button.setAttribute('aria-label', `${text}: ${option.textContent}`);
          button.disabled = mode.value === 'all' || index + delta < 0 || index + delta >= ids.length;
          button.addEventListener('click', () => move(id, index + delta, key)); row.append(button);
        });
        handle.disabled = mode.value === 'all';
        list.append(row);
      });
      select.disabled = mode.value === 'all';
      synchronize();
    }
    select.addEventListener('change', render); mode.addEventListener('change', render);
    select.form.addEventListener('submit', synchronize);
    render();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize); else initialize();
  document.addEventListener('htmx:afterSwap', initialize);
})();
