//--- Dados dummy dos abrigos
const shelters = [
  { id: 'abrigo1', name: 'Abrigo Esperança', email: 'esperanca@mail.com', phone: '1234-5678', address: 'Rua da Paz, 123', capacity: 50, pets: 'Sim', womenChildren: 'Sim' },
  { id: 'abrigo2', name: 'Lar dos Anjos', email: 'anjos@mail.com', phone: '2345-6789', address: 'Avenida Harmonia, 456', capacity: 30, pets: 'Não', womenChildren: 'Não' },
  { id: 'abrigo3', name: 'Refúgio da Paz', email: 'refugio@mail.com', phone: '3456-7890', address: 'Praça do Amor, 789', capacity: 20, pets: 'Sim', womenChildren: 'Sim' },
  { id: 'abrigo4', name: 'Casa da Solidariedade', email: 'solidariedade@mail.com', phone: '4567-8901', address: 'Alameda da Luz, 12', capacity: 40, pets: 'Não', womenChildren: 'Sim' },
  { id: 'abrigo5', name: 'Lar da Harmonia', email: 'harmonia@mail.com', phone: '5678-9012', address: 'Rua Estrela, 345', capacity: 25, pets: 'Sim', womenChildren: 'Não' },
  { id: 'abrigo6', name: 'Refúgio do Amor', email: 'amor@mail.com', phone: '6789-0123', address: 'Rua do Sol, 678', capacity: 15, pets: 'Não', womenChildren: 'Sim' },
];

//--- Dados dummy de itens dos abrigos
const items = {
  abrigo1: [
    { name: 'Arroz', category: 'Comida', perishable: true, quantity: 50 },
    { name: 'Feijão', category: 'Comida', perishable: true, quantity: 40 },
  ],
  abrigo2: [
    { name: 'Cobertores', category: 'Vestuário', perishable: false, quantity: 20 },
    { name: 'Fraldas', category: 'Higiene', perishable: true, quantity: 100 },
  ],
  abrigo3: [],
};

//--- Simula se o usuário está logado
const isLoggedIn = false; // Alterar para false para testar comportamento sem login

//--- Seletores do DOM
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

const addItemButton = document.getElementById('add-item-button');
const transferButton = document.getElementById('transfer-button');

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

//--- Renderiza itens do abrigo selecionado
function renderItems(shelterId) {
  const itemsTableBody = document.querySelector('#shelter-items tbody');
  itemsTableBody.innerHTML = ''; // Limpa a tabela

  const shelterItems = items[shelterId] || [];
  if (shelterItems.length === 0) {
    itemsTableBody.innerHTML = '<tr><td colspan="4">Nenhum item encontrado</td></tr>';
    return;
  }

  shelterItems.forEach(item => {
    const row = document.createElement('tr');
    row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.category}</td>
            <td>${item.perishable ? 'Sim' : 'Não'}</td>
            <td>${item.quantity}</td>
        `;
    itemsTableBody.appendChild(row);
  });
}

//--- Seleciona um abrigo
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

  renderItems(shelter.id); // Exibe os itens do abrigo selecionado

  // Habilita botões se o usuário estiver logado
  addItemButton.disabled = !isLoggedIn;
  transferButton.disabled = !isLoggedIn;
}

//--- Exibe o bloco de informação após a primeira pesquisa
viewButton.addEventListener('click', () => {
  if (shelterInfo.classList.contains('hidden')) {
    shelterInfo.classList.remove('hidden');
    donationImage.style.display = 'flex';
    document.querySelector('.content-home').style.flexDirection = 'row';
  }
});
