const dropdown = document.querySelector('.language-selector');
const language_menu = dropdown.querySelector('.language-selector-menu');
const select = dropdown.querySelector('.select');
const options = dropdown.querySelectorAll('.language-selector-menu button');

select.addEventListener('click', () => {
    language_menu.classList.toggle('language-selector-menu-open');
});

window.addEventListener("click", e => {
    const size = dropdown.getBoundingClientRect();

    if(
        e.clientX < size.left || e.clientX > size.right || e.clientY < size.top || e.clientY > size.bottom
    ) {
        language_menu.classList.remove('language-selector-menu-open');
    }
});

options.forEach(option => {
    option.addEventListener('click', () => {
        options.forEach(option => {
            option.classList.remove('language-active');
        });
        option.classList.add('language-active');
    });
});

const accountBtn = document.getElementById("account-btn");
const accountPanel = document.getElementById("account-panel");

accountBtn.addEventListener("click", function(event) {
    event.stopPropagation();
    accountPanel.classList.toggle("active");
});

document.addEventListener("click", function(event) {
    if (!accountPanel.contains(event.target) && event.target !== accountBtn) {
        accountPanel.classList.remove("active");
    }
});
