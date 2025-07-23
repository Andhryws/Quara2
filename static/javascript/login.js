const form = document.querySelector('#form');

form.addEventListener('submit', function (e){
    e.preventDefault();

    let isValid = true;  // flag para validar todos os campos

    const fields = [
        {
            id: 'email',
            label: 'E-mail',
            validator: emailIsValid
        },
        
        {
            id: 'senha',
            label: 'Senha',
            validator: passwordIsSecure
        },

    ];

    const errorIcon = '<i class="fa-solid fa-circle-exclamation"></i>';

    fields.forEach(function (field){
        const input = document.getElementById(field.id);
        const inputBox = input.closest('.input-box');
        const inputValue = input.value;

        const errorSpan = inputBox.querySelector('.error');
        errorSpan.innerHTML = '';

        inputBox.classList.remove('invalido');
        inputBox.classList.add('valido');

        const fieldValidator = field.validator(inputValue);

        if (!fieldValidator.isValid){
            errorSpan.innerHTML = `${errorIcon} ${fieldValidator.errorMessage}`;
            inputBox.classList.add('invalido');
            inputBox.classList.remove('valido');
            isValid = false;  // marcar que tem erro
        }
    });

    if (isValid) {
        form.submit(); // se passou na validação, envia o formulário
    }
});

function isVazio(value){
    return value.trim() === '';
}


function emailIsValid(value){
    const validator = {
        isValid: true,
        errorMessage: null
    }
     if (isVazio(value)){
        validator.isValid = false;
        validator.errorMessage = 'O email é obrigatório!';
        return validator;
    }

    const regex = new RegExp("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$");
    if (!regex.test(value)){
        validator.isValid = false;
        validator.errorMessage = 'O email é inválido!';
        return validator;
    }
    return validator;
}


function passwordIsSecure(value){
    const validator = {
        isValid: true,
        errorMessage: null
    }

     if (isVazio(value)){
        validator.isValid = false;
        validator.errorMessage = 'A senha é obrigatória!';
        return validator;
    }
    return validator;
}

const passwordIcons = document.querySelectorAll('.password-icone');

passwordIcons.forEach(icon => {
    icon.addEventListener('click', function () {
        const input = this.parentElement.querySelector('.form-control');
        input.type = input.type === 'password' ? 'text' : 'password';
        this.classList.toggle('fa-eye');
    })
})

