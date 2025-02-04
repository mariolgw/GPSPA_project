// script.js

// Fetching a list of stations
const dropdownMenu = document.getElementById('dropdown-menu');

async function fetchStations() {
    try {
        const response = await fetch('../components/stations.json');
        const stations = await response.json();
        populateDropdown(stations);
    } catch (error) {
        console.error('Error fetching stations:', error);
    }
}

function populateDropdown(stations) {
    dropdownMenu.innerHTML = '';
    stations.forEach(station => {
        const item = document.createElement('div');
        item.className = 'dropdown-item';
        item.textContent = station;
        item.onclick = () => selectStation(station);
        dropdownMenu.appendChild(item);
    });
}

function filterStations() {
    const input = document.querySelector('.station-select').value.toLowerCase();
    const items = dropdownMenu.querySelectorAll('.dropdown-item');
    items.forEach(item => {
        if (item.textContent.toLowerCase().includes(input)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}

function toggleDropdown() {
    dropdownMenu.classList.toggle('active');
}

function showTimetable(station) {
    let timetableContainer = document.getElementById('timetable-container');
    if (!timetableContainer) {
        timetableContainer = document.createElement('div');
        timetableContainer.id = 'timetable-container';
        document.body.appendChild(timetableContainer);
    }

    // Fetch and display the timetable (simulated data for now)
    const mockTimetable = [
        { time: '09:00', destination: 'Downtown', platform: '1', status: 'On Time' },
        { time: '09:15', destination: 'Airport', platform: '2', status: 'Delayed 5m' },
        { time: '09:30', destination: 'South Station', platform: '1', status: 'On Time' }
    ];

    const timetableHTML = `
        <div class="timetable">
            <h2>${station} - Current Timetable</h2>
            <table>
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Destination</th>
                        <th>Platform</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${mockTimetable.map(train => `
                        <tr>
                            <td>${train.time}</td>
                            <td>${train.destination}</td>
                            <td>${train.platform}</td>
                            <td>${train.status}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;

    timetableContainer.innerHTML = timetableHTML;
}

function selectStation(station) {
    document.querySelector('.station-select').value = station;
    dropdownMenu.classList.remove('active');
    showTimetable(station);
}

// Initialize the dropdown on page load
fetchStations();