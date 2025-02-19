// when the website load, this javascript code will auto load
document.addEventListener("DOMContentLoaded", function(){
    activateMenu();
})
function activateMenu()
{
    var current = location.pathname.split('/')[1];
    if (current === "") return;

    var prev_active_nav = document.querySelector(".nav-link.active");
    var prev_mobile_active_nav = document.querySelector(".nav-mobile-link.active");
    prev_mobile_active_nav.classList.remove("active");
    prev_active_nav.classList.remove("active");

    var nav_links = document.getElementsByClassName("nav-link");
    var nav_mobile_links = document.getElementsByClassName("nav-mobile-link");
    for (var i = 0, len = nav_links.length; i < len; i++) {
        if (nav_links[i].getAttribute("href").indexOf(current) !== -1) {
            nav_links[i].classList.add("active");
            nav_mobile_links[i].classList.add("active");
        }
    }
}

function previewFile(imagePreviewId, fileInputId) {
    const preview = document.getElementById(imagePreviewId);
    const file = document.getElementById(fileInputId).files[0];
    const reader = new FileReader();

    reader.addEventListener("load", function () {
        // Convert image file to base64 string and set it as src of image
        preview.src = reader.result;
    }, false);

    if (file) {
        reader.readAsDataURL(file);
    }
}