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

  - `__init__.py`  
    Marks each subfolder as a Python package.

  - `main.py`
    Main entry point for the NATS Messaging CLI Application.

- `tests/`  
  Contains test scripts for each layer of the system:
  
  - `test_save.py` – Directly tests saving to the database.
  - `test_service.py` – Tests message processing logic.

- `requirements.txt`  
  Python dependencies used in this project.

- `README.md`  
  Full project documentation and setup instructions.

- `.gitignore`
  Anything that should be ignored.

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

This CLI application uses a modular 3-layered architecture to publish and persist messages through the NATS messaging system.

### 🧠 Overview

- Ensure that the NATS server is running locally.
- You only run **`main.py`** — it acts as the CLI and the entry point to the system.
- It publishes messages to the `NATS` server and waits for a response from the API Layer.
- The rest of the processing (validation, DB saving) is handled **fully downstream** via the API → Service → Data layers.

---

### ✅ How to Run

1. **Make sure PostgreSQL is running and the `nats_messages_db` is set up.**
2. **Start the NATS server locally.**
3. **Run the application with this in terminal:**

```bash
cd nats-messaging
python -m nats_messaging.main
```

#### Use the CLI to send messages
```bash
💬 Type a message to publish to 'updates.messages' (type 'exit' to quit):
📤 > Hello from NATS!
✅ Message processed and saved.
```

If you enter an empty message
```bash
📤 >     
⚠️  Message was ignored (empty or whitespace).
```
---

### **How to Check**

The valid message should appear in the messages table.
Use pgAdmin to verify that the message was inserted into the messages table.

Preconditions:
- PostgreSQL must be running
- The service and data layers must be functioning

Use this SQL query:
```sql
SELECT * FROM messages;
```
---
### 🧩 How It Works Internally

1. `main.py`:
   - Publishes the message to the NATS server using `await nc.publish(...)`
   - Waits for a signal that the message was handled (via `asyncio.Event`)
   - Receives the result (`True` or `False`) via `asyncio.Queue` and displays success/failure to the user

2. `nats_subscriber.py` (API Layer):
   - Subscribes to the NATS subject `'updates.messages'`
   - Receives incoming messages and decodes them
   - Passes the data to the **Service Layer** for business logic processing

3. `message_service.py` (Service Layer):
   - Decodes and validates the message content
   - If valid, it calls `save_message()` in the **Data Layer**
   - Returns a boolean indicating success or ignore

4. `message_repository.py` (Data Layer):
   - Connects to PostgreSQL and inserts the message with a timestamp

---

### **📦 NATS Messaging System – Layered Architecture Flow**
```bash
┌──────────────────────────────────────┐
│          USER (CLI Input)            │
│    Types a message in the terminal   │
└────────────────┬─────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│            main.py (CLI)             │
│ - Publishes message to NATS          │
│ - await nc.publish(..., message)     │
└────────────────┬─────────────────────┘
                 │
                 ▼
         NATS Server (Broker)
                 │
                 ▼
┌──────────────────────────────────────┐
│      nats_subscriber.py (API Layer)  │
│ - Subscribes to 'updates.messages'   │
│ - Receives msg as msg.data (bytes)   │
│ - Prints decoded content             │
│ - Calls: process_message(msg.data)   │
└────────────────┬─────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│ message_service.py (Service Layer)   │
│ - Decodes, strips, validates msg     │
│ - If valid, calls: save_message()    │
└────────────────┬─────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────┐
│ message_repository.py (Data Layer)   │
│ - Connects to PostgreSQL             │
│ - INSERT INTO messages table         │
│   (content, timestamp)               │
└──────────────────────────────────────┘
```


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