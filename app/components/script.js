// script.js

// API base URL
const API_BASE_URL = 'http://127.0.0.1:5000';

// Get DOM elements
const dropdownMenu = document.getElementById('dropdown-menu');
const stationInput = document.querySelector('.station-select');
const timetableContainer = document.getElementById('timetable-container');

// Store refresh intervals for cleanup
const refreshIntervals = new Map();
const countdownIntervals = new Map();

// Route color mapping
const ROUTE_COLORS = {
    'AMARELA': '#ffcc00',
    'VERDE': '#00cc99',
    'VERMELHA': '#ff3366',
    'AZUL': '#6699cc'
};

/**
 * Fetches the list of all available stations from the API.
 * This is called when the page loads to populate the station dropdown.
 * @async
 * @throws {Error} If the API request fails
 * @returns {Promise<void>}
 */
async function fetchStations() {
    const response = await fetch(`${API_BASE_URL}/station_names`);
    if (!response.ok) {
        throw new Error('Failed to fetch stations');
    }
    const stations = await response.json();
    populateDropdown(stations);
}

/**
 * Populates the dropdown menu with station names.
 * Groups stations by name and associates each with its stop IDs.
 * @param {Array<Object>} stations - Array of station objects containing stop_name and stop_id
 */
function populateDropdown(stations) {
    dropdownMenu.innerHTML = '';
    const stationMap = new Map();
    
    stations.forEach(station => {
        if (!stationMap.has(station.stop_name)) {
            stationMap.set(station.stop_name, []);
        }
        stationMap.get(station.stop_name).push(station.stop_id);
    });

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
 * Filters the station list based on user input.
 * Called whenever the user types in the search box.
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
 * Toggles the visibility of the dropdown menu.
 * Called when the user clicks the search input.
 */
function toggleDropdown() {
    dropdownMenu.classList.toggle('active');
}

/**
 * Displays the timetables for a selected station.
 * Creates route badges and timetable sections for each direction.
 * @async
 * @param {string} stationName - The name of the selected station
 * @param {Array<string>} stopIds - Array of stop IDs associated with the station
 */
async function showTimetables(stationName, stopIds) {
    timetableContainer.style.display = 'block';
    timetableContainer.innerHTML = '';
    clearAllIntervals();

    const stationHeader = document.createElement('div');
    stationHeader.className = 'station-header';
    
    const stationNameEl = document.createElement('h2');
    stationNameEl.className = 'station-name';
    stationNameEl.textContent = stationName;
    stationHeader.appendChild(stationNameEl);

    const badgeContainer = document.createElement('div');
    badgeContainer.className = 'route-badges';
    
    timetableContainer.appendChild(stationHeader);

    // Keep track of routes we've already added badges for
    const addedRoutes = new Set();

    for (const stopId of stopIds) {
        const response = await fetch(`${API_BASE_URL}/station_info?stop_id=${stopId}`);
        if (!response.ok) continue;
        
        const stationInfoList = await response.json();
        if (!stationInfoList || !stationInfoList.length) continue;
        
        for (const stationInfo of stationInfoList) {
            // Create route badge if we haven't seen this route
            if (!addedRoutes.has(stationInfo.route_long_name)) {
                const badge = document.createElement('span');
                badge.className = 'route-badge';
                badge.style.backgroundColor = `#${stationInfo.route_color || '6B7280'}`;
                badge.textContent = stationInfo.route_long_name;
                badgeContainer.appendChild(badge);
                addedRoutes.add(stationInfo.route_long_name);
            }
            
            // Create timetable section
            const timetableSection = await createTimetableSection(stopId);
            timetableContainer.appendChild(timetableSection);
            
            await updateTimetable(stopId);
            
            // Set up intervals
            const timetableInterval = setInterval(() => updateTimetable(stopId), 30000);
            refreshIntervals.set(stopId, timetableInterval);
            
            const countdownInterval = setInterval(() => updateCountdown(stopId), 1000);
            countdownIntervals.set(stopId, countdownInterval);
        }
    }

    stationHeader.appendChild(badgeContainer);
}

/**
 * Creates a new timetable section for a specific stop ID.
 * @async
 * @param {string} stopId - The ID of the stop
 * @returns {Promise<HTMLElement>} The created timetable section element
 */
async function createTimetableSection(stopId) {
    const section = document.createElement('div');
    section.className = 'timetable-section';
    section.id = `timetable-${stopId}`;

    const table = document.createElement('table');
    table.className = 'w-full';
    
    table.innerHTML = `
        <tbody id="timetable-body-${stopId}">
            <tr><td colspan="2" class="text-center">Loading...</td></tr>
        </tbody>
    `;
    section.appendChild(table);
    return section;
}

/**
 * Updates the timetable display for a specific stop ID.
 * Fetches latest train times and updates the display with countdown timers.
 * @async
 * @param {string} stopId - The ID of the stop to update
 */
async function updateTimetable(stopId) {
    const tbody = document.getElementById(`timetable-body-${stopId}`);
    const response = await fetch(`${API_BASE_URL}/next_trains?stop_id=${stopId}`);
    if (!response.ok) {
        tbody.innerHTML = '<tr><td colspan="2" class="text-center">Failed to load timetable</td></tr>';
        return;
    }
    
    const data = await response.json();
    if (!data.directions) {
        tbody.innerHTML = '<tr><td colspan="2" class="text-center">No upcoming trains</td></tr>';
        return;
    }

    tbody.innerHTML = '';

    Object.entries(data.directions).forEach(([direction, trains]) => {
        // Get route info for the direction
        const routeInfo = getRouteInfo(direction);
        
        // Direction header with route color
        const headerRow = document.createElement('tr');
        headerRow.innerHTML = `
            <td colspan="2" class="direction-header" style="background-color: ${routeInfo.color}">
                Direction: ${direction}
            </td>
        `;
        tbody.appendChild(headerRow);

        // Column headers under direction
        const columnHeaders = document.createElement('tr');
        columnHeaders.className = 'column-headers';
        columnHeaders.innerHTML = `
            <th>Scheduled</th>
            <th>Wait Time</th>
        `;
        tbody.appendChild(columnHeaders);

        trains.forEach(train => {
            const row = document.createElement('tr');
            
            // Calculate seconds until departure
            const now = new Date();
            const [hours, minutes, seconds] = train.departure_time.split(':').map(Number);
            const departureTime = new Date(now);
            departureTime.setHours(hours, minutes, seconds);
            
            // Handle cases where the departure is tomorrow
            if (departureTime < now) {
                departureTime.setDate(departureTime.getDate() + 1);
            }
            
            const timeDiff = Math.max(0, Math.floor((departureTime - now) / 1000));
            const waitMinutes = Math.floor(timeDiff / 60);
            const waitSeconds = timeDiff % 60;
            const formattedWaitTime = `${waitMinutes}m${waitSeconds.toString().padStart(2, '0')}s`;
            
            row.innerHTML = `
                <td class="departure-time">${train.departure_time}</td>
                <td class="countdown">${formattedWaitTime}</td>
            `;
            tbody.appendChild(row);
        });

        const spacerRow = document.createElement('tr');
        spacerRow.innerHTML = '<td colspan="2" class="direction-spacer"></td>';
        tbody.appendChild(spacerRow);
    });
}

/**
 * Returns the color information for a given direction based on route mapping.
 * @param {string} direction - The direction/terminus of the route
 * @returns {Object} An object containing the color for the route
 */
function getRouteInfo(direction) {
    // Map direction names to their route colors
    const routeMapping = {
        'Odivelas': { color: ROUTE_COLORS.AMARELA },
        'Rato': { color: ROUTE_COLORS.AMARELA },
        'Telheiras': { color: ROUTE_COLORS.VERDE },
        'Cais do Sodré': { color: ROUTE_COLORS.VERDE },
        'Aeroporto': { color: ROUTE_COLORS.VERMELHA },
        'São Sebastião': { color: ROUTE_COLORS.VERMELHA },
        'Reboleira': { color: ROUTE_COLORS.AZUL },
        'Santa Apolónia': { color: ROUTE_COLORS.AZUL }
    };
    
    return routeMapping[direction] || { color: '#6B7280' };
}

/**
 * Updates all countdown timers for a specific stop ID.
 * Called every second to keep wait times accurate.
 * @param {string} stopId - The ID of the stop to update countdowns for
 */
function updateCountdown(stopId) {
    const tbody = document.getElementById(`timetable-body-${stopId}`);
    if (!tbody) return;
    
    const rows = tbody.querySelectorAll('tr');
    rows.forEach(row => {
        const departureCell = row.querySelector('.departure-time');
        const countdownCell = row.querySelector('.countdown');
        
        if (!departureCell || !countdownCell) return;
        
        const departureTime = departureCell.textContent;
        if (!departureTime) return;
        
        const now = new Date();
        const [hours, minutes, seconds] = departureTime.split(':').map(Number);
        const departure = new Date(now);
        departure.setHours(hours, minutes, seconds);
        
        // Handle cases where the departure is tomorrow
        if (departure < now) {
            departure.setDate(departure.getDate() + 1);
        }
        
        const timeDiff = Math.max(0, Math.floor((departure - now) / 1000));
        const waitMinutes = Math.floor(timeDiff / 60);
        const waitSeconds = timeDiff % 60;
        countdownCell.textContent = `${waitMinutes}m${waitSeconds.toString().padStart(2, '0')}s`;
    });
}

/**
 * Clears all active refresh and countdown intervals.
 * Called when switching stations or unloading the page.
 */
function clearAllIntervals() {
    refreshIntervals.forEach((intervalId) => clearInterval(intervalId));
    refreshIntervals.clear();
    countdownIntervals.forEach((intervalId) => clearInterval(intervalId));
    countdownIntervals.clear();
}

/**
 * Handles station selection from the dropdown.
 * Updates the input field and displays the timetables.
 * @param {string} stationName - The name of the selected station
 * @param {Array<string>} stopIds - Array of stop IDs associated with the station
 */
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
        const checkDropdown = setInterval(() => {
            const dropdownItems = dropdownMenu.querySelectorAll('.dropdown-item');
            if (dropdownItems.length > 0) {
                clearInterval(checkDropdown);
                
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