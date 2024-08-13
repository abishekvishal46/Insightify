        document.getElementById('getMapBtn').addEventListener('click', function() {
    const getMapBtn = document.getElementById('getMapBtn');
    const inputFieldContainer = document.getElementById('inputFieldContainer');
    const domainListContainer = document.getElementById('domainListContainer');
    const topImage = document.getElementById('topImage');
    document.getElementById('sparkle').style.display = 'block';

    getMapBtn.style.display = 'none';
    inputFieldContainer.classList.add('show');
    domainListContainer.classList.add('show');
    topImage.classList.add('show');

    setTimeout(() => {
        const domainItems = document.querySelectorAll('.domain-item');
        domainItems.forEach(item => {
            item.classList.add('show');
        });
    }, 10);
});

const domainButtons = document.querySelectorAll('.domain-item');
const inputField = document.getElementById('input');

domainButtons.forEach(button => {
    button.addEventListener('click', function() {
        inputField.value = button.textContent.trim();
    });
});
var TxtType = function(el, toRotate, period) {
    this.toRotate = toRotate;
    this.el = el;
    this.loopNum = 0;
    this.period = parseInt(period, 10) || 2000;
    this.txt = '';
    this.tick();
    this.isDeleting = false;
};

TxtType.prototype.tick = function() {
    var i = this.loopNum % this.toRotate.length;
    var fullTxt = this.toRotate[i];

    if (this.isDeleting) {
        this.txt = fullTxt.substring(0, this.txt.length - 1);
    } else {
        this.txt = fullTxt.substring(0, this.txt.length + 1);
    }

    this.el.innerHTML = '<span class="wrap">' + this.txt + '</span>';

    var that = this;
    var delta = 200 - Math.random() * 100;

    if (this.isDeleting) { delta /= 2; }

    if (!this.isDeleting && this.txt === fullTxt) {
        delta = this.period;
        this.isDeleting = true;
    } else if (this.isDeleting && this.txt === '') {
        this.isDeleting = false;
        this.loopNum++;
        delta = 500;
    }

    setTimeout(function() {
        that.tick();
    }, delta);
};

window.onload = function() {
    var elements = document.getElementsByClassName('typewrite');
    for (var i = 0; i < elements.length; i++) {
        var toRotate = elements[i].getAttribute('data-type');
        var period = elements[i].getAttribute('data-period');
        if (toRotate) {
            // Initialize the typing effect
            new TxtType(elements[i], JSON.parse(toRotate), period);
        }
    }

    // Change the color and underline for "Hordarchier" using JavaScript
    var highlightWord = "Hordarchier";
    var elements = document.querySelectorAll('.typewrite');
    elements.forEach(function(element) {
        var spans = element.querySelectorAll('.wrap span');
        spans.forEach(function(span) {
            var innerHTML = span.innerHTML;
            if (innerHTML.includes(highlightWord)) {
                span.innerHTML = innerHTML.replace(highlightWord, `<span style="color: red; text-decoration: underline;">${highlightWord}</span>`);
            }
        });
    });

    // Inject CSS for cursor effect
    var css = document.createElement("style");
    css.type = "text/css";
    css.innerHTML = ".typewrite > .wrap { border-right: 0.08em solid #333333}";
    document.body.appendChild(css);
};