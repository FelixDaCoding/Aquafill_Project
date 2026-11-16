// AquaFill Settings Slice JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const tabBtns = document.querySelectorAll('.settings-tab-btn');
    const tabContents = document.querySelectorAll('.settings-tab-content');

    if (tabBtns.length > 0 && tabContents.length > 0) {
        tabBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const targetId = this.dataset.tab;

                tabBtns.forEach(b => {
                    b.classList.remove('active');
                });

                tabContents.forEach(tc => {
                    tc.classList.add('hidden');
                });

                this.classList.add('active');

                const targetEl = document.getElementById(targetId);
                if (targetEl) {
                    targetEl.classList.remove('hidden');
                }
            });
        });
    }

    console.log('[AquaFill] Settings slice JS loaded successfully.');
});
