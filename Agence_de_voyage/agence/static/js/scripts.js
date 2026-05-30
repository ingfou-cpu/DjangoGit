/*!
* Start Bootstrap - Grayscale v7.0.6 (https://startbootstrap.com/theme/grayscale)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-grayscale/blob/master/LICENSE)
*/
//
// Scripts
//

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    
        // ============================================
        // Carousel - Défilement automatique toutes les 3 secondes en boucle
        // ============================================
        var carousel = document.getElementById('carouselExampleCaptions');
        
        if (carousel) {
            // Initialiser le carousel avec les options
            var carouselInstance = new bootstrap.Carousel(carousel, {
                interval: 3000,
                wrap: true,
                ride: 'carousel',
                pause: false
            });
    
            // Événement après chaque transition de slide
            carousel.addEventListener('slid.bs.carousel', function() {
                var items = carousel.querySelectorAll('.carousel-item');
                var lastItem = items[items.length - 1];
                var activeItem = carousel.querySelector('.carousel-item.active');
    
                // Si on est à la dernière slide, forcer le retour au début
                if (activeItem === lastItem) {
                    setTimeout(function() {
                        carouselInstance.to(0);
                    }, 3000);
                }
            });
        }
    
    });
    // Toggle Developer button text on collapse show/hide
    document.querySelectorAll('[id^="btn-dev-"]').forEach(function(btn) {
        var targetId = btn.getAttribute('data-bs-target');
        var targetEl = document.querySelector(targetId);
        if (targetEl) {
            targetEl.addEventListener('shown.bs.collapse', function () {
                btn.textContent = 'Masquer';
            });
            targetEl.addEventListener('hidden.bs.collapse', function () {
                btn.textContent = 'Developer';
            });
        }
    });

});
