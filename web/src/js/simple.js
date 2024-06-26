"use strict";

window.onload = function(){

    // Input
    var catUrl = document.querySelector('.cat-url');

    // Buttons events
    var runCatBtn = document.querySelector('.run-cat-btn');
    var emptyCatBtn = document.querySelector('.empty-cat-btn');
    var weatherBtn = document.querySelector('.weather-btn');
    var weather1 = document.querySelector('.weather1');
    var weather2 = document.querySelector('.weather2');
    var weather3 = document.querySelector('.weather3');
    var weather4 = document.querySelector('.weather4');

    
    // Input 'Enter key' event
    catUrl.addEventListener("keydown", function(event) {
        if (event.keyCode == 13) {
            identityCat();
        }
    });
    
    runCatBtn.addEventListener("click", function(event) {
        identityCat();
    });

    weatherBtn.addEventListener("click", function(event) {
        getWeatherInfo();
    });
    
    emptyCatBtn.addEventListener("click", function(event) {
        catUrl.value = '';
        catUrl.focus();
    });
    
    // cat identification result from go-be-service
    async function identityCat() {
        var urlVal = catUrl.value;
    
        try{
            const response1 = await axios({
                method: 'post',
                url: 'http://localhost/web/cat', // in k8s ingress env
                // url: 'http://localhost:3001/web/cat', // in docker-compose env
                data: {
                    cat_url: urlVal,
                },
            });

            showCat(response1.data);
        } catch(error) {
            // console.error("Error calling /work/cat:", error);
            if (error.response) {
                console.log(error.response.data);
            }
        }
    }
    function showCat(data) {
        alert(JSON.stringify(data, null, 4));
    }

    async function getWeatherInfo() {
        try{
            const result = await axios({
                method: 'post',
                url: 'http://localhost/weather', // in k8s ingress env
                // url: 'http://localhost:3001/weather', // in docker-compose env
                // data: {
                // },
            });

            showWeather(result.data);
        } catch(error) {
            // console.error("Error calling /work/cat:", error);
            if (error.response) {
                console.log(error.response.data);
            }
        }
    }
    function showWeather(data) {
        data.weather_list.forEach((weather, index) => {
            var iconUrl = "https://openweathermap.org/img/wn/10d@" + weather.Weather[0].Icon + ".png"
            document.querySelector(`.weather${index + 1}`).textContent = weather.Name + " " + weather.Main.Temp + "°C, " + weather.Main.Humidity + "% "
            + `<img src="${iconUrl}">`;
        });
        weather1.textContent = data.weather_list[0].weather_info;
        weather2.textContent = data.weather_list[1].weather_info;
        weather3.textContent = data.weather_list[2].weather_info;
        weather4.textContent = data.weather_list[3].weather_info;
    }
    
    
    // Get references to the elements
    var runMnistBtn = document.querySelector('.run-mnist-btn');
    var emptyMnistBtn = document.querySelector('.empty-mnist-btn');

    runMnistBtn.addEventListener("click", identifyDigit);

    emptyMnistBtn.addEventListener("click", function() {
            // svcListInput.focus();
            console.log("empty draw board");
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
        console.log("draw the result,", data);
    }

    var cat_btn1 = document.querySelector('#cat_btn1');
    var cat_btn2 = document.querySelector('#cat_btn2');
    var noncat_btn1 = document.querySelector('#noncat_btn1');
    var noncat_btn2 = document.querySelector('#noncat_btn2');

    var cat_url1 = document.querySelector('#cat_url1');
    var cat_url2 = document.querySelector('#cat_url2');
    var noncat_url1 = document.querySelector('#noncat_url1');
    var noncat_url2 = document.querySelector('#noncat_url2');

    cat_btn1.addEventListener("click", function(event) {
        copyToClipboard("cat_url1");
    });
    cat_btn2.addEventListener("click", function(event) {
        copyToClipboard("cat_url2");
    });
    noncat_btn1.addEventListener("click", function(event) {
        copyToClipboard("noncat_url1");
    });
    noncat_btn2.addEventListener("click", function(event) {
        copyToClipboard("noncat_url2");
    });


    cat_url1.addEventListener("click", function(event) {
        copyToClipboard("cat_url1");
    });
    cat_url2.addEventListener("click", function(event) {
        copyToClipboard("cat_url2");
    });
    noncat_url1.addEventListener("click", function(event) {
        copyToClipboard("noncat_url1");
    });
    noncat_url2.addEventListener("click", function(event) {
        copyToClipboard("noncat_url2");
    });


    function copyToClipboard(id) {
        var textToCopy = document.getElementById(id).innerText.trim();
        navigator.clipboard.writeText(textToCopy).then(function() {
                // console.log('Copying to clipboard was successful!');
        }, function(err) {
                console.error('Could not copy text: ', err);
        });
    }

}
