document.addEventListener("DOMContentLoaded", function () {
    const items = document.querySelectorAll("li");
    items.forEach((item) => {
        item.addEventListener("mouseenter", () => {
            item.style.transform = "scale(1.05)";
            item.style.transition = "transform 0.2s";
        });
        item.addEventListener("mouseleave", () => {
            item.style.transform = "scale(1)";
        });
    });
});
