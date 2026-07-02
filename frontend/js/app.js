// Connect to the FastAPI WebSocket server
const socket = new WebSocket("ws://localhost:8000/ws");

// DOM Element References
const connectionStatus = document.getElementById("connection-status");
const insertBtn = document.getElementById("insert-btn");
const resetBtn = document.getElementById("reset-btn");
const nodeValueInput = document.getElementById("node-value");
const visualizationArea = document.getElementById("visualization-area");
const dsSelector = document.getElementById("ds-selector");
const previewBtn = document.getElementById("preview-btn");

// --- 1. WebSocket Event Handlers ---

// Triggered when connection to FastAPI is successful
socket.onopen = (event) => {
    connectionStatus.textContent = "Connected";
    connectionStatus.className = "connected";
    console.log("WebSocket connection established successfully.");
};

// Triggered when connection is lost
socket.onclose = (event) => {
    connectionStatus.textContent = "Disconnected";
    connectionStatus.className = "disconnected";
    console.error("WebSocket connection closed.");
};

// Triggered whenever the Python backend sends data via websocket.send_json()
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Data received from Python:", data);

    if (data.type === "UPDATE_VISUAL") {
        renderNodes(data.payload);
    }
};

// --- 2. Interactive Event Listeners ---

// Send a message to Python when "Insert Node" is clicked
insertBtn.addEventListener("click", () => {
    const value = parseInt(nodeValueInput.value);

    if (isNaN(value)) {
        alert("Please enter a valid number!");
        return;
    }

    if (value < -999 || value > 999) {
        alert("Value must be between -999 and 999!")
        return
    }

    console.log(value)

    // Construct a JSON command to send over the socket
    const message = {
        action: "INSERT",
        value: value
    };

    socket.send(JSON.stringify(message));
    console.log("Sent action to Python:", message);
});

// Handle clicking the "Preview" button
previewBtn.addEventListener("click", () => {
    const selectedStructure = dsSelector.value;

    const message = {
        action: "SWITCH_STRUCTURE",
        structure: selectedStructure
    };

    socket.send(JSON.stringify(message));
    console.log("Requested structure change to:", selectedStructure);
});

// Update socket.onmessage to handle both linear and complex structures
socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Data received from Python:", data);

    if (data.type === "UPDATE_VISUAL") {
        renderVisuals(data.structure_type, data.payload);
    }
};

// Replace your old renderNodes function with a flexible visual renderer
function renderVisuals(structureType, payload) {
    visualizationArea.innerHTML = ""; // Clear canvas

    // LOG THIS: Inspect exactly what Python is handing to your frontend
    console.log(`[DEBUG] Rendering ${structureType} with payload:`, payload);

    switch (structureType) {
        case "LINKED_LIST":
            renderLinkedList(payload);
            break;
        case "QUEUE":
            renderQueue(payload);
            break;
        case "HEAP":
            renderHeap(payload);
            break;
        default:
            console.error("Unknown structure type:", structureType);
    }
}

// Clear everything when "Reset" is clicked
resetBtn.addEventListener("click", () => {
    visualizationArea.innerHTML = "";
    socket.send(JSON.stringify({ action: "RESET" }));
});

// --- 3. Rendering Logic ---

/**
 * Dynamically updates the DOM based on array data received from Python.
 * @param {Array<number>} nodeList - List of numbers to display as visual nodes.
 */
function renderNodes(nodeList) {
    // Clear out the previous layout
    visualizationArea.innerHTML = "";

    // Generate HTML elements for each item in the data structure
    nodeList.forEach((value) => {
        const nodeElement = document.createElement("div");
        nodeElement.className = "visual-node";
        nodeElement.textContent = value;

        // Append the newly created element to our canvas area
        visualizationArea.appendChild(nodeElement);
    });
}

function renderVisuals(structureType, payload) {
    visualizationArea.innerHTML = ""; // Clear canvas

    switch (structureType) {
        case "LINKED_LIST":
            renderLinkedList(payload);
            break;
        case "QUEUE":
            renderQueue(payload);
            break;
        case "HEAP":
            renderHeap(payload);
            break;
        default:
            console.error("Unknown structure type:", structureType);
    }
}

// ─── LINKED LIST RENDERING ──────────────────────────────────────────
function renderLinkedList(nodes) {
    if (!nodes || nodes.length === 0) {
        visualizationArea.innerHTML = "<p class='empty-text'>List is empty (Head -> Null)</p>";
        return;
    }

    const container = document.createElement("div");
    container.className = "linked-list-container";

    nodes.forEach((node) => {
        const nodeEl = document.createElement("div");
        nodeEl.className = "visual-node";

        // FIX: Extract the internal 'value' property from the python dictionary
        nodeEl.textContent = node.value;
        container.appendChild(nodeEl);

        if (node.has_next) {
            const arrowEl = document.createElement("div");
            arrowEl.className = "node-arrow";
            arrowEl.innerHTML = "➔";
            container.appendChild(arrowEl);
        }
    });

    visualizationArea.appendChild(container);
}

// ─── QUEUE RENDERING ────────────────────────────────────────────────
function renderQueue(items) {
    if (!items || items.length === 0) {
        visualizationArea.innerHTML = "<p class='empty-text'>Queue is empty</p>";
        return;
    }

    const container = document.createElement("div");
    container.className = "queue-container";

    items.forEach((value, index) => {
        const itemEl = document.createElement("div");
        itemEl.className = "visual-node queue-item";

        if (index === 0) itemEl.classList.add("queue-front");
        if (index === items.length - 1) itemEl.classList.add("queue-rear");

        // Queues return flat items, but let's make sure it handles objects or numbers safely
        itemEl.textContent = typeof value === 'object' ? value.value : value;
        container.appendChild(itemEl);
    });

    visualizationArea.appendChild(container);
}

// ─── HEAP RENDERING ─────────────────────────────────────────────────
function renderHeap(flatArray) {
    if (!flatArray || flatArray.length === 0) {
        visualizationArea.innerHTML = "<p class='empty-text'>Heap is empty</p>";
        return;
    }

    const container = document.createElement("div");
    container.className = "heap-grid";

    flatArray.forEach((value, index) => {
        const nodeEl = document.createElement("div");
        nodeEl.className = "visual-node heap-node";

        // Safety check for objects vs numbers
        nodeEl.textContent = typeof value === 'object' ? value.value : value;

        const label = document.createElement("span");
        label.className = "node-index";
        label.textContent = `[${index}]`;
        nodeEl.appendChild(label);

        container.appendChild(nodeEl);
    });

    visualizationArea.appendChild(container);
}