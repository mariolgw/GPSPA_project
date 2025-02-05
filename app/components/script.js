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
    const timetableContainer = document.getElementById('timetable-container');
    const stationName = document.getElementById('station-name');
    const timetableBody = document.getElementById('timetable-body');

    // Show the container
    timetableContainer.style.display = 'block';
    
    // Update station name
    stationName.textContent = `${station} - Current Timetable`;

    // Fetch and display the timetable (simulated data for now)
    const mockTimetable = [
        { time: '09:00', direction: 'Downtown', status: 'On Time' },
        { time: '09:15', direction: 'Airport', status: 'Delayed 5m' },
        { time: '09:30', direction: 'South Station', status: 'On Time' }
    ];

    // Create the rows
    timetableBody.innerHTML = mockTimetable.map(train => `
        <tr>
            <td>${train.time}</td>
            <td>${train.direction}</td>
            <td>${train.status}</td>
        </tr>
    `).join('');
}

// When you're ready to fetch real data, you can use this function
async function fetchTimetableData(station) {
    try {
        const response = await fetch(`/api/timetable/${station}`);
        const timetableData = await response.json();
        return timetableData;
    } catch (error) {
        console.error('Error fetching timetable:', error);
        return null;
    }
}

function selectStation(station) {
    document.querySelector('.station-select').value = station;
    dropdownMenu.classList.remove('active');
    showTimetable(station);
}

// Initialize the dropdown on page load
fetchStations();