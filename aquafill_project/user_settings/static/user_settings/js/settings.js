// AquaFill Settings Slice JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const tabBtns = document.querySelectorAll('.settings-tab-btn');
    const tabContents = document.querySelectorAll('.settings-tab-content');

    if (tabBtns.length > 0 && tabContents.length > 0) {
        tabBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const targetId = this.dataset.tab;

                tabBtns.forEach(b => {
                    b.classList.remove('active', 'bg-aqua-teal', 'text-white');
                    b.classList.add('text-slate-600', 'hover:bg-slate-100');
                });

                tabContents.forEach(tc => {
                    tc.classList.add('hidden');
                });

                this.classList.add('active', 'bg-aqua-teal', 'text-white');
                this.classList.remove('text-slate-600', 'hover:bg-slate-100');

                const targetEl = document.getElementById(targetId);
                if (targetEl) {
                    targetEl.classList.remove('hidden');
                }
            });
        });
    }

    console.log('[AquaFill] Settings slice JS loaded successfully.');
});
