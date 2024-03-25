const primaryNav = document.querySelector(".primary-nav");
const navToggle = document.querySelector(".mobile-nav");


navToggle.addEventListener("click", () => {
    const visible = primaryNav.getAttribute("data-visible")
    console.log(visible)

    if (visible === "false") {
        primaryNav.setAttribute("data-visible", true);
    }else {
        primaryNav.setAttribute('data-visible', false)
    }
});