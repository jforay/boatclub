document.addEventListener('DOMContentLoaded', function (){
    const boatTypeDropdown = document.getElementById('boat_type');

    const marinaIdElement = document.getElementById('marina-id');
    const marinaId = marinaIdElement ? marinaIdElement.dataset.marinaId : null;

    boatTypeDropdown.addEventListener('change', function() {
        const boatType = this.value;

        let fetchUrl = `/filter-boats/?boat_type=${encodeURIComponent(boatType)}`;

        if (marinaId) {
            fetchUrl += `&marina_id=${marinaId}`
        }

        fetch(fetchUrl)
        .then(response => response.json())
        .then(data => {
            const gridContainer = document.getElementById('boat-grid');
            gridContainer.innerHTML = ''; // Clear the current grid content

            // Populate the grid with the filtered boats
            data.boats.forEach(boat => {
                console.log(boat.image);
                const item = `
                    <a href="/boats/${boat.id}" class="grid-item">
                        <div>
                            <h3>${boat.name}</h3>
                            <img src="${boat.image}" alt="${boat.name}" style="max-width: 75%; height: auto;">
                            <p>${boat.boat_type}</p>
                        </div>
                    </a>`;
                gridContainer.innerHTML += item;
            });
        })
        .catch(error => {
            console.error('Error fetching boat data:', error);
        });
    });
});