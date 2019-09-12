from reportlab.platypus import (
    BaseDocTemplate, 
    PageTemplate, 
    Frame, 
    Paragraph, Spacer, Image
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm, cm
from reportlab.platypus.flowables import Image 
import os
from reportlab.pdfgen import canvas
from ReadingXML import *

#Font styles
styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']
styleT = styles['Title']



class PageNumCanvas(canvas.Canvas):
    """
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    """
 
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
 
    #----------------------------------------------------------------------
    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()
 
    #----------------------------------------------------------------------
    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)
 
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            self.draw_logo()
            canvas.Canvas.showPage(self)
 
        canvas.Canvas.save(self)
 
    #----------------------------------------------------------------------
    def draw_page_number(self, page_count):
        """
        Add the page number
        """
        page = "Page %s of %s" % (self._pageNumber, page_count)
        self.setFont("Helvetica", 9)
        self.drawRightString(195*mm, 10*mm, page)


    def draw_logo(self):
        '''
        This function adds the logo on each page
        '''
        logo = Image("NXP-Logo.png", 2*cm, 2*cm, kind='proportional')
        logo.drawOn(self, 180*mm, 280*mm)


def header_footer(canvas, doc): 
    '''
    This functions adds a header and a footer to a page
    '''
    canvas.saveState()
    text1 = '<font size=14>%s </font>' % full_name.split('.')[0]
    if len(number) > 0 : 
        cqc_number = "Customer Quality Complaint (CQC) Number : " + number
        text2 = '<font size=12>%s</font>' % cqc_number
        header = (Paragraph(text1+"<br/>"+text2, styleT))
    else:    
        A = "                       "
        text2 = '<font size=12>%s</font>' % A
        header = (Paragraph(text1+"<br/>"+text2, styleT))
    
    w, h = header.wrap(doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height+doc.topMargin+h/2)

    if len(comment) > 0 and len(comment) < 324 :
        footer= Paragraph("Comment(s) : "+comment,styleN)
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h+1*cm)

    canvas.restoreState()

    
