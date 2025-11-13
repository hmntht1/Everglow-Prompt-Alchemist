from flask import Flask, request, jsonify, render_template_string
import base64
import os
import io
from google import genai
from PIL import Image
import sys

# --- 1. PYTHON FLASK SETUP (Minimal Global Scope) ---
app = Flask(__name__)
print(f"Flask app initialized. Python version: {sys.version}")

# --- 2. HTML TEMPLATE (Contains all HTML, CSS, and Client-side JS) ---
# The HTML template remains identical to the previous version.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Everglow - The Magic Alchemist (Python)</title>

    <!-- External Dependencies: Fonts and Icons -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&amp;display=swap" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/regular/style.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/thin/style.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/light/style.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/bold/style.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/fill/style.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/duotone/style.css">

    <!-- INLINE CSS: All necessary styles are embedded here -->
    <style>
        /* CSS Variables */
        :root {
            --bg-dark: #0a0a20; 
            --text-light: #f0f0ff;
            --accent-pink: #ff69b4; 
            --accent-blue: #6495ed; 
            --card-bg: rgba(255, 255, 255, 0.05); 
        }

        /* Basic Setup and Tailwind-like utility styles */
        body {
            background-color: var(--bg-dark);
            color: var(--text-light);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            padding: 2rem 1rem;
            margin: 0;
            line-height: 1.5;
        }

        .selection\:bg-pink-500::selection {
            background-color: var(--accent-pink);
            color: white;
        }
        
        .w-full { width: 100%; }
        .max-w-lg { max-width: 32rem; }
        .mx-auto { margin-left: auto; margin-right: auto; }
        .space-y-8 > * + * { margin-top: 2rem; }
        .text-center { text-align: center; }
        .text-5xl { font-size: 3rem; }
        .font-extrabold { font-weight: 800; }
        .mb-2 { margin-bottom: 0.5rem; }
        .text-xl { font-size: 1.25rem; }
        .text-text-light\/70 { color: rgba(240, 240, 255, 0.7); }
        .font-medium { font-weight: 500; }
        .tracking-widest { letter-spacing: 0.1em; }
        .p-6 { padding: 1.5rem; }
        .rounded-2xl { border-radius: 1rem; }
        .space-y-6 > * + * { margin-top: 1.5rem; }
        .text-3xl { font-size: 1.875rem; }
        .tracking-wider { letter-spacing: 0.05em; }
        .text-text-light\/90 { color: rgba(240, 240, 255, 0.9); }
        .text-md { font-size: 1rem; }
        .pt-4 { padding-top: 1rem; }
        .pb-2 { padding-bottom: 0.5rem; }
        .max-w-sm { max-width: 24rem; }
        .flex { display: flex; }
        .items-center { align-items: center; }
        .justify-center { justify-content: center; }
        .font-semibold { font-weight: 600; }
        .py-3 { padding-top: 0.75rem; padding-bottom: 0.75rem; }
        .px-6 { padding-left: 1.5rem; padding-right: 1.5rem; }
        .rounded-xl { border-radius: 0.75rem; }
        .transition-all { transition-property: all; }
        .duration-300 { transition-duration: 300ms; }
        .transform { transform: var(--tw-transform); }
        .hover\:scale-\[1\.02\]:hover { transform: scale(1.02); }
        .text-xl { font-size: 1.25rem; }
        .mr-2 { margin-right: 0.5rem; }
        .hidden { display: none; }
        .text-sm { font-size: 0.875rem; }
        .overflow-hidden { overflow: hidden; }
        .text-ellipsis { text-overflow: ellipsis; }
        .whitespace-nowrap { white-space: nowrap; }
        .pt-2 { padding-top: 0.5rem; }
        .p-4 { padding: 1rem; }
        .text-left { text-align: left; }
        .font-mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
        .flex-1 { flex: 1 1 0%; }
        .min-h-\[16rem\] { min-height: 16rem; }
        .space-y-2 > * + * { margin-top: 0.5rem; }
        .object-contain { object-fit: contain; }
        .max-h-96 { max-height: 24rem; }
        .gap-4 { gap: 1rem; }
        .pt-16 { padding-top: 4rem; }
        .py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
        .px-4 { padding-left: 1rem; padding-right: 1rem; }
        .hover\:scale-\[1\.05\]:hover { transform: scale(1.05); }
        .text-lg { font-size: 1.125rem; }
        .h-16 { height: 4rem; }
        .mt-2 { margin-top: 0.5rem; }
        .hover\:scale-\[1\.01\]:hover { transform: scale(1.01); }
        .relative { position: relative; }
        .z-10 { z-index: 10; }
        .fixed { position: fixed; }
        .inset-0 { top: 0; right: 0; bottom: 0; left: 0; }
        .bg-black { background-color: #000; }
        .bg-opacity-70 { background-color: rgba(0, 0, 0, 0.7); }
        .backdrop-blur-md { backdrop-filter: blur(8px); }
        .z-\[100\] { z-index: 100; }
        .border-2 { border-width: 2px; }
        .font-bold { font-weight: 700; }
        .text-text-light\/80 { color: rgba(240, 240, 255, 0.8); }
        .rounded-lg { border-radius: 0.5rem; }
        .duration-200 { transition-duration: 200ms; }
        .hover\:scale-105:hover { transform: scale(1.05); }
        .mr-1 { margin-right: 0.25rem; }
        .text-xs { font-size: 0.75rem; }
        .text-text-light\/50 { color: rgba(240, 240, 255, 0.5); }
        
        /* Custom Components and Colors */
        .glowing-title {
            color: var(--text-light);
            text-shadow: 0 0 10px var(--accent-pink), 0 0 20px var(--accent-pink);
            transition: text-shadow 0.3s ease-in-out;
        }

        .floating-card {
            background-color: var(--card-bg);
            border: 2px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(5px);
            -webkit-backdrop-filter: blur(5px);
        }

        .textarea-input {
            background-color: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: var(--text-light);
            resize: none;
            transition: border-color 0.3s, box-shadow 0.3s;
        }

        .textarea-input:focus {
            outline: none;
            border-color: var(--accent-blue);
            box-shadow: 0 0 8px rgba(100, 149, 237, 0.5);
        }

        .btn-accent {
            background-color: var(--accent-pink);
            color: var(--bg-dark);
            box-shadow: 0 4px 15px rgba(255, 105, 180, 0.4);
        }

        .btn-accent:hover {
            background-color: #ff85c1;
            box-shadow: 0 6px 20px rgba(255, 105, 180, 0.6);
        }

        .btn-primary {
            background-color: var(--accent-blue);
            color: var(--bg-dark);
            box-shadow: 0 4px 15px rgba(100, 149, 237, 0.4);
        }

        .btn-primary:hover {
            background-color: #8bb8fc;
            box-shadow: 0 6px 20px rgba(100, 149, 237, 0.6);
        }

        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }

        .animate-spin {
            animation: spin 1s linear infinite;
        }
        
        /* Specific canvas styling */
        #original-canvas, #result-canvas {
            max-width: 100%;
            display: block;
        }

        /* UPLOAD FIX: CSS technique to overlay invisible file input over button */
        .upload-container {
            position: relative;
            cursor: pointer; 
            display: block;
            width: 100%;
            max-width: 24rem;
            margin-left: auto;
            margin-right: auto;
        }

        #image-input {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0; 
            cursor: pointer;
            z-index: 1; 
        }
    </style>
