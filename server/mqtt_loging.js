const mqtt = require("mqtt");
const brokerUrl = "mqtt://your_broker_address:1883"; // Use 1883 for unencrypted, 8883 for encrypted

// Configure connection options (optional, but recommended for production)
const options = {
  username: "your_username",
  password: "your_password",
  clientId: "nodejs_hook_client_" + Math.random().toString(16).substr(2, 8),
};

// Connect to the broker
const client = mqtt.connect(brokerUrl, options);

client.on("connect", () => {
  console.log("Connected to MQTT broker");
  // Subscribe to a topic you want to "hook" or monitor
  client.subscribe("sensors/+/data", (err) => {
    if (!err) {
      console.log("Subscribed to sensors/+/data");
    }
  });
});

// This is the "hook" functionality: the callback when a message is received
client.on("message", (topic, message) => {
  console.log(`Received message on topic: ${topic.toString()}`);
  console.log(`Message payload: ${message.toString()}`);

  // **Perform your server-side logic here:**
  // Example: Parse JSON data, store in database, trigger API call, etc.
  try {
    const data = JSON.parse(message.toString());
    // Further processing...
  } catch (e) {
    console.error("Failed to parse JSON message", e);
  }
});

client.on("error", (error) => {
  console.error("Connection error:", error);
});

// Graceful disconnection on script termination (optional)
process.on("SIGINT", () => {
  client.end();
  console.log("Disconnected from MQTT broker. Exiting.");
  process.exit(0);
});
