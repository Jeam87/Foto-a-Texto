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
<script src="https://cdn.jsdelivr.net/npm/docx@9.5.1/build/index.umd.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jspdf@3.0.3/dist/jspdf.umd.min.js"></script>
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
    <div id="loading" class="hidden text-center mt-4 text-sm text-blue-600">Preparando... ⏳</div>
    <textarea spellcheck="false" autocorrect="off" autocapitalize="off" id="resultado" class="w-full mt-4 h-40 p-3 border rounded-xl hidden"></textarea>

    <div id="acciones" class="hidden mt-3 grid grid-cols-2 gap-2">
      <button type="button" id="btnCopiar" class="bg-gray-900 text-white py-3 rounded-xl text-sm font-bold">📋 Copiar</button>
      <button type="button" id="btnWhatsapp" class="bg-green-500 text-white py-3 rounded-xl text-sm font-bold">💬 WhatsApp</button>
      <button type="button" id="btnWord" class="bg-blue-600 text-white py-3 rounded-xl text-sm font-bold">📄 Word</button>
      <button type="button" id="btnPdf" class="bg-red-600 text-white py-3 rounded-xl text-sm font-bold">📕 PDF</button>
      <button type="button" id="btnCompartir" class="col-span-2 bg-gray-100 py-3 rounded-xl text-sm font-bold">📤 Compartir archivo</button>
    </div>
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

async function prepararImagenOCR(file) {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => {
      const escala = Math.min(3, Math.max(1.5, 1800 / Math.max(img.width, img.height)));
      const canvas = document.createElement('canvas');
      canvas.width = Math.round(img.width * escala);
      canvas.height = Math.round(img.height * escala);
      const ctx = canvas.getContext('2d', { willReadFrequently: true });
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      const datos = ctx.getImageData(0, 0, canvas.width, canvas.height);
      for (let i = 0; i < datos.data.length; i += 4) {
        const gris = Math.round(0.299 * datos.data[i] + 0.587 * datos.data[i+1] + 0.114 * datos.data[i+2]);
        datos.data[i] = gris; datos.data[i+1] = gris; datos.data[i+2] = gris;
      }
      ctx.putImageData(datos, 0, 0);
      canvas.toBlob(blob => resolve(blob), 'image/png', 1.0);
    };
    img.src = URL.createObjectURL(file);
  });
}

document.getElementById('drop').onclick = () => document.getElementById('file').click();
document.getElementById('file').onchange = (e) => {
  fileData = e.target.files[0];
  if (!fileData) return;
  const drop = document.getElementById('drop');
  const oldPreview = document.getElementById('previewFoto');
  if (oldPreview) oldPreview.remove();
  const img = document.createElement('img');
  img.id = 'previewFoto';
  img.className = 'mx-auto mt-4 max-h-64 max-w-full rounded-xl object-contain shadow-sm';
  img.src = URL.createObjectURL(fileData);
  drop.appendChild(img);
};

document.getElementById('btn').onclick = async () => {
  if(!fileData) return alert('Primero sube una foto');
  if(!checkPaywall()) return;
  document.getElementById('loading').classList.remove('hidden');
  document.getElementById('resultado').classList.add('hidden');
  document.getElementById('acciones').classList.add('hidden');
  try{
    const imagenProcesada = await prepararImagenOCR(fileData);
    const { data: { text } } = await Tesseract.recognize(imagenProcesada, 'spa', {
      logger: m => {
        if (m.status === 'recognizing text') {
          document.getElementById('loading').innerText = `Leyendo imagen... ${Math.round(m.progress * 100)}% ⏳`;
        }
      }
    });
    const res = document.getElementById('resultado');
    res.value = text.trim();
    res.classList.remove('hidden');
    document.getElementById('acciones').classList.remove('hidden');
    document.getElementById('acciones').style.display = 'grid';
    if(localStorage.getItem('esPro')!== 'si'){
      let creditos = parseInt(localStorage.getItem('creditos') || '0');
      localStorage.setItem('creditos', (creditos+1).toString());
      actualizarUI();
    }
  }catch(err){ alert('Error al convertir: '+err.message); }
  document.getElementById('loading').classList.add('hidden');
};

// --- ACCIONES QUE AHORA SI JALAN ---
function obtenerTextoOCR(){ return document.getElementById('resultado').value || ''; }

async function copiarOCR(){
  const t=obtenerTextoOCR(); if(!t) return alert('No hay texto');
  try{ await navigator.clipboard.writeText(t); alert('Texto copiado!'); }
  catch{ document.getElementById('resultado').select(); document.execCommand('copy'); alert('Texto copiado!'); }
}

async function crearWordBlob(){
  const t=obtenerTextoOCR(); const D=window.docx;
  if(!D) throw new Error('docx no cargó');
  const paras = t.split(/\\r?\\n/).map(l => new D.Paragraph({ children: [new D.TextRun(l || ' ')] }));
  const doc = new D.Document({ sections: [{ properties:{}, children: paras.length?paras:[new D.Paragraph(' ')] }] });
  return await D.Packer.toBlob(doc);
}
async function descargarWord(){
  try{
    const b=await crearWordBlob(); const u=URL.createObjectURL(b); const a=document.createElement('a');
    a.href=u; a.download='texto_ocr.docx'; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(()=>URL.revokeObjectURL(u),1000);
  } catch(e){ alert('Error Word: '+e.message); }
}
async function crearPdfBlob(){
  const t=obtenerTextoOCR(); const {jsPDF}=window.jspdf; const p=new jsPDF({unit:'mm',format:'a4'});
  const margin=15, width=180, lineH=6; let y=margin;
  p.setFont('helvetica','normal'); p.setFontSize(11);
  for(const line of t.split(/\\r?\\n/)){
    const parts = p.splitTextToSize(line||' ', width);
    for(const part of parts){ if(y>282){p.addPage(); y=margin;} p.text(part, margin, y); y+=lineH; }
  }
  return p.output('blob');
}
async function descargarPdf(){
  try{
    const b=await crearPdfBlob(); const u=URL.createObjectURL(b); const a=document.createElement('a');
    a.href=u; a.download='texto_ocr.pdf'; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(()=>URL.revokeObjectURL(u),1000);
  } catch(e){ alert('Error PDF: '+e.message); }
}
function enviarWhatsApp(){
  const t=obtenerTextoOCR(); if(!t) return;
  window.open('https://wa.me/?text='+encodeURIComponent(t),'_blank');
}
async function compartirArchivo(){
  try{
    const b=await crearPdfBlob(); const f=new File([b],'texto_ocr.pdf',{type:'application/pdf'});
    if(navigator.share && navigator.canShare && navigator.canShare({files:[f]})){
      await navigator.share({title:'Texto OCR', files:[f]});
      return;
    }
    throw new Error('share no soportado');
  }catch{ await descargarPdf(); }
}

document.getElementById('btnCopiar').onclick = copiarOCR;
document.getElementById('btnWord').onclick = descargarWord;
document.getElementById('btnPdf').onclick = descargarPdf;
document.getElementById('btnWhatsapp').onclick = enviarWhatsApp;
document.getElementById('btnCompartir').onclick = compartirArchivo;
</script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True) 
