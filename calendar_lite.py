"""MODEL 01 Lite - English-only photo wall calendar. MIT License."""
from __future__ import annotations
import argparse
import calendar
import datetime as dt
import html
import sys
from pathlib import Path
from tkinter import Tk, Frame, Label, Button, Entry, StringVar, filedialog, messagebox, Listbox, END
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'output'
OUTPUT.mkdir(exist_ok=True)
MONTHS = list(calendar.month_name)[1:]


def image_for_month(images, month):
    if not images:
        return None
    return images[month] if len(images) >= 13 else images[month - 1] if len(images) >= 12 else images[(month - 1) % len(images)]


def cover_image(images):
    return images[0] if images else None


def draw_photo(c, path, x, y, w, h):
    if not path:
        c.setFillColorRGB(.9, .93, .96)
        c.rect(x, y, w, h, fill=1, stroke=0)
        c.setFillColorRGB(.3, .4, .5)
        c.drawCentredString(x + w / 2, y + h / 2, 'Add your own photo')
        return
    with Image.open(path) as raw:
        img = ImageOps.exif_transpose(raw).convert('RGB')
        iw, ih = img.size
        target_ratio = w / h
        if iw / ih > target_ratio:
            cropw = int(ih * target_ratio)
            left = (iw - cropw) // 2
            img = img.crop((left, 0, left + cropw, ih))
        else:
            croph = int(iw / target_ratio)
            top = (ih - croph) // 2
            img = img.crop((0, top, iw, top + croph))
        c.drawImage(ImageReader(img), x, y, w, h, mask='auto')


def month_grid(c, year, month, x, top, w, h, compact=False):
    weeks = calendar.monthcalendar(year, month)
    rows = 6 if not compact else 6
    heading = 25 if not compact else 14
    c.setFont('Helvetica-Bold', 17 if not compact else 8.2)
    c.setFillColorRGB(.1, .2, .32)
    c.drawString(x, top - heading + (5 if not compact else 2), f'{MONTHS[month-1]} {year}')
    table_top = top - heading - (9 if not compact else 2)
    header_h = 24 if not compact else 12
    cell_h = (h - heading - header_h - (9 if not compact else 2)) / rows
    cell_w = w / 7
    c.setFillColorRGB(.1, .33, .55)
    c.rect(x, table_top - header_h, w, header_h, fill=1, stroke=0)
    for col, name in enumerate(['Mon','Tue','Wed','Thu','Fri','Sat','Sun']):
        c.setFillColorRGB(1, 1, 1)
        c.setFont('Helvetica-Bold', 9 if not compact else 5.8)
        c.drawCentredString(x + col * cell_w + cell_w / 2, table_top - header_h + (8 if not compact else 3), name if not compact else name[0])
    for r in range(rows):
        for col in range(7):
            xx = x + col * cell_w
            yy = table_top - header_h - (r + 1) * cell_h
            c.setFillColorRGB(.975, .985, .995) if col < 5 else c.setFillColorRGB(.94, .96, .98)
            c.rect(xx, yy, cell_w, cell_h, fill=1, stroke=0)
            c.setStrokeColorRGB(.82, .86, .9)
            c.rect(xx, yy, cell_w, cell_h, fill=0, stroke=1)
            day = weeks[r][col] if r < len(weeks) else 0
            if day:
                c.setFillColorRGB(.14, .2, .28)
                c.setFont('Helvetica-Bold', 12 if not compact else 6.3)
                c.drawCentredString(xx + cell_w / 2, yy + cell_h / 2 - (4 if not compact else 2), str(day))


def make_pdf(year, images, destination=None):
    OUTPUT.mkdir(exist_ok=True)
    filename = f'Wall_Calendar_Model01_{year}_EN_14pages_{dt.datetime.now():%Y%m%d_%H%M%S}.pdf'
    destination = Path(destination) if destination else OUTPUT / filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(destination), pagesize=A4)
    W, H = A4
    c.setTitle(f'Model 01 Lite Wall Calendar {year}')
    # Cover
    draw_photo(c, cover_image(images), 34, 188, W-68, H-270)
    c.setFillColorRGB(.08, .22, .36)
    c.setFont('Helvetica-Bold', 46)
    c.drawCentredString(W/2, 105, str(year))
    c.setFont('Helvetica', 17)
    c.drawCentredString(W/2, 77, 'PHOTO WALL CALENDAR')
    c.setFont('Helvetica', 10)
    c.drawCentredString(W/2, 55, 'MODEL 01 LITE | ENGLISH EDITION')
    c.showPage()
    # Twelve months
    for month in range(1, 13):
        draw_photo(c, image_for_month(images, month), 34, H-340, W-68, 302)
        month_grid(c, year, month, 34, H-365, W-68, 394)
        c.setFont('Helvetica', 8)
        c.setFillColorRGB(.45, .5, .55)
        c.drawCentredString(W/2, 24, f'MODEL 01 LITE  |  {month:02d} / {year}')
        c.showPage()
    # Annual overview, always 4 rows x 3 columns (no clipped last row)
    c.setFillColorRGB(.08, .22, .36)
    c.setFont('Helvetica-Bold', 23)
    c.drawCentredString(W/2, H-44, f'{year} - YEAR AT A GLANCE')
    margin_x = 26
    gap_x = 12
    col_w = (W - 2*margin_x - 2*gap_x)/3
    top = H-68
    bottom = 35
    gap_y = 10
    box_h = (top-bottom-3*gap_y)/4
    for m in range(1,13):
        row, col = divmod(m-1, 3)
        xx = margin_x + col*(col_w+gap_x)
        tt = top - row*(box_h+gap_y)
        month_grid(c, year, m, xx, tt, col_w, box_h, compact=True)
    c.showPage()
    c.save()
    return destination


