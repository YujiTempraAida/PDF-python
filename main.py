import io
import PyPDF2
from PyPDF2 import PageObject
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm

# ページ中心からみたテキストボックス左上の座標
PAGE_X = 70 * mm
PAGE_Y = 0 * mm

# 入力するテキスト
PAGE_INPUTTEXT = '''
全ての試合が終わったら昼休憩になります。

会場のPCやタブレットから結果入力にご協力ください。

推奨進行順
※必ずこの通りに進行する必要はありませんが、
効率よく進行することが出来る順番の一つです。

1. Winners Round 1
2. Winners Round 2
3. Losers Round 1
4. Losers Round 2
5. Winners Round 3
6. Losers Round 4
7. Winners Round 3 & Losers Round 5

'''

inputTextList = PAGE_INPUTTEXT.splitlines()

# フォント登録 - 源真ゴシック（ http://jikasei.me/font/genshin/）
GEN_SHIN_GOTHIC_LIGHT_TTF = "./fonts/GenShinGothic-Light.ttf"
pdfmetrics.registerFont(TTFont('GenShinGothic-Light', GEN_SHIN_GOTHIC_LIGHT_TTF))
FONTSIZE = 8

# 既存PDFにテキストを追加する
def add_text(input_file: str, output_file: str):
    # 既存PDF（テキストを追加するPDF）
    fi = open(input_file, 'rb')
    pdf_reader = PyPDF2.PdfReader(fi)
    pages_num = len(pdf_reader.pages)

    # テキストを追加したPDFの書き込み用
    pdf_writer = PyPDF2.PdfWriter()

    # テキストだけのPDFをメモリ（binary stream）に作成
    bs = io.BytesIO()
    c = canvas.Canvas(bs)
    for i in range(0, pages_num):
        # 既存PDF
        pdf_page = pdf_reader.pages[i]
        # PDFページのサイズ
        page_size = get_page_size(pdf_page)
        # テキストのPDF作成
        add_text_pdf(c, page_size, inputTextList)
    c.save()

    # テキストだけのPDFをメモリから読み込み（seek操作はPyPDF2に実装されているので不要）
    pdf_num_reader = PyPDF2.PdfReader(bs)

    # 既存PDFとテキストだけのPDFのマージ
    for i in range(0, pages_num):
        # 既存PDF
        pdf_page = pdf_reader.pages[i]
        # ページ番号だけのPDF
        pdf_num = pdf_num_reader.pages[i]

        # ２つのPDFを重ねる
        pdf_page.merge_page(pdf_num)
        pdf_writer.add_page(pdf_page)

    # マージしたPDFを保存
    fo = open(output_file, 'wb')
    pdf_writer.write(fo)

    bs.close()
    fi.close()
    fo.close()

# テキストだけのPDFを作成
def add_text_pdf(c: canvas.Canvas, page_size: tuple, textList: list):
    c.setPageSize(page_size)
    c.setFont("GenShinGothic-Light", FONTSIZE)

    # 1行ずつ記述
    counter = 0
    for i in textList:
        c.drawString(PAGE_X + page_size[0] / 2.0, PAGE_Y- (FONTSIZE + 1) * counter + page_size[1] / 2.0, i)
        counter += 1

    c.showPage()

# 既存PDFからページサイズ（幅, 高さ）を取得する
def get_page_size(page: PageObject) -> tuple:
    page_box = page.mediabox
    width = page_box.width
    height = page_box.height
    return float(width), float(height)


if __name__ == '__main__':
    # テスト用
    infile = 'input.pdf'
    outfile = 'output.pdf'
    add_text(infile, outfile)