'use strict';


window.onload = function(){
	var catUrl = document.querySelector('.cat-url')
	var runCatBtn = document.querySelector('.run-cat-btn')
	var emptyCatBtn = document.querySelector('.empty-cat-btn')
	
	// 검색버튼클릭 또는 엔터키
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
				url: '/work/cat',
				data: {
					cat_url: url
				}
			});

			showCat(response1.data)
		} catch(error) {
			console.error("Error calling /work/cat:", error);
		}
	}
	function showCat(data) {
		console.log("draw the result,", data)
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
					const response2 = await axios.post("/work/mnist", {
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


}





