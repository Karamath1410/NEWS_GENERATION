document.addEventListener('DOMContentLoaded', function() {
    // Handle all article images
    const articleImages = document.querySelectorAll('.article-image');

    articleImages.forEach(img => {
        // Add loading class
        img.classList.add('loading');

        // Create loading spinner
        const spinner = document.createElement('div');
        spinner.classList.add('spinner');
        img.parentElement.appendChild(spinner);

        img.onload = function() {
            // Remove loading class and spinner when image loads
            img.classList.remove('loading');
            if (spinner) {
                spinner.remove();
            }
        };

        img.onerror = function() {
            // Handle error case
            img.classList.add('error');
            if (spinner) {
                spinner.remove();
            }

            // Set fallback image
            img.src = '/static/images/placeholder.svg';
            img.alt = 'Image not available';

            // Log error
            console.error('Failed to load image:', img.dataset.originalSrc);
        };

        // Store original source and set it
        img.dataset.originalSrc = img.src;
        const tempSrc = img.src;
        img.src = '';
        img.src = tempSrc;
    });
});

// Lazy loading for images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}