def make_preview(year, images, destination=None):
    destination = Path(destination) if destination else OUTPUT / f'Wall_Calendar_Model01_{year}_Preview.png'
    destination.parent.mkdir(parents=True, exist_ok=True)
    im = Image.new('RGB', (960, 1360), '#f7f9fc')
    d = ImageDraw.Draw(im)
    d.text((55, 30), f'{year}  |  WALL CALENDAR - MODEL 01 LITE', fill='#153657')
    photo = image_for_month(images, 1)
    if photo:
        with Image.open(photo) as raw:
            src = ImageOps.fit(ImageOps.exif_transpose(raw).convert('RGB'), (850, 550))
            im.paste(src, (55, 85))
    else:
        d.rectangle((55,85,905,635),fill='#dce7f1')
        d.text((360,355),'YOUR PHOTO HERE',fill='#153657')
    d.text((55, 675), f'JANUARY {year}', fill='#153657', stroke_width=0)
    x0, y0, cw, ch = 55, 725, 121, 80
    for i, name in enumerate(['MON','TUE','WED','THU','FRI','SAT','SUN']):
        x = x0+i*cw
        d.rectangle((x,y0,x+cw,y0+48),fill='#1b578a')
        d.text((x+39,y0+17),name,fill='white')
    for r, week in enumerate(calendar.monthcalendar(year,1)):
        for i, day in enumerate(week):
            x=x0+i*cw; y=y0+48+r*ch
            d.rectangle((x,y,x+cw,y+ch),fill='#ffffff' if i<5 else '#e8eff6',outline='#c2cbd6')
            if day: d.text((x+51,y+30),str(day),fill='#20364c')
    im.save(destination)
    return destination