def create_report(title, path_savefig, folder, index, comments, path_pdf, fig_number):
    '''
    This function creates a report without cqc number
    '''
    global full_name
    global comment
    global number
    global  repNum
    full_name = str(title)
    comment = str(comments)
    number = ''
    repNum = str(fig_number)
    doc = BaseDocTemplate(path_pdf+'\\'+title)
    if repNum == '28' :
        column_gap = 2 * cm
        doc.addPageTemplates(
            [
                PageTemplate(
                    frames=[
                        Frame(
                            doc.leftMargin,
                            1.5*cm+doc.bottomMargin,
                            doc.width / 4,
                            doc.height-0.5*cm,
                            id='left',
                            rightPadding=column_gap / 4,
                            showBoundary=0  # set to 1 for debugging
                        ),
                         Frame(
                            doc.leftMargin + doc.width / 4,
                            1.5*cm+doc.bottomMargin,
                            doc.width / 4,
                            doc.height-0.5*cm,
                            id='middle-left',
                            rightPadding=column_gap / 4,
                            leftPadding= column_gap / 4,
                            showBoundary=0
                        ),
                        Frame(
                            doc.leftMargin +0.1*cm+ 2*doc.width / 4,
                            1.5*cm+doc.bottomMargin,
                            doc.width / 4,
                            doc.height-0.5*cm,
                            id='middle-right',
                            rightPadding=column_gap / 4,
                            leftPadding= column_gap /4,
                            showBoundary=0
                        ),
                        Frame(
                            doc.leftMargin +0.1*cm+ 3*doc.width / 4,
                            1.5*cm+doc.bottomMargin,
                            doc.width / 4,
                            doc.height-0.5*cm,
                            id='right',
                            leftPadding=column_gap / 4,
                            showBoundary=0
                        ),
                    ],
                    onPage=header_footer
                ),
            ]
        )
        flowables = []
        files = os.listdir(path_savefig+folder)
        files.sort(key=natural_keys)
        if len(index) == 0:
            for ind, val in enumerate(files):
                flowables.append(Image(path_savefig+folder+"\\"+val, 4.5*cm, 4.5*cm, kind='proportional'))
        else:
            for ind2, val2 in enumerate(index):
                for ind, val in enumerate(files):
                    if val2.split('m_')[-1] in val :
                        flowables.append(Image(path_savefig+folder+"\\"+val, 4.5*cm, 4.5*cm, kind='proportional'))


    elif repNum == '15' :
        column_gap = 1.5 * cm
        doc.addPageTemplates(
            [
                PageTemplate(
                    frames=[
                        Frame(
                            doc.leftMargin,
                            2*cm+doc.bottomMargin,
                            doc.width / 3,
                            doc.height-1*cm,
                            id='left',
                            rightPadding=column_gap / 3,
                            showBoundary=0  # set to 1 for debugging
                        ),
                         Frame(
                            doc.leftMargin + doc.width / 3,
                            2*cm+doc.bottomMargin,
                            doc.width / 3,
                            doc.height-1*cm,
                            id='middle',
                            rightPadding=column_gap / 3,
                            leftPadding= column_gap /3,
                            showBoundary=0
                        ),
                        Frame(
                            doc.leftMargin + 2*doc.width / 3,
                            2*cm+doc.bottomMargin,
                            doc.width / 3,
                            doc.height-1*cm,
                            id='right',
                            leftPadding=column_gap / 3,
                            showBoundary=0
                        ),
                    ],
                    onPage=header_footer
                ),
            ]
        )
        flowables = []
        files = os.listdir(path_savefig+folder)
        files.sort(key=natural_keys)
        if len(index) == 0:
            for ind, val in enumerate(files):
                flowables.append(Image(path_savefig+folder+"\\"+val, 6*cm, 6*cm, kind='proportional'))
        else:
            for ind2, val2 in enumerate(index):
                for ind, val in enumerate(files):
                    if val2.split('m_')[-1] in val :
                        flowables.append(Image(path_savefig+folder+"\\"+val, 6*cm, 6*cm, kind='proportional'))
        
    else:
        column_gap = 2 * cm
        doc.addPageTemplates(
            [
                PageTemplate(
                    frames=[
                        Frame(
                            doc.leftMargin,
                            1*cm+doc.bottomMargin,
                            doc.width / 2,
                            doc.height,
                            id='left',
                            rightPadding=column_gap / 2,
                            showBoundary=0  # set to 1 for debugging
                      
                        ),
                        Frame(
                            doc.leftMargin + doc.width / 2,
                            1*cm+doc.bottomMargin,
                            doc.width / 2,
                            doc.height,
                            id='right',
                            leftPadding=column_gap / 2,
                            showBoundary=0
                        ),
                    ],
                    onPage=header_footer
                ),
            ]
        )
        flowables = []
        files = os.listdir(path_savefig+folder)
        files.sort(key=natural_keys)
        if len(index) == 0:
            for ind, val in enumerate(files):
                flowables.append(Image(path_savefig+folder+"\\"+val, 8*cm, 8*cm, kind='proportional'))
        else:
            for ind2, val2 in enumerate(index):
                for ind, val in enumerate(files):
                    if val2.split('m_')[-1] in val :
                        flowables.append(Image(path_savefig+folder+"\\"+val, 8*cm, 8*cm, kind='proportional'))
    doc.build(flowables, canvasmaker=PageNumCanvas)

