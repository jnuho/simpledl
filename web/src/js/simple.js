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
            // Make a POST request to the backend
            const response = await fetch('http://localhost/weather', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    // Add any required payload here if needed
                    // key: value
                })
            });
             // Check if the response is OK (status 200)
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            
            // Parse the JSON response
            const data = await response.json();

            // Get the weather list from the response
            const weatherList = data.weather_list;
        
            showWeather(weatherList);
        } catch(error) {
            // console.error("Error calling /work/cat:", error);
            if (error.response) {
                console.log(error.response.data);
            }
        }
    }
    function showWeather(weatherList) {
        alert(weatherList)
        // Iterate over the weather list using forEach and xtract the required elements
        weatherList.forEach(weather => {
            alert(weather)
            const name = weather.name;
            const temp = weather.main.temp;
            const humidity = weather.main.humidity;
            const icon = weather.weather[0].icon;
            
            // Do something with the extracted data
            console.log(`City: ${name}, Temperature: ${temp}, Icon: ${icon}`);

            var iconUrl = "https://openweathermap.org/img/wn/" + icon + ".png";
            document.querySelector(`.weather${index + 1}`).innerHTML = name + " " + temp + "°C, " + humidity + "% " + `<img src="${iconUrl}">`;
        });
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
