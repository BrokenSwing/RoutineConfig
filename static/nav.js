window.addEventListener("load", () => {
    let burger = document.querySelector("#nav .navbar-brand .navbar-burger");
    burger.addEventListener("click", () => {
        burger.classList.toggle("is-active");
        let menu = document.querySelector("#nav .navbar-menu");
        menu.classList.toggle("is-active");
    });
});