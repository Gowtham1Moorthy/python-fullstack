function switchLogin(button){
    const loginForm = document.getElementById('login');
    const signUpForm = document.getElementById('signup');

    loginForm.classList.toggle('show');
    signUpForm.classList.toggle('show');

    if(button.classList.contains('login')){
        button.classList.remove('login');
        button.innerHTML = 'Have an account?';
    }
    else{
        button.classList.add('login');
        button.innerHTML = 'New User?';
    }
}