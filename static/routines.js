let createRoutineButton = document.getElementById("create-routine-button");
let modal = document.getElementById("creation-modal");

createRoutineButton.addEventListener("click", (e) => {
    modal.classList.toggle("is-active");
    e.preventDefault();
});

document.querySelector("#creation-modal .modal-background").addEventListener("click", () => {
    modal.classList.toggle("is-active");
});

document.querySelector("#creation-modal button[aria-label='close']").addEventListener("click", () => {
    modal.classList.toggle("is-active");
});

let confirmCreationButton = document.getElementById("modal-create");
let cancelCreationButton = document.getElementById("modal-cancel");
let form = document.querySelector("#creation-modal form");

cancelCreationButton.addEventListener("click", (e) => {
    modal.classList.toggle("is-active");
    e.preventDefault();
});

confirmCreationButton.addEventListener("click", (e) => {
    e.preventDefault();
    form.submit();
});