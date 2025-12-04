const modal = document.querySelector('.modal');
const openModalBtn = document.querySelector('button');
const closeModalBtn = document.querySelector('.close-button');

openModalBtn.addEventListener('click', () => {
    modal.style.display = 'block';
});

closeModalBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});