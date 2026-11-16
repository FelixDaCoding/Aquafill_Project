// AquaFill Authentication Slice JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const passwordInputs = document.querySelectorAll('input[type="password"]');

    passwordInputs.forEach(input => {
        // Provide visual indicator for caps lock
        input.addEventListener('keyup', function(e) {
            if (e.getModifierState && e.getModifierState('CapsLock')) {
                input.title = 'Caps Lock is ON';
            } else {
                input.title = '';
            }
        });
    });

    console.log('[AquaFill] Auth slice JS loaded.');
});
