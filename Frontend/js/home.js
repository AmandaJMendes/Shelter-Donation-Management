//--- Dados dummy dos abrigos
let shelters = [];

window.onload = async () => {
  const response = await fetch('http://127.0.0.1:5000/abrigos', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  shelters = await response.json();
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
      option.textContent = shelter.shelter_name;
      option.dataset.id = shelter.id;
      option.addEventListener('click', () => selectShelter(shelter));
      dropdownOptions.appendChild(option);
    });
  }
}

//--- Renderiza itens do abrigo selecionado
async function renderItems(shelterId) {
  const itemsTableBody = document.querySelector('#shelter-items tbody');
  itemsTableBody.innerHTML = ''; // Limpa a tabela

  const response = await fetch(`http://127.0.0.1:5000/itens/shelter/${shelterId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  const items = await response.json();

  const shelterItems = items || [];
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
  const { address_city: city,
    address_neighborhood: neighborhood,
    address_state: state,
    address_street: street } = shelter;
  searchBar.value = shelter.shelter_name;
  dropdownOptions.style.display = 'none';
  viewButton.disabled = false;
  shelterEmail.textContent = shelter.email;
  shelterPhone.textContent = shelter.phone;
  shelterAddress.textContent = `${street}, ${neighborhood}, ${city} - ${state}`;
  shelterCapacity.textContent = shelter.capacity;
  shelterPets.textContent = shelter.accepts_pets ? 'Sim' : 'Não';
  shelterWomenChildren.textContent = shelter.women_and_children_only ? 'Sim' : 'Não';

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

addItemButton.addEventListener('click', () => {
  window.location.href = 'items.html';
});

transferButton.addEventListener('click', () => {
  window.location.href = 'transfer.html';
});
