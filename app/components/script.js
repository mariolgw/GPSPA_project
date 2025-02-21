// script.js

// API base URL
const API_BASE_URL = 'http://127.0.0.1:5000';

// Get DOM elements
const dropdownMenu = document.getElementById('dropdown-menu');
const stationInput = document.querySelector('.station-select');
const timetableContainer = document.getElementById('timetable-container');

// Store refresh intervals for cleanup
const refreshIntervals = new Map();

async function fetchStations() {
    try {
        const response = await fetch(`${API_BASE_URL}/station_names`);
        if (!response.ok) {
            throw new Error('Failed to fetch stations');
        }
        const stations = await response.json();
        populateDropdown(stations);
    } catch (error) {
        console.error('Error fetching stations:', error);
        alert('Failed to load stations. Please try again later.');
    }
}

function populateDropdown(stations) {
    dropdownMenu.innerHTML = '';
    // Group stations by name to handle multiple stop_ids
    const stationMap = new Map();
    
    stations.forEach(station => {
        if (!stationMap.has(station.stop_name)) {
            stationMap.set(station.stop_name, []);
        }
        stationMap.get(station.stop_name).push(station.stop_id);
    });

    // Create dropdown items for unique station names
    stationMap.forEach((stopIds, stationName) => {
        const item = document.createElement('div');
        item.className = 'dropdown-item';
        item.textContent = stationName;
        item.dataset.stopIds = JSON.stringify(stopIds);
        item.onclick = () => selectStation(stationName, stopIds);
        dropdownMenu.appendChild(item);
    });
}

function filterStations() {
    const input = stationInput.value.toLowerCase();
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

async function getStationInfo(stopId) {
    const response = await fetch(`${API_BASE_URL}/station_info?stop_id=${stopId}`);
    if (!response.ok) {
        throw new Error('Failed to fetch station info');
    }
    return await response.json();
}

async function createTimetableSection(stopId, stationInfo) {
    const section = document.createElement('div');
    section.className = 'timetable-section';
    section.id = `timetable-${stopId}`;

    // Create table
    const table = document.createElement('table');
    table.className = 'w-full';
    table.innerHTML = `
        <thead>
            <tr>
                <th>Time</th>
                <th>Direction</th>
            </tr>
        </thead>
        <tbody id="timetable-body-${stopId}">
            <tr><td colspan="2" class="text-center">Loading...</td></tr>
        </tbody>
    `;
    section.appendChild(table);

    return section;
}

async function updateTimetable(stopId) {
    const tbody = document.getElementById(`timetable-body-${stopId}`);
    try {
        const response = await fetch(`${API_BASE_URL}/next_trains?stop_id=${stopId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch timetable');
        }
        const data = await response.json();

        if (data.error) {
            tbody.innerHTML = '<tr><td colspan="2" class="text-center">No upcoming trains</td></tr>';
            return;
        }

        tbody.innerHTML = data.trains.map(train => `
            <tr>
                <td class="departure-time">${train.departure_time}</td>
                <td class="direction">${train.stop_headsign}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error(`Error updating timetable for stop ${stopId}:`, error);
        tbody.innerHTML = '<tr><td colspan="2" class="text-center">Failed to load timetable</td></tr>';
    }
}

async function showTimetables(stationName, stopIds) {
    timetableContainer.style.display = 'block';
    timetableContainer.innerHTML = '';
    clearAllIntervals();

    // Create station header with route badges
    const stationHeader = document.createElement('div');
    stationHeader.className = 'station-header';
    
    // Create station name element
    const stationNameEl = document.createElement('h2');
    stationNameEl.className = 'station-name';
    stationNameEl.textContent = stationName;
    stationHeader.appendChild(stationNameEl);

    // Container for route badges
    const badgeContainer = document.createElement('div');
    badgeContainer.className = 'route-badges';
    
    timetableContainer.appendChild(stationHeader);

    // Create and populate timetable for each stop_id
    for (const stopId of stopIds) {
        try {
            const stationInfo = await getStationInfo(stopId);
            
            // Create route badge
            const badge = document.createElement('span');
            badge.className = 'route-badge';
            badge.style.backgroundColor = `#${stationInfo.route_color || '6B7280'}`;
            badge.textContent = stationInfo.route_short_name || 'Train';
            badgeContainer.appendChild(badge);
            
            const timetableSection = await createTimetableSection(stopId, stationInfo);
            timetableContainer.appendChild(timetableSection);
            
            // Initial update and set refresh interval
            await updateTimetable(stopId);
            const intervalId = setInterval(() => updateTimetable(stopId), 30000);
            refreshIntervals.set(stopId, intervalId);
        } catch (error) {
            console.error(`Error setting up timetable for stop ${stopId}:`, error);
        }
    }

    // Add badges after collecting all routes
    stationHeader.appendChild(badgeContainer);
}

function clearAllIntervals() {
    refreshIntervals.forEach((intervalId) => clearInterval(intervalId));
    refreshIntervals.clear();
}

function selectStation(stationName, stopIds) {
    stationInput.value = stationName;
    dropdownMenu.classList.remove('active');
    showTimetables(stationName, stopIds);
}

// Initialize the dropdown on page load
fetchStations();

// Handle URL parameters when page loads
window.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const stationName = urlParams.get('station');
    const stopId = urlParams.get('stop_id');
    
    if (stationName && stopId) {
        // Wait for stations to be fetched and populated
        const checkDropdown = setInterval(() => {
            const dropdownItems = dropdownMenu.querySelectorAll('.dropdown-item');
            if (dropdownItems.length > 0) {
                clearInterval(checkDropdown);
                
                // Find the matching station in the dropdown
                const matchingItem = Array.from(dropdownItems)
                    .find(item => item.textContent === decodeURIComponent(stationName));
                
                if (matchingItem) {
                    const stopIds = JSON.parse(matchingItem.dataset.stopIds);
                    selectStation(decodeURIComponent(stationName), stopIds);
                }
            }
        }, 100);
    }
});

// Clean up intervals when page is unloaded
window.addEventListener('unload', clearAllIntervals);
