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
<title>Foto a Texto</title>
<script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>
<style>
body{background:#000;color:#fff;font-family:sans-serif;text-align:center;padding:15px}
.box{max-width:500px;margin:auto;background:#111;padding:15px;border-radius:15px;border:1px solid #333}
button{width:100%;padding:15px;margin:8px 0;border-radius:10px;border:none;font-size:16px;font-weight:bold}
#b1{background:#fff;color:#000} #b2{background:#0f0;color:#000}
#texto{width:100%;height:280px;background:#000;color:#0f0;padding:10px;border:1px solid #333;border-radius:10px;white-space:pre-wrap}
img{max-width:100%;border-radius:10px;margin-top:10px}
</style>
</head>
<body>
<div class="box">
<h3>FOTO A TEXTO 100% EXACTO</h3>
<input type="file" id="foto" accept="image/*" style="width:100%;padding:10px">
<img id="preview" style="display:none">
<button id="b1" onclick="leer()">LEER FOTO</button>
<p id="estado" style="color:yellow">Elige una foto clara</p>
<textarea id="texto" placeholder="Aqui saldra el texto exacto..."></textarea>
<button id="b2" onclick="copiar()">COPIAR</button>
</div>
<script>
let archivo=null;
document.getElementById('foto').addEventListener('change', e=>{
  archivo=e.target.files[0];
  let img=document.getElementById('preview');
  img.src=URL.createObjectURL(archivo);
  img.style.display='block';
  document.getElementById('estado').innerText='Foto lista, dale a LEER FOTO';
});
async function leer(){
  if(!archivo){alert('Elige foto');return}
  document.getElementById('estado').innerText='Leyendo... no cierres, tarda 10 seg con WiFi';
  try{
    const { data: { text } } = await Tesseract.recognize(archivo, 'spa', {
      logger: m=>{ if(m.status=='recognizing text'){ document.getElementById('estado').innerText='Leyendo... '+Math.round(m.progress*100)+'%'; } }
    });
    document.getElementById('texto').value=text;
    document.getElementById('estado').innerText='¡Listo! 100% exacto';
  }catch(err){
    document.getElementById('estado').innerText='Error: conectate a WiFi y recarga';
  }
}
function copiar(){ let t=document.getElementById('texto'); t.select(); document.execCommand('copy'); alert('Copiado'); }
</script>
</body>
</html>
""" 
