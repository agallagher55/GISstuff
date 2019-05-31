def read_pdf(pdf_file):
    import PyPDF2

    with open(pdf_file, 'rb') as pdf_obj:
        reader = PyPDF2.PdfFileReader(pdf_obj)

        if reader.isEncrypted:
            reader.decrypt('')

        num_pages = reader.numPages
        text = ""

        print "Reading '{}'".format(pdf_file)
        print "\tNumber of Pages: {}".format(num_pages)

        for i in range(num_pages):
            page_obj = reader.getPage(i)
            text += page_obj.extractText()

        print text
        return text


read_pdf(r"C:\Users\gallaga\Desktop\trafficcounts\17ATR390.pdf")

read_pdf(r"C:\Users\gallaga\Desktop\Essentials-Windows-CMD-Command-You-Should-Know-2.pdf")
