from flask import Flask, request, render_template_string, jsonify
import os, requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Foto a Texto EXACTO - Gratis</title>
<style>
body{background:#0f0f0f;color:#fff;font-family:sans-serif;padding:12px;margin:0}
.card{background:#1e1e1e;padding:18px;border-radius:16px;max-width:520px;margin:auto;text-align:center}
button{background:#00ff88;color:#000;border:none;padding:14px;width:100%;border-radius:12px;font-weight:bold;margin-top:10px;font-size:16px}
.btn2{background:#333;color:#fff}
textarea{width:100%;height:280px;background:#111;color:#fff;border:1px solid #333;border-radius:12px;padding:12px;margin-top:12px;box-sizing:border-box;font-size:15px}
#loader{display:none;margin-top:12px;background:#222;border-radius:10px;padding:12px}
.dot{animation:blink 1s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
</style></head><body>
<div class="card">
<h3>📸 Foto a Texto - 100% EXACTO</h3>
<p style="color:#aaa;font-size:12px">Toma foto y lo copia idéntico. Modelo gratis activado.</p>
<input type="file" id="file" accept="image/*" capture="environment" style="background:#222;padding:10px;border-radius:10px;width:100%;box-sizing:border-box">
<img id="prev" style="display:none;max-width:100%;border-radius:12px;margin-top:10px">
<div id="loader"><span class="dot">🤖 IA leyendo... 4-5 segundos (gratis)</span></div>
<textarea id="out" placeholder="Aquí aparecerá el texto exacto de la foto..."></textarea>
<button onclick="copiar()">📋 COPIAR TEXTO</button>
<button class="btn2" onclick="compartir()">📤 Compartir WhatsApp</button>
<p id="msg" style="font-size:11px;color:#00ff88;margin-top:8px">✅ Modo GRATIS activado - sin costo</p>
</div>
<script>
let imgBase64 = null;
document.getElementById('file').onchange = e => {
 let f = e.target.files[0]; if(!f) return;
 let reader = new FileReader();
 reader.onload = async ev => {
  imgBase64 = ev.target.result;
  document.getElementById('prev').src = imgBase64;
  document.getElementById('prev').style.display='block';
  document.getElementById('loader').style.display='block';
  document.getElementById('out').value='';
  document.getElementById('msg').innerText='Enviando a IA gratis...';
  let res = await fetch('/leer', {
   method:'POST', headers:{'Content-Type':'application/json'},
   body: JSON.stringify({ imagen: imgBase64 })
  });
  let data = await res.json();
  document.getElementById('loader').style.display='none';
  if(data.texto){
   document.getElementById('out').value = data.texto;
   document.getElementById('msg').innerText='✅ Listo - 100% exacto';
  } else {
   document.getElementById('out').value = 'Error: ' + data.error;
   document.getElementById('msg').innerText='Error, revisa la key en Vercel';
  }
 }
 reader.readAsDataURL(f);
}
function copiar(){ let t=document.getElementById('out'); t.select(); document.execCommand('copy'); alert('Copiado!'); }
function compartir(){ let txt=document.getElementById('out').value; if(!txt) return alert('No hay texto'); window.open('https://wa.me/?text='+encodeURIComponent(txt),'_blank'); }
</script></body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/leer', methods=['POST'])
def leer():
    try:
        data = request.json
        imagen_b64 = data.get('imagen','')
        api_key = os.environ.get('OPENROUTER_API_KEY')
        if not api_key:
            return jsonify({"error":"Pon tu OPENROUTER_API_KEY en Vercel > Settings > Env Variables"}), 500

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://jacona.app",
            "X-Title": "Jacona Foto a Texto"
        }

        payload = {
            "model": "meta-llama/llama-3.2-11b-vision-instruct:free",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extrae TODO el texto de esta imagen de forma 100% EXACTA. Respeta cada letra, acento, mayúscula, número, punto y salto de línea. No resumas, no traduzcas, no agregues nada. Si es un documento, mantén el formato original. Solo devuelve el texto puro que ves."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": imagen_b64}
                        }
                    ]
                }
            ],
            "temperature": 0
        }

        r = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=50)
        rj = r.json()

        if 'error' in rj:
            return jsonify({"error": str(rj['error'])}), 500

        texto_final = rj['choices'][0]['message']['content']
        return jsonify({"texto": texto_final})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