def create_report_cqc(title, cqc_number, path_savefig, folder, index, comments, path_pdf, fig_number):
    '''
    This function creates a report with cqc number
    '''
    global full_name
    global comment
    global number
    global  repNum
    full_name = str(title)
    comment = str(comments)
    number = str(cqc_number)
    repNum = str(fig_number)
    doc = BaseDocTemplate(path_pdf+'\\'+title)
    

    if repNum == '28' :
        column_gap = 2 * cm
        
        doc.addPageTemplates(
            [
                PageTemplate(
                    frames=[
                        Frame(
                            doc.leftMargin,
                            1.5*cm+doc.bottomMargin,
                            doc.width / 4,
                            doc.height-0.5*cm,
                            id='left',
                            rightPadding=column_gap / 4,
                            showBoundary=0  # set to 1 for debugging
                        ),
                         Frame(
                            doc.leftMargin + doc.width / 4,
                            1.5*cm+doc.bottomMargin,
                            doc.width / 4,
                            doc.height-0.5*cm,
                            id='middle-left',
                            rightPadding=column_gap /4,
                            leftPadding= column_gap /4,
                            showBoundary=0
                        ),
                        Frame(
                            doc.leftMargin +0.1*cm+ 2*doc.width / 4,
                            1.5*cm+doc.bottomMargin,
                            doc.width / 4,
                            doc.height-0.5*cm,
                            id='middle-right',
                            rightPadding=column_gap / 4,
                            leftPadding= column_gap /4,
                            showBoundary=0
                        ),
                        Frame(
                            doc.leftMargin +0.1*cm+3*doc.width / 4,
                            1.5*cm+doc.bottomMargin,
                            doc.width / 4,
                            doc.height-0.5*cm,
                            id='right',
                            leftPadding=column_gap / 4,
                            showBoundary=0
                        ),
                    ],
                    onPage=header_footer
                ),
            ]
        )
        flowables = []
        files = os.listdir(path_savefig+folder)
        files.sort(key=natural_keys)
        if len(index) == 0:
            for ind, val in enumerate(files):
                flowables.append(Image(path_savefig+folder+"\\"+val, 4.5*cm, 4.5*cm, kind='proportional'))
        else:
            for ind2, val2 in enumerate(index):
                for ind, val in enumerate(files):
                    if val2.split('m_')[-1] in val :
                        flowables.append(Image(path_savefig+folder+"\\"+val, 4.5*cm, 4.5*cm, kind='proportional'))

    elif repNum == '15' :
        column_gap = 1.5 * cm
        
        doc.addPageTemplates(
            [
                PageTemplate(
                    frames=[
                        Frame(
                            doc.leftMargin,
                            2*cm+doc.bottomMargin,
                            doc.width / 3,
                            doc.height-1*cm,
                            id='left',
                            rightPadding=column_gap / 3,
                            showBoundary=0  # set to 1 for debugging
                        ),
                         Frame(
                            doc.leftMargin + doc.width / 3,
                            2*cm+doc.bottomMargin,
                            doc.width / 3,
                            doc.height-1*cm,
                            id='middle',
                            rightPadding=column_gap / 3,
                            leftPadding= column_gap /3,
                            showBoundary=0
                        ),
                        Frame(
                            doc.leftMargin + 2*doc.width / 3,
                            2*cm+doc.bottomMargin,
                            doc.width / 3,
                            doc.height-1*cm,
                            id='right',
                            leftPadding=column_gap / 3,
                            showBoundary=0
                        ),
                    ],
                    onPage=header_footer
                ),
            ]
        )
        flowables = []
        files = os.listdir(path_savefig+folder)
        files.sort(key=natural_keys)
        if len(index) == 0:
            for ind, val in enumerate(files):
                flowables.append(Image(path_savefig+folder+"\\"+val, 6*cm, 6*cm, kind='proportional'))
        else:
            for ind2, val2 in enumerate(index):
                for ind, val in enumerate(files):
                    if val2.split('m_')[-1] in val :
                        flowables.append(Image(path_savefig+folder+"\\"+val, 6*cm, 6*cm, kind='proportional'))
            
    else:
        column_gap = 2 * cm
        doc.addPageTemplates(
            [
                PageTemplate(
                    frames=[
                        Frame(
                            doc.leftMargin,
                            1*cm+doc.bottomMargin,
                            doc.width / 2,
                            doc.height,
                            id='left',
                            rightPadding=column_gap / 2,
                            showBoundary=0  # set to 1 for debugging
                        ),
                        Frame(
                            doc.leftMargin + doc.width / 2,
                            1*cm+doc.bottomMargin,
                            doc.width / 2,
                            doc.height,
                            id='right',
                            leftPadding=column_gap / 2,
                            showBoundary=0
                        ),
                    ],
                    onPage=header_footer
                ),
            ]
        )
        flowables = []
        files = os.listdir(path_savefig+folder)
        files.sort(key=natural_keys)
        if len(index) == 0:
            for ind, val in enumerate(files):
                flowables.append(Image(path_savefig+folder+"\\"+val, 8*cm, 8*cm, kind='proportional'))
        else:
            for ind2, val2 in enumerate(index):
                for ind, val in enumerate(files):
                    if val2.split('m_')[-1] in val :
                        flowables.append(Image(path_savefig+folder+"\\"+val, 8*cm, 8*cm, kind='proportional'))
            


    doc.build(flowables, canvasmaker=PageNumCanvas)

   