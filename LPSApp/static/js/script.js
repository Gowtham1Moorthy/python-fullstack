// ---------------- Up Arrow -----------------
document.addEventListener("DOMContentLoaded", function () {
    const scrollToTopButton = document.getElementById("scroll-to-top");

    scrollToTopButton.addEventListener("click", () => {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    });

    window.addEventListener("scroll", () => {
        if (window.pageYOffset > 60) {
            scrollToTopButton.style.display = "block";
        } else {
            scrollToTopButton.style.display = "none";
        }
    });
});

// // -----------------------------------------Dark Mode--------------------------
window.addEventListener('DOMContentLoaded', () => {
    const icon = document.querySelector(".mode");
    const switchInput = document.getElementById('switch');
    
    // Initialize color mode based on local storage or system preferences
    const preferredColorMode = localStorage.getItem('colorMode');
    if (preferredColorMode === 'dark-mode') {
        applyColorPalette('dark-mode');
        switchInput.checked = true;
    } else {
        applyColorPalette('scratchman');
        switchInput.checked = false;
    }
    
    icon.addEventListener("click", () => {
        toggleColorPalette();
    });
});

function toggleColorPalette() {
    const switchInput = document.getElementById('switch');
    if (switchInput.checked) {
        applyColorPalette('dark-mode');
        localStorage.setItem('colorMode', 'dark-mode');
    } else {
        applyColorPalette('scratchman');
        localStorage.setItem('colorMode', 'scratchman');
    }
}

function applyColorPalette(palette) {
    const root = document.documentElement;
    root.className = palette;
}

//--------------------------End Dark Mode----------------------------

function toggleMenu(button){
    const content = document.querySelector('.dropdown-content');
    content.classList.toggle('show');
    if(button.classList.contains('showing')){
        enableScrolling();
        button.innerHTML = '&#9776;'
    }
    else{
        disableScrolling();
        button.innerHTML = '&#x2715;'
    }
    button.classList.toggle('showing');
}

// Function to disable the scrolling
function disableScrolling() {
    const header = document.querySelector('header');
    const scrollY = window.scrollY;

    header.removeAttribute('id');
    document.body.style.position = "fixed";
    document.body.style.top = `${-scrollY}px`;
}

// Function to enable the scrolling
function enableScrolling() {
    const header = document.querySelector('header');
    const scrollY = parseInt(document.body.style.top);

    header.setAttribute('id', 'mainHeader');
    document.body.style.position = "";
    document.body.style.top = "";
    window.scrollTo(0, -scrollY); // Scroll back down to where screen was at
}

function extractTicketNames(inputString) {
    // Regular expression to match text within angle brackets
    var regex = /<Ticket: (.*?)>/g;

    // Use the match method to find all matches in the input string
    var matches = inputString.match(regex);

    // Check if there are matches
    if (matches) {
      // Extract and return the ticket names from the matches
        return matches.map(match => match.replace('<Ticket: ', '').replace('>', ''));
    } else {
      // Return an empty array if no matches are found
        return [];
    }
}

function slugify(str) {
    return String(str)
      .normalize('NFKD') // split accented characters into their base characters and diacritical marks
      .replace(/[\u0300-\u036f]/g, '') // remove all the accents, which happen to be all in the \u03xx UNICODE block.
      .trim() // trim leading or trailing whitespace
      .toLowerCase() // convert to lowercase
      .replace(/[^a-z0-9 -]/g, '') // remove non-alphanumeric characters
      .replace(/\s+/g, '-') // replace spaces with hyphens
      .replace(/-+/g, '-'); // remove consecutive hyphens
}

function searchLotto(input, tickets) {
    const ticketNames = extractTicketNames(tickets);
    const search = input.value.toLowerCase();

    // Filter ticket names based on the search term
    const matchingTickets = ticketNames.filter(ticketName => ticketName.toLowerCase().includes(search));

    // Display search results in the 'searchResults' container
    displaySearchResults(matchingTickets);
}

function displaySearchResults(results) {
    const resultsContainer = document.querySelector('.lottoCards');

    // Clear previous results
    resultsContainer.innerHTML = '';

    // Display each result
    if(results){
        if(results.length > 0){
            results.forEach(result => {
                const slugResult = slugify(result);
                const resultLink = document.createElement('a');
                const lottoCard = document.createElement('div');
                lottoCard.classList.add('lottoCard');
                const lottoName = document.createElement('h2');
    
                resultLink.href = `../home/${slugResult}`;
                lottoName.textContent = result;
    
                lottoCard.appendChild(lottoName);
                resultLink.appendChild(lottoCard);
                resultsContainer.appendChild(resultLink);
            });
        }
        else{
            const lottoCard = document.createElement('div');
            lottoCard.classList.add('lottoCard');
            const lottoName = document.createElement('h2');

            lottoName.textContent = 'No Results';

            lottoCard.appendChild(lottoName);
            resultsContainer.appendChild(lottoCard);
        }
    }
}
