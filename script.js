document.addEventListener('DOMContentLoaded', function() {
    console.log('Script loaded');

    // Handle skill cards
    const skillCards = document.querySelectorAll('.skill-card');
    console.log('Found skill cards:', skillCards.length);

    function toggleDetails(card) {
        const skillDetails = card.querySelector('.skill-details');
        const toggleBtn = card.querySelector('.toggle-btn');

        if (skillDetails.classList.contains('hidden')) {
            skillDetails.classList.remove('hidden');
            toggleBtn.textContent = 'LESS';
        } else {
            skillDetails.classList.add('hidden');
            toggleBtn.textContent = 'MORE';
        }
    }

    skillCards.forEach(card => {
        card.addEventListener('click', function(e) {
            if (!e.target.closest('.skill-details')) {
                toggleDetails(this);
            }
        });

        const toggleBtn = card.querySelector('.toggle-btn');
        toggleBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            toggleDetails(card);
        });
    });

    // Handle publication cards
    const publicationCards = document.querySelectorAll('.publication-card');
    publicationCards.forEach(card => {
        const link = card.querySelector('a');
        if (link) {
            card.style.cursor = 'pointer';
            card.addEventListener('click', (e) => {
                // If not clicking the link directly, trigger the link click
                if (!e.target.closest('a')) {
                    window.open(link.href, link.target || '_self');
                }
            });
        }
    });
});
