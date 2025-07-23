// Initialize the map
const map = L.map('map').setView([40.5549, -74.2761], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Store markers by ticket ID
const markerMap = {};

fetch('/tickets')
  .then(res => res.json())
  .then(tickets => {
    const activeTickets = tickets.filter(t => t.status !== 'closed');

    activeTickets.forEach(ticket => {
      const {
        id,
        latitude,
        longitude,
        location_name,
        issue,
        description,
        status,
        assigned_to,
        assigned_by,
        location_id
      } = ticket;

      // Create marker & popup
      const popup = `
        <strong>${location_name}</strong><br>
        <em>${issue}</em><br>
        Assigned to: ${assigned_to || "N/A"}
      `;

      const marker = L.marker([latitude, longitude]).addTo(map)
        .bindPopup(popup);

      markerMap[id] = marker;

      // Build ticket list item
      const ticketList = document.getElementById('tickets');
      const li = document.createElement('li');
      li.setAttribute('data-ticket-id', id);

      const summary = document.createElement('div');
      summary.textContent = `${issue} (${location_name})`;
      summary.style.cursor = 'pointer';

      const details = document.createElement('div');
      details.style.display = 'none';
      details.innerHTML = `
        <strong>Description:</strong> ${description}<br>
        <strong>Status:</strong> ${status}<br>
        <strong>Assigned To:</strong> ${assigned_to || 'N/A'}<br>
        <strong>Assigned By:</strong> ${assigned_by || 'N/A'}<br>
        <strong>Location ID:</strong> ${location_id}<br>
        <button class="complete-btn">✅ Complete</button>
      `;

      // Expand/collapse and zoom to marker
      summary.onclick = () => {
        details.style.display = details.style.display === 'none' ? 'block' : 'none';
        map.setView([latitude, longitude], 16);
        marker.openPopup();
      };

      li.appendChild(summary);
      li.appendChild(details);
      ticketList.appendChild(li);

      // Handle "Complete" button
      details.querySelector('.complete-btn').onclick = () => {
        fetch(`/tickets/${id}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ status: 'closed' })
        })
          .then(res => {
            if (!res.ok) throw new Error("Failed to update ticket.");
            // Remove marker and list item
            map.removeLayer(marker);
            li.remove();
          })
          .catch(err => {
            alert("❌ Could not complete ticket.");
            console.error(err);
          });
      };
    });
  });