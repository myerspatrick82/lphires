// This file contains the JavaScript code for the website, implementing interactivity and dynamic behavior through functions and event listeners.

document.addEventListener('DOMContentLoaded', function() {
    // Example function to show an alert when a button is clicked
    const button = document.getElementById('myButton');
    if (button) {
        button.addEventListener('click', function() {
            alert('Button was clicked!');
        });
    }

    function selectRole(role) {
    switch (role) {
        case 'pop-artist':
            window.location.href = 'roles/pop-artist.html';
            break;
        case 'ai-researcher':
            window.location.href = 'roles/ai-researcher.html';
            break;
        case 'data-analyst':
            window.location.href = 'roles/data-analyst.html';
            break;
        default:
            console.error('Unknown role:', role);
    }
}

    
    
}
);