try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO

import os
import re
import argparse
from PyPDF2 import PdfFileReader, PdfFileWriter

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color

def write_files_to_output(directory, output_path):

    output = PdfFileWriter()

    for file in os.listdir(directory):
        # build the path
        path = os.path.join(directory, file)
        # check whether it is a directory
        if os.path.isdir(path):
            print(file)


            # iterate over the folders in this folder
            for inner_file in os.listdir(path):
                path_1 = os.path.join(path, inner_file)
                if os.path.isdir(path_1):
                    for pdf_file in os.listdir(path_1):
                        # get the PDF
                        if pdf_file.endswith(".pdf"):
                            # build the path to the PDF
                            path_inner = os.path.join(path_1, pdf_file)
                            file_to_pdf = open(path_inner, 'rb')

                            # read the PDF in
                            existing_pdf = PdfFileReader(file_to_pdf)

                            #  number = pdf_file.split('_')[0]

                            # search for a student number in the file name
                            pattern = re.compile('[sS]\d{7}')
                            result = pattern.search(pdf_file)
                            if result is None:
                                # search the first page of the file
                                page = existing_pdf.getPage(0)

                                page_content = page.extractText()
                                result = pattern.search(page_content)

                            number = result.group(0) if result is not None else '0'

                            # concatenate
                            version_student = str(file) + '_' + str(number)
                            # create the canvas with the watermark on it
                            packet = BytesIO()
                            # create a new PDF with Reportlab
                            can = canvas.Canvas(packet, pagesize=A4)
                            # shift about the canvas to have it start at the middle of the page
                            # can.translate(A4[0] / 2, A4[1] / 2)
                            # can.rotate(45)
                            # shift it back
                            # can.translate(- A4[0] / 2, - A4[1] / 2)

                            can.setFillColor(Color(0,50,100,alpha=0.5))
                            #0.5,0.5,0.5)
                            can.setFont("Helvetica",30)
                            x,y = can._pagesize
                            can.drawCentredString(x / 2 , 10, str(version_student))

                            can.save()

                            # move to the beginning of the StringIO buffer
                            packet.seek(0)
                            new_pdf = PdfFileReader(packet)


                            # iterate over all pages

                            nPages = existing_pdf.getNumPages()
                            even = nPages % 2 == 0
                            for i in range(nPages):
                                # add the watermark every page here
                                page = existing_pdf.getPage(i)
                                # this is where the watermark is added
                                page.mergePage(new_pdf.getPage(0))
                                # add the page to the output
                                output.addPage(page)
                            if not even:
                                # add a blank A4 page
                                output.addBlankPage(210, 297)

                            print(path_inner)
                else:
                    continue

                # pick out the PDF
        else:
            continue

    file_output = open(output_path, "wb")
    output.write(file_output)
    file_output.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('source_directory',help='The root folder PDFs in which should be merged')
    parser.add_argument('file_name', default='output.pdf')
    args = parser.parse_args()
    # the target path for the PDF
    output_path = os.path.join(args.source_directory, args.file_name)
    # do the actual job
    write_files_to_output(args.source_directory, output_path)

