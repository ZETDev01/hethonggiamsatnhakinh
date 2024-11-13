from flask import Flask, request, render_template
from Crypto.Cipher import AES
import base64

app = Flask(__name__)

# AES key and IV
AES_KEY = bytes([0x2B, 0x7E, 0x15, 0x16, 0x28, 0xAE, 0xD2, 0xA6, 0xAB, 0xF7, 0x11, 0xD7, 0x09, 0x05, 0x2A, 0x3C])
AES_IV = bytes([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F])

def unpad_pkcs7(data):
    padding_len = data[-1]
    return data[:-padding_len] if padding_len < 16 else data

def decrypt_aes(ciphertext):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    decrypted = cipher.decrypt(ciphertext)
    # Remove padding
    decrypted = unpad_pkcs7(decrypted)
    return decrypted

@app.route('/', methods=['GET', 'POST'])
def home():
    decrypted_data = None
    error = None
    
    if request.method == 'POST':
        base64_data = request.form.get('data')
        if not base64_data:
            error = "No data provided."
        else:
            try:
                # Decode Base64 data
                encrypted_data = base64.b64decode(base64_data)
                print("Encrypted Data (bytes):", encrypted_data)  # Debugging

                # Decrypt the data
                decrypted_data_bytes = decrypt_aes(encrypted_data)
                
                # Try to clean up non-JSON prefix by locating JSON start `{`
                json_start = decrypted_data_bytes.find(b'{')
                if json_start != -1:
                    decrypted_data_bytes = decrypted_data_bytes[json_start:]
                
                # Convert to string for JSON parsing
                decrypted_data_str = decrypted_data_bytes.decode('utf-8', errors='ignore')
                print("Decrypted Data (cleaned string):", decrypted_data_str)  # Debugging
                
                return render_template('index.html', data=decrypted_data_str)

            except Exception as e:
                error = f"Error: {str(e)}"

    return render_template('index.html', data=decrypted_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
