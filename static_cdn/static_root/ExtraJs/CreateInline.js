const multiField = document.getElementsByClassName('multiField');
const addButton = document.getElementById('add-button');
const deleteButton = document.getElementById('delete-button');
const formsetDiv = document.getElementById('formset-div');

const multiFieldInitialLength = multiField.length;
let counter = multiFieldInitialLength - 1;

let totalFormHiddenInput;
let prefix;


const initial = (value) => {
    prefix = value;
    totalFormHiddenInput = document.getElementById(`id_${prefix}-TOTAL_FORMS`);
};


const deleteButtonStatus = () => {
    deleteButton.disabled = multiField.length === 1;
};


deleteButtonStatus();


addButton.addEventListener('click', ev => {
    const oldId = `${prefix}-${counter}`;
    const newId = `${prefix}-${counter + 1}`;
    const valueInputId = `id_${prefix}-${counter + 1}-value`;
    const multiFieldClone = $(formsetDiv.lastElementChild).clone();
    multiFieldClone.find('select,option').removeAttr('selected', 'selected').removeClass('is-invalid').end();
    multiFieldClone.html(multiFieldClone.html().split(oldId).join(newId));
    multiFieldClone.find(`#${valueInputId}`).val(null).end();
    multiFieldClone.children().remove('div.alert');
    multiFieldClone.insertAfter(formsetDiv.lastElementChild);
    counter++;
    totalFormHiddenInput.value++;
    deleteButtonStatus();
});


deleteButton.addEventListener('click', ev => {
    const lastElement = formsetDiv.lastElementChild;
    lastElement.remove();
    counter--;
    totalFormHiddenInput.value--;
    deleteButtonStatus();
});
