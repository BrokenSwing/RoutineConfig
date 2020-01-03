document.querySelectorAll("a[data-target]").forEach((link) => {
    link.addEventListener("click", (e) => {
        e.preventDefault();
        document.getElementById(e.target.dataset.target).submit();
    });
});