</head>
<body class="selection:bg-pink-500 selection:text-white">

    <div class="w-full max-w-lg mx-auto space-y-8">
        
        <header class="text-center">
            <h1 class="glowing-title text-5xl font-extrabold mb-2">Everglow</h1>
            <h2 class="text-xl text-text-light/70 font-medium tracking-widest">THE MAGIC ALCHEMIST</h2>
        </header>

        <div class="floating-card p-6 md:p-8 rounded-2xl text-center text-text-light space-y-6">
            
            <div class="text-3xl font-extrabold tracking-wider" style="color: var(--accent-pink);">
                The Magic Alchemist
            </div>
            
            <p class="text-text-light/90 text-md">
                Whisper your **Spell**, or upload an image to refine its essence.
            </p>
            
            <!-- UPLOAD FIX: Wrap button and input in a container -->
            <div class="w-full pt-4 pb-2">
                <div class="upload-container">
                    <button id="upload-button" class="w-full flex items-center justify-center font-semibold py-3 px-6 rounded-xl transition-all duration-300 transform hover:scale-[1.02] btn-accent">
                        <i class="ph ph-upload-simple text-xl mr-2"></i> Upload Image
                    </button>
                    <!-- File input is now overlaid on the button -->
                    <input type="file" id="image-input" accept="image/*">
                </div>
            </div>
            
            <div id="input-status" class="text-sm text-text-light\/70 w-full overflow-hidden text-ellipsis whitespace-nowrap pt-2">
                Status: Ready to Cast Spell.
            </div>

            <textarea id="prompt-input" rows="4" placeholder="e.g., A wizard cat wearing a golden monocle, digital art, or 'Change the background to a rainy Neo-Tokyo street.'" class="textarea-input w-full p-4 rounded-xl text-left font-mono text-sm"></textarea>

            <div class="py-4 flex flex-col sm:flex-row justify-center gap-4">
      
                <div class="flex-1 min-h-[16rem] space-y-2" id="original-panel-container">
                    <div class="text-sm font-semibold text-text-light/70" id="original-label">Source Magic</div>
                    <canvas id="original-canvas" class="hidden w-full h-full object-contain rounded-lg floating-card p-1 max-h-96 mx-auto"></canvas>
                    <div id="original-image-placeholder" class="text-center text-text-light/50 pt-16">
                        Source will display here.
                    </div>
                </div>

                <div class="flex-1 min-h-[16rem] space-y-2">
                    <div class="text-sm font-semibold text-text-light/70" id="result-label">Enchanted Result</div>
                    <canvas id="result-canvas" class="hidden w-full h-full object-contain rounded-lg floating-card p-1 max-h-96 mx-auto"></canvas>
                    <div id="result-image-placeholder" class="text-center text-text-light/50 pt-16">
                        Output will appear here.
                    </div>
                </div>

            </div>
            <div id="result-actions" class="hidden flex justify-center gap-4 pt-4">
                <button id="download-button" class="flex items-center font-semibold py-2 px-4 rounded-xl transition-all duration-300 hover:scale-[1.05] btn-primary">
                    <i class="ph ph-download-simple text-lg mr-2"></i> Download Enchantment
                </button>
            </div>

            <div class="h-16 flex flex-col items-center justify-center">
                <div id="loading-amulet" class="hidden w-10 h-10 border-4 border-accent-pink border-t-transparent rounded-full animate-spin"></div>
                <div id="message-box" class="text-sm text-accent-pink hidden mt-2 font-semibold"></div>
            </div>

            <button id="magic-button" class="w-full relative overflow-hidden font-bold py-4 px-6 rounded-xl transition-all duration-300 transform btn-primary hover:scale-[1.01]">
                <span class="relative z-10">CAST THE ENCHANTMENT!</span>
            </button>
            
            <p class="text-xs text-text-light/50 pt-4">
                Powered by Python Flask.
            </p>
        </div>
        
    </div>

    <!-- Modal remains hidden by default -->
    <div id="beautify-modal-backdrop" class="fixed inset-0 bg-black bg-opacity-70 backdrop-blur-md hidden z-[100] flex items-center justify-center p-4">
        <div id="beautify-modal" class="floating-card p-6 rounded-xl w-full max-w-sm text-center space-y-4 border-2" style="background-color: #1a1a3a; border-color: var(--accent-pink);">
            
            <i class="ph ph-sparkle text-5xl" style="color: var(--accent-pink);"></i>
            <h3 class="text-xl font-bold" style="color: var(--text-light);">Instant Magic Boost!</h3>
            
            <p class="text-sm text-text-light/80">
                Would you like to automatically **Enhance** the uploaded portrait (<span id="modal-filename" class="font-semibold">file.jpg</span>) for a professional, 8K look?
            </p>

            <div class="flex gap-4 justify-center pt-2">
                <button id="modal-confirm" class="font-bold py-2 px-4 rounded-lg transition-all duration-200 hover:scale-105 btn-primary">
                    <i class="ph ph-magic-wand text-lg mr-1"></i> Initiate Magic Boost
                </button>
                <button id="modal-decline" class="font-semibold py-2 px-4 rounded-lg transition-all duration-200 hover:scale-105" style="background-color: rgba(255, 255, 255, 0.1); color: var(--text-light);">
                    Override Spell
                </button>
            </div>
        </div>
    </div>
    
    <!-- JavaScript for Canvas Preview, UI Logic, and Flask API Calls -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            // Element references
            const imageInput = document.getElementById('image-input');
            const inputStatus = document.getElementById('input-status');
            const promptInput = document.getElementById('prompt-input');
            const originalCanvas = document.getElementById('original-canvas');
            const resultCanvas = document.getElementById('result-canvas');
            const originalPlaceholder = document.getElementById('original-image-placeholder');
            const resultPlaceholder = document.getElementById('result-image-placeholder');
            const resultActions = document.getElementById('result-actions');
            const downloadButton = document.getElementById('download-button');
            const magicButton = document.getElementById('magic-button');
            const loadingAmulet = document.getElementById('loading-amulet');
            const messageBox = document.getElementById('message-box');
            const modalBackdrop = document.getElementById('beautify-modal-backdrop');
            const modalConfirm = document.getElementById('modal-confirm');
            const modalDecline = document.getElementById('modal-decline');
            const modalFilename = document.getElementById('modal-filename');

            let base64Image = null; 

            // --- UI/Utility Functions ---
            
            function showMessage(text, isError = false) {
                messageBox.textContent = isError ? "Error: " + text : text;
                messageBox.classList.remove('hidden');
                messageBox.style.color = isError ? 'red' : 'var(--accent-pink)';
                setTimeout(() => messageBox.classList.add('hidden'), 5000);
            }

            function closeModal() {
                modalBackdrop.classList.add('hidden');
            }
            
            function showLoading() {
                loadingAmulet.classList.remove('hidden');
                magicButton.disabled = true;
                magicButton.innerHTML = '<span class="relative z-10">Casting...</span>';
            }
            
            function hideLoading() {
                loadingAmulet.classList.add('hidden');
                magicButton.disabled = false;
                magicButton.innerHTML = '<span class="relative z-10">CAST THE ENCHANTMENT!</span>';
            }

            function drawImageOnCanvas(canvas, imageUrl) {
                const ctx = canvas.getContext('2d');
                const img = new Image();
                
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                img.onload = () => {
                    const maxWidth = 350; 
                    const maxHeight = 350; 
                    let renderWidth = img.width;
                    let renderHeight = img.height;

                    if (renderWidth / maxWidth > renderHeight / maxHeight) {
                        renderHeight = renderHeight * (maxWidth / renderWidth);
                        renderWidth = maxWidth;
                    } else {
                        renderWidth = renderWidth * (maxHeight / renderHeight);
                        renderHeight = maxHeight;
                    }

                    canvas.width = renderWidth;
                    canvas.height = renderHeight;
                    
                    ctx.drawImage(img, 0, 0, renderWidth, renderHeight);
                    canvas.classList.remove('hidden');
                };
                img.src = imageUrl;
            }

            // --- Event Listeners ---

            // 1. File Input Change (Triggered by CSS overlay technique)
            imageInput.addEventListener('change', (event) => {
                const file = event.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        const imageUrl = e.target.result;
                        
                        base64Image = imageUrl.split(',')[1];
                        
                        drawImageOnCanvas(originalCanvas, imageUrl);

                        inputStatus.textContent = `Status: File uploaded: ${file.name}`;
                        originalPlaceholder.classList.add('hidden');

                        modalFilename.textContent = file.name;
                        modalBackdrop.classList.remove('hidden');

                        resultCanvas.classList.add('hidden');
                        resultPlaceholder.classList.remove('hidden');
                        resultActions.classList.add('hidden');
                    };
                    reader.readAsDataURL(file);
                } else {
                    inputStatus.textContent = 'Status: Ready to Cast Spell.';
                    originalPlaceholder.classList.remove('hidden');
                    originalCanvas.classList.add('hidden');
                    base64Image = null;
                }
            });
            
            // 2. Modal Interactions
            modalConfirm.addEventListener('click', () => {
                // Pre-fills the prompt for "Magic Boost" 
                promptInput.value = `A professional, 8K quality, highly detailed portrait, ${promptInput.value.trim()}`;
                closeModal();
            });
            
            modalDecline.addEventListener('click', closeModal);

            // 3. Magic Button (API Call to Flask Backend)
            magicButton.addEventListener('click', async () => {
                const prompt = promptInput.value.trim();
                const fileIsUploaded = base64Image !== null;

                if (!prompt && !fileIsUploaded) {
                    showMessage("Whisper a Spell or upload a Source Image first!", true);
                    return;
                }

                showLoading();
                
                try {
                    const response = await fetch('/api/enchant', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            prompt: prompt,
                            image_data: base64Image 
                        })
                    });

                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
                    }

                    const result = await response.json();

                    if (result.success) {
                        const resultUrl = `data:image/png;base64,${result.result_image_base64}`;
                        
                        drawImageOnCanvas(resultCanvas, resultUrl);

                        resultPlaceholder.classList.add('hidden');
                        resultActions.classList.remove('hidden');
                        inputStatus.textContent = 'Status: Enchantment Complete!';
                    } else {
                        showMessage(result.message || "Enchantment failed.", true);
                    }

                } catch (error) {
                    console.error('API Error:', error);
                    showMessage(error.message || "A critical error occurred while contacting the server.", true);
                    // Also check for the specific 503 error if the Gemini client failed initialization
                    if (error.message.includes("503") || error.message.includes("client not initialized")) {
                        showMessage("Server Error: Gemini API key is missing or invalid. Check your GEMINI_API_KEY environment variable.", true);
                    }
                } finally {
                    hideLoading();
                }
            });

            // 4. DOWNLOAD OPTION
            downloadButton.addEventListener('click', () => {
                if (resultCanvas.classList.contains('hidden')) {
                    showMessage("No result image available to download.", true);
                    return;
                }
                
                const dataURL = resultCanvas.toDataURL('image/png'); 
                
                const a = document.createElement('a');
                a.href = dataURL;
                a.download = 'everglow_enchanted_result.png'; 
                
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            });
        });
    </script>

