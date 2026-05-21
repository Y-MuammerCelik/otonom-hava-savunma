import os
import sys
import argparse
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def register_fonts():
    font_name = 'Helvetica'
    font_bold_name = 'Helvetica-Bold'
    windir = os.environ.get('WINDIR', 'C:\\Windows')
    fonts_dir = os.path.join(windir, 'Fonts')
    arial_path = os.path.join(fonts_dir, 'arial.ttf')
    arial_bold_path = os.path.join(fonts_dir, 'arialbd.ttf')
    
    if os.path.exists(arial_path):
        try:
            pdfmetrics.registerFont(TTFont('Arial', arial_path))
            font_name = 'Arial'
            if os.path.exists(arial_bold_path):
                pdfmetrics.registerFont(TTFont('Arial-Bold', arial_bold_path))
                font_bold_name = 'Arial-Bold'
        except Exception:
            pass
    return font_name, font_bold_name

def build_simple_pdf(mesafe, hiz, irtifa, skor, filename="Hesaplama_Sonucu.pdf"):
    font_name, font_bold_name = register_fonts()
    
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'], fontName=font_bold_name,
        fontSize=18, leading=22, textColor=colors.HexColor('#1E3A8A'), alignment=1, spaceAfter=20
    )
    
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'], fontName=font_name, fontSize=12, leading=16, spaceAfter=10
    )
    
    story = []
    
    # Header
    story.append(Paragraph("OTONOM HAVA SAVUNMA & TEHDİT SKORLAMA SİSTEMİ", title_style))
    story.append(Paragraph("Sistem Hesaplama Sonuç Raporu", ParagraphStyle('Sub', parent=title_style, fontSize=14, textColor=colors.HexColor('#4B5563'), spaceAfter=30)))
    
    # Info
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    story.append(Paragraph(f"<b>Rapor Tarihi:</b> {now_str}", body_style))
    story.append(Spacer(1, 15))
    
    # Identify threat level text
    try:
        skor_val = float(skor)
    except ValueError:
        skor_val = 0.0
        
    if skor_val <= 35:
        durum = "DÜŞÜK TEHDİT"
        renk = colors.HexColor('#10B981') # Green
    elif skor_val <= 65:
        durum = "ORTA TEHDİT"
        renk = colors.HexColor('#F59E0B') # Orange
    else:
        durum = "YÜKSEK TEHDİT"
        renk = colors.HexColor('#EF4444') # Red
    
    # Input Table
    data = [
        [Paragraph("<b>Parametre</b>", ParagraphStyle('Th', parent=body_style, fontName=font_bold_name, textColor=colors.white)),
         Paragraph("<b>Değer</b>", ParagraphStyle('Th', parent=body_style, fontName=font_bold_name, textColor=colors.white))],
        ["Mesafe", f"{mesafe} km"],
        ["Hız", f"{hiz} km/h"],
        ["İrtifa", f"{irtifa} m"],
        ["Hesaplanan Tehdit Skoru", f"%{skor}"]
    ]
    
    t = Table(data, colWidths=[200, 200])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), font_bold_name),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F3F4F6')),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#D1D5DB')),
        ('FONTNAME', (0,1), (-1,-1), font_name),
        ('FONTSIZE', (0,1), (-1,-1), 12),
        ('PADDING', (0,0), (-1,-1), 10),
        # Highlight score row
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#E5E7EB')),
        ('FONTNAME', (0,4), (-1,4), font_bold_name),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 30))
    
    # Conclusion box
    story.append(Paragraph("Sistem Kararı:", ParagraphStyle('C', parent=body_style, fontName=font_bold_name)))
    
    decision_data = [[Paragraph(f"<font color='white'><b>{durum}</b></font>", ParagraphStyle('Status', parent=body_style, alignment=1, fontSize=16))]]
    dt = Table(decision_data, colWidths=[400], rowHeights=[40])
    dt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), renk),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 2, colors.HexColor('#1F2937'))
    ]))
    story.append(dt)
    
    doc.build(story)
    print(f"Successfully generated simple PDF: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate simple threat score report")
    parser.add_argument("mesafe", help="Mesafe (km)")
    parser.add_argument("hiz", help="Hiz (km/h)")
    parser.add_argument("irtifa", help="Irtifa (m)")
    parser.add_argument("skor", help="Tehdit Skoru (%)")
    
    args = parser.parse_args()
    build_simple_pdf(args.mesafe, args.hiz, args.irtifa, args.skor)
