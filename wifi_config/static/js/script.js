const socket = io();

const networkList = document.getElementById('network-list');
const refreshBtn = document.getElementById('refresh-btn');
const passwordInput = document.getElementById('password');
const connectBtn = document.getElementById('connect-btn');
const exitApBtn = document.getElementById('exit-ap-btn');
const statusDiv = document.getElementById('status');

refreshBtn.addEventListener('click', () => {
    socket.emit('get_networks');
    statusDiv.textContent = 'Refreshing networks...';
});

connectBtn.addEventListener('click', () => {
    const ssid = networkList.value;
    const password = passwordInput.value;
    if (ssid && password) {
        socket.emit('connect_wifi', { ssid, password });
        statusDiv.textContent = 'Connecting...';
    } else {
        alert('Please select a network and enter a password.');
    }
});

exitApBtn.addEventListener('click', () => {
    socket.emit('exit_ap_mode');
    statusDiv.textContent = 'Exiting AP mode...';
});

socket.on('networks_list', (data) => {
    networkList.innerHTML = '<option value="">Select a network</option>';
    data.networks.forEach((network) => {
        const option = document.createElement('option');
        option.value = network;
        option.textContent = network;
        networkList.appendChild(option);
    });
    statusDiv.textContent = 'Networks refreshed.';
});

socket.on('connection_result', (data) => {
    if (data.success) {
        statusDiv.textContent = `Connected successfully. IP: ${data.ip}`;
    } else {
        statusDiv.textContent = `Connection failed: ${data.error}`;
        alert('Connection failed. Please try again.');
    }
});

socket.on('exit_ap_result', (data) => {
    if (data.success) {
        statusDiv.textContent = data.message;
    } else {
        statusDiv.textContent = `Failed to exit AP mode: ${data.message}`;
        alert('Failed to exit AP mode. Please try again.');
    }
});

// Initial network list population
socket.emit('get_networks');