document.addEventListener("DOMContentLoaded", function () {
    function toggleDropdown() {
        const dropdown = document.getElementById("dropdownMenu");
        dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
    }

    function closeDropdown(event) {
        const dropdown = document.getElementById("dropdownMenu");
        if (!event.target.closest(".dropdown")) {
            dropdown.style.display = "none";
        }
    }
    const profileSection = document.querySelector(".dropdown > div");
    if (profileSection) {
        profileSection.addEventListener("click", toggleDropdown);
    }

    window.addEventListener("click", closeDropdown);
});