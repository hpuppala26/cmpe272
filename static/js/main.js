window.onload = function () { startstick() };

function startstick() {
    window.onscroll = function () { stickyfunc() };
    var navbar = document.getElementById("navbar");
    var sticky = navbar.offsetTop;

    function stickyfunc() {
        if (window.pageYOffset >= sticky) {
            navbar.classList.add('sticky');
        }
        else {
            navbar.classList.remove('sticky');
        }
    }
}