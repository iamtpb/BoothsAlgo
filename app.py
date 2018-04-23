from flask import Flask, request, render_template

app = Flask(__name__)


def twos_complement(n):
    n2c = []
    flip = False
    for i in n[::-1]:
        if flip:
            if i == '0':
                n2c.append('1')
            else:
                n2c.append('0')
        else:
            n2c.append(i)
            if i == '1':
                flip = True
    return "".join(n2c[::-1])


def get_binary_and_2c(n, nbits=16):
    if (n > 0):
        bn = bin(n)[2:].zfill(nbits)
        bn2c = twos_complement(bn)
    else:
        bn2c = bin(-1 * n)[2:].zfill(nbits)
        bn = twos_complement(bn2c)
    return bn, bn2c


def apply_booths(a, b, q, m, m2c, nbits):
    for i in range(nbits):
        if b[-1] + q == '10':
            a = bin(int(a, 2) + int(m2c, 2))[2:].zfill(nbits)[-nbits:]
        if b[-1] + q == '01':
            a = bin(int(a, 2) + int(m, 2))[2:].zfill(nbits)[-nbits:]
        # asr
        q = b[-1]
        b = a[-1] + b[:-1]
        a = a[0] + a[:-1]

    return a + b


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=["POST"])
def booths_mul():
    nbits = 16
    n1 = int(request.form['n1'])
    n2 = int(request.form['n2'])
    # n1 -> multiplicand, n2 -> multiplier
    m, m2c = get_binary_and_2c(n1, nbits)
    b, b2c = get_binary_and_2c(n2, nbits)
    q = '0'
    a = '0' * nbits

    ans = apply_booths(a, b, q, m, m2c, nbits)

    if (ans[0] == '1'):
        # negative number
        ans2c = twos_complement(ans)
        ans = -1 * int(ans2c, 2)
        op = "" + str(n1) + " x " + str(n2) + " = " + str(ans)
        return render_template('result.html', results=op)
    else:
        # positive number
        ans = int(ans, 2)
        op = "" + str(n1) + " x " + str(n2) + " = " + str(ans)
        return render_template('result.html', results=op)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)