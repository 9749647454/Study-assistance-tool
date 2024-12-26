// Smooth Scroll for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Simple Testimonial Slider
let testimonials = document.querySelectorAll('.testimonials blockquote');
let currentTestimonial = 0;

function showTestimonial(index) {
    testimonials.forEach((testimonial, i) => {
        testimonial.style.display = (i === index) ? 'block' : 'none';
    });
}

// Initial testimonial setup
showTestimonial(currentTestimonial);

// Change testimonial every 5 seconds
setInterval(() => {
    currentTestimonial = (currentTestimonial + 1) % testimonials.length;
    showTestimonial(currentTestimonial);
}, 5000);

// Mobile Menu Toggle (for small screens)
const nav = document.querySelector('nav');
const navLinks = document.querySelector('.nav-links');
const hamburger = document.createElement('div');

hamburger.innerHTML = '☰'; // Menu icon
hamburger.classList.add('hamburger');
hamburger.style.cursor = 'pointer';
hamburger.style.fontSize = '1.5em';
hamburger.style.color = 'white';

nav.appendChild(hamburger);

hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('nav-open');
});

// Close mobile menu when clicking a link
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('nav-open');
    });
});
