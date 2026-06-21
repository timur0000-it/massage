
const testCreation = document.getElementById("test_form")

testCreation.addEventListener("submit", (e) => {
    e.preventDefault()
    
    console.log("Отправлен сабмит");
    const allAnswers = document.querySelectorAll('.answers');
    const title = document.querySelector('.title');
    const errorDiv = document.getElementById("error-message");
    errorDiv.innerHTML = ""
    let hasErrors = false; 
    let count = 0
    if(title.value === ''){
        errorDiv.innerHTML = `Внимание! Вы не заполнили название теста.Пожалуйста заполните`;
        title.style.borderColor = 'red'
        hasErrors = true;
    }
    else {
            title.style.borderColor = '';
    }
    allAnswers.forEach(input =>{
        if(input.value === ''){
            count +=1
            input.style.borderColor = 'red'
        }
        else {
            input.style.borderColor = ''; // Сбрасываем цвет, если поле заполнили
        }
    })
    if(count !== 0){
        hasErrors = true
        if(errorDiv.innerHTML !== ''){
            errorDiv.innerHTML += "<br> Внимание! Вы не заполнили все вопросы. Заполните оставшиеся."
            
        }
        else{
            errorDiv.innerHTML = `Внимание! Вы не заполнили все вопросы. Заполните оставшиеся.`
           
        }
    }
    if(hasErrors){
        return
    }
    else{
        testCreation.submit()
    }
    
    
})

