// This file contains the JavaScript code for the website, implementing interactivity and dynamic behavior through functions and event listeners.
const readMoreBtn = document.querySelector('.read-more-btn');
const text = document.querySelector('.text');
// Initially hide the extra text

readMoreBtn.addEventListener('click', () => {
    // Toggle the visibility of the extra text
    text.classList.toggle('show-more');

    // Change the button text based on the visibility of the extra text
    if(readMoreBtn.innerText === 'Read More'){
        readMoreBtn.innerText = 'Read Less';
    }
    else{
        readMoreBtn.innerText = 'Read More';
    }
});
// Functionality to toggle the visibility of the extra text when the button is clicked