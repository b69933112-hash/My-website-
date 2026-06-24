from flask import Flask, render_template_string

app = Flask(__name__)

# HTML, CSS और JavaScript कोड (लॉगिन फॉर्म, कैमरा और लूडो गेम के साथ)
HTML_CODE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>मल्टी-फंक्शन सर्वर</title>
    <style>
        body { text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #eef2f3; margin: 0; padding: 20px; }
        h1 { color: #333; margin-bottom: 5px; }
        
        /* रजिस्ट्रेशन फॉर्म स्टाइल */
        .form-container { background: white; max-width: 320px; margin: 40px auto; padding: 25px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: left; }
        .form-container h2 { text-align: center; margin-top: 0; color: #333; }
        .input-group { margin-bottom: 15px; }
        .input-group label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; font-size: 14px; }
        .input-group input { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-size: 15px; }
        .submit-btn { width: 100%; background-color: #4CAF50; padding: 12px; font-size: 16px; font-weight: bold; border: none; color: white; border-radius: 6px; cursor: pointer; }
        
        /* मुख्य कंटेंट (शुरुआत में छुपा रहेगा) */
        #main-content { display: none; }
        
        /* बटन स्टाइल */
        .btn { padding: 12px 24px; font-size: 16px; font-weight: bold; cursor: pointer; border-radius: 25px; border: none; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: 0.2s; }
        .cam-btn { background-color: #e91e63; margin-bottom: 15px; }
        
        #video { display: none; margin: 10px auto; border: 4px solid #fff; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.15); max-width: 90%; }
        
        /* लूडो गेम स्टाइल */
        .game-container { background: white; max-width: 360px; margin: 20px auto; padding: 15px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .status { font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #555; }
        
        /* मिनी लूडो ट्रैक */
        .board { display: flex; justify-content: space-between; background: #ddd; padding: 10px; border-radius: 8px; margin: 15px 0; position: relative; height: 50px; align-items: center; }
        .cell { width: 30px; height: 30px; background: #fff; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 12px; border: 1px solid #ccc; }
        
        /* गोटियाँ */
        .token { width: 18px; height: 18px; border-radius: 50%; display: inline-block; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3); }
        .red-token { background-color: #ff3838; }
        .blue-token { background-color: #2f89fc; }
        
        /* पासा */
        .dice-container { margin: 15px 0; }
        .dice-btn { background-color: #4caf50; padding: 10px 20px; font-size: 18px; }
        .dice-value { font-size: 24px; font-weight: bold; margin-left: 10px; color: #333; }
        .welcome-text { color: #4CAF50; font-size: 18px; font-weight: bold; margin-bottom: 15px; }
    </style>
</head>
<body>

    <!-- 1. नाम, ईमेल, फोन नंबर और पासवर्ड डालने का फॉर्म -->
    <div class="form-container" id="login-form">
        <h2>📝 अपनी जानकारी डालें</h2>
        <form onsubmit="handleLogin(event)">
            <div class="input-group">
                <label>आपका नाम:</label>
                <input type="text" id="username" required placeholder="पूरा नाम लिखें">
            </div>
            <div class="input-group">
                <label>ईमेल आईडी:</label>
                <input type="email" id="email" required placeholder="example@gmail.com">
            </div>
            <div class="input-group">
                <label>फ़ोन नंबर:</label>
                <input type="tel" id="phone" pattern="[0-9]{10}" required placeholder="10 अंकों का नंबर">
            </div>
            <div class="input-group">
                <label>पासवर्ड:</label>
                <input type="password" id="password" required placeholder="पासवर्ड बनाएं">
            </div>
            <button type="submit" class="submit-btn">गेम चालू करें 🚀</button>
        </form>
    </div>

    <!-- 2. मुख्य गेम और कैमरा स्क्रीन (लॉगिन के बाद दिखेगी) -->
    <div id="main-content">
        <h1>मल्टी-फंक्शन सर्वर</h1>
        <div class="welcome-text" id="user-welcome"></div>

        <!-- कैमरा सेक्शन -->
        <button class="btn cam-btn" onclick="openCamera()">📸 मोबाइल कैमरा खोलें</button>
        <br>
        <video id="video" width="320" height="240" autoplay playsinline></video>

        <!-- लूडो गेम सेक्शन -->
        <div class="game-container">
            <h2>🎲 मिनी लूडो गेम</h2>
            <div class="status" id="turn-text">बारी: <span style="color:#ff3838;">लाल खिलाड़ी</span></div>
            
            <div class="board">
                <div class="cell" id="cell-0">स्टार्ट</div>
                <div class="cell" id="cell-1">1</div>
                <div class="cell" id="cell-2">2</div>
                <div class="cell" id="cell-3">3</div>
                <div class="cell" id="cell-4">4</div>
                <div class="cell" id="cell-5">5</div>
                <div class="cell" id="cell-6">6</div>
                <div class="cell" id="cell-7">जीत!</div>
            </div>

            <div class="dice-container">
                <button class="btn dice-btn" id="roll-btn" onclick="rollDice()">पासा फेंकें 🎲</button>
                <span class="dice-value" id="dice-display">-</span>
            </div>
        </div>
    </div>

    <script>
        // --- लॉगिन हैंडलर स्क्रिप्ट ---
        function handleLogin(event) {
            event.preventDefault(); // पेज रीलोड होने से रोकें
            
            const name = document.getElementById('username').value;
            
            // फॉर्म छुपाएं और मुख्य गेम स्क्रीन दिखाएं
            document.getElementById('login-form').style.display = 'none';
            document.getElementById('main-content').style.display = 'block';
            
            // यूजर का स्वागत करें
            document.getElementById('user-welcome').innerText = "स्वागत है, " + name + "! आपका लॉगिन सफल रहा।";
            
            // लूडो बोर्ड लोड करें
            updateBoard();
        }

        // --- कैमरा स्क्रिfrom flask import Flask, render_template_string

app = Flask(__name__)

# HTML, CSS और JavaScript कोड (लॉगिन फॉर्म, कैमरा और लूडो गेम के साथ)
HTML_CODE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>मल्टी-फंक्शन सर्वर</title>
    <style>
        body { text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #eef2f3; margin: 0; padding: 20px; }
        h1 { color: #333; margin-bottom: 5px; }
        
        /* रजिस्ट्रेशन फॉर्म स्टाइल */
        .form-container { background: white; max-width: 320px; margin: 40px auto; padding: 25px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: left; }
        .form-container h2 { text-align: center; margin-top: 0; color: #333; }
        .input-group { margin-bottom: 15px; }
        .input-group label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; font-size: 14px; }
        .input-group input { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-size: 15px; }
        .submit-btn { width: 100%; background-color: #4CAF50; padding: 12px; font-size: 16px; font-weight: bold; border: none; color: white; border-radius: 6px; cursor: pointer; }
        
        /* मुख्य कंटेंट (शुरुआत में छुपा रहेगा) */
        #main-content { display: none; }
        
        /* बटन स्टाइल */
        .btn { padding: 12px 24px; font-size: 16px; font-weight: bold; cursor: pointer; border-radius: 25px; border: none; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: 0.2s; }
        .cam-btn { background-color: #e91e63; margin-bottom: 15px; }
        
        #video { display: none; margin: 10px auto; border: 4px solid #fff; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.15); max-width: 90%; }
        
        /* लूडो गेम स्टाइल */
        .game-container { background: white; max-width: 360px; margin: 20px auto; padding: 15px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .status { font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #555; }
        
        /* मिनी लूडो ट्रैक */
        .board { display: flex; justify-content: space-between; background: #ddd; padding: 10px; border-radius: 8px; margin: 15px 0; position: relative; height: 50px; align-items: center; }
        .cell { width: 30px; height: 30px; background: #fff; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 12px; border: 1px solid #ccc; }
        
        /* गोटियाँ */
        .token { width: 18px; height: 18px; border-radius: 50%; display: inline-block; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3); }
        .red-token { background-color: #ff3838; }
        .blue-token { background-color: #2f89fc; }
        
        /* पासा */
        .dice-container { margin: 15px 0; }
        .dice-btn { background-color: #4caf50; padding: 10px 20px; font-size: 18px; }
        .dice-value { font-size: 24px; font-weight: bold; margin-left: 10px; color: #333; }
        .welcome-text { color: #4CAF50; font-size: 18px; font-weight: bold; margin-bottom: 15px; }
    </style>
</head>
<body>

    <!-- 1. नाम, ईमेल, फोन नंबर और पासवर्ड डालने का फॉर्म -->
    <div class="form-container" id="login-form">
        <h2>📝 अपनी जानकारी डालें</h2>
        <form onsubmit="handleLogin(event)">
            <div class="input-group">
                <label>आपका नाम:</label>
                <input type="text" id="username" required placeholder="पूरा नाम लिखें">
            </div>
            <div class="input-group">
                <label>ईमेल आईडी:</label>
                <input type="email" id="email" required placeholder="example@gmail.com">
            </div>
            <div class="input-group">
                <label>फ़ोन नंबर:</label>
                <input type="tel" id="phone" pattern="[0-9]{10}" required placeholder="10 अंकों का नंबर">
            </div>
            <div class="input-group">
                <label>पासवर्ड:</label>
                <input type="password" id="password" required placeholder="पासवर्ड बनाएं">
            </div>
            <button type="submit" class="submit-btn">गेम चालू करें 🚀</button>
        </form>
    </div>

    <!-- 2. मुख्य गेम और कैमरा स्क्रीन (लॉगिन के बाद दिखेगी) -->
    <div id="main-content">
        <h1>मल्टी-फंक्शन सर्वर</h1>
        <div class="welcome-text" id="user-welcome"></div>

        <!-- कैमरा सेक्शन -->
        <button class="btn cam-btn" onclick="openCamera()">📸 मोबाइल कैमरा खोलें</button>
        <br>
        <video id="video" width="320" height="240" autoplay playsinline></video>

        <!-- लूडो गेम सेक्शन -->
        <div class="game-container">
            <h2>🎲 मिनी लूडो गेम</h2>
            <div class="status" id="turn-text">बारी: <span style="color:#ff3838;">लाल खिलाड़ी</span></div>
            
            <div class="board">
                <div class="cell" id="cell-0">स्टार्ट</div>
                <div class="cell" id="cell-1">1</div>
                <div class="cell" id="cell-2">2</div>
                <div class="cell" id="cell-3">3</div>
                <div class="cell" id="cell-4">4</div>
                <div class="cell" id="cell-5">5</div>
                <div class="cell" id="cell-6">6</div>
                <div class="cell" id="cell-7">जीत!</div>
            </div>

            <div class="dice-container">
                <button class="btn dice-btn" id="roll-btn" onclick="rollDice()">पासा फेंकें 🎲</button>
                <span class="dice-value" id="dice-display">-</span>
            </div>
        </div>
    </div>

    <script>
        // --- लॉगिन हैंडलर स्क्रिप्ट ---
        function handleLogin(event) {
            event.preventDefault(); // पेज रीलोड होने से रोकें
            
            const name = document.getElementById('username').value;
            
            // फॉर्म छुपाएं और मुख्य गेम स्क्रीन दिखाएं
            document.getElementById('login-form').style.display = 'none';
            document.getElementById('main-content').style.display = 'block';
            
            // यूजर का स्वागत करें
            document.getElementById('user-welcome').innerText = "स्वागत है, " + name + "! आपका लॉगिन सफल रहा।";
            
            // लूडो बोर्ड लोड करें
            updateBoard();
        }

        // --- कैमरा स्क्रिप्ट ---
        async function openCamera() {
            const video = document.getElementById('video');
            video.style.display = "block";
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: "user" }
                });
                video.srcObject = stream;
            } catch (err) {
                alert("कैमरा चालू करने की अनुमति नहीं मिली: " + err);
            }
        }

        // --- लूडो गेम स्क्रिप्ट ---
        let positions = { red: 0, blue: 0 };
        let currentTurn = 'red';
        const maxCells = 7;

        function updateBoard() {
            for(let i=0; i<=maxCells; i++) {
                document.getElementById(`cell-${i}`).innerHTML = i === 0 ? "START" : i === maxCells ? "WIN" : i;
            }
            let redCell = document.getElementById(`cell-${positions.red}`);
            if(redCell) redCell.innerHTML += '<span class="token red-token"></span>';
            
            let blueCell = document.getElementById(`cell-${positions.blue}`);
            if(blueCell) blueCell.innerHTML += '<span class="token blue-token"></span>';
        }

        function rollDice() {
            const diceValue = Math.floor(Math.random() * 6) + 1;
            document.getElementById('dice-display').innerText = diceValue;
            
            positions[currentTurn] += diceValue;
            
            if (positions[currentTurn] >= maxCells) {
                positions[currentTurn] = maxCells;
                updateBoard();
                alert((currentTurn === 'red' ? '🔴 लाल खिलाड़ी' : '🔵 नीला खिलाड़ी') + ' जीत गया! 🎉');
                resetGame();
                return;
            }

            updateBoard();

            if (currentTurn === 'red') {
                currentTurn = 'blue';
                document.getElementById('turn-text').innerHTML = 'बारी: <span style="color:#2f89fc;">नीला खिलाड़ी</span>';
            } else {
                currentTurn = 'red';
                document.getElementById('turn-text').innerHTML = 'बारी: <span style="color:#ff3838;">लाल खिलाड़ी</span>';
            }
        }

        function resetGame() {
            positions = { red: 0, blue: 0 };
            currentTurn = 'red';
            document.getElementById('turn-text').innerHTML = 'बारी: <span style="color:#ff3838;">लाल खिलाड़ी</span>';
            document.getElementById('dice-display').innerText = '-';
            updateBoard();
        }
    </scriptप्ट ---
        async function openCamera() {
            const video = document.getElementById('video');
            video.style.display = "block";
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: "user" }
                });
                video.srcObject = stream;
            } catch (err) {
                alert("कैमरा चालू करने की अनुमति नहीं मिली: " + err);
            }
        }

        // --- लूडो गेम स्क्रिप्ट ---
        let positions = { red: 0, blue: 0 };
        let currentTurn = 'red';
        const maxCells = 7;

        function updateBoard() {
            for(let i=0; i<=maxCells; i++) {
                document.getElementById(`cell-${i}`).innerHTML = i === 0 ? "START" : i === maxCells ? "WIN" : i;
            }
            let redCell = document.getElementById(`cell-${positions.red}`);
            if(redCell) redCell.innerHTML += '<span class="token red-token"></span>';
            
            let blueCell = document.getElementById(`cell-${positions.blue}`);
            if(blueCell) blueCell.innerHTML += '<span class="token blue-token"></span>';
        }

        function rollDice() {
            const diceValue = Math.floor(Math.random() * 6) + 1;
            document.getElementById('dice-display').innerText = diceValue;
            
            positions[currentTurn] += diceValue;
            
            if (positions[currentTurn] >= maxCells) {
                positions[currentTurn] = maxCells;
                updateBoard();
                alert((currentTurn === 'red' ? '🔴 लाल खिलाड़ी' : '🔵 नीला खिलाड़ी') + ' जीत गया! 🎉');
                resetGame();
                return;
            }

            updateBoard();

            if (currentTurn === 'red') {
                currentTurn = 'blue';
                document.getElementById('turn-text').innerHTML = 'बारी: <span style="color:#2f89fc;">नीला खिलाड़ी</span>';
            } else {
                currentTurn = 'red';
                document.getElementById('turn-text').innerHTML = 'बारी: <span style="color:#ff3838;">लाल खिलाड़ी</span>';
            }
        }

        function resetGame() {
            positions = { red: 0, blue: 0 };
            currentTurn = 'red';
            document.getElementById('turn-text').innerHTML = 'बारी: <span style="color:#ff3838;">लाल खिलाड़ी</span>';
            document.getElementById('dice-display').innerText = '-';
            updateBoard();
        }
    </script>
</<!-- कॉन्टैक्ट पेज पर जाने के लिए बटन -->
<div style="margin: 20px 0;">
    <a href="/contact">
        <button style="padding: 10px; font-size: 16px;">कॉन्टैक्ट पेज पर जाएं</button>
    </a>
</div>
>
</html>
"""
@app.route('/contact')
