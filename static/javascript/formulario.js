const form = document.querySelector('#form');

form.addEventListener('submit', function (e){
    e.preventDefault();

    let isValid = true;

    const fields = [
        {
            id: 'name',
            label: 'Nome',
            validator: nameIsValid
        },
        {
            id: 'email',
            label: 'E-mail',
            validator: emailIsValid
        },
        {
            id: 'aniversario',
            label: 'Nascimento',
            validator: dateIsValid
        },
        {
            id: 'cpf',
            label: 'CPF',
            validator: cpfIsValid
        },
        {
            id: 'senha',
            label: 'Senha',
            validator: passwordIsSecure
        },
        {
            id: 'confirm_senha',
            label: 'Confirmar Senha',
            validator: passwordMatch
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
            isValid = false;
        }
    });

    if (isValid) {
        form.submit(); // Envia o formulário após validação
    }
});


function isVazio(value){
    return value.trim() === '';
}

function nameIsValid(value){
    const validator = {
        isValid: true,
        errorMessage: null
    };
    

    if (isVazio(value)){
        validator.isValid = false;
        validator.errorMessage = 'O campo é obrigatório!';
        return validator;
    }

    const min = 2;
    
    if (value.length < min){
        validator.isValid = false;
        validator.errorMessage = `O nome deve ter no mínimo ${min} caracteres!`;
        return validator;
    }
    const regex = /^[a-zA-ZÁ-ÿ\s]+$/;
    if (!regex.test(value)){
        validator.isValid = false;
        validator.errorMessage = 'O nome só pode conter letras e espaços!';
    }

    return validator;
}

function dateIsValid(value){
    const validator = {
        isValid: true,
        errorMessage: null
    }
     if (isVazio(value)){
        validator.isValid = false;
        validator.errorMessage = 'O nascimento é obrigatório!';
        return validator;
    }

    const ano = new Date(value).getFullYear();

    if(ano < 1910 || ano> new Date().getFullYear()) {
        validator.isValid = false;
        validator.errorMessage = 'Data inválida!'
        return validator;
    }

     return validator;
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

function cpfIsValid(value){
    const validator = {
        isValid: true,
        errorMessage: null
    }
     if (isVazio(value)){
        validator.isValid = false;
        validator.errorMessage = 'O CPF é obrigatório!';
        return validator;
    }

    const min = 11;
    
    if (value.length < min){
        validator.isValid = false;
        validator.errorMessage = `O CPF deve ter no mínimo ${min} caracteres!`;
        return validator;
    }
    // Regex para validar CPF (apenas números)
    const regex = /^\d{11}$/;
    if (!regex.test(value)){
        validator.isValid = false;
        validator.errorMessage = 'O CPF é inválido!';
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

function passwordMatch(value){
    const validator = {
        isValid: true,
        errorMessage: null
    }

    const passwordValue = document.getElementById('senha').value;

    if (value === '' || passwordValue !== value){
        validator.isValid = false;
        validator.errorMessage = 'As senhas não conferem!';
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