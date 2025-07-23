const tableBody = document.querySelector('#dashboard-table tbody');
const sortSelect = document.getElementById('sort-by');
let allTickets = [];

fetch('/tickets')
  .then(res => res.json())
  .then(data => {
    allTickets = data;
    renderTable(allTickets);
  });

sortSelect.addEventListener('change', () => {
  const key = sortSelect.value;
  const sorted = [...allTickets].sort((a, b) => {
    if (key === 'date_created') {
      return new Date(b.date_created) - new Date(a.date_created);
    } else {
      return (a[key] || '').localeCompare(b[key] || '');
    }
  });
  renderTable(sorted);
});

function renderTable(tickets) {
  tableBody.innerHTML = '';
  tickets.forEach(ticket => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${ticket.issue}</td>
      <td>${ticket.status}</td>
      <td>${ticket.assigned_to || '—'}</td>
      <td>${ticket.assigned_by || '—'}</td>
      <td>${ticket.location_name}</td>
      <td>${new Date(ticket.date_created).toLocaleString()}</td>
    `;
    tableBody.appendChild(tr);
  });
}