const saveBtn = document.getElementById('save-btn');
const skipBtn = document.getElementById('skip-btn');
const overlay = document.getElementById('loading-overlay');

// Function to show the overlay
function showLoadingOverlay() {
    overlay.style.display = 'block';
}

// Function to hide the overlay
function hideLoadingOverlay() {
    overlay.style.display = 'none';
}

// Update the page with the new movie details
function updateMovieDetails(movie) {
    document.getElementById('movie-title').innerText = movie.title;
    document.getElementById('movie-cover').src = movie.cover;
    document.getElementById('movie-producer').innerText = movie.producer;
    document.getElementById('movie-year').innerText = movie.release_year;
    document.getElementById('movie-duration').innerText = movie.runtime;
}

// Handle skipping to the next movie
skipBtn.addEventListener('click', () => {
    showLoadingOverlay(); // Show the loading overlay before fetching
    fetch('/skip', { method: 'POST' })
        .then(response => response.json())
        .then(movie => {
            updateMovieDetails(movie);
            hideLoadingOverlay(); // Hide the loading overlay after fetching
        });
});

// Handle saving the current movie and going to the next one
saveBtn.addEventListener('click', () => {
    showLoadingOverlay(); // Show the loading overlay before fetching
    fetch('/save', { method: 'POST' })
        .then(response => response.json())
        .then(movie => {
            updateMovieDetails(movie);
            hideLoadingOverlay(); // Hide the loading overlay after fetching
        });
});

// Show loading overlay on initial page load
document.addEventListener('DOMContentLoaded', function () {
    showLoadingOverlay(); // Show the overlay initially when loading
    fetch('/') // Simulate loading data for the first movie
        .then(() => {
            hideLoadingOverlay(); // Hide the overlay once data is fetched
        });
});

