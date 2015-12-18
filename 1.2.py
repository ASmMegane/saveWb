import urllib2, re, urllib, os


def saveContent(cnt,name, address, number):
    try:
        Content = urllib2.urlopen(cnt).read()
    except ValueError:
        return False
    try:
        out = open(name, 'wb')
        out.write(Content)
        out.close()
        os.chdir(address)
        return True
    except IOError:
        newName = 'unnamedFile-' + str(number)
        out = open(str(number) + '_' + newName, 'wb')
        out.write(Content)
        out.close()
        return False


def findeContent(countContent, contentForSave, address, content, url, regexpPatrn):
    i = 0
    for i in range(countContent):        
        startNameCont = contentForSave[i].rfind('/')
        startNameDir = contentForSave[i].find('/') + 1
        dirCont = address + contentForSave[i][startNameDir:startNameCont]
        if not(os.access(dirCont, os.W_OK )):
            a = os.makedirs(dirCont)        
        os.chdir(dirCont)    
        nameCont = contentForSave[i][startNameCont + 1:]
        if ((contentForSave[i][0] == '/' and contentForSave[i][1] == '/') or contentForSave[i][:5] == 'http:/'):
            rightContent = contentForSave[i]        
        elif (contentForSave[i][0] == '/'):
            rightContent = url + contentForSave[i][1:]
        else:            
            rightContent = contentForSave[i]
        if saveContent(rightContent, nameCont, address, i):
            flag = re.search(regexpPatrn, content)
            if not(flag == None):
                content = content.replace(contentForSave[i], 'file://' + dirCont + '/' + nameCont) 
    return content

url = 'http://lenta.ru/'
content = urllib2.urlopen(url).read()
image = re.findall('<img .*? src="(.*?)"', content)
script = re.findall('<script .*? src="(.*?)"', content)
link = re.findall('<link .*? href="(.*?)"', content)
address = os.path.abspath('1.2.py')
address = address[:-7] + '/'
countImg = len(image)
countScript = len(script)
countLink = len(link)

regexpPatrn =  '<link .*? href="(.*?)"'
content = findeContent(countLink, link, address, content, url, regexpPatrn)
regexpPatrn = '<img .*? src="(.*?)"'
content = findeContent(countImg, image, address, content, url, regexpPatrn)
regexpPatrn = '<script .*? src="(.*?)"'
content = findeContent(countScript, script, address, content, url, regexpPatrn)

os.chdir(address)
outFile = open('lenta.html', 'wb')
outFile.write(content)
outFile.close()
