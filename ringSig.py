from pysolcrypto.aosring import *

def key_generate():
    (_, (pk, sk)) = aosring_randkeys(1)
    return (pk, sk)

def generate_sign(pkeys, mypair, msg):
    return aosring_sign(pkeys=pkeys, mypair=mypair, tees=[_ for _ in range(len(pkeys))] , alpha=100, message=msg)

def ring_check(proof, msg):
    return aosring_check(*proof, message=msg)



def generate_update_data(pkeys, mykeys, msg):

    # print(pkeys)
    # print(mykeys)
    # print(msg)

    proof = generate_sign(pkeys, mykeys, msg)       # 生成环签名
    check = ring_check(proof, msg)                  # 验证签名
    assert check

    pubkeys = ([item.n for sublist in proof[0] for item in sublist])
    tees = (proof[1])				# tees
    seeds = (proof[2]) 				# seed
    message = (msg)						# msg

    return (pubkeys, tees, seeds, message)


if __name__ == '__main__':
    mykeys = key_generate()  # 生成个人用户
    msg = 12345  # 待签名消息

    pkeys = []
    for i in range(3):
        (_pk, _sk) = key_generate()
        pkeys.append(_pk)
    pkeys.append(mykeys[0])

    (pubkeys, tees, seeds, message) = generate_update_data(pkeys=pkeys, mykeys=mykeys, msg=msg)

    pk = [(10808862739180240800625244685433171639772449921935357866815394786361315289335, 20021672719867850588203001376841722588490485674755015289306384856892627625339), (15280758219306493573997656506818841667164983279631582322120951117019968948414, 288654710244974768920740254915893179347133791174751210156287377856034254384), (5967268979977893754247247649668884967124721978048270265259601081811590517274, 14895844367297769825803767762528880474589796227926679722428180091060670200708), (10078008779988595446595994499252126191520664684821107384959087630529805074513, 15519247598148863439940584221092305285861625177188421719245933055240615060021)]
    sk = ((10078008779988595446595994499252126191520664684821107384959087630529805074513, 15519247598148863439940584221092305285861625177188421719245933055240615060021), 2127284665741882271136116082539280607887375868157977618800864247319744403493)

    msg = msg

    generate_sign(pk, sk, msg)
    # print(generate_update_data(pkeys, mykeys, msg))
