// script.js

// API base URL
const API_BASE_URL = 'http://127.0.0.1:5000';

// Get DOM elements
const dropdownMenu = document.getElementById('dropdown-menu');
const stationInput = document.querySelector('.station-select');
const timetableContainer = document.getElementById('timetable-container');

// Store refresh intervals for cleanup
const refreshIntervals = new Map();

/**
 * Fetch the list of stations from the API and populate the dropdown menu.
 */
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

/**
 * Populate the dropdown menu with the list of stations.
 * @param {Array} stations - List of station objects.
 */
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

/**
 * Filter the dropdown menu based on the input value.
 */
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

/**
 * Toggle the visibility of the dropdown menu.
 */
function toggleDropdown() {
    dropdownMenu.classList.toggle('active');
}

/**
 * Fetch station information from the API.
 * @param {string} stopId - The ID of the stop to retrieve information for.
 * @returns {Object} Station information.
 */
async function getStationInfo(stopId) {
    const response = await fetch(`${API_BASE_URL}/station_info?stop_id=${stopId}`);
    if (!response.ok) {
        throw new Error('Failed to fetch station info');
    }
    return await response.json();
}

/**
 * Create a timetable section for a specific stop.
 * @param {string} stopId - The ID of the stop.
 * @param {Object} stationInfo - Information about the station.
 * @returns {HTMLElement} The timetable section element.
 */
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

/**
 * Update the timetable for a specific stop.
 * @param {string} stopId - The ID of the stop.
 */
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

/**
 * Display timetables for the selected station and stop IDs.
 * @param {string} stationName - The name of the station.
 * @param {Array} stopIds - List of stop IDs for the station.
 */
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

/**
 * Clear all refresh intervals.
 */
func
function clearAllIntervals() {
    refreshIntervals.forEach((intervalId) => clearInterval(intervalId));
    refreshIntervals.clear();
}

/**
 * Handle station selection from the dropdown menu.
 * @param {string} stationName - The name of the selected station.
 * @param {Array} stopIds - List of stop IDs for the selected station.
 */
function selectStation(stationName, stopIds) {
    stationInput.value = stationName;
    dropdownMenu.classList.remove('active');
    showTimetables(stationName, stopIds);
}

// Initialize the dropdown on page load
fetchStations();

// Clean up intervals when page is unloaded
window.addEventListener('unload', clearAllIntervals);