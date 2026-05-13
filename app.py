<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ classroom.name }}</title>

    <meta http-equiv="refresh" content="5">

    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            display: flex;
            height: 100vh;
        }

        aside {
            width: 260px;
            background: #1f2937;
            color: white;
            padding: 1rem;
        }

        main {
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .messages {
            flex: 1;
            padding: 1rem;
            overflow-y: auto;
            background: #f5f5f5;
        }

        .message {
            background: white;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 8px;
        }

        form {
            display: flex;
            padding: 1rem;
            gap: 10px;
            background: white;
        }

        input {
            flex: 1;
            padding: 12px;
        }

        button {
            padding: 12px 16px;
            cursor: pointer;
        }

        .online {
            color: #4ade80;
        }
    </style>
</head>
<body>
    <aside>
        <h2>{{ classroom.name }}</h2>
        <p>{{ classroom.beschreibung }}</p>

        <h3>Teilnehmer</h3>

        <ul>
            {% for user in users %}
                <li>
                    <span class="online">●</span>
                    {{ user }}
                </li>
            {% endfor %}
        </ul>

        <a href="{{ url_for('leave', username=username) }}">
            <button>Verlassen</button>
        </a>
    </aside>

    <main>
        <div class="messages">
            {% for msg in messages %}
                <div class="message">
                    <strong>{{ msg.sender }}</strong>
                    <small>{{ msg.time }}</small>
                    <p>{{ msg.text }}</p>
                </div>
            {% endfor %}
        </div>

        <form method="POST">
            <input type="text" name="message" placeholder="Nachricht eingeben..." required>
            <button type="submit">Senden</button>
        </form>
    </main>
</body>
</html>
