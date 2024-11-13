<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Decrypt AES CBC</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.9-1/crypto-js.js"></script>
</head>
<body>
    <h2>Decrypt AES-128 CBC</h2>
    <form id="decryptForm">
        <label for="encryptedData">Encrypted Data (Base64):</label><br>
        <textarea id="encryptedData" rows="4" cols="50" placeholder="Nhập chuỗi mã hóa (Base64)"></textarea><br><br>

        <label for="key">AES Key (16-byte):</label><br>
        <input type="text" id="key" value="2222222222222222"><br><br>

        <button type="button" onclick="decryptData()">Decrypt</button>
    </form>
    
    <h3>Decrypted Text:</h3>
    <div id="output"></div>

    <script>
        function decryptData() {
            // Lấy chuỗi mã hóa từ người dùng
            const encryptedBase64 = document.getElementById("encryptedData").value;
            const key = document.getElementById("key").value;

            if (!encryptedBase64 || !key) {
                alert("Vui lòng nhập đầy đủ dữ liệu mã hóa và khóa!");
                return;
            }

            // Giải mã Base64 để lấy dữ liệu nhị phân
            const encryptedData = CryptoJS.enc.Base64.parse(encryptedBase64);

            // Tách IV từ 16 byte đầu tiên và dữ liệu mã hóa từ byte thứ 17 trở đi
            const iv = CryptoJS.lib.WordArray.create(encryptedData.words.slice(0, 4), 16); // IV 16 bytes
            const ciphertext = CryptoJS.lib.WordArray.create(encryptedData.words.slice(4), encryptedData.sigBytes - 16); // Phần còn lại là ciphertext

            // Khóa AES
            const keyWordArray = CryptoJS.enc.Utf8.parse(key);

            // Giải mã
            const decrypted = CryptoJS.AES.decrypt(
                { ciphertext: ciphertext },
                keyWordArray,
                {
                    iv: iv,
                    mode: CryptoJS.mode.CBC,
                    padding: CryptoJS.pad.Pkcs7
                }
            );

            // Hiển thị kết quả sau khi chuyển về chuỗi
            document.getElementById("output").innerText = decrypted.toString(CryptoJS.enc.Utf8);
        }
    </script>
</body>
</html>
