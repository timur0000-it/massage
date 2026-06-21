function getCookie(name){
    const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')
    return m ? decodeURIComponent(m.pop()) : ''

}

csrftoken = getCookie('csrftoken')
all_buttons = document.querySelectorAll('.btn')

all_buttons.forEach(btn => {
    btn.addEventListener('click', () => {
        
        const url = btn.dataset.url;
        console.log("Sending request to:", url)
        const messsage = document.getElementById('message')
        
        btn.disabled = true;
        fetch(url, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken}
        })
        .then(resp => {
            if (!resp) 
                {return 0}
            else {return resp.json()}
        })
            .then(json => {
                if (!json.status){
                    return 0
                }
                else if(json.status === 'ok' ){
                     const course_id = json.course_id
                     console.log(course_id);
                        const course = document.getElementById(`${course_id}`)
                        console.log(course);
                        course.remove()
                        messsage.textContent = ''  
                }
                else if(json.status === 'have'){
                    const course_id = json.course_id
                    messsage.textContent = 'Уже есть в корзине'
                 
                }
                else{
                    console.log(json.status);
                    messsage.textContent = 'Что то пошло не так'
                    return 0
                }
                    
            })
        .finally(()=> {btn.disabled = false})
    })
});
