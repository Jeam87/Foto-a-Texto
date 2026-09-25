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
    <div id="drop" class="mt-6 border-2 border-dashed border-gray-300 rounded-xl p-6 text-center cursor-pointer">
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
    <div style="background:white; border-radius:20px; padding:24px; max-width:360px; width:100%; text-align:center;">
      <h2 style="font-size:20px; font-weight:bold;">🚀 Te acabaste los 2 créditos gratis</h2>
      <a onclick="localStorage.setItem('esPro','si');localStorage.setItem('proExpira',(Date.now()+30*86400000).toString());location.reload()" href="https://mpago.la/2LprVEr" target="_blank" style="display:block; background:#2563eb; color:white; padding:14px; border-radius:12px; font-weight:bold; margin-top:20px; text-decoration:none;">PRO MES - $49/mes</a>
      <button onclick="document.getElementById('paywall').style.display='none'" style="margin-top:16px; font-size:12px; color:#aaa; background:none; border:none;">Cerrar</button>
    </div>
  </div>
<script>
let fileData=null; let motorML='TextDetector' in window;
document.getElementById('motor').innerText=motorML?'Motor: ML Kit Offline ⚡ Rápido':'Motor: Tesseract Offline';
function actualizarUI(){ const t=document.getElementById('creditos-text'), b=document.getElementById('pro-badge'); if(localStorage.getItem('esPro')==='si'){ b.classList.remove('hidden'); t.innerText='PRO Activo ∞'; } else { b.classList.add('hidden'); let c=parseInt(localStorage.getItem('creditos')||'0'); t.innerText=c<2?(2-c)+' créditos gratis':'Sin créditos'; } } actualizarUI();
function checkPaywall(){ let c=parseInt(localStorage.getItem('creditos')||'0'); if(localStorage.getItem('esPro')!=='si' && c>=2){ document.getElementById('paywall').style.display='flex'; return false;} return true; }
async function prepararImagenOCR(file){ return new Promise((resolve)=>{ const img=new Image(); img.onload=()=>{ const escala=Math.min(3,Math.max(1.5,1800/Math.max(img.width,img.height))); const c=document.createElement('canvas'); c.width=Math.round(img.width*escala); c.height=Math.round(img.height*escala); const ctx=c.getContext('2d',{willReadFrequently:true}); ctx.drawImage(img,0,0,c.width,c.height); const d=ctx.getImageData(0,0,c.width,c.height); for(let i=0;i<d.data.length;i+=4){ const g=Math.round(0.299*d.data[i]+0.587*d.data[i+1]+0.114*d.data[i+2]); d.data[i]=g; d.data[i+1]=g; d.data[i+2]=g; } ctx.putImageData(d,0,0); c.toBlob(b=>resolve(b),'image/png',1.0); }; img.src=URL.createObjectURL(file); }); }
document.getElementById('drop').onclick=()=>document.getElementById('file').click();
document.getElementById('file').onchange=async(e)=>{
  let f=e.target.files[0]; if(!f) return; const drop=document.getElementById('drop'); const old=document.getElementById('previewFoto'); if(old) old.remove();
  if(f.type==='application/pdf'){
    document.getElementById('drop-text').innerText='📄 Leyendo PDF...';
    const pdf=await pdfjsLib.getDocument(URL.createObjectURL(f)).promise; const page=await pdf.getPage(1); const vp=page.getViewport({scale:2.5});
    const canvas=document.createElement('canvas'); canvas.width=vp.width; canvas.height=vp.height; await page.render({canvasContext:canvas.getContext('2d'), viewport:vp}).promise;
    canvas.id='previewFoto'; canvas.className='mx-auto mt-4 max-h-64 rounded-xl border'; drop.appendChild(canvas);
    canvas.toBlob(b=>{ fileData=new File([b],'pdf.png',{type:'image/png'}); document.getElementById('drop-text').innerText='📄 PDF listo'; },'image/png');
  } else { fileData=f; const im=document.createElement('img'); im.id='previewFoto'; im.className='mx-auto mt-4 max-h-64 rounded-xl'; im.src=URL.createObjectURL(f); drop.appendChild(im); document.getElementById('drop-text').innerText='📷 Foto lista'; }
};
async function reconocerMLKit(blob){ try{ const bmp=await createImageBitmap(blob); const det=new TextDetector(); const r=await det.detect(bmp); if(!r||!r.length) return null; return r.map(x=>x.rawValue).join("\\n"); }catch{ return null; } }
document.getElementById('btn').onclick=async()=>{
  if(!fileData) return alert('Sube foto o PDF'); if(!checkPaywall()) return;
  document.getElementById('loading').classList.remove('hidden');
  try{
    const blob=await prepararImagenOCR(fileData); let texto=null;
    if(motorML){ document.getElementById('loading').innerText='ML Kit Offline ⚡...'; texto=await reconocerMLKit(blob); }
    if(!texto){ document.getElementById('loading').innerText='Leyendo...'; const {data:{text}}=await Tesseract.recognize(blob,'spa'); texto=text; }
    const res=document.getElementById('resultado'); res.value=texto.trim(); res.classList.remove('hidden'); document.getElementById('acciones').classList.remove('hidden'); document.getElementById('acciones').style.display='grid';
    if(localStorage.getItem('esPro')!=='si'){ localStorage.setItem('creditos',(parseInt(localStorage.getItem('creditos')||'0')+1).toString()); actualizarUI(); }
  }catch(e){ alert(e.message); } document.getElementById('loading').classList.add('hidden');
};
function obtenerTexto(){ return document.getElementById('resultado').value||''; }
async function copiarOCR(){ const t=obtenerTexto(); if(!t) return; await navigator.clipboard.writeText(t); alert('Copiado!'); }
async function descargarWord(){
  const t=obtenerTexto(); if(!t) return alert('No hay texto');
  try{
    const D=window.docx;
    if(D && D.Document && D.Packer){
      const paras=t.split(/\\r?\\n/).map(l=>new D.Paragraph({children:[new D.TextRun(l||' ')]}));
      const doc=new D.Document({sections:[{children:paras}]});
      const blob=await D.Packer.toBlob(doc);
      const u=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=u; a.download='texto_ocr.docx'; a.click(); setTimeout(()=>URL.revokeObjectURL(u),1000);
      return;
    }
    throw new Error('docx no cargó');
  }catch(e){
    // FALLBACK 100% COMPATIBLE CON WORD - ESTE SI JALA SIEMPRE
    const htmlContent = `<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word'><head><meta charset='utf-8'></head><body><pre style='font-family:Arial; white-space:pre-wrap;'>${t.replace(/</g,'&lt;')}</pre></body></html>`;
    const blob=new Blob([htmlContent],{type:'application/msword'});
    const u=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=u; a.download='texto_ocr.doc'; a.click(); setTimeout(()=>URL.revokeObjectURL(u),1000);
  }
}
async function crearPdfBlob(){ const t=obtenerTexto(); const {jsPDF}=window.jspdf; const p=new jsPDF(); let y=15; for(const line of t.split(/\\r?\\n/)){ const parts=p.splitTextToSize(line||' ',180); for(const part of parts){ if(y>280){p.addPage(); y=15;} p.text(part,15,y); y+=7; } } return p.output('blob'); }
async function descargarPdf(){ const b=await crearPdfBlob(); const u=URL.createObjectURL(b); const a=document.createElement('a'); a.href=u; a.download='texto_ocr.pdf'; a.click(); }
function enviarWhatsApp(){ const t=obtenerTexto(); if(t) window.open('https://wa.me/?text='+encodeURIComponent(t),'_blank'); }
async function compartirArchivo(){ try{ const b=await crearPdfBlob(); const f=new File([b],'texto_ocr.pdf',{type:'application/pdf'}); if(navigator.canShare&&navigator.canShare({files:[f]})){ await navigator.share({files:[f]}); return;} }catch{} descargarPdf(); }
document.getElementById('btnCopiar').onclick=copiarOCR; document.getElementById('btnWord').onclick=descargarWord; document.getElementById('btnPdf').onclick=descargarPdf; document.getElementById('btnWhatsapp').onclick=enviarWhatsApp; document.getElementById('btnCompartir').onclick=compartirArchivo;
</script>
</body>
</html>
"""
if __name__ == '__main__':
    app.run(debug=True) 
