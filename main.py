import codecs

file = codecs.open('files/CBR-837Aam274-288.txt', 'r', 'cp1251')
u = file.read()   # now the contents have been transformed to a Unicode string
out = codecs.open('files/CBR-837Aam274-288-UTF8.txt', 'w', 'utf-8')
out.write(u)   # and now the contents have been output as UTF-8

with open('files/CBR-837Aam274-288-UTF8.txt') as file:
    words = [word for line in file for word in line.split()]
    print(words)