document.addEventListener('DOMContentLoaded', function (){
    const boatTypeDropdown = document.getElementById('boat_type');
    const marinaDropdown = document.getElementById('marina');

    if (!boatTypeDropdown || !marinaDropdown) return;

    function buildFetchUrl() {
        const boatType = boatTypeDropdown.value;
        const marinaId = marinaDropdown.value;

        const params = new URLSearchParams();
        if (boatType) params.set('boat_type', boatType);
        if (marinaId) params.set('marina_id', marinaId);

        const query = params.toString();
        return query ? `/filter-boats/?${query}` : '/filter-boats/';
    }

    function renderBoats(data) {
        const gridContainer = document.getElementById('boat-grid');
        if (!gridContainer) return;

        gridContainer.innerHTML = '';

        data.boats.forEach(boat => {
            const imageTag = boat.image
                ? `<img src="${boat.image}" alt="${boat.name}" style="max-width: 75%; height: auto;">`
                : '';

            const item = `
                <a href="/boats/${boat.id}/" class="grid-item">
                    <div>
                        <h3>${boat.name}</h3>
                        ${imageTag}
                        <p>${boat.boat_type}</p>
                    </div>
                </a>`;
            gridContainer.innerHTML += item;
        });
    }

    function fetchAndRender() {
        fetch(buildFetchUrl())
            .then(response => response.json())
            .then(renderBoats)
            .catch(error => {
                console.error('Error fetching boat data:', error);
            });
    }

    boatTypeDropdown.addEventListener('change', fetchAndRender);
    marinaDropdown.addEventListener('change', fetchAndRender);
});
