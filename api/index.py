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
<title>Foto a Texto PRO ML</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/docx@8.5.0/build/index.js"></script>
<script src="https://cdn.jsdelivr.net/npm/jspdf@3.0.3/dist/jspdf.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<script>pdfjsLib.GlobalWorkerOptions.workerSrc='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';</script>
</head>
<body class="bg-gray-50 min-h-screen flex flex-col items-center p-4">
  <div class="w-full max-w-md bg-white rounded-2xl shadow-lg p-6 mt-10">
    <h1 class="text-2xl font-bold text-center">Foto a Texto PRO 📸➡️📝</h1>
    <p id="motor" class="text-center text-[11px] text-gray-400 mt-1">Motor: Detectando...</p>
    <p class="text-center text-sm text-gray-500 mt-1"><span id="creditos-text"></span> <span id="pro-badge" class="hidden bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs ml-1">PRO ACTIVO</span></p>

    <div id="drop" class="mt-6 border-2 border-dashed border-gray-300 rounded-xl p-6 text-center cursor-pointer hover:bg-gray-50">
      <input type="file" id="file" accept="image/*,application/pdf,.pdf" class="hidden">
      <p id="drop-text" class="text-gray-600">Toca para subir foto o PDF</p>
    </div>

    <button id="btn" class="w-full mt-4 bg-black text-white py-3 rounded-xl font-bold">Convertir a Texto</button>
    <div id="loading" class="hidden text-center mt-4 text-sm text-blue-600">Leyendo...</div>
    <textarea spellcheck="false" id="resultado" class="w-full mt-4 h-48 p-3 border rounded-xl hidden"></textarea>

    <div id="acciones" class="hidden mt-3 grid grid-cols-2 gap-2">
      <button type="button" id="btnCopiar" class="bg-gray-900 text-white py-3 rounded-xl text-sm font-bold">📋 Copiar</button>
      <button type="button" id="btnWhatsapp" class="bg-green-500 text-white py-3 rounded-xl text-sm font-bold">💬 WhatsApp</button>
      <button type="button" id="btnWord" class="bg-blue-600 text-white py-3 rounded-xl text-sm font-bold">📄 Word</button>
      <button type="button" id="btnPdf" class="bg-red-600 text-white py-3 rounded-xl text-sm font-bold">📕 PDF</button>
      <button type="button" id="btnCompartir" class="col-span-2 bg-gray-100 py-3 rounded-xl text-sm font-bold">📤 Compartir archivo</button>
    </div>
  </div>

  <div id="paywall" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.7); z-index:9999; align-items:center; justify-content:center; padding:20px;">
    <div id="paywall-box" style="background:white; border-radius:20px; padding:24px; max-width:360px; width:100%; text-align:center;">
      <h2 style="font-size:20px; font-weight:bold;">🚀 Te acabaste los 2 créditos gratis</h2>
      <a onclick="autoActivarPro('mensual')" href="https://mpago.la/2LprVEr" target="_blank" style="display:block; width:100%; background:#2563eb; color:white; padding:14px; border-radius:12px; font-weight:bold; margin-top:20px; text-decoration:none;">PRO MES - $49/mes</a>
      <a onclick="autoActivarPro('anual')" href="https://mpago.la/28kWMCz" target="_blank" style="display:block; width:100%; background:#000; color:white; padding:14px; border-radius:12px; font-weight:bold; margin-top:12px; text-decoration:none;">PRO AÑO - $249/año</a>
      <button onclick="document.getElementById('paywall').style.display='none'" style="margin-top:16px; font-size:12px; color:#aaa; background:none; border:none;">Cerrar</button>
    </div>
  </div>

<script>
let fileData=null;
let fileOriginal=null;
let motorML=false;
if('TextDetector' in window){ motorML=true; document.getElementById('motor').innerText='Motor: ML Kit Offline ⚡ Rápido'; }
else { document.getElementById('motor').innerText='Motor: Tesseract Offline'; }

