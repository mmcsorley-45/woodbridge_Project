let allLocations = [];

const typeSelect = document.getElementById('type-select');
const locationSelect = document.getElementById('location_id');
const form = document.getElementById('ticket-form');

// Load all locations once on page load
fetch('/locations')
  .then(res => res.json())
  .then(data => {
    allLocations = data;
  });

// When the user selects a type, filter location dropdown
typeSelect.addEventListener('change', () => {
  const selectedType = typeSelect.value;

  // Clear previous options
  locationSelect.innerHTML = '<option value="">-- Select Location --</option>';

  // Filter and repopulate
  allLocations
    .filter(loc => loc.type === selectedType)
    .forEach(loc => {
      const opt = document.createElement('option');
      opt.value = loc.id;
      opt.textContent = loc.name;
      locationSelect.appendChild(opt);
    });
});

// On form submit
form.onsubmit = (e) => {
  e.preventDefault();

  const data = {
    issue: document.getElementById('issue').value,
    description: document.getElementById('description').value,
    assigned_to: document.getElementById('assigned_to').value,
    assigned_by: document.getElementById('assigned_by').value,
    location_id: parseInt(locationSelect.value)
  };

  fetch('/tickets', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
    .then(res => {
      if (!res.ok) throw new Error("Failed to create ticket.");
      return res.json();
    })
    .then(() => {
      alert("✅ Ticket Created");
      window.location.href = '/';  // Redirect home
    })
    .catch(err => {
      alert("❌ Could not create ticket");
      console.error(err);
    });
};