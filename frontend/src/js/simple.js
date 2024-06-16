'use strict';

window.onload = function(){

  // Input
  var catUrl = document.querySelector('.cat-url')

  // Buttons events
  var runCatBtn = document.querySelector('.run-cat-btn')
  var emptyCatBtn = document.querySelector('.empty-cat-btn')
  
  // Input 'Enter key' event
  catUrl.addEventListener("keydown", function(event) {
    if (event.keyCode == 13) {
      identityCat()
    }
  });
  
  runCatBtn.addEventListener("click", function(event) {
    identityCat();
  });
  
  emptyCatBtn.addEventListener("click", function(event) {
    catUrl.value = '';
    catUrl.focus();
  });
  
  // ECS 클러스터 리스트 조회
  async function identityCat() {
    var url = catUrl.value;
  
    try{
      const response1 = await axios({
        method: 'post',
        url: 'http://localhost:8080/web/cat', // in k8s ingress env
        // url: 'http://localhost:3001/web/cat', // in docker-compose env
        data: {
          cat_url: url
        },
      });

      showCat(response1.data)
    } catch(error) {
      // console.error("Error calling /work/cat:", error);
      if (error.response) {
        console.log(error.response.data)
      }
    }
  }
  function showCat(data) {
    alert(JSON.stringify(data, null, 4))
  }
  
  
  // Get references to the elements
  var runMnistBtn = document.querySelector('.run-mnist-btn');
  var emptyMnistBtn = document.querySelector('.empty-mnist-btn');

  runMnistBtn.addEventListener("click", identifyDigit);

  emptyMnistBtn.addEventListener("click", function() {
      // svcListInput.focus();
      console.log("empty draw board")
  });

  // Function to get the service list
  async function identifyDigit() {
      var digit = "";

      try {
          const response2 = await axios.post("http://localhost/web/mnist", { // in k8s ingress env
          // const response2 = await axios.post("http://localhost:3001/web/mnist", { // in docker-compose env
              drawn_digit: digit
          });

          showDigit(response2.data);
      } catch (error) {
          console.error(error);
      }
  }

  function showDigit(data) {
    console.log("draw the result,", data)
  }

  var cat_btn1 = document.querySelector('#cat_btn1')
  var cat_btn2 = document.querySelector('#cat_btn2')
  var cat_btn3 = document.querySelector('#cat_btn3')
  var noncat_btn1 = document.querySelector('#noncat_btn1')
  var noncat_btn2 = document.querySelector('#noncat_btn2')
  var noncat_btn3 = document.querySelector('#noncat_btn3')

  var cat_url1 = document.querySelector('#cat_url1')
  var cat_url2 = document.querySelector('#cat_url2')
  var cat_url3 = document.querySelector('#cat_url3')
  var noncat_url1 = document.querySelector('#noncat_url1')
  var noncat_url2 = document.querySelector('#noncat_url2')
  var noncat_url3 = document.querySelector('#noncat_url3')

  cat_btn1.addEventListener("click", function(event) {
    copyToClipboard("cat_url1");
  });
  cat_btn2.addEventListener("click", function(event) {
    copyToClipboard("cat_url2");
  });
  cat_btn3.addEventListener("click", function(event) {
    copyToClipboard("cat_url3");
  });
  noncat_btn1.addEventListener("click", function(event) {
    copyToClipboard("noncat_url1");
  });
  noncat_btn2.addEventListener("click", function(event) {
    copyToClipboard("noncat_url2");
  });
  noncat_btn3.addEventListener("click", function(event) {
    copyToClipboard("noncat_url3");
  });


  cat_url1.addEventListener("click", function(event) {
    copyToClipboard("cat_url1");
  });
  cat_url2.addEventListener("click", function(event) {
    copyToClipboard("cat_url2");
  });
  cat_url3.addEventListener("click", function(event) {
    copyToClipboard("cat_url3");
  });
  noncat_url1.addEventListener("click", function(event) {
    copyToClipboard("noncat_url1");
  });
  noncat_url2.addEventListener("click", function(event) {
    copyToClipboard("noncat_url2");
  });
  noncat_url3.addEventListener("click", function(event) {
    copyToClipboard("noncat_url3");
  });


  function copyToClipboard(id) {
    var textToCopy = document.getElementById(id).innerText.trim();
    navigator.clipboard.writeText(textToCopy).then(function() {
        // console.log('Copying to clipboard was successful!');
    }, function(err) {
        console.error('Could not copy text: ', err);
    });
  }

  /**const pasteButton = document.querySelector('.paste-btn')
  pasteButton.addEventListener('click', ()=> {
    const inputElement = document.querySelector('.cat-url')
    pasteClipboard(inputElement)
  });

  async function pasteClipboard(input) {
    const text = await navigator.clipboard.readText();
    input.value = text;
  }
  */

}





