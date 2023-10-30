// ---------------- Up Arrow ----------------
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

// -----------------------------------------Dark Mode--------------------------
const icon = document.querySelector(".mode");
const switchInput = document.getElementById('switch');

// Initialize color mode based on local storage or system preferences
const preferredColorMode = localStorage.getItem('colorMode');
if (preferredColorMode === 'light-mode') {
    applyColorPalette('light-mode');
    switchInput.checked = true;
} else {
    applyColorPalette('dark-mode');
    switchInput.checked = false;
}

icon.addEventListener("click", toggleColorPalette);

function toggleColorPalette() {
    const switchInput = document.getElementById('switch');
    if (switchInput.checked) {
        applyColorPalette('light-mode');
        localStorage.setItem('colorMode', 'light-mode');
    } else {
        applyColorPalette('dark-mode');
        localStorage.setItem('colorMode', 'dark-mode');
    }
}

function applyColorPalette(palette) {
    const root = document.documentElement;
    root.className = palette;
}




