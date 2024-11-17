const dropdowns = document.querySelectorAll('.operator-selector');

dropdowns.forEach(dropdown => {
    const select = dropdown.querySelector('.select');
    const caret = dropdown.querySelector('.caret');
    const menu = dropdown.querySelector('.menu');
    const options = dropdown.querySelectorAll('.menu li');
    const selected = dropdown.querySelector('.selected');
    const spanText = document.getElementById('operation_id');
    const hiddenInput = document.getElementById('chosen_operation')

    select.addEventListener('click', () => {
        select.classList.toggle('select-clicked');
        caret.classList.toggle('caret-rotate');
        menu.classList.toggle('menu-open');
    });

    options.forEach(option => {
        option.addEventListener('click', () => {
            selected.innerText = option.innerText;
            hiddenInput.value = spanText.innerText.substring(0, 1);

            selected.classList.add("text-fade-in");

            setTimeout(() => {
                selected.classList.remove("text-fade-in");
            }, 300);

            select.classList.remove('select-clicked');

            caret.classList.remove('caret-rotate');

            menu.classList.remove('menu-open');

            options.forEach(option => {
                option.classList.remove('operator-active');
            });

            option.classList.add('operator-active');
        });
    });

    window.addEventListener("click", e => {
        const size = dropdown.getBoundingClientRect();

        if(
            e.clientX < size.left || e.clientX > size.right || e.clientY < size.top || e.clientY > size.bottom
        ) {
            select.classList.remove('select-clicked');
            caret.classList.remove('caret-rotate');

            menu.classList.remove('menu-open');
        }
    });
});