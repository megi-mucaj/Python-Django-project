var updateBtns = document.getElementsByClassName('update-cart')

    for (i = 0; i<updateBtns.length; i++) {
        updateBtns[i].addEventListener('click', function(){
            var productId = this.dataset.product  //here we query atributes
            var action = this.dataset.action
            console.log('productId:', productId, 'action:', action)

            console.log('USER:', user)

            updateUserOrder(productId, action)



        })
    }

function updateUserOrder(productId, action){
    console.log("great")
   var url = '/update_Item/'
   //var url = {name: "update_Item"}
//Fetch is used to build POST request data, and post those data in url above
    fetch(url, {
        method:'POST',              //we pass in the data
        headers:{
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'X-CSRFToken':csrftoken,
        },

        body:JSON.stringify({'productId':productId, 'action':action})  //posting data in  backend
    })
    .then((response) => {           //we get the response turned into Json value
       return response.json()
    })
    .then((data) => {
        console.log('data', data)           //than we console it out, but Django wont let us //
        location.reload()                   //send this post request, so we have to take care of //
                                    //creating and sending a csrf_token.
                                    //To avoid this error we take CSRF TOKEN already done in google
    });

}






