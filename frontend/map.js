const map = L.map('map').setView([40.5548, -74.2925], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Map data © OpenStreetMap contributors'
}).addTo(map);

let markerMap = {};  // For clicking from list → map

fetch('/tickets')
  .then(res => res.json())
  .then(tickets => {
    const activeTickets = tickets.filter(t => t.status !== 'closed');

    activeTickets.forEach(ticket => {
  const { latitude, longitude, location_name } = ticket;

  const popup = `
    <strong>${location_name}</strong><br>
    <em>${ticket.issue}</em><br>
    Assigned to: ${ticket.assigned_to || "N/A"}
  `;

  const marker = L.marker([latitude, longitude]).addTo(map)
    .bindPopup(popup);

  markerMap[ticket.id] = marker;

  const ticketList = document.getElementById('tickets');

  // Create outer list item
  const li = document.createElement('li');

  // Add summary info
  const summary = document.createElement('div');
  summary.textContent = `${ticket.issue} (${location_name})`;
  summary.style.cursor = 'pointer';

  // Add detail dropdown
  const details = document.createElement('div');
  details.style.display = 'none';
  details.style.marginTop = '8px';
  details.style.fontSize = '0.9rem';

  details.innerHTML = `
    <strong>Description:</strong> ${ticket.description}<br>
    <strong>Status:</strong> ${ticket.status}<br>
    <strong>Assigned To:</strong> ${ticket.assigned_to || 'N/A'}<br>
    <strong>Assigned By:</strong> ${ticket.assigned_by || 'N/A'}<br>
    <strong>Location ID:</strong> ${ticket.location_id}
  `;

  summary.onclick = () => {
    // Toggle dropdown
    details.style.display = details.style.display === 'none' ? 'block' : 'none';
    // Center map and open marker popup
    map.setView([latitude, longitude], 16);
    marker.openPopup();
  };

  li.appendChild(summary);
  li.appendChild(details);
  ticketList.appendChild(li);
});
  })
  .catch(err => {
    console.error('Error fetching tickets:', err);
  });