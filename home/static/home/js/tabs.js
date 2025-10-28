function showTab(tabId) {
    // Hide all tabs
    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => content.style.display = 'none');

    // Remove 'active' class from all buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(button => button.classList.remove('active'));

    // Show the selected tab
    document.getElementById(tabId).style.display = 'block';

    // Add 'active' class to the clicked button
    event.target.classList.add('active');
}