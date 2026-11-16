// AquaFill Home Slice JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('station-search');
    const filterButtons = document.querySelectorAll('.station-filter-btn');
    const stationCards = document.querySelectorAll('.station-card');

    function filterStations() {
        const query = (searchInput ? searchInput.value.toLowerCase() : '');
        const activeFilterBtn = document.querySelector('.station-filter-btn.active');
        const filterType = activeFilterBtn ? activeFilterBtn.dataset.filter : 'all';

        stationCards.forEach(card => {
            const name = card.dataset.name ? card.dataset.name.toLowerCase() : '';
            const building = card.dataset.building ? card.dataset.building.toLowerCase() : '';
            const status = card.dataset.status || '';

            const matchesQuery = name.includes(query) || building.includes(query);
            let matchesFilter = true;

            if (filterType === 'online') {
                matchesFilter = (status === 'ONLINE');
            } else if (filterType === 'low_water') {
                matchesFilter = (status === 'LOW_WATER');
            } else if (filterType === 'maintenance') {
                matchesFilter = (status === 'MAINTENANCE' || status === 'OFFLINE');
            }

            if (matchesQuery && matchesFilter) {
                card.classList.remove('hidden');
            } else {
                card.classList.add('hidden');
            }
        });
    }

    if (searchInput) {
        searchInput.addEventListener('input', filterStations);
    }

    if (filterButtons) {
        filterButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                filterButtons.forEach(b => {
                    b.classList.remove('active', 'bg-aqua-navy', 'text-white');
                    b.classList.add('bg-white', 'text-slate-600');
                });
                this.classList.add('active', 'bg-aqua-navy', 'text-white');
                this.classList.remove('bg-white', 'text-slate-600');
                filterStations();
            });
        });
    }

    // Modal toggling for reporting station
    const openReportBtns = document.querySelectorAll('.open-report-btn');
    const reportModal = document.getElementById('report-modal');
    const closeReportBtn = document.getElementById('close-report-modal');
    const modalStationSelect = document.getElementById('id_station');

    if (openReportBtns && reportModal) {
        openReportBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const stationId = this.dataset.stationId;
                if (modalStationSelect && stationId) {
                    modalStationSelect.value = stationId;
                }
                reportModal.classList.remove('hidden');
            });
        });
    }

    if (closeReportBtn && reportModal) {
        closeReportBtn.addEventListener('click', function() {
            reportModal.classList.add('hidden');
        });
    }

    console.log('[AquaFill] Home slice JS initialized.');
});
