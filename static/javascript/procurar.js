document.getElementById('search').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const allItems = document.querySelectorAll('.items-container .item');
    
    allItems.forEach(item => {
        const name = item.querySelector('.item-subtitulo').textContent.toLowerCase();
        const category = item.querySelector('.item-category').textContent.toLowerCase();
        const matchesSearch = name.includes(searchTerm) || category.includes(searchTerm);
        
        item.style.display = matchesSearch ? 'flex' : 'none';
        
        // Oculta seções vazias
        const section = item.closest('section');
        const visibleItems = section.querySelectorAll('.item[style*="flex"]').length;
        section.style.display = visibleItems > 0 ? 'block' : 'none';
    });
});