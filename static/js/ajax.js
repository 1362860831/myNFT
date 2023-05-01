$.ajax({
  url: "http://127.0.0.1:5000/ajax/name",
  type: "get",
  success: function(msg) {
      var table_1_name = document.querySelector('#table_1_name');
      table_1_name.innerHTML = msg
      var sidebar_name = document.querySelector('#sidebar-name')
      sidebar_name.innerHTML = msg
      var top_name = document.querySelector('#top-name')
      top_name.innerHTML = msg
  }
})

$.ajax({
  url: "http://127.0.0.1:5000/ajax/pk",
  type: "get",
  success: function(msg) {
      var table_1_pk = document.querySelector('#table_1_pk');
      table_1_pk.innerHTML = msg
  }
})

$.ajax({
  url: "http://127.0.0.1:5000/ajax/sk",
  type: "get",
  success: function(msg) {
      var table_1_sk = document.querySelector('#table_1_sk');
      table_1_sk.innerHTML = msg
  }
})

$.ajax({
  url: "http://127.0.0.1:5000/ajax/account",
  type: "get",
  success: function(msg) {
      var table_1_account = document.querySelector('#table_1_account');
      table_1_account.innerHTML = msg
      var top_account = document.querySelector('#top-account')
      top_account.innerHTML = 'Your account on our chain is :' + msg
  }
})

$.ajax({
  url: "http://127.0.0.1:5000/ajax/balance",
  type: "get",
  success: function(msg) {
      var table_1_balance = document.querySelector('#table_1_balance');
      table_1_balance.innerHTML = msg
  }
})

$.ajax({
  url: "http://127.0.0.1:5000/ajax/tokenNum",
  type: "get",
  success: function(msg) {
      var table_1_tokenNum = document.querySelector('#table_1_tokenNum');
      table_1_tokenNum.innerHTML = msg
  }
})

function check_token_id() {
    var id = document.getElementById('token_id').value
    var data= {
        data: JSON.stringify({
            'id': id,
        }),
    }
    $.ajax({
      url: "http://127.0.0.1:5000/ajax/ownerOf",
      type: "post",
      data: data,
      dataType: 'json',
      success: function(msg) {
          console.log('ok')
          var owner = msg.owner
          var owner_of_token = document.querySelector('#owner_of_token');
          owner_of_token.innerHTML = owner
      }
    })
}

function check_similar_img() {
    var img_base64 = document.getElementById("similar_preview").getAttribute('src');
    var data= {
        data: JSON.stringify({
            'img_base64': img_base64,
        }),
    };
    $.ajax({
        url: "http://127.0.0.1:5000/ajax/similar" ,
        type: 'POST',
        data: data,
        dataType: 'json',
        success: function(msg) {
//            console.log(msg.res)
            if (msg.flag) {
                document.getElementById("similar_found").setAttribute('src', msg.data)
                document.getElementById("similar_watermark").setAttribute('src', msg.watermark)
            }
        }
    })
}

function mint() {
    var img_base64 = document.getElementById("image-preview").getAttribute('src');
    var watermark_base64 = document.getElementById("watermark-preview").getAttribute('src')
    var data= {
        data: JSON.stringify({
            'img_base64': img_base64,
            'watermark_base64': watermark_base64,
        }),
    };
    $.ajax({
        url: "http://127.0.0.1:5000/mint" ,
        type: 'POST',
        data: data,
        dataType: 'json',
        success: function(msg) {
            console.log(msg.data)
                document.getElementById("zero-watermark-preview").setAttribute('src', msg.data)
        }
    })
}