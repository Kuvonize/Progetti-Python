from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from dotenv import load_dotenv
import os
import json
from PIL import Image,ImageDraw,ImageFont
from uuid import uuid4
from pathlib import Path

output_dir=Path('generated')
output_dir.mkdir(exist_ok=True)

load_dotenv()

app=Flask(
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
    )

app.config['SECRET_KEY']=os.getenv('SECRET_KEY','dev_key')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET','POST'])
def create():
    with open('app/quotes.json','r', encoding='utf-8') as f:
        quotes=json.load(f)
    if request.method == 'POST':
        # 1) Leggi i dati dal form
        sfondo       = request.form.get('sfondo')
        print("DEBUG sfondo:", repr(sfondo))
        print("DEBUG files backgrounds:", [p.name for p in Path("app/static/backgrounds").glob("*")])
        if not sfondo or not (Path('app/static/backgrounds')/sfondo).exists():
            flash('Sfondo non valido', 'error')
            return  render_template("create.html", quotes=quotes, valori=request.form)            
        motto        = request.form.get('motto')
        testo        = request.form.get('testo')
        if not testo.strip() and not motto.strip():
            flash("Devi scrivere un testo o scegliere un motto", "error")
            return  render_template("create.html", quotes=quotes, valori=request.form)
        font         = request.form.get('font')
        if not font or not (Path("app/static/fonts") / font).exists():
            flash("Font non valido", "error")
            return  render_template("create.html", quotes=quotes, valori=request.form)
        dimensione   = request.form.get('dimensione')
        try:
            dim=int(dimensione)
            if dim <12 or dim >72:
                raise ValueError
        except ValueError:
            flash("Dimensione font non valida (12-72)", "error")
            return  render_template("create.html", quotes=quotes, valori=request.form)
        colore       = request.form.get('colore')
        allineamento = request.form.get('allineamento')
        mittente     = request.form.get('da')
        destinatario = request.form.get('per')

        # 2) Testo finale (priorità al personalizzato)
        testo = (testo or "").strip()
        motto = (motto or "").strip()
        testo_finale = testo if testo else motto
        if not testo_finale:
            return "Devi inserire un testo o scegliere un motto.", 400

        # 3) Percorsi e nome file output
        file_name   = f"{uuid4()}.png"
        path_output = Path("generated") / file_name
        path_sfondo = Path("app/static/backgrounds") / sfondo
        path_font   = Path("app/static/fonts") / font

        # 4) Apri immagine + draw + font
        img  = Image.open(path_sfondo).convert("RGBA")
        draw = ImageDraw.Draw(img)
        W, H = img.size
        try:
            dim = int(dimensione) if dimensione else 36
        except ValueError:
            dim = 36
        font_obj   = ImageFont.truetype(str(path_font), size=dim)
        font_small = ImageFont.truetype(str(path_font), size=max(14, dim // 2))

        # 5) Colore (mappa semplice)
        mappa_colori = {
            'black': (0, 0, 0, 255),
            'white': (255, 255, 255, 255),
            'red':   (255, 0, 0, 255),
        }
        fill_color = mappa_colori.get(colore, (0, 0, 0, 255))

        # 6) Word-wrap: spezza il testo entro i margini (8% per lato)
        margin_x = int(W * 0.08)
        usable_w = W - 2 * margin_x
        righe = []
        corrente = ""
        for parola in testo_finale.split():
            proposta = (corrente + " " + parola).strip()
            width_prop = draw.textbbox((0, 0), proposta, font=font_obj)[2]
            if width_prop <= usable_w or not corrente:
                corrente = proposta
            else:
                righe.append(corrente)
                corrente = parola
        if corrente:
            righe.append(corrente)

        # 7) Posizionamento verticale (centrato sul blocco)
        line_h  = draw.textbbox((0, 0), "Ay", font=font_obj)[3]
        total_h = line_h * len(righe)
        y = (H - total_h) // 2

        # (facoltativo) “Per:” in alto
        if destinatario:
            draw.text((margin_x, int(H * 0.06)),
                    f"Per: {destinatario}", font=font_small, fill=fill_color)

        # 8) Disegna ogni riga (centrato o sinistra)
        for riga in righe:
            text_w = draw.textbbox((0, 0), riga, font=font_obj)[2]
            x = (W - text_w) // 2 if allineamento == "center" else margin_x
            # (opzionale) ombra leggera
            draw.text((x+1, y+1), riga, font=font_obj, fill=(0, 0, 0, 120))
            draw.text((x, y), riga, font=font_obj, fill=fill_color)
            y += line_h

        # (facoltativo) “Da:” in basso a destra
        if mittente:
            da_text = f"Da: {mittente}"
            da_w = draw.textbbox((0, 0), da_text, font=font_small)[2]
            draw.text((W - da_w - margin_x, H - int(H * 0.08)),
                    da_text, font=font_small, fill=fill_color)

        # 9) Salva e mostra risultato
        img.save(path_output, format="PNG")
        flash("E-card generata!", "success")
        return render_template("result.html", image_name=file_name)
    elif request.method=='GET':
        return render_template("create.html", quotes=quotes, valori=request.form)     

@app.route('/g/<nomefile>')
def serve_generated(nomefile):
    return send_file(output_dir/nomefile, mimetype='image/png')

@app.route('/download/<nomefile>')
def download_card(nomefile):
    return send_file(output_dir/nomefile, as_attachment=True, download_name='e_card.png')

if __name__=='__main__':
    app.run(debug=True)