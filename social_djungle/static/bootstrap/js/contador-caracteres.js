function escribirLongitud(length) {
	var form = document.getElementById('newMicropost');
	var label;
	if (! document.getElementById('text-length')) {
		label = document.createElement("label");
		label.setAttribute('id', 'text-length');
		form.appendChild(label);
	} else {
		label = document.getElementById('text-length');
	}
	var contenido = document.createTextNode('Caracteres restantes: ' + length);
	label.appendChild(contenido);
}

function calcLength() {
	var textarea = document.getElementsByName('publication')[0]
	var label;
	num = 140 - textarea.value.length
	if (document.getElementById('text-length')) {
		label = document.getElementById('text-length');
		if (label.hasChildNodes) {
			label.removeChild(label.firstChild);
		}
	}
	escribirLongitud(num)
	var button = document.getElementById("micropostButton");
	var classes = "btn btn-primary btn-large";
	if ((num < 0) || (num==140)) {
		button.setAttribute('class', classes + " disabled");
		button.setAttribute('disabled', '')
	} else {
		button.setAttribute('class', classes);
		button.removeAttribute('disabled')
	}
}
