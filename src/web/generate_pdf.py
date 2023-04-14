import datetime
import io
import tempfile
import PyPDF2
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import Table, TableStyle,Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sp_data import page3
import singleton as sg
import logging

global c_page
def load_data(personID):
    inst = sg.SnowConnect()
    session = inst.getsession()
    try:
        return page3(session,personID)
    except Exception as e:
        del inst
        # del session
        inst = sg.SnowConnect()
        session = inst.getsession()
        return page3(session,personID)

def style(x):
    x.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), "0x9fbac9"),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'HeiseiMin-W3'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('LEFTPADDING', (0, 0), (-1, 0), 1),
        ('RIGHTPADDING', (0, 0), (-1, 0), 1),
        ('BACKGROUND', (0, 1), (-1, -1), "0xd7dbdf"),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'HeiseiMin-W3'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('LEFTPADDING', (0, 1), (-1, -1), 1),
        ('RIGHTPADDING', (0, 1), (-1, -1), 1),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('WORDWRAP', (1, 1), (1, 1), 1),
        ('ROUNDEDCORNERS',[2,2,2,2])
]))

def Generate_pdf(x,position):
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))
    global c_page
    dt_now = datetime.datetime.now()
    filename = "HR_CARD " + str(dt_now.year) + str(dt_now.month)+ str(dt_now.day)+ str(dt_now.hour)+ str(dt_now.minute)+ str(dt_now.second)
    pdf_file = PyPDF2.PdfWriter()
    styles = getSampleStyleSheet()
    style1 = styles["Normal"]
    style1.alignment = TA_CENTER    
    style1.fontSize = 10    
    style1.fontName = 'HeiseiMin-W3'
    for i in range(len(x)):
        if position != -1:
            header_1 = list(x[i][str(position)].keys())
            values_1 = list(x[i][str(position)].values())
            try :
                 df1,df2,df3,df4,df5,df6,df7,image = load_data(values_1[0])
            except Exception as e:
                 logging.info(e)
        else:
            try :
                 df1,df2,df3,df4,df5,df6,df7,image = load_data(x[i]['社員ID'])
            except Exception as e:
                 logging.info(e)
            header_1 = list(x[i].keys())[1:]
            values_1 = list(x[i].values())[1:]
        pdf_bytes = io.BytesIO()
        pdf_file.write(pdf_bytes)
        c_page = canvas.Canvas(filename, pagesize=A4)
        c_page.setFont('HeiseiMin-W3', 16)
        final_header = []
        for cell in header_1:
            cell = str(cell)
            para = Paragraph(cell, style1)
            final_header.append(para)
        final_values = []
        for cell in values_1:
            cell = str(cell)
            para = Paragraph(cell, style1)
            final_values.append(para)
        data= [final_header] + [final_values]
        h13 =[]
        h13_13 = 0
        for h in header_1:
            h13.append(len(h))
            h13_13 += len(h)
        h13_13 = 380/h13_13
        h13 = [x*h13_13 for x in h13]
        for hh in range(len(h13)):
            if h13[hh] < 13:
                h13[hh] = 13
        table = Table(data,colWidths=h13)
        style(table)
        table.wrapOn(c_page, 0 , 0)
        table.drawOn(c_page, 175, 635)
        img = Image.open("13.png")
        with tempfile.NamedTemporaryFile(delete=False) as d:
            img.save(d, 'png')
            d.flush()
            c_page.drawImage(d.name, 155 ,755, height=50 , width=430)
        img = Image.open("jera.png")
        with tempfile.NamedTemporaryFile(delete=False) as f:
            img.save(f, 'png')
            f.flush()
            c_page.drawImage(f.name, 25 ,700, height=150 , width=130)
        if len(image)==0 or image['FACE_PHOTO_RECORD'][0] == None :
          image13 = Image.open("No_image_available2.png")
        else:
          image13 = Image.open(io.BytesIO(image['FACE_PHOTO_RECORD'][0]))
        img_width, img_height = image13.size
        if img_width > 180 :
            img_width,img_height = [180,240]
        with tempfile.NamedTemporaryFile(delete=False) as g:
            image13.save(g, 'png')
            g.flush()
            c_page.drawImage(g.name, 30,600, height=img_height/2, width=img_width/2)
        x_axis,y = 20,565
        lst = [df1,df2,df3,df4,df5,df6,df7]
        df_names=["基本情報","住所情報","職務情報","親会社職歴情報","出身情報","教育情報","資格情報"]
        for i in range(len(lst)):
            data,remaining_data = [],[]
            table_header_print=False
            data0,remaining_data0 = [],[lst[i].columns.to_list()]+ lst[i].values.tolist()
            quiter = False
            for row in data0:
                table_row = []
                for cell in row:
                    cell = str(cell)
                    para = Paragraph(cell, style1)
                    table_row.append(para)
                data.append(table_row)
            for row in remaining_data0:
                table_row = []
                for cell in row:
                    cell = str(cell)
                    para = Paragraph(cell, style1)
                    table_row.append(para)
                remaining_data.append(table_row)
            while True:
                if len(data)==0 and len(remaining_data)>1:
                    data.append(remaining_data.pop(0))
                    data.append(remaining_data.pop(0))
                elif len(data)==0 and (len(remaining_data)==0 or remaining_data==[]):
                  break
                elif len(data)==0:
                    data.append(remaining_data.pop(0))
                if i == 0:
                    col_width =[]
                    col_width_max = 0
                    for h in lst[i].columns:
                        col_width.append(len(h))
                        col_width_max += len(h)
                    col_width_max = 555/col_width_max
                    col_width = [x*col_width_max for x in col_width]
                    for cli in range(len(col_width)):
                        if col_width[cli] < 13:
                            col_width[cli] = 13
                elif i == 1:
                    col_width = [69.375,69.375,208.125,208.125]
                elif i == 2:
                    col_width = [68,86,77,77,77,101,67]
                elif i == 3:
                    col_width = [69.375,69.375,319.125,97.125]
                elif i == 4:
                    col_width = [52.5, 93.5, 147.5, 93.5, 88.5, 79.5]
                elif i == 5:
                    col_width = [462.5,92.5]
                elif i == 6:
                    col_width = [365,100,90]
                table = Table(data,colWidths=col_width)
                style(table)
                table_width,table_height = table.wrapOn(c_page, 0 , 0)
                if table_height > y :
                    col_width = 555/len(data[0])
                    table = Table(data,colWidths=col_width)
                    style(table)
                    table_width,table_height = table.wrapOn(c_page, 0 , 0)
                if len(remaining_data)>=0 and (y - table_height) < 58 :
                    if len(data)==2:
                        remaining_data.insert(0,data.pop())
                        remaining_data.insert(0,data.pop())
                    elif len(data)==1:
                        remaining_data.insert(0,data.pop())
                    else:
                        if i == 0:
                            col_width =[]
                            col_width_max = 0
                            for h in lst[i].columns:
                                col_width.append(len(h))
                                col_width_max += len(h)
                            col_width_max = 555/col_width_max
                            col_width = [x*col_width_max for x in col_width]
                            for cli in range(len(col_width)):
                                if col_width[cli] < 13:
                                    col_width[cli] = 13
                        elif i == 1:
                            col_width = [69.375,69.375,69.375*3,69.375*3]
                        elif i == 2:
                            col_width = [68,86,77,77,77,103,67]
                        elif i == 3:
                            col_width = [69.375,69.375,319.125,97.125]
                        elif i == 4:
                            col_width = [52.5, 93.5, 147.5, 93.5, 88.5, 79.5]
                        elif i == 5:
                            col_width = [462.5,92.5]
                        elif i == 6:
                            col_width = [365,100,90]
                        table = Table(data,colWidths=col_width)
                        style(table)
                        table_width,table_height = table.wrapOn(c_page, 0 , 0)
                        if table_height > y :
                            col_width = 555/len(data[0])
                            table = Table(data,colWidths=col_width)
                            style(table)
                            table_width,table_height = table.wrapOn(c_page, 0 , 0)
                        if table_header_print==False:
                            c_page.drawString(x_axis, y, df_names[i])
                            y -= 13
                            table_header_print = True
                        table.drawOn(c_page,x_axis,y-table_height)
                        data=[data[0]]
                    c_page.save()
                    pdf_file.add_page(PyPDF2.PdfReader(open(filename, "rb")).pages[0])
                    c_page = canvas.Canvas(filename,pagesize=A4)
                    c_page.setFont('HeiseiMin-W3', 16)
                    if len(remaining_data)>0:
                      data.append(remaining_data.pop(0))
                    y=810
                elif len(remaining_data) > 0 and (y - table_height) >= 58:
                    data.append(remaining_data.pop(0))
                elif len(remaining_data)==0:
                    if table_header_print==False:
                        c_page.drawString(x_axis, y, df_names[i])
                        y -= 13
                        table_header_print = True
                    table.drawOn(c_page,x_axis,y-table_height)
                    y = y-table_height
                    quiter = True
                if quiter:
                    y -= 30
                    break
        c_page.save()
        pdf_file.add_page(PyPDF2.PdfReader(open(filename, "rb")).pages[0])
        # output_file = open(filename, "wb") 
        # pdf_file.write(output_file)
        # output_file.close()
    pdf_bytes = io.BytesIO()
    pdf_file.write(pdf_bytes)
    return pdf_bytes.getvalue()