# 📨 NATS Service Subscriber with PostgreSQL Persistence 

This is a complete 3-layered Python application that:

- Subscribes to messages via **NATS**
- Processes them in a **Service Layer**
- Stores them in a **PostgreSQL** database
- Follows a modular architecture with full test coverage

---

## 📁 Folder Structure

- `nats_messaging/`  
  Main application package containing all source code, divided by responsibility:
  
  - `api/`  
    Contains the NATS subscriber that listens for messages from the message bus and initiates processing.

  - `service/`  
    Handles business logic. Receives raw message data, validates and transforms it before passing to the data layer.

  - `data/`  
    Manages direct communication with the PostgreSQL database (e.g., saving messages).

  - `config.py`  
    (Optional) Central place for storing database or server configuration variables.

  - `__init__.py`  
    Marks each subfolder as a Python package.

- `tests/`  
  Contains test scripts for each layer of the system:
  
  - `test_save.py` – Directly tests saving to the database.
  - `test_service.py` – Tests message processing logic.
  - `test_publish.py` – Publishes test messages to NATS.

- `requirements.txt`  
  Python dependencies used in this project.

- `README.md`  
  Full project documentation and setup instructions.


---

## 🐘 PostgreSQL Setup

### 1. Install PostgreSQL

- Download from: https://www.postgresql.org/download/
- Default port: `5432`
- Make sure to install **pgAdmin** for GUI database management

### 2. Create Database

Create a new database in pgAdmin with the following details:

- **Database Name**: `nats_messages_db`

### 3. Create Table

Use the following SQL code inside `nats_messages_db`:

```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL
);
```

---
## 📤 NATS Server Setup

### 1. Download and Extract NATS Server

- Visit the official download page: https://nats.io/download/servers/
- Download the appropriate version for your operating system (Windows/Linux/macOS)
- Extract the archive to a folder of your choice (e.g., `~/tools/nats-server/` or `C:\Tools\nats-server\`)

### 2. Run the NATS Server

Open a terminal and navigate to the folder where `nats-server` binary is located. Then start the server with:

```bash
./nats-server.exe      # On Windows
./nats-server          # On Linux/macOS
```

You should see output like:
```bash
[INF] Starting nats-server
[INF] Listening on 0.0.0.0:4222
[INF] Server is ready
```

Keep this terminal open while using the application.

## 🚀 Running the Application

To be added

## ⚙️ Individual Component Testing

### 🔹 Test: `test_save.py`

**Purpose:**  
Tests the **data layer** by calling `save_message()` directly, bypassing NATS and the service layer.

**Runs:**  
- Connects to PostgreSQL
- Inserts a test message directly into the `messages` table

**How to Run:**

```bash
cd nats-messaging
python tests/test_save.py
```

**Expected Output:**

```bash
[DB] Message saved: This is a test message from test_save.py
```

**How to Check:**

Use pgAdmin to verify that the message was inserted into the messages table.

Preconditions:

- PostgreSQL server is running
- Database nats_messages_db and table messages exist

Use this SQL query:
```sql
SELECT * FROM messages;
```


---

### 🔹 Test: `test_service.py`

**Purpose:**  
Tests the **service layer** by calling `process_message()` with sample input.

**Runs:**  
- Simulates how a message would be received by the subscriber
- Validates and processes the message (there are intentionally two types of messages, one is normal which will be accepted, the other one is blank and it will be ignored to be saved)
- Calls `save_message()` underneath

**How to Run:**

```bash
cd nats-messaging
python tests/test_service.py
```
**Expected Output:**
```bash
[DB] Message saved: This is a message from test_service
[Service] Ignored empty or whitespace-only message.
```

**How to Check:**

The test message should appear in the messages table.
Use pgAdmin to verify that the message was inserted into the messages table.

Preconditions:
- PostgreSQL must be running
- The service and data layers must be functioning

Use this SQL query:
```sql
SELECT * FROM messages;
```


### 🔹 Test: `test_publish.py`

> Ensure the NATS server is running before continuing with these steps.

### Step 1: Start the NATS Subscriber

In one terminal:

```bash
cd nats-messaging
python -m nats_messaging.main
```
Expected output:
```bash
🚀 Starting NATS Messaging Subscriber...
[NATS] Connected to nats://localhost:4222
[NATS] Subscribed to subject 'updates.messages'

```

### Step 2: Publish a Test Message
In a second terminal (keep subscriber running), run this:
```bash
cd nats-messaging
python tests/test_publish.py
```
You'll be prompted to enter a message (I entered `Hi there!`):

```bash
💬 Enter the message to publish to 'updates.messages': Hi there!
✅ Message sent: Hi there!
```

If you enter invalid input (e.g. no input), it will output like this:
```bash
💬 Enter the message to publish to 'updates.messages':  
⚠️  Message is empty. Exiting.
```

**Expected Subscriber Output:**

In the first terminal (subscriber), you should now see for the valid input:
```bash
[NATS] Received on 'updates.messages': Hi there!
[DB] Message saved: Hi there!
```