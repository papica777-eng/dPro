<!DOCTYPE html>
<html lang="bg">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Портфолио на Димитър Продромов</title>
    
    <!-- Връзка към манифеста за PWA -->
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#4f46e5">
    <link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/10823/10823366.png">

    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 text-gray-800 font-sans p-4">

    <div class="max-w-2xl mx-auto bg-white p-6 rounded-xl shadow-lg mt-6">
        <h1 class="text-3xl font-bold text-center text-indigo-600 mb-2">Димитър Продромов</h1>
        <p class="text-center text-gray-500 mb-6">Junior Backend Developer • Firebase Project</p>

        <!-- Бутон за инсталиране (показва се само ако може) -->
        <div id="installContainer" class="hidden mb-6 text-center">
            <button id="installBtn" class="bg-gray-800 text-white px-4 py-2 rounded-lg font-bold shadow-md hover:bg-black transition">
                📲 Инсталирай като Приложение
            </button>
        </div>

        <!-- Секция 1: Тест на Поздрав -->
        <div class="mb-6 p-4 border rounded-lg bg-gray-50">
            <h2 class="text-xl font-bold mb-3">👋 Тест: База Данни</h2>
            <input type="text" id="nameInput" placeholder="Въведете вашето име..." 
                   class="w-full p-2 border rounded mb-3">
            <button onclick="testGreet()" 
                    class="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700 transition">
                Изпрати
            </button>
            <div id="greetResult" class="mt-3 text-sm font-medium text-gray-700 min-h-[20px]"></div>
        </div>

        <!-- Секция 2: Тест на Диагностика -->
        <div class="p-4 border rounded-lg bg-gray-50">
            <h2 class="text-xl font-bold mb-3">🩺 Тест: Диагностика</h2>
            <button onclick="testHealth()" 
                    class="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 transition">
                Провери Статус
            </button>
            <div id="healthResult" class="mt-3 text-sm font-medium text-gray-700 min-h-[20px]"></div>
        </div>
    </div>

    <script>
        // --- PWA Инсталация Логика ---
        let deferredPrompt;
        const installBtn = document.getElementById('installBtn');
        const installContainer = document.getElementById('installContainer');

        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            installContainer.classList.remove('hidden');
        });

        installBtn.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const { outcome } = await deferredPrompt.userChoice;
                if (outcome === 'accepted') {
                    installContainer.classList.add('hidden');
                }
                deferredPrompt = null;
            }
        });

        // --- API Логика ---
        // Проверете дали портът е 5001 или 5002 според вашата конфигурация
        const API_BASE = 'http://127.0.0.1:5001/kodi-backend/us-central1/'; 

        async function testGreet() {
            const name = document.getElementById('nameInput').value;
            const resultDiv = document.getElementById('greetResult');
            
            if (!name) {
                resultDiv.innerHTML = '<span class="text-red-500">Моля, въведете име!</span>';
                return;
            }

            resultDiv.innerText = 'Зареждане...';

            try {
                const response = await fetch(`${API_BASE}greetUserDB?name=${encodeURIComponent(name)}`);
                const text = await response.text();
                resultDiv.innerText = text;
            } catch (error) {
                resultDiv.innerHTML = `<span class="text-red-500">Грешка: ${error.message}</span>`;
            }
        }

        async function testHealth() {
            const resultDiv = document.getElementById('healthResult');
            resultDiv.innerText = 'Проверка...';

            try {
                const response = await fetch(`${API_BASE}systemHealth`);
                const data = await response.json();
                
                const dbStatusIcon = data.database.status === 'OK' ? '✅' : '❌';
                const serverStatusIcon = data.server.status === 'OK' ? '✅' : '❌';

                resultDiv.innerHTML = `
                    <div>Сървър: ${data.server.status} ${serverStatusIcon}</div>
                    <div>База данни: ${data.database.status} ${dbStatusIcon}</div>
                    <div class="text-xs text-gray-500 mt-1">${data.database.message}</div>
                `;
            } catch (error) {
                resultDiv.innerHTML = `<span class="text-red-500">Грешка: ${error.message}</span>`;
            }
        }
    </script>
</body>
</html>
