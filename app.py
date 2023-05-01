import json
import os
import time

import cv2
from web3 import Web3, HTTPProvider
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response
import secrets
from extension import db, cors
from models import User, PublicKeys, Tokens
from MyNFT import MyNFT
from Faucet import Faucet
from AOSRing import AOSRing
from imageDecoder import decode_image, encode_image
from lsh import vgg_lshash, Register
from ringSig import generate_update_data, key_generate
from watermark import watermark_gen, watermark_verify
from PIL import Image
import numpy as np

################################# 设置参数 ########################################
MINT_PRIZE = 1            # 注册花费

entroypoint = "http://localhost:7545"
truffleFile = './build/contracts/MyNFT.json'
contract_address = "0xe815c2C5C53EF453dF6456f523BC65dED0202505"
FaucetFile = './build/contracts/Faucet.json'
Faucet_address = "0x2C29699b620De2E3852bFB24e31bCfBe4F137E58"
RingSigFile = './build/contracts/AOSRing.json'
RingSig_address = '0xfC8C802B76D1f8F94b2892C67De2C8f3D81d6Ed2'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:7b5b2e4afcb3e1ff30de9780ee3f05ac28cc12fa@127.0.0.1:3307/webUsers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
cors.init_app(app)



# 初始化
@app.cli.command()
def create():
    '''
    初始化flask
    :return:
    '''
    db.drop_all()
    db.create_all()
    for i in range(30):
        name = 'test' + str(i)
        password = 'test123'
        User.register(name, password)
        PublicKeys.register(name)
    Tokens.add(0)
    # print(PublicKeys.getRandomKeys())

#################################### 页面渲染 ###############################################
@app.route('/')
def index():
    if session.get('name') is None:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/buttons')
def buttons():
    return render_template('buttons.html', name=session.get('name'))

@app.route('/dropdowns')
def dropdowns():
    return render_template('dropdowns.html', name=session.get('name'))

@app.route('/typography')
def typography():
    return render_template('typography.html', name=session.get('name'))

@app.route('/basic_elements')
def basic_elements():
    return render_template('basic_elements.html', name=session.get('name'))

@app.route('/chartjs')
def chartjs():
    return render_template('chartjs.html', name=session.get('name'))

@app.route('/basic-table')
def basic_table():
    return render_template('basic-table.html', name=session.get('name'))

@app.route('/mdi')
def mdi():
    return render_template('mdi.html', name=session.get('name'))

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method=='POST':
        name = request.form.get('name')
        password = request.form.get('password')
        res = User.login(name, password)
        if res==False:
            print('login error!')
            return redirect(url_for('error_404'))
        else :
            session['name'] = name
            session['account'] = User.getAccount(name)
            session['publicKey'] = PublicKeys.getPublicKey(name)
            session['privateKey'] = PublicKeys.getPrivateKey(name)
            print(session)
            return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    if request.method=='POST':
        name = request.form.get('name')
        password = request.form.get('password')
        res = User.register(name, password)
        if res==False:
            print('register error!')
            return redirect(url_for('error_404'))
        else:
            PublicKeys.register(name)
            return redirect(url_for('login'))

@app.route('/error-404')
def error_404():
    return render_template('error-404.html')

