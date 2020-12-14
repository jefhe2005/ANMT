'''
a="987654321"
b=""
def rev(a,l):
    global b
    if l==1:
        b = b + a[-l]
        return
    rev(a,l-1)
    b=b+a[-l]
    return b
print(rev(a,len(a)))
'''

