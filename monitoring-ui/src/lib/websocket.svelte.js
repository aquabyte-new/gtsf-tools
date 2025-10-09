export class WebSocketClient {
    constructor(url, options = {}) {
        this.url = url;
        this.options = { reconnectDelay: 5000, ...options };

        this.websocket = null;
        this.connectionStatus = 'disconnected';
        this.reconnectInterval = null;

        this.listeners = {
            message: [],
            statusChange: [],
            error: []
        };
    }

    connect() {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            return;
        }

        this.setStatus('connecting');

        try {
            this.websocket = new WebSocket(this.url);

            this.websocket.onopen = (event) => {
                console.log('WebSocket connected');
                this.setStatus('connected');

                // Clear reconnect interval on successful connection
                if (this.reconnectInterval) {
                    clearInterval(this.reconnectInterval);
                    this.reconnectInterval = null;
                }
            };

            this.websocket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.emit('message', data);
                } catch (error) {
                    console.error('Error parsing WebSocket message:', error);
                    this.emit('error', error);
                }
            };

            this.websocket.onclose = (event) => {
                console.log('WebSocket disconnected');
                this.setStatus('disconnected');

                // Start reconnection attempts if not manually closed
                if (event.code !== 1000) { // 1000 = normal closure
                    this.scheduleReconnect();
                }
            };

            this.websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.setStatus('error');
                this.emit('error', error);
            };

        } catch (error) {
            console.error('Failed to create WebSocket connection:', error);
            this.setStatus('error');
            this.emit('error', error);
            this.scheduleReconnect();
        }
    }

    disconnect() {
        if (this.reconnectInterval) {
            clearInterval(this.reconnectInterval);
            this.reconnectInterval = null;
        }

        if (this.websocket) {
            this.websocket.close(1000); // Normal closure
            this.websocket = null;
        }

        this.setStatus('disconnected');
    }

    reconnect() {
        this.disconnect();
        this.connect();
    }

    scheduleReconnect() {
        if (this.reconnectInterval) {
            return; // Already scheduled
        }

        this.reconnectInterval = setInterval(() => {
            this.connect();
        }, this.options.reconnectDelay);
    }

    setStatus(status) {
        if (this.connectionStatus !== status) {
            this.connectionStatus = status;
            this.emit('statusChange', status);
        }
    }

    // Event emitter methods
    on(event, callback) {
        if (this.listeners[event]) {
            this.listeners[event].push(callback);
        }
    }

    off(event, callback) {
        if (this.listeners[event]) {
            this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
        }
    }

    emit(event, data) {
        if (this.listeners[event]) {
            this.listeners[event].forEach(callback => callback(data));
        }
    }

    // Getters
    get status() {
        return this.connectionStatus;
    }

    get isConnected() {
        return this.connectionStatus === 'connected';
    }

    get isConnecting() {
        return this.connectionStatus === 'connecting';
    }

    get isDisconnected() {
        return this.connectionStatus === 'disconnected';
    }

    get hasError() {
        return this.connectionStatus === 'error';
    }
}
