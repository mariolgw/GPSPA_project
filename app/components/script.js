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

async function fetchStations() {
    const response = await fetch(`${API_BASE_URL}/station_names`);
    if (!response.ok) {
        throw new Error('Failed to fetch stations');
    }
    const stations = await response.json();
    populateDropdown(stations);
}

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

async function createTimetableSection(stopId) {
    const section = document.createElement('div');
    section.className = 'timetable-section';
    section.id = `timetable-${stopId}`;

    const table = document.createElement('table');
    table.className = 'w-full';
    
    // Remove initial headers - they'll be added per direction
    table.innerHTML = `
        <tbody id="timetable-body-${stopId}">
            <tr><td colspan="2" class="text-center">Loading...</td></tr>
        </tbody>
    `;
    section.appendChild(table);
    return section;
}

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
            row.innerHTML = `
                <td class="departure-time">${train.departure_time}</td>
                <td class="countdown">${train.countdown}</td>
            `;
            tbody.appendChild(row);
        });

        const spacerRow = document.createElement('tr');
        spacerRow.innerHTML = '<td colspan="2" class="direction-spacer"></td>';
        tbody.appendChild(spacerRow);
    });
}

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

function clearAllIntervals() {
    refreshIntervals.forEach((intervalId) => clearInterval(intervalId));
    refreshIntervals.clear();
    countdownIntervals.forEach((intervalId) => clearInterval(intervalId));
    countdownIntervals.clear();
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