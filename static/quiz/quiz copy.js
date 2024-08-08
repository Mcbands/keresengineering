console.log("Hello World Quiz")
const url = window.location.href
// console.log(url)
const quizBox = document.getElementById('quiz-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const timertBox = document.getElementById('timer-box')
// let data

const activateTimer = (time) => {
    if (time.toString().length < 2) {
        timertBox.innerHTML = `<b>0${time}:00</b>`
       }
        else{
         timertBox.innerHTML = `<b>${time}:00</b>`

        }

        let minutes = time - 1
        let seconds = 60
        let displaySeconds
        let displayMinutes

        const timer = setInterval(()=>{
           seconds --
           if(seconds < 0){
            seconds = 59
            minutes --
           }

           if(minutes.toString().length < 2){
             displayMinutes = "0"+minutes
           } else{
            displayMinutes = minutes 
           }

           if(seconds.toString().length < 2){
            displaySeconds = "0"+ seconds
          } else{
           displaySeconds = seconds 
          }

          if(minutes === 0 && seconds === 0){
           timertBox.innerHTML = "<b>00:00</b>"
            setTimeout(()=>{
                clearInterval(timer)
                alert("Timer Over")
                sendData()

            }, 500)
          }

          timertBox.innerHTML = `<b>${displayMinutes}:${displaySeconds} </b>`

        }, 1000)

}





$.ajax({
    type: 'GET',
    url: `${url}data`,
    success: function(response){
        // console.log(response);
        const data = response.data
        data.forEach(el => {  
            for (const [question, answers] of Object.entries(el)){
                quizBox.innerHTML += `
                <hr style="border: none; height: 1px; background: linear-gradient(to right, rgba(0,0,0,0), rgba(0,0,0,0.75), rgba(0,0,0,0)); box-shadow: 0 2px 2px -2px rgba(0,0,0,0.4);">
<div class="mb-2" style="padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15); background: #2d71a1; background: linear-gradient(-45deg, #1391a5, #274685); color: #fff; box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.15);">
    <b>${question}</b>
</div>

                
                `
                answers.forEach(answer=>{
                    quizBox.innerHTML += `
                    <div class="mb-2">
                     <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                    <label for="${question}"> ${answer}</label>
                     </div>
                `
                })
            }
        });
        activateTimer(response.time)
    }, 
    error: function (error){
        console.log('Error:', error);
    }
});


const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')


const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el=>{
        if (el.checked){
            data[el.name]= el.value
        } else {
            if(!data[el.name]) {
                data[el.name] = null
            }
        }
    })
    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function(response){
            // console.log(response) 
            const results = response.results
            console.log(results)
            quizForm.style.display = 'none';

            // quizForm.classList.add('not-visible')
            scoreBox.innerHTML = `${response.passed ? 'Congratulations! ' : 'Oops..:( '}Your result is ${response.score.toFixed(0)}%`

            results.forEach(res=>{
                const resDiv = document.createElement('div')
                for (const [question,resp] of Object.entries(res)){
                    //  console.log(question)
                    //  console.log(resp)
                    //  console.log('*****')

                    resDiv.innerHTML += question
                    const cls = [ 'container', 'p-3', 'text-light', 'h6']
                    resDiv.classList.add(...cls)

                    if (resp=='not answered'){
                        resDiv.innerHTML += '- not answered'
                        resDiv.classList.add('bg-danger')
                    }
                    else {
                        const answer = resp['answered']
                        const correct = resp['correct_answer']
                        // console.log(answer, correct)
                        if (answer == correct){
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += `answered: ${answer}`
                        }
                        else {
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += `| correct answer: ${correct}`
                            resDiv.innerHTML += `| answered: ${answer}`
                        }
                    }
                    
                }
                // const body = document.getElementsByTagName('BODY')[0]
                resultBox.append(resDiv)
        })
        },
        error: function (error){
            console.log(error)
        }
    })
}

quizForm.addEventListener('submit', e=>{
    e.preventDefault()
    sendData()
})

