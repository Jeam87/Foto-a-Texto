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
    <p class="text-center text-sm text-gray-500 mt-1"><span id="creditos-text"></span> <span id="pro-badge" class="hidden bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs ml-1">PRO ACTIVO</span></p>
    <div id="drop" class="mt-6 border-2 border-dashed border-gray-300 rounded-xl p-8 text-center cursor-pointer hover:bg-gray-50">
      <input type="file" id="file" accept="image/*" class="hidden">
      <p class="text-gray-600">Toca para subir foto o arrastra aquí</p>
    </div>
    <button id="btn" class="w-full mt-4 bg-black text-white py-3 rounded-xl font-bold">Convertir a Texto</button>
    <div id="loading" class="hidden text-center mt-4 text-sm text-blue-600">Convirtiendo... ⏳</div>
    <textarea id="resultado" class="w-full mt-4 h-40 p-3 border rounded-xl hidden"></textarea>
    <button id="copiar" class="hidden w-full mt-2 bg-gray-100 py-2 rounded-xl text-sm">Copiar texto</button>
  </div>

  <div id="paywall" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.7); z-index:9999; align-items:center; justify-content:center; padding:20px;">
    <div id="paywall-box" style="background:white; border-radius:20px; padding:24px; max-width:360px; width:100%; text-align:center; font-family:sans-serif;">
      <h2 style="font-size:20px; font-weight:bold;">🚀 Te acabaste los 2 créditos gratis</h2>
      <p style="font-size:14px; color:#666; margin-top:8px;">Pasa a PRO para convertir ilimitado</p>
      <a onclick="autoActivarPro('mensual')" href="https://mpago.la/2LprVEr" target="_blank" style="display:block; width:100%; background:#2563eb; color:white; padding:14px; border-radius:12px; font-weight:bold; margin-top:20px; text-decoration:none; text-align:center;">PRO MES - $49/mes</a>
      <a onclick="autoActivarPro('anual')" href="https://mpago.la/28kWMCz" target="_blank" style="display:block; width:100%; background:#000; color:white; padding:14px; border-radius:12px; font-weight:bold; margin-top:12px; text-decoration:none; text-align:center;">PRO AÑO - $249/año</a>
      <button onclick="document.getElementById('paywall').style.display='none'" style="margin-top:16px; font-size:12px; color:#aaa; background:none; border:none;">Cerrar</button>
    </div>
  </div>

<script>
let fileData = null;

function revisarExpiracion(){
  const expira = localStorage.getItem('proExpira');
  if(expira && new Date().getTime() > parseInt(expira)){
    localStorage.removeItem('esPro');
    localStorage.removeItem('proExpira');
    localStorage.removeItem('proTipo');
    localStorage.setItem('creditos','0');
  }
}
revisarExpiracion();

function actualizarUI(){
  revisarExpiracion();
  const txt = document.getElementById('creditos-text');
  const badge = document.getElementById('pro-badge');
  if(localStorage.getItem('esPro') === 'si'){
    badge.classList.remove('hidden');
    const expira = parseInt(localStorage.getItem('proExpira') || '0');
    const dias = Math.ceil((expira - new Date().getTime()) / (1000*60*60*24));
    txt.innerText = dias > 0? `PRO activo - vence en ${dias} días` : 'PRO Ilimitado ∞';
  } else {
    badge.classList.add('hidden');
    let creditos = parseInt(localStorage.getItem('creditos') || '0');
    txt.innerText = creditos < 2? (2 - creditos) + ' créditos gratis restantes' : 'Sin créditos - Pasa a PRO';
  }
}
actualizarUI();

function checkPaywall(){
  revisarExpiracion();
  let creditos = parseInt(localStorage.getItem('creditos') || '0');
  if(localStorage.getItem('esPro')!== 'si' && creditos >= 2){
    document.getElementById('paywall').style.display='flex';
    return false;
  }
  return true;
}

function autoActivarPro(tipo){
  let dias = tipo === 'anual'? 365 : 30;
  let expira = new Date().getTime() + (dias * 24 * 60 * 60 * 1000);
  localStorage.setItem('esPro','si');
  localStorage.setItem('proExpira', expira.toString());
  localStorage.setItem('proTipo', tipo);
  document.getElementById('paywall-box').innerHTML = '<h2 style="font-weight:bold;font-size:20px">¡Pago recibido! 🎉</h2><p style="margin-top:10px;color:#666">Ya eres PRO por ' + dias + ' días.<br>Cierra Mercado Pago y recarga la página.</p><button onclick="location.reload()" style="margin-top:16px;background:#000;color:#fff;padding:10px 20px;border-radius:10px">Ya pagué, activar PRO</button>';
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
    if(localStorage.getItem('esPro')!== 'si'){
      let creditos = parseInt(localStorage.getItem('creditos') || '0');
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
</script>
</body>
</html>
"""
