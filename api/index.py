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
<script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<style>
body{background:#000;color:#fff;font-family:sans-serif;text-align:center;padding:10px}
.box{max-width:520px;margin:auto;background:#111;padding:15px;border-radius:15px;border:1px solid #333}
button{width:100%;padding:14px;margin:6px 0;border-radius:10px;border:none;font-weight:bold;font-size:15px}
#b1{background:#fff;color:#000} #b2{background:#0f0;color:#000} #b3{background:#333;color:#fff}
#texto{width:100%;height:350px;background:#000;color:#0f0;padding:10px;border:1px solid #333;border-radius:10px}
img{max-width:100%;border-radius:10px;margin:5px 0}
</style>
</head>
<body>
<div class="box">
<h3>FOTO Y PDF A TEXTO PRO</h3>
<input type="file" id="files" multiple accept="image/*,.pdf" style="width:100%;padding:10px">
<div id="prev"></div>
<button id="b1" onclick="leerTodo()">LEER TODO</button>
<p id="estado" style="color:yellow">Elige 1 o varias fotos o PDF</p>
<textarea id="texto" placeholder="Aqui saldra todo el texto junto..."></textarea>
<button id="b2" onclick="copiar()">COPIAR TODO</button>
<button id="b3" onclick="borrar()">BORRAR</button>
</div>
<script>
let archivos=[];
document.getElementById('files').addEventListener('change', e=>{
 archivos=[...e.target.files]; let p=document.getElementById('prev'); p.innerHTML='';
 archivos.forEach(f=>{
  if(f.type.startsWith('image/')){ let im=document.createElement('img'); im.src=URL.createObjectURL(f); p.appendChild(im); }
  else { p.innerHTML+='<div>📄 '+f.name+'</div>'; }
 });
 document.getElementById('estado').innerText=archivos.length+' archivos listos';
});

async function leerTodo(){
 if(!archivos.length){alert('Elige archivos');return}
 document.getElementById('texto').value='';
 for(let i=0;i<archivos.length;i++){
  let f=archivos[i];
  document.getElementById('estado').innerText='Leyendo '+(i+1)+'/'+archivos.length+' : '+f.name;
  if(f.type=='application/pdf'){
   let pdf=await pdfjsLib.getDocument(URL.createObjectURL(f)).promise;
   for(let pg=1;pg<=pdf.numPages;pg++){
    let page=await pdf.getPage(pg);
    let vp=page.getViewport({scale:2});
    let canvas=document.createElement('canvas'); canvas.width=vp.width; canvas.height=vp.height;
    await page.render({canvasContext:canvas.getContext('2d'),viewport:vp}).promise;
    let {data:{text}}=await Tesseract.recognize(canvas,'spa');
    document.getElementById('texto').value+='\\n--- '+f.name+' Pag '+pg+' ---\\n'+text+'\\n';
   }
  } else {
   let {data:{text}}=await Tesseract.recognize(f,'spa',{logger:m=>{
    if(m.status=='recognizing text') document.getElementById('estado').innerText='Leyendo '+(i+1)+'/'+archivos.length+' '+Math.round(m.progress*100)+'%';
   }});
   document.getElementById('texto').value+='\\n--- '+f.name+' ---\\n'+text+'\\n';
  }
 }
 document.getElementById('estado').innerText='¡Todo listo! '+archivos.length+' archivos';
}
function copiar(){ let t=document.getElementById('texto'); t.select(); document.execCommand('copy'); alert('Todo copiado'); }
function borrar(){ document.getElementById('texto').value=''; document.getElementById('prev').innerHTML=''; archivos=[]; document.getElementById('estado').innerText='Borrado'; }
</script>
</body>
</html>
"""
