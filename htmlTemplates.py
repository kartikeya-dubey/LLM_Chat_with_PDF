css = '''
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
}
.chat-message.user {
    background-color: #2b313e;
    font-weight: bold;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .avatar {
    width: 10%;
}
.chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    border-radius: 20%;
    object-fit: cover;
}
.chat-message .message {
    width: 80%;
    padding: 0 1.5rem;
    color: #fff;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/xH3b9Dr/istockphoto-1628291798-170667a.webp" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/B2570wH/face.jpg">
    </div>    
    <div class="message" style="color: CornflowerBlue;">{{MSG}}</div>
</div>
'''