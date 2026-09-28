// Keep wide Markdown tables inside their column without changing native table semantics.
document.addEventListener('DOMContentLoaded', function() {
    // Rich notes start inside inert templates; mount them before looking for tables.
    if (typeof initializeInlinePopovers === 'function') initializeInlinePopovers();

    var language = document.documentElement.lang.toLowerCase();
    var instruction = 'Scrollable table. Use the Left and Right Arrow keys to scroll.';
    if (language.indexOf('zh') === 0) {
        instruction = '可横向滚动的表格。使用左右方向键滚动。';
    } else if (language.indexOf('ja') === 0) {
        instruction = '横にスクロールできる表。左右の矢印キーでスクロールします。';
    }

    var wrappers = [];
    document.querySelectorAll('#content table, .inline_expandable-content table').forEach(function(table) {
        // Embedded Gists manage their own tables; do not wrap an existing scroll container twice.
        if (table.closest('.gist') || table.parentElement.classList.contains('table-scroll')) return;
        var wrapper = document.createElement('div');
        wrapper.className = 'table-scroll';
        var caption = table.caption ? table.caption.textContent.trim() : '';
        var label = caption ? caption + '. ' + instruction : instruction;
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);

        // Scrolling or clicking a table must not close its surrounding disclosure.
        // Default link actions and keyboard events (including Escape) remain available.
        wrapper.addEventListener('click', function(event) { event.stopPropagation(); });
        wrappers.push({ element: wrapper, table: table, label: label });
    });

    function updateScrollability() {
        wrappers.forEach(function(item) {
            var wrapper = item.element;
            // Native closed details can retain a measurable width even while hiding their contents.
            // Only overflowing tables outside closed details and with visible layout need a tab stop.
            var overflowing = !wrapper.closest('details:not([open])') && wrapper.clientWidth > 0 &&
                wrapper.scrollWidth > wrapper.clientWidth + 1;
            if (overflowing) {
                wrapper.setAttribute('tabindex', '0');
                wrapper.setAttribute('role', 'region');
                wrapper.setAttribute('aria-label', item.label);
            } else {
                wrapper.removeAttribute('tabindex');
                wrapper.removeAttribute('role');
                wrapper.removeAttribute('aria-label');
            }
        });
    }

    if (!wrappers.length) return;
    updateScrollability();

    // Covers resizing, opening hidden disclosures, and font/math changes to table width.
    if (typeof ResizeObserver !== 'undefined') {
        var observer = new ResizeObserver(updateScrollability);
        wrappers.forEach(function(item) {
            observer.observe(item.element);
            observer.observe(item.table);
        });
    } else {
        // Older browsers can still refresh after mouse/keyboard disclosure interactions.
        document.addEventListener('click', updateScrollability);
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' || event.key === ' ') requestAnimationFrame(updateScrollability);
        });
    }
    // Native details may open/close without a size change reported by ResizeObserver.
    document.addEventListener('toggle', updateScrollability, true);
    window.addEventListener('resize', updateScrollability);
    window.addEventListener('load', updateScrollability);
    if (document.fonts) document.fonts.ready.then(updateScrollability);
});
