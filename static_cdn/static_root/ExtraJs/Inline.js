const multiField = document.getElementsByClassName('multiField');
const addButton = document.getElementById('add-button');
const deleteButton = document.getElementById('delete-button');
const formsetDiv = document.getElementById('formset-div');

let counter = multiField.length - 1;
let totalFormHiddenInput;
let prefix;


const initial = (value) => {
    prefix = value;
    totalFormHiddenInput = document.getElementById(`id_${prefix}-TOTAL_FORMS`);
};


const deleteButtonStatus = (value) => {
    deleteButton.disabled = !value;
};

addButton.addEventListener('click', ev => {
    const oldId = `${prefix}-${counter}`;
    const newId = `${prefix}-${counter + 1}`;
    let lastElementHtml = formsetDiv.lastElementChild.innerHTML;
    lastElementHtml = lastElementHtml.split(oldId).join(newId);
    const multiFieldClone = multiField[0].cloneNode(true);
    multiFieldClone.innerHTML = lastElementHtml;
    formsetDiv.appendChild(multiFieldClone);
    counter++;
    totalFormHiddenInput.value++;
    deleteButtonStatus(counter);
});

deleteButton.addEventListener('click', ev => {
    const lastElement = formsetDiv.lastElementChild;
    lastElement.remove();
    counter--;
    totalFormHiddenInput.value--;
    deleteButtonStatus(counter);
});
