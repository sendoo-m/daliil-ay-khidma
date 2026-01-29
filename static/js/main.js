// دليل أي خدمة - Main JavaScript

$(document).ready(function() {
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
    
    // Confirm delete actions
    $('.btn-delete').on('click', function(e) {
        if (!confirm('هل أنت متأكد من الحذف؟')) {
            e.preventDefault();
        }
    });
    
    // Smooth scroll to top
    $('.scroll-to-top').on('click', function() {
        $('html, body').animate({scrollTop: 0}, 'slow');
        return false;
    });
    
    // Bootstrap tooltips initialization
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