@app.route('/error-500')
def error_500():
    return render_template('error-500.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

#################################### 前后端交互 ###############################################
@app.route('/ajax/name')
def getName():
    return session.get('name')

@app.route('/ajax/account')
def getAccount():
    return session.get('account')

@app.route('/ajax/pk')
def getpk():
    return str(session.get('publicKey'))

@app.route('/ajax/sk')
def getsk():
    return str(session.get('privateKey'))


@app.route('/ajax/balance')
def getBalance():
    # web3 = Web3(HTTPProvider(entroypoint))
    # balance = web3.eth.getBalance(session.get('account'))
    return redirect(url_for('get_balance'))

@app.route('/ajax/tokenNum')
def getTokenNum():
    return redirect(url_for('balanceOf'))

@app.route('/ajax/similar', methods=['POST'])
def getSimilar():
    data = json.loads(request.form.get("data"))
    img_base64 = data['img_base64']
    filename = decode_image(img_base64)
    (res, flag) = vgg_lshash(filename, 4, 16)

    msg = {
        'flag': flag,
        'data': None,
        'watermark': None,
    }

    if flag:
        print('image found!')
        msg['data'] = encode_image(res)

        zero_watermark = np.load(res+'_zero_watermark.npy')
        watermark_01 = np.load(res + '_watermark_01.npy')

        NC, ber, watermark_retrieved = watermark_verify(Image.open(open(filename, 'rb')), zero_watermark, watermark_01)
        print("normalized correlation=", NC)
        print("bit error ratio=", ber)

        retval, im_at_fixed = cv2.threshold(watermark_retrieved, 0.5, 255, cv2.THRESH_BINARY)
        cv2.imwrite('watermark.jpg', im_at_fixed)
        watermark_retrieved_base64 = encode_image('watermark.jpg')
        os.remove('watermark.jpg')

        msg['watermark'] = watermark_retrieved_base64
        os.remove(filename)

    else:
    #     Register(filename, res)
        msg['res'] = 'image not found!'
        os.remove(filename)
        print('image not found!')
    return jsonify(msg)


#################################### 区块链交互 ###############################################
@app.route("/mint", methods=['POST'])
def mint():
    #
    data = json.loads(request.form.get("data"))
    img_base64 = data['img_base64']
    watermark_base64 = data['watermark_base64']

    img_filename = decode_image(img_base64)
    wm_filename = decode_image(watermark_base64)


    (res, flag) = vgg_lshash(img_filename, 4, 16)
    if flag:
        print('image found!')
        os.remove(img_filename)
        data = encode_image(res)
        res = {'data': data}
        return jsonify(res)
    else:
        Register(img_filename, res)
        # msg['res'] = 'image not found!'

        original_img = Image.open(open(img_filename, 'rb'))
        watermark_img = Image.open(open(wm_filename, 'rb'))

        zero_watermark, watermark_01 = watermark_gen(original_img, watermark_img)
        np.save(img_filename + '_zero_watermark.npy', np.array(zero_watermark))
        np.save(img_filename + '_watermark_01.npy', np.array(watermark_01))

        retval, im_at_fixed = cv2.threshold(zero_watermark, 0.5, 255, cv2.THRESH_BINARY)
        cv2.imwrite('watermark.jpg', im_at_fixed)
        zero_watermark_base64 = encode_image('watermark.jpg')
        os.remove('watermark.jpg')

        res = {'data': None}
        res['data'] = zero_watermark_base64


    ###########################################################################################################
        message = {
            'name': session.get('name'),
            'account': session.get('account'),
            'function': 'MyNFT.mint',
            'data': {
                img_base64,
                watermark_base64,
            }
        }
        msg = abs(hash(str(message)))

        if Verify(msg) == False:
            return redirect(url_for('error_404'))

        myNFT = MyNFT(entroypoint, truffleFile, contract_address, session.get('name'), session.get('account'))
        address = session.get('account')
        if (Web3.isAddress(address) == False):
            return redirect(url_for('error_404'))

        value = MINT_PRIZE
        value = Web3.toWei(value, 'ether')

        token_id = Tokens.getMax()
        # print(token_id)
        myNFT.mint(address, token_id, value)
        Tokens.add(token_id + 1)

        # return redirect(url_for('index'))

        return jsonify(res)

@app.route("/burn")
def burn():
    pass

@app.route("/isApprovedForAll")
def isApprovedForAll():
    pass

@app.route("/supportsInterface")
def supportsInterface():
    pass

@app.route("/ajax/ownerOf", methods=['POST'])
def ownerOf():
    myNFT = MyNFT(entroypoint, truffleFile, contract_address, session.get('name'), session.get('account'))
    # print(request.data)
    data = json.loads(request.form.get("data"))
    id = data['id']
    id = int(id)
    # print(id)
    try:
        owner = myNFT.ownerOf(id)
        res = {
            'owner': owner
        }

        return jsonify(res)
    except ValueError as e:
        # return redirect(url_for('error_404'))
        res = {
            'owner': 'null'
        }
        return jsonify(res)

@app.route("/balanceOf")
def balanceOf():
    myNFT = MyNFT(entroypoint, truffleFile, contract_address, session.get('name'), session.get('account'))
    address = session.get('account')
    res = myNFT.balanceOf(address)
    return str(res)

@app.route("/setApprovalForAll")
def setApprovalForAll():
    pass

@app.route("/approve")
def approve():
    pass

@app.route("/getApproved")
def getApproved():
    pass

@app.route("/transferFrom", methods=['POST'])
def transferFrom():
    message = {
        'name': session.get('name'),
        'account': session.get('account'),
        'function': 'MyNFT.transferFrom',
        'data': {
            'src': session.get('account'),
            'dst': request.form.get('target_address'),
        }
    }
    msg = abs(hash(str(message)))

    if Verify(msg) == False:
        return redirect(url_for('error_404'))

    myNFT = MyNFT(entroypoint, truffleFile, contract_address, session.get('name'), session.get('account'))
    # myNFT = session.get('myNFT')
    _from = session.get('account')
    to = request.form.get("target_address")

    if (Web3.isAddress(_from) == False | Web3.isAddress(to) == False):
        return redirect(url_for('error_404'))

    id = request.form.get("token_id")
    id = int(id)
    try:
        myNFT.transferFrom(_from, to, id)
    except ValueError as e:
        return redirect(url_for('error_404'))

    return redirect(url_for('index'))

@app.route("/safeTransferFrom")
def safeTransferFrom():
    pass

@app.route("/safeTransferFromWithData")
def safeTransferFromWithData():
    pass

@app.route("/faucet")
def get_eth():
    faucet = Faucet(entroypoint, FaucetFile, Faucet_address, session.get('name'))

    # amount = request.form.get('amount')
    amount = 0.1
    amount = Web3.toWei(amount, 'ether')
    faucet.withdraw(amount, session.get('account'))

    myNFT = MyNFT(entroypoint, truffleFile, contract_address, session.get('name'), session.get('account'))
    balance = myNFT.get_balance()
    return redirect(url_for('index'))
    # return render_template("faucet.html", name=session.get('name'), account=session.get('account'), balance=balance)

@app.route("/get_balance")
def get_balance():
    web3 = Web3(HTTPProvider(entroypoint))
    balance = web3.eth.getBalance(session.get('account'))
    balance = Web3.fromWei(balance, 'ether')
    return str(balance) + 'ether'

def Verify(msg):
    aosRing = AOSRing(entroypoint, RingSigFile, RingSig_address, session.get('name'))

    mykeys = key_generate()  # 生成个人用户
    # msg = 12345  # 待签名消息

    pkeys = []
    for i in range(3):
        (_pk, _sk) = key_generate()
        pkeys.append(_pk)
    pkeys.append(mykeys[0])

    (pubkeys, tees, seeds, message) = generate_update_data(pkeys=pkeys, mykeys=mykeys, msg=msg)


    flag = aosRing.Verify(pubkeys, tees, seeds, message)
    return flag


#####################################################################################
if __name__ == '__main__':
    secret = secrets.token_urlsafe(32)
    app.secret_key = secret
    app.run(host='0.0.0.0', debug=True)
