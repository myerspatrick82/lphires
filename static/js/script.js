// This file contains the JavaScript code for the website, implementing interactivity and dynamic behavior through functions and event listeners.

document.addEventListener('DOMContentLoaded', () => {
    const readMoreBtn = document.querySelector('.read-more-btn');
    const text = document.querySelector('.text');

    // If the elements exist on the page
    if (readMoreBtn && text) {
        readMoreBtn.addEventListener('click', () => {
            // Toggle the visibility of the extra text
            text.classList.toggle('show-more');

            // Change the button text based on the visibility of the extra text
            if (readMoreBtn.innerText === 'Read More') {
                readMoreBtn.innerText = 'Read Less';
            } else {
                readMoreBtn.innerText = 'Read More';
            }
        });
    } else {
        console.warn('readMoreBtn or text element not found on the page.');
    }
});
