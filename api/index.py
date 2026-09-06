from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Foto a Texto PRO</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>
</head>
<body class="bg-gray-50 min-h-screen flex flex-col items-center p-4">
  <div class="w-full max-w-md bg-white rounded-2xl shadow-lg p-6 mt-10">
    <h1 class="text-2xl font-bold text-center">Foto a Texto PRO 📸➡️📝</h1>
    <p class="text-center text-sm text-gray-500 mt-1"><span id="creditos-text">2 créditos gratis</span> | <span id="pro-badge" class="hidden bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs">PRO ACTIVO</span></p>

    <div id="drop" class="mt-6 border-2 border-dashed border-gray-300 rounded-xl p-8 text-center cursor-pointer hover:bg-gray-50">
      <input type="file" id="file" accept="image/*" class="hidden">
      <p class="text-gray-600">Toca para subir foto o arrastra aquí</p>
    </div>

    <button id="btn" class="w-full mt-4 bg-black text-white py-3 rounded-xl font-bold">Convertir a Texto</button>

    <div id="loading" class="hidden text-center mt-4 text-sm text-blue-600">Convirtiendo... ⏳</div>
    <textarea id="resultado" class="w-full mt-4 h-40 p-3 border rounded-xl hidden" placeholder="Aquí aparecerá tu texto..."></textarea>
    <button id="copiar" class="hidden w-full mt-2 bg-gray-100 py-2 rounded-xl text-sm">Copiar texto</button>
  </div>

  <!-- PAYWALL -->
  <div id="paywall" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.7); z-index:9999; align-items:center; justify-content:center; padding:20px;">
    <div style="background:white; border-radius:20px; padding:24px; max-width:360px; width:100%; text-align:center; font-family:sans-serif;">
      <h2 style="font-size:20px; font-weight:bold;">🚀 Te acabaste los 2 créditos gratis</h2>
      <p style="font-size:14px; color:#666; margin-top:8px;">Pasa a PRO para convertir fotos ilimitadas</p>
      <a href="https://mpago.la/2LprVEr" target="_blank" style="display:block; width:100%; background:#2563eb; color:white; padding:14px; border-radius:12px; font-weight:bold; margin-top:20px; text-decoration:none; text-align:center;">PRO MES - $49/mes</a>
      <a href="https://mpago.la/28kWMCz" target="_blank" style="display:block; width:100%; background:#000; color:white; padding:14px; border-radius:12px; font-weight:bold; margin-top:12px; text-decoration:none; text-align:center;">PRO AÑO - $249/año (Ahorras 60%)</a>
      <p style="font-size:11px; color:#999; margin-top:14px;">Después de pagar, mándame comprobante por WhatsApp y te activo al instante.</p>
      <button onclick="document.getElementById('paywall').style.display='none'" style="margin-top:12px; font-size:12px; color:#aaa; background:none; border:none;">Cerrar</button>
    </div>
  </div>

<script>
let fileData = null;
let creditos = parseInt(localStorage.getItem('creditos') || '0');
let esPro = localStorage.getItem('esPro');

function actualizarUI(){
  const txt = document.getElementById('creditos-text');
  const badge = document.getElementById('pro-badge');
  if(localStorage.getItem('esPro') === 'si'){
    txt.innerText = 'PRO Ilimitado ∞';
    badge.classList.remove('hidden');
  } else {
    txt.innerText = (2 - creditos) + ' créditos gratis restantes';
    if(creditos >= 2) txt.innerText = 'Sin créditos';
  }
}
actualizarUI();

function checkPaywall(){
  if(localStorage.getItem('esPro')!== 'si' && creditos >= 2){
    document.getElementById('paywall').style.display='flex';
    return false;
  }
  return true;
}

document.getElementById('drop').onclick = () => document.getElementById('file').click();
document.getElementById('file').onchange = (e) => { fileData = e.target.files[0]; document.getElementById('drop').innerHTML = '✅ ' + fileData.name; };

document.getElementById('btn').onclick = async () => {
  if(!fileData) return alert('Primero sube una foto');
  if(!checkPaywall()) return;

  document.getElementById('loading').classList.remove('hidden');
  document.getElementById('resultado').classList.add('hidden');

  try{
    const { data: { text } } = await Tesseract.recognize(fileData, 'spa');
    document.getElementById('resultado').value = text;
    document.getElementById('resultado').classList.remove('hidden');
    document.getElementById('copiar').classList.remove('hidden');

    // Solo cuenta si NO es PRO
    if(localStorage.getItem('esPro')!== 'si'){
      creditos++;
      localStorage.setItem('creditos', creditos);
      actualizarUI();
    }
  }catch(err){ alert('Error al convertir'); }
  document.getElementById('loading').classList.add('hidden');
};

document.getElementById('copiar').onclick = () => {
  navigator.clipboard.writeText(document.getElementById('resultado').value);
  alert('Copiado!');
};

// Para que te actives PRO manualmente después de que te paguen:
// Abre la consola del navegador y escribe: localStorage.setItem('esPro','si')
</script>
</body>
</html>
"""

# Necesario para Vercel
if __name__ == '__main__':
    app.run()
