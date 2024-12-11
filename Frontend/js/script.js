//--- Informações dummy dos abrigos
const shelters = [
    { id: 'abrigo1', name: 'Abrigo Esperança', email: 'esperanca@mail.com', phone: '1234-5678', address: 'Rua da Paz, 123', capacity: 50, pets: 'Sim', womenChildren: 'Sim' },
    { id: 'abrigo2', name: 'Lar dos Anjos', email: 'anjos@mail.com', phone: '2345-6789', address: 'Avenida Harmonia, 456', capacity: 30, pets: 'Não', womenChildren: 'Não' },
    { id: 'abrigo3', name: 'Refúgio da Paz', email: 'refugio@mail.com', phone: '3456-7890', address: 'Praça do Amor, 789', capacity: 20, pets: 'Sim', womenChildren: 'Sim' },
    { id: 'abrigo4', name: 'Casa da Solidariedade', email: 'solidariedade@mail.com', phone: '4567-8901', address: 'Alameda da Luz, 12', capacity: 40, pets: 'Não', womenChildren: 'Sim' },
    { id: 'abrigo5', name: 'Lar da Harmonia', email: 'harmonia@mail.com', phone: '5678-9012', address: 'Rua Estrela, 345', capacity: 25, pets: 'Sim', womenChildren: 'Não' },
    { id: 'abrigo6', name: 'Refúgio do Amor', email: 'amor@mail.com', phone: '6789-0123', address: 'Rua do Sol, 678', capacity: 15, pets: 'Não', womenChildren: 'Sim' },
    { id: 'abrigo7', name: 'Abrigo da Esperança Viva', email: 'esperancaviva@mail.com', phone: '7890-1234', address: 'Avenida da Vida, 89', capacity: 35, pets: 'Sim', womenChildren: 'Sim' },
    { id: 'abrigo8', name: 'Casa da Alegria', email: 'alegria@mail.com', phone: '8901-2345', address: 'Rua Felicidade, 56', capacity: 20, pets: 'Sim', womenChildren: 'Não' },
    { id: 'abrigo9', name: 'Lar dos Corações Unidos', email: 'coracoesunidos@mail.com', phone: '9012-3456', address: 'Praça União, 78', capacity: 50, pets: 'Sim', womenChildren: 'Sim' },
    { id: 'abrigo10', name: 'Refúgio do Sol', email: 'sol@mail.com', phone: '0123-4567', address: 'Avenida Solar, 90', capacity: 30, pets: 'Não', womenChildren: 'Não' },
   
];

const searchBar = document.getElementById('search-bar');
const dropdownOptions = document.getElementById('dropdown-options');
const viewButton = document.getElementById('view-button');
const shelterInfo = document.querySelector('.shelter-info');
const donationImage = document.querySelector('.donation-image');

const shelterEmail = document.getElementById('shelter-email');
const shelterPhone = document.getElementById('shelter-phone');
const shelterAddress = document.getElementById('shelter-address');
const shelterCapacity = document.getElementById('shelter-capacity');
const shelterPets = document.getElementById('shelter-pets');
const shelterWomenChildren = document.getElementById('shelter-women-children');


let isInfoVisible = false;

//--- Exibe todas as opções quando o foco estiver na barra de pesquisa
searchBar.addEventListener('focus', () => {
    renderOptions(shelters);
    dropdownOptions.style.display = 'block';
});

//--- Filtra as opções ao digitar
searchBar.addEventListener('input', () => {
    const query = searchBar.value.toLowerCase();
    const filteredShelters = shelters.filter(shelter =>
        shelter.name.toLowerCase().includes(query)
    );
    renderOptions(filteredShelters);
});

//--- Fecha o dropdown ao clicar fora ou ESC
document.addEventListener('click', (event) => {
    if (!event.target.closest('.search-container')) {
        dropdownOptions.style.display = 'none';
    }
});

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        dropdownOptions.style.display = 'none';
    }
});

//--- Atualiza lista de opção
function renderOptions(options) {
    dropdownOptions.innerHTML = '';
    if (options.length === 0) {
        dropdownOptions.innerHTML = '<div>Nenhum abrigo encontrado</div>';
    } else {
        options.forEach(shelter => {
            const option = document.createElement('div');
            option.textContent = shelter.name;
            option.dataset.id = shelter.id;
            option.addEventListener('click', () => selectShelter(shelter));
            dropdownOptions.appendChild(option);
        });
    }
}


function selectShelter(shelter) {
    searchBar.value = shelter.name;
    dropdownOptions.style.display = 'none';
    viewButton.disabled = false;

    
    shelterEmail.textContent = shelter.email;
    shelterPhone.textContent = shelter.phone;
    shelterAddress.textContent = shelter.address;
    shelterCapacity.textContent = shelter.capacity;
    shelterPets.textContent = shelter.pets;
    shelterWomenChildren.textContent = shelter.womenChildren;
}

//--- Exibe o bloco de informação dps da primeira pesquisa, estava usadno para ajustar a imagem
viewButton.addEventListener('click', () => {
    if (shelterInfo.classList.contains('hidden')) {
        shelterInfo.classList.remove('hidden'); 
        donationImage.style.display = 'flex'; 
        document.querySelector('.content-home').style.flexDirection = 'row'; 
    }
});