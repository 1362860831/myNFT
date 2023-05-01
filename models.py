from extension import db
from web3 import Web3, HTTPProvider
from werkzeug.security import check_password_hash, generate_password_hash
from ringSig import key_generate
import random

entroypoint = "http://localhost:7545"

class User(db.Model):
    __tablename__ = 'users'
    user_name = db.Column(db.String(255), primary_key=True, nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    user_account = db.Column(db.String(42), nullable=False)

    @staticmethod
    def register(name, password):
        '''
        注册一个用户并添加到数据库
        :param name:
        :param password:
        :return:
        '''

        if User.isExist(name):
            print('the name has been registered!')
            return False

        user = User()
        user.user_name = name

        w3 = Web3(HTTPProvider(entroypoint))
        acct = w3.geth.personal.newAccount(name)
        password_hash = generate_password_hash(password)

        user.user_password = password_hash
        user.user_account = acct

        db.session.add(user)
        db.session.commit()
        return True

    @staticmethod
    def isExist(name):
        return db.session.query(db.exists().where(User.user_name == name)).scalar()

    @staticmethod
    def login(name, password):
        if not User.isExist(name):
            print('the name has not been registered!')
            return False

        user = db.session.query(User).filter(User.user_name == name).one()


        if check_password_hash(user.user_password, password):
            return True
        else:
            print('the password is wrong!')
            return False

    @staticmethod
    def getAccount(name):
        user = db.session.query(User).filter(User.user_name == name).one()
        return user.user_account

class PublicKeys(db.Model):
    __tablename__ = 'publicKeys'
    user_name = db.Column(db.String(255), primary_key=True, nullable=False)
    user_privateKey = db.Column(db.String(255), nullable=False)
    user_publicKey = db.Column(db.String(255), nullable=False)

    @staticmethod
    def register(name):
        '''
        注册一个用户的环签名公钥
        :param name:
        :param publicKey:
        :return:
        '''

        if PublicKeys.isExist(name):
            print('the name has been registered!')
            return False

        user = PublicKeys()
        user.user_name = name
        (pk,sk) = key_generate()
        user.user_publicKey = str(pk)
        user.user_privateKey = str(sk)

        db.session.add(user)
        db.session.commit()
        return True

    @staticmethod
    def getPublicKey(name):
        user = db.session.query(PublicKeys).filter(PublicKeys.user_name == name).one()
        strs = user.user_publicKey.replace('(',"").replace(')',"").replace(' ',"").split(',')
        res = []
        for str in strs:
            res.append(int(str))
        res = tuple(res)
        # print(res)
        return res

    @staticmethod
    def getPrivateKey(name):
        user = db.session.query(PublicKeys).filter(PublicKeys.user_name == name).one()
        return int(user.user_privateKey)

    @staticmethod
    def getRandomKeys():
        users = db.session.query(PublicKeys).all()
        users = random.sample(users, 4)
        res = []
        for user in users:
            res.append(PublicKeys.getPublicKey(user.user_name))
        return res


    @staticmethod
    def isExist(name):
        return db.session.query(db.exists().where(PublicKeys.user_name == name)).scalar()

class Tokens(db.Model):
    __tablename__ = 'tokens'
    token_id = db.Column(db.Integer(), nullable=False, primary_key=True)

    @staticmethod
    def getMax():
        return db.session.query(db.func.max(Tokens.token_id)).scalar()

    @staticmethod
    def add(token_id):
        token = Tokens()
        token.token_id = token_id
        db.session.add(token)
        db.session.commit()

