function setNavbarActive(navItemId) {
    let navElements = document.getElementsByClassName("main-nav-item");
    let activeElement = document.getElementById(navItemId);

    for (element of navElements) {
        element.classList.remove("active");
    }
    activeElement.classList.add("active");
}