def make_simulation(year, images, destination=None):
    destination = Path(destination) if destination else OUTPUT / f'Wall_Calendar_Model01_{year}_Simulation.html'
    destination.parent.mkdir(parents=True, exist_ok=True)
    sections=[]
    for m in range(1,13):
        weeks=calendar.monthcalendar(year,m)
        head=''.join(f'<th>{name}</th>' for name in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
        body=''.join('<tr>'+''.join(f'<td>{day or ""}</td>' for day in week)+'</tr>' for week in weeks)
        photo=image_for_month(images,m)
        uri=Path(photo).resolve().as_uri() if photo else ''
        pic=f'<img src="{html.escape(uri,quote=True)}" alt="Month photo">' if photo else '<div class="placeholder">Your photo</div>'
        sections.append(f'<section class="page">{pic}<h2>{MONTHS[m-1]} {year}</h2><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></section>')
    source='''<!doctype html><html lang="en"><meta charset="utf-8"><title>Model 01 Lite Simulation</title><style>body{font:16px Arial;background:#e9eff4;color:#17314b;margin:0;padding:25px}.bar{position:sticky;top:0;background:#fff;padding:14px;text-align:center;z-index:2}.page{background:white;max-width:650px;min-height:800px;margin:24px auto;padding:30px;box-shadow:0 4px 18px #999}.page img,.placeholder{width:100%;height:370px;object-fit:cover;background:#d9e4ec}.placeholder{display:grid;place-items:center}h2{text-align:center}table{border-collapse:collapse;width:100%;table-layout:fixed}th{background:#1b578a;color:white}td,th{border:1px solid #c6d1da;text-align:center;height:45px}td:nth-child(n+6){background:#edf3f8}button{padding:10px 20px;background:#1b578a;color:white;border:0;cursor:pointer}@media print{.bar{display:none}.page{box-shadow:none;break-after:page}}</style><div class="bar"><button onclick="previous()">Previous</button> <strong id="counter"></strong> <button onclick="next()">Next</button></div>'''+''.join(sections)+'''<script>let index=0;const pages=[...document.querySelectorAll('.page')];function show(){pages.forEach((p,i)=>p.style.display=i===index?'block':'none');document.getElementById('counter').textContent=(index+1)+' / 12'}function next(){index=(index+1)%12;show()}function previous(){index=(index+11)%12;show()}show()</script></html>'''
    destination.write_text(source,encoding='utf-8')
    return destination


class CalendarApp:
    def __init__(self, root):
        self.root=root
        root.title('MODEL 01 LITE - Photo Wall Calendar (English)')
        root.geometry('820x620')
        self.year=StringVar(value=str(dt.date.today().year+1))
        self.images=[]
        Label(root,text='MODEL 01 LITE - PHOTO WALL CALENDAR',font=('Arial',18,'bold')).pack(pady=16)
        bar=Frame(root);bar.pack(pady=6)
        Label(bar,text='Year:').pack(side='left')
        Entry(bar,textvariable=self.year,width=9).pack(side='left',padx=10)
        Button(bar,text='Import 12 / 13 photos',command=self.import_images,bg='#1674c5',fg='white').pack(side='left',padx=8)
        Button(bar,text='Clear photos',command=self.clear).pack(side='left',padx=8)
        Label(root,text='12 photos: January-December | 13 photos: Cover + January-December',fg='#31506a').pack(pady=10)
        self.listbox=Listbox(root,width=95,height=17)
        self.listbox.pack(padx=15,pady=10)
        buttons=Frame(root);buttons.pack(side='bottom',pady=20)
        Button(buttons,text='1  GENERATE PDF (14 pages)',command=self.pdf,bg='#008e50',fg='white',height=2).pack(side='left',padx=7)
        Button(buttons,text='2  SIMULATION HTML',command=self.simulation,bg='#e5ad15',height=2).pack(side='left',padx=7)
        Button(buttons,text='3  PREVIEW PNG',command=self.preview,bg='#1674c5',fg='white',height=2).pack(side='left',padx=7)
        Button(buttons,text='4  OPEN OUTPUT',command=self.open_output,bg='#ee7e19',fg='white',height=2).pack(side='left',padx=7)
        self.refresh()
    def valid_year(self):
        try:
            y=int(self.year.get()); assert 1900<=y<=2100
            return y
        except (ValueError,AssertionError):
            messagebox.showerror('Invalid year','Enter a year between 1900 and 2100.')
            return None
    def import_images(self):
        selected=filedialog.askopenfilenames(title='Select 12 or 13 images',filetypes=[('Images','*.jpg *.jpeg *.png *.webp *.bmp')])
        if not selected:return
        if len(selected) not in (12,13):
            messagebox.showwarning('Image count','Please select exactly 12 or 13 images.')
            return
        self.images=list(selected)
        self.refresh()
    def clear(self):self.images=[];self.refresh()
    def refresh(self):
        self.listbox.delete(0,END)
        if not self.images:self.listbox.insert(END,'No photos imported. You can still generate a sample PDF.')
        for i,path in enumerate(self.images):
            name='Cover' if len(self.images)==13 and i==0 else MONTHS[i-1 if len(self.images)==13 else i]
            self.listbox.insert(END,f'{i+1:02d}  {name:12}  {Path(path).name}')
    def run_action(self,fn):
        year=self.valid_year()
        if year is None:return
        try:
            path=fn(year,self.images)
            messagebox.showinfo('Created',f'Saved successfully:\n{path}')
        except Exception as exc:
            messagebox.showerror('Error',str(exc))
    def pdf(self):self.run_action(make_pdf)
    def simulation(self):self.run_action(make_simulation)
    def preview(self):self.run_action(make_preview)
    def open_output(self):
        import os
        os.startfile(str(OUTPUT)) if sys.platform=='win32' else messagebox.showinfo('Output folder',str(OUTPUT))


def main():
    parser=argparse.ArgumentParser(description='Model 01 Lite photo wall calendar')
    parser.add_argument('--demo',action='store_true',help='Generate demo PDF, PNG and HTML using bundled sample images')
    parser.add_argument('--year',type=int,default=2027)
    args=parser.parse_args()
    if args.demo:
        images=sorted(str(p) for p in (ROOT/'demo'/'sample_images').glob('*.jpg'))
        if len(images)!=13: raise RuntimeError('Demo needs 13 images')
        for fn in (make_pdf,make_preview,make_simulation):print(fn(args.year,images))
    else:
        root=Tk();CalendarApp(root);root.mainloop()

if __name__=='__main__':main()
