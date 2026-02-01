/**
 * Main JavaScript - Daliil Ay Khidma
 */

$(document).ready(function() {
    
    // ==========================================
    // Back to Top Button
    // ==========================================
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('#backToTop').fadeIn();
        } else {
            $('#backToTop').fadeOut();
        }
    });
    
    $('#backToTop').click(function() {
        $('html, body').animate({ scrollTop: 0 }, 800);
        return false;
    });
    
    
    // ==========================================
    // Auto-hide Alerts
    // ==========================================
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
    
    
    // ==========================================
    // Navbar Scroll Effect
    // ==========================================
    $(window).scroll(function() {
        if ($(this).scrollTop() > 50) {
            $('.navbar').addClass('shadow-sm');
        } else {
            $('.navbar').removeClass('shadow-sm');
        }
    });
    
    
    // ==========================================
    // Smooth Scroll for Anchor Links
    // ==========================================
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        
        var target = $(this.hash);
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top - 70
            }, 800);
        }
    });
    
    
    // ==========================================
    // Form Validation Feedback
    // ==========================================
    $('form').on('submit', function() {
        var form = $(this);
        if (form[0].checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.addClass('was-validated');
    });
    
    
    // ==========================================
    // Image Lazy Loading
    // ==========================================
    if ('loading' in HTMLImageElement.prototype) {
        const images = document.querySelectorAll('img[loading="lazy"]');
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
    
    
    // ==========================================
    // Tooltips Initialization
    // ==========================================
    var tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    
    // ==========================================
    // Popovers Initialization
    // ==========================================
    var popoverTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="popover"]')
    );
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    
    // ==========================================
    // AJAX CSRF Token Setup
    // ==========================================
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    const csrftoken = getCookie('csrftoken');
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    
    
    // ==========================================
    // Search Modal Auto-focus
    // ==========================================
    $('#searchModal').on('shown.bs.modal', function() {
        $('#searchModal input[name="q"]').focus();
    });
    
    
    // ==========================================
    // Print Friendly Console
    // ==========================================
    console.log('%c Daliil Ay Khidma ', 
        'background: #0d6efd; color: white; font-size: 20px; padding: 10px;'
    );
    console.log('%c Made with ❤️ in Egypt ', 
        'background: #198754; color: white; font-size: 14px; padding: 5px;'
    );
    
});

// // دليل أي خدمة - Main JavaScript

// $(document).ready(function() {
//     // Auto-hide alerts after 5 seconds
//     setTimeout(function() {
//         $('.alert').fadeOut('slow');
//     }, 5000);
    
//     // Confirm delete actions
//     $('.btn-delete').on('click', function(e) {
//         if (!confirm('هل أنت متأكد من الحذف؟')) {
//             e.preventDefault();
//         }
//     });
    
//     // Smooth scroll to top
//     $('.scroll-to-top').on('click', function() {
//         $('html, body').animate({scrollTop: 0}, 'slow');
//         return false;
//     });
    
//     // Bootstrap tooltips initialization
//     var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
//     var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
//         return new bootstrap.Tooltip(tooltipTriggerEl);
//     });
// });
