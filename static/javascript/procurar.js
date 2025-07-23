const searchInput = document.getElementById('search');
searchInput.addEventListener('input', (event) => {
    const value = event.target.value;

    const items = document.querySelectorAll('.items .item');
    const noResults = document.getElementById('no_results');

    let hasResults = false;

    items.forEach(item => {
        const itemTitle = item.querySelector('.item-titulo').textContent;

        if(formatString(itemTitle).indexOf(value) !== -1){
            item.style.display = 'flex';
            item.style.flexDirection = 'column';
            hasResults = true;
        }else{
            item.style.display = 'none';
        }
    })
    if(hasResults){
        noResults.style.display = 'none';
    }else {
        noResults.style.display = 'block';
    }
});

function formatString(value){
    return value.toLowerCase()
    .trim()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');
}