function revisarExpiracion(){ const e=localStorage.getItem('proExpira'); if(e && Date.now()>parseInt(e)){ localStorage.removeItem('esPro'); localStorage.removeItem('proExpira'); localStorage.setItem('creditos','0'); } }
revisarExpiracion();
function actualizarUI(){ revisarExpiracion(); const t=document.getElementById('creditos-text'), b=document.getElementById('pro-badge'); if(localStorage.getItem('esPro')==='si'){ b.classList.remove('hidden'); const d=Math.ceil((parseInt(localStorage.getItem('proExpira'))-Date.now())/86400000); t.innerText=d>0?`PRO activo - ${d} días`:'PRO ∞'; } else { b.classList.add('hidden'); let c=parseInt(localStorage.getItem('creditos')||'0'); t.innerText=c<2?(2-c)+' créditos gratis':'Sin créditos - PRO'; } }
actualizarUI();
function checkPaywall(){ revisarExpiracion(); let c=parseInt(localStorage.getItem('creditos')||'0'); if(localStorage.getItem('esPro')!=='si' && c>=2){ document.getElementById('paywall').style.display='flex'; return false;} return true; }
function autoActivarPro(t){ let d=t==='anual'?365:30; localStorage.setItem('esPro','si'); localStorage.setItem('proExpira',(Date.now()+d*86400000).toString()); location.reload(); }

async function prepararImagenOCR(file){
  return new Promise((resolve)=>{
    const img=new Image();
    img.onload=()=>{
      const escala=Math.min(3, Math.max(1.5, 1800/Math.max(img.width,img.height)));
      const c=document.createElement('canvas'); c.width=Math.round(img.width*escala); c.height=Math.round(img.height*escala);
      const ctx=c.getContext('2d',{willReadFrequently:true}); ctx.drawImage(img,0,0,c.width,c.height);
      const data=ctx.getImageData(0,0,c.width,c.height);
      for(let i=0;i<data.data.length;i+=4){ const g=Math.round(0.299*data.data[i]+0.587*data.data[i+1]+0.114*data.data[i+2]); data.data[i]=g; data.data[i+1]=g; data.data[i+2]=g; }
      ctx.putImageData(data,0,0);
      c.toBlob(b=>resolve(b),'image/png',1.0);
    };
    img.src=URL.createObjectURL(file);
  });
}

document.getElementById('drop').onclick=()=>document.getElementById('file').click();

document.getElementById('file').onchange=async(e)=>{
  fileOriginal=e.target.files[0];
  if(!fileOriginal) return;
  const drop=document.getElementById('drop');
  const old=document.getElementById('previewFoto');
  if(old) old.remove();

  if(fileOriginal.type==='application/pdf'){
    document.getElementById('drop-text').innerText='📄 Leyendo PDF...';
    try{
      const url=URL.createObjectURL(fileOriginal);
      const pdf=await pdfjsLib.getDocument(url).promise;
      const page=await pdf.getPage(1);
      const viewport=page.getViewport({scale:2.5});
      const canvas=document.createElement('canvas');
      canvas.width=viewport.width; canvas.height=viewport.height;
      const ctx=canvas.getContext('2d');
      await page.render({canvasContext:ctx, viewport}).promise;
      canvas.id='previewFoto';
      canvas.className='mx-auto mt-4 max-h-64 rounded-xl border';
      drop.appendChild(canvas);
      canvas.toBlob(b=>{
        fileData=new File([b],'pdf-page.png',{type:'image/png'});
        document.getElementById('drop-text').innerText='📄 PDF cargado - listo para convertir';
      },'image/png',1.0);
    }catch(err){ alert('Error leyendo PDF: '+err.message); }
  } else {
    fileData=fileOriginal;
    const im=document.createElement('img');
    im.id='previewFoto';
    im.className='mx-auto mt-4 max-h-64 rounded-xl';
    im.src=URL.createObjectURL(fileData);
    drop.appendChild(im);
    document.getElementById('drop-text').innerText='📷 Foto lista - toca para cambiar';
  }
};

async function reconocerMLKit(blob){
  try{
    const bitmap = await createImageBitmap(blob);
    const detector = new TextDetector();
    const result = await detector.detect(bitmap);
    if(!result || result.length===0) return null;
    return result.map(r=>r.rawValue).join("\\n");
  } catch(err){ return null; }
}

document.getElementById('btn').onclick=async()=>{
  if(!fileData) return alert('Sube foto o PDF primero');
  if(!checkPaywall()) return;
  document.getElementById('loading').classList.remove('hidden');
  document.getElementById('resultado').classList.add('hidden');
  document.getElementById('acciones').classList.add('hidden');
  try{
    const blob = await prepararImagenOCR(fileData);
    let texto = null;
    if(motorML){
      document.getElementById('loading').innerText='Leyendo con ML Kit Offline ⚡...';
      texto = await reconocerMLKit(blob);
    }
    if(!texto){
      document.getElementById('loading').innerText='Leyendo con Tesseract... ⏳';
      const {data:{text}} = await Tesseract.recognize(blob,'spa',{ logger:m=>{ if(m.status==='recognizing text') document.getElementById('loading').innerText=`Leyendo ${Math.round(m.progress*100)}%`; }});
      texto=text;
    }
    const res=document.getElementById('resultado'); res.value=texto.trim(); res.classList.remove('hidden');
    document.getElementById('acciones').classList.remove('hidden');
    document.getElementById('acciones').style.display='grid';
    if(localStorage.getItem('esPro')!=='si'){ localStorage.setItem('creditos',(parseInt(localStorage.getItem('creditos')||'0')+1).toString()); actualizarUI(); }
  }catch(e){ alert('Error: '+e.message); }
  document.getElementById('loading').classList.add('hidden');
};

function obtenerTexto(){ return document.getElementById('resultado').value||''; }
async function copiarOCR(){ const t=obtenerTexto(); if(!t) return; try{ await navigator.clipboard.writeText(t); alert('Copiado!'); }catch{ const r=document.getElementById('resultado'); r.select(); document.execCommand('copy'); alert('Copiado!'); } }
async function descargarWord(){
  try{
    const t=obtenerTexto(); if(!t) return alert('No hay texto');
    const D=window.docx; if(!D) return alert('docx no cargó, recarga la página');
    const paras=t.split(/\\r?\\n/).map(l=>new D.Paragraph({children:[new D.TextRun(l||' ')]}));
    const doc=new D.Document({sections:[{children:paras}]});
    const blob=await D.Packer.toBlob(doc);
    const u=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=u; a.download='texto_ocr.docx'; a.click(); setTimeout(()=>URL.revokeObjectURL(u),1000);
  }catch(e){ alert('Error Word: '+e.message); }
}
async function crearPdfBlob(){ const t=obtenerTexto(); const {jsPDF}=window.jspdf; const p=new jsPDF(); let y=15; p.setFontSize(11); for(const line of t.split(/\\r?\\n/)){ const parts=p.splitTextToSize(line||' ',180); for(const part of parts){ if(y>280){p.addPage(); y=15;} p.text(part,15,y); y+=7; } } return p.output('blob'); }
async function descargarPdf(){ const b=await crearPdfBlob(); const u=URL.createObjectURL(b); const a=document.createElement('a'); a.href=u; a.download='texto_ocr.pdf'; a.click(); setTimeout(()=>URL.revokeObjectURL(u),1000); }
function enviarWhatsApp(){ const t=obtenerTexto(); if(t) window.open('https://wa.me/?text='+encodeURIComponent(t),'_blank'); }
async function compartirArchivo(){ try{ const b=await crearPdfBlob(); const f=new File([b],'texto_ocr.pdf',{type:'application/pdf'}); if(navigator.canShare&&navigator.canShare({files:[f]})){ await navigator.share({files:[f], title:'Texto OCR'}); return;} }catch{} descargarPdf(); }

document.getElementById('btnCopiar').onclick=copiarOCR;
document.getElementById('btnWord').onclick=descargarWord;
document.getElementById('btnPdf').onclick=descargarPdf;
document.getElementById('btnWhatsapp').onclick=enviarWhatsApp;
document.getElementById('btnCompartir').onclick=compartirArchivo;
</script>
</body>
</html>
"""
if __name__ == '__main__':
    app.run(debug=True) 
