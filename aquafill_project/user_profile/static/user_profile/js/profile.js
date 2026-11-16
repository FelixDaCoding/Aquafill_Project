// AquaFill Profile Slice JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const quickLogBtns = document.querySelectorAll('.quick-log-btn');
    const amountInput = document.getElementById('id_amount_ml');

    if (quickLogBtns && amountInput) {
        quickLogBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const amount = this.dataset.amount;
                amountInput.value = amount;
                // Visual feedback
                this.classList.add('scale-95', 'ring-2', 'ring-teal-400');
                setTimeout(() => {
                    this.classList.remove('scale-95', 'ring-2', 'ring-teal-400');
                }, 200);
            });
        });
    }

    console.log('[AquaFill] Profile slice JS loaded successfully.');
});
