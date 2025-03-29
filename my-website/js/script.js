// This file contains the JavaScript code for the website, implementing interactivity and dynamic behavior through functions and event listeners.

document.addEventListener('DOMContentLoaded', function() {
    // Example function to show an alert when a button is clicked
    const button = document.getElementById('myButton');
    if (button) {
        button.addEventListener('click', function() {
            alert('Button was clicked!');
        });
    }
});