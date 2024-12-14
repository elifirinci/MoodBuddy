const startBtn = document.getElementById('start-btn');
const videoContainer = document.getElementById('video-container');
const videoFeed = document.getElementById('video-feed');
const adviceBox = document.getElementById('advice-box');
const detectionMessage = document.getElementById('detection-message');
const emotionAdvice = document.getElementById('emotion-advice');
const yesBtn = document.getElementById('yes-btn');
const noBtn = document.getElementById('no-btn');
const adviceResponseButtons = document.getElementById('advice-response-buttons'); 
const adviceYesBtn = document.getElementById('advice-yes-btn'); 
const adviceNoBtn = document.getElementById('advice-no-btn');    

const emotionBasedAdvice = {
    "Angry": "Hey buddy, Just relax.. Take a deep breath and count until 15.",
    "Fear": "Are you OK? Just sit and drink water. Calm down buddy, Let's watch some funny videos!",
    "Happy": "You look so happy! What about listening to some energetic songs? Here’s a great playlist for you.",
    "Sad": "How about sharing your sadness with someone?",
    "Surprise": "You look surprised. Is everything OK? I can make you relaxed.. "
}
const emotionLinks = {
    "Happy": "https://open.spotify.com/playlist/0pNISUo6NbtnpBD13jRtQb?si=fa912e5b0385462c", 
    "Sad": "https://web.whatsapp.com/", 
    "Angry": "https://www.online-stopwatch.com/timer/15second/",  
    "Fear": "https://www.youtube.com/watch?v=Wa2tUkK2-IY&ab_channel=LifeAwesome", 
    "Surprise": "https://open.spotify.com/intl-tr/album/7AVeCLQjO6ZtsP6gAewUSs?si=03xwMkbKTYK615vC_p5OkQ",  
};

startBtn.addEventListener('click', async () => {
    videoContainer.style.display = 'block';
    videoFeed.src = "/video_feed";


    
    setTimeout(async () => {
        const response = await fetch('/detect_emotion', {
            method: 'POST',
        });
        const data = await response.json();

       if (data.success) {
            adviceBox.style.display = 'block';
            detectionMessage.textContent =
                `We detected your emotion. Your emotion is ${data.emotion}. Do you want some advice?`;

            yesBtn.addEventListener('click', () => {
               
                emotionAdvice.textContent = emotionBasedAdvice[data.emotion];
                emotionAdvice.style.display = 'block'; 
                document.getElementById('response-buttons').style.display = 'none'; 

               
                adviceResponseButtons.style.display = 'block';
            });

           
            noBtn.addEventListener('click', () => {
                window.location.reload(); 
            });

            
            adviceYesBtn.addEventListener('click', () => {
                const link = emotionLinks[data.emotion];  
                window.open(link, '_blank');
            });

            
            adviceNoBtn.addEventListener('click', () => {
                window.location.reload();  
            });


        } else {
            alert(data.message);
        }
    }, 2000); 
});