</body>
</html>
"""

# --- 3. FLASK ROUTES ---

# Global variable to hold the initialized client (if successful)
# This will be initialized in the first request if needed.
_gemini_client = None

def get_gemini_client():
    """Initializes and returns the Gemini client (lazy initialization)."""
    global _gemini_client
    if _gemini_client is None:
        API_KEY = os.environ.get("GEMINI_API_KEY")
        if not API_KEY:
            print("CRITICAL: GEMINI_API_KEY environment variable is NOT set.")
            return None
        try:
            _gemini_client = genai.Client(api_key=API_KEY)
            print("Gemini client initialized successfully (lazily).")
        except Exception as e:
            print(f"CRITICAL: Error initializing Gemini client: {e}")
            _gemini_client = None
    return _gemini_client


@app.route('/')
def index():
    """Serves the main HTML application."""
    print("Serving root page '/'.")
    return render_template_string(HTML_TEMPLATE)

@app.route('/status')
def status_check():
    """Simple route to check if the Python server is actively running."""
    # We don't call get_gemini_client() here to prevent unnecessary initialization
    # but we check if the API key is present in the environment
    api_key_status = "Set" if os.environ.get("GEMINI_API_KEY") else "NOT SET"
    
    # We try to initialize the client here to provide a status on the health check page
    client_status = get_gemini_client() is not None
    
    status = "OK" if client_status else f"CRITICAL (API Key Status: {api_key_status})"
    
    return f"Server Status: {status} - Python {sys.version}", 200

@app.route('/api/enchant', methods=['POST'])
def enchant():
    """
    Handles the image generation request from the client and calls the Gemini API.
    """
    client = get_gemini_client()
    if not client:
        return jsonify({"success": False, "message": "Gemini API client not initialized. Check GEMINI_API_KEY environment variable."}), 503

    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        image_base64 = data.get('image_data')
        
        if not prompt and not image_base64:
            return jsonify({"success": False, "message": "Prompt or image data is required."}), 400

        # --- Base64 Decoding and Image Preparation ---
        if image_base64:
            # Image-to-Image editing (using gemini-2.5-flash-image-preview)
            image_bytes = base64.b64decode(image_base64)
            input_image = Image.open(io.BytesIO(image_bytes))
            
            parts = [input_image, prompt]
            
            gemini_response = client.models.generate_content(
                model='gemini-2.5-flash-image-preview',
                contents=parts,
            )
            
            # Extract image data from the response
            if gemini_response.candidates and gemini_response.candidates[0].content.parts[0].inline_data:
                generated_image_data = gemini_response.candidates[0].content.parts[0].inline_data.data
            else:
                return jsonify({"success": False, "message": "Image editing failed or returned no data."}), 500
            
        else:
            # Text-to-Image generation (using imagen-4.0-generate-001)
            gemini_response = client.models.generate_images(
                model='imagen-4.0-generate-001',
                prompt=prompt,
                config=dict(
                    number_of_images=1,
                    output_mime_type="image/png",
                )
            )
            
            # Process response from imagen-4.0-generate-001
            if gemini_response.generated_images and gemini_response.generated_images[0].image.image_bytes:
                generated_image_data = gemini_response.generated_images[0].image.image_bytes
            else:
                return jsonify({"success": False, "message": "Image generation failed or returned no images."}), 500

        # Encode the generated image back to base64 for the client
        result_image_base64 = base64.b64encode(generated_image_data).decode('utf-8')

        return jsonify({
            "success": True,
            "message": "Enchantment successful.",
            "result_image_base64": result_image_base64
        })

    except Exception as e:
        print(f"Error during image processing: {e}")
        return jsonify({"success": False, "message": f"An API or processing error occurred: {str(e)}"}), 500
    
# --- 4. RUNNER ---
# The Flask instance must be named 'app' for Gunicorn to find it via Procfile.
# The `create_app` function is no longer needed globally, as all logic is now defined on the Flask instance 'app'.