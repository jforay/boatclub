function showTab(tabId) {
    const contents = document.querySelectorAll('.tab-content');

    contents.forEach(content => {
        content.style.display = 'none';
        content.innerHTML = '';
    });

    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(button => button.classList.remove('active'));

    const selectedTab = document.getElementById(tabId);
    selectedTab.style.display = 'block';

    if (tabId === 'welcome') {
        selectedTab.innerHTML = `
            <div style="padding:56.25% 0 0 0;position:relative;">
                <iframe
                    src="https://player.vimeo.com/video/678911241?autoplay=1&muted=1&badge=0&autopause=0&player_id=0&app_id=58479"
                    frameborder="0"
                    allow="autoplay; fullscreen; picture-in-picture; clipboard-write"
                    style="position:absolute;top:0;left:0;width:100%;height:100%;"
                    title="Destination Boat Clubs Carolinas Opening">
                </iframe>
            </div>
        `;
    }

    if (tabId === 'boat-club') {
        selectedTab.innerHTML = `
            <div style="padding:56.25% 0 0 0;position:relative;">
                <iframe
                    src="https://player.vimeo.com/video/798803825?badge=0&autopause=0&player_id=0&app_id=58479"
                    frameborder="0"
                    allow="autoplay; fullscreen; picture-in-picture; clipboard-write"
                    style="position:absolute;top:0;left:0;width:100%;height:100%;"
                    title="Destination What is a Boat Club">
                </iframe>
            </div>
        `;
    }

    if (tabId === 'how-it-works') {
        selectedTab.innerHTML = `
            <div style="padding:56.25% 0 0 0;position:relative;">
                <iframe
                    src="https://player.vimeo.com/video/678912129?badge=0&autopause=0&player_id=0&app_id=58479"
                    frameborder="0"
                    allow="autoplay; fullscreen; picture-in-picture; clipboard-write"
                    style="position:absolute;top:0;left:0;width:100%;height:100%;"
                    title="How it Works">
                </iframe>
            </div>
        `;
    }

    const clickedButton = document.querySelector(`.tab-button[onclick="showTab('${tabId}')"]`);

    if (clickedButton) {
        clickedButton.classList.add('active');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    showTab('welcome');
});