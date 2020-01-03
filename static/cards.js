document.querySelectorAll("form a[data-target]").forEach((link) => {
    link.addEventListener("click", (e) => {
        e.preventDefault();
        console.log("Clicked !");
        document.getElementById(e.target.dataset.target).submit();
    });
});