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
    console.log(scrollY);

    header.removeAttribute('id');
    document.body.style.position = "fixed";
    document.body.style.top = `${-scrollY}px`;
}

// Function to enable the scrolling
function enableScrolling() {
    const header = document.querySelector('header');
    const scrollY = parseInt(document.body.style.top);
    console.log(scrollY);

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
    const cards = document.querySelectorAll('.lottoCard');
    var i = 0;
    cards.forEach(card => {
        const name = card.querySelector('h2');
        if(!results.includes(name.textContent)){
            card.style.display = 'none';
            i++;
        }
        else{
            card.style.display = 'flex';
        }
    });
    if(i==cards.length){
        const lottoCard = document.createElement('div');
        lottoCard.classList.add('lottoCard');
        lottoCard.classList.add('noResults');
        const lottoName = document.createElement('h2');

        lottoName.textContent = 'No Results';

        lottoCard.appendChild(lottoName);
        resultsContainer.appendChild(lottoCard);
    }
}

function showLotto(card){
    const cards = document.querySelectorAll(".lottoCard");
    if(card.classList.contains('show')){
        disableScrolling();
        card.innerHTML = '&#x2715;';
        card.classList.remove('show');
        card.parentElement.classList.remove("active");
        const cardInfo = card.parentElement.querySelector('.hidden');

        cards.forEach(c => {
            if (c !== card.parentElement) {
                c.classList.remove("active");
                const otherCard = c.querySelector('.hidden');
                otherCard.style.opacity = 0;
                otherCard.style.display = "none";

                const button = c.querySelector('button');
                button.innerHTML = '';
                button.classList.add('show');
                button.classList.remove("active");
            }
        });
        card.parentElement.classList.add("active");
        cardInfo.style.display = "block";

        setTimeout(() => {
            cardInfo.style.opacity = 1;
        }, 200);
    }
    else{
        enableScrolling();
        card.innerHTML = '';
        card.classList.add('show');
        card.parentElement.classList.remove("active");
        const cardInfo = card.parentElement.querySelector('.hidden');
        cardInfo.style.opacity = 0;
        cardInfo.style.display = "none";
    }
}