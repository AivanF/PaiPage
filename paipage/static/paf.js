/**
 * Copyright (c) AivanF 2020
 *
 * @summary PaiPage Forms JS
 * @author AivanF <projects@aivanf.com>
 *
 * Created at 2020-05-22
 */
;const PAF = function($) {
const version = 'PAF.js 2020.05.23';
console.log(version);

const Container = {};

Container.Forms = {};
Container.preprocessForm = function(form) {
	form.codes = {};
	form.parts.forEach(function (part) {
		// Must have:
		if (!(part.type && part.code && part.name)) {
			console.error('Got bad form part', part);
		}
		// May have: hideCreate, hideEdit, subtype, etc.
		form.codes[part.code] = part;
	});
	Container.Forms[form.type] = form;
	return form;
}
Container.toupdate = [];

const SELECT_NULL = '__no__';


function escapeHtml(unsafe) {
	return unsafe
		 .replace(/&/g, "&amp;")
		 .replace(/</g, "&lt;")
		 .replace(/>/g, "&gt;")
		 .replace(/"/g, "&quot;")
		 .replace(/'/g, "&#039;");
 }
function isFunction(value) {
	return typeof value === 'function';
}
function ifFunction(value, arg) {
	if (isFunction(value))
		return value(arg);
	else 
		return value;
}
function isDefined(value) {
	return typeof value !== 'undefined';
}
function ifUndefined(value, other) {
	if (isDefined(value)) {
		return value;
	} else {
		return other;
	}
}
function notNull(value) {
	return value !== null;
}
function exists(value) {
	return isDefined(value) && notNull(value);
}
function ifMany(value, callMany, callSingle) {
	if (Array.isArray(value)) {
		if (value.length === 1) {
			return ifFunction(callSingle, value[0]);
		} else {
			return ifFunction(callMany, value);
		}
	} else {
		return ifFunction(callSingle, value);
	}
}
function isMany(value) {
	return ifMany(value, true, false);
}
function forMany(value, callback) {
	let result = [];
	if (Array.isArray(value)) {
		let len = value.length;
		for (let i = 0; i < len; i++) {
			result.push(callback(value[i]));
		}
	} else {
		result.push(callback(value));
	}
	return result;
}

const get_value_def = (el => Array.isArray(el) ? el[0] : el);
const get_label_def = (el => Array.isArray(el) ? el[1] : el);

function findSelecting(ar, key) {
	let len = ar.length;
	for (let i = 0; i < len; i++) {
		if (key == get_value_def(ar[i]))
			return ar[i];
	}
	return null;
}



const PartViewHandlers = {};
Container.PartViewHandlers = PartViewHandlers;
const SelectablesViewHandlers = {};
Container.SelectablesViewHandlers = SelectablesViewHandlers;

PartViewHandlers['int'] = function (part, value) {
	return `${value}`;
};
PartViewHandlers['str'] = function (part, value) {
	// can_copy = true;  // TODO: here!
	return value;
};
PartViewHandlers['str2str'] = function (part, value) {
	let result = '';
	Object.keys(value).forEach(function (key) {
		result += `<br><i>${key}:</i> ${value[key]}`;
	});
	return result;
};
PartViewHandlers['bool'] = function (part, value) {
	return `${value}`;
};
PartViewHandlers['select'] = function (part, value) {
	if (!selectables[part.subtype]) {
		console.error(`Missing selectables for "${part.subtype}" subtype`);
		return;
	}
	let found = findSelecting(selectables[part.subtype], value);
	if (SelectablesViewHandlers[part.subtype]) {
		return SelectablesViewHandlers[part.subtype](found, value);
	} else {
		let empty_option = part.empty_option || '';
		if (found == null || found == '') {
			return empty_option;
		} else {
			return get_label_def(found);
		}
	}
};

Container.buildFormView = function(form, obj) {
	let result = '';
	form.parts.forEach(function(part) {
		if (!PartViewHandlers[part.type]) {
			console.error(`Missing PartViewHandlers for "${part.type}" type`);
			return;
		}
		let value = PartViewHandlers[part.type](part, obj[part.code]);
		if (exists(value))
			result += `<b>${part.name}:</b> ${value}<br>`;
	});
	return result;
}



Container.textCounter = function(ind, maxlen) {
	let o = $('#' + ind);
	let rem = maxlen - o.val().length;
	o.attr('title', 'Symbols: ' + rem).tooltip('fixTitle').tooltip('show');
}

function makeSelect(ind, options, settings) {
	// value, multiple, get_value, get_label, error_text, allow_clear, empty_option
	const get_value = settings['get_value'] || get_value_def;
	const get_label = settings['get_label'] || get_label_def;
	const empty_option = settings['empty_option'] || '-';
	let result = '<select class="form-control" id="' + ind + '"';
	if (settings['multiple']) { result += ' multiple="multiple"'; }
	result += '>';
	let s;
	if (settings['allow_clear']) {
		// create fake option
		if (!settings['multiple'] && !notNull(settings['value'])) {
			s = ' selected';
		} else {
			s = '';
		}
		result += `<option value="${SELECT_NULL}" ${s}>${empty_option}</option>`;
	}
	if (options) {
		for (i in options) {
			const cur = options[i];
			s = false;
			if (Array.isArray(settings['value'])) {
				s = settings['value'].includes(get_value(cur));
				if (!s) {
					if (typeof s === 'string') {
						s = settings['value'].includes(+get_value(cur));
					} else {
						s = settings['value'].includes(get_value(cur).toString());
					}
				}
			} else {
				s = get_value(cur) == settings['value'];
			}
			s = s ? ' selected' : '';
			result += '<option value="' + get_value(cur) + '" ' + s + '>' + get_label(cur) + '</option>';
		}
	}
	result += '</select>';
	Container.toupdate.push(function() {
		$('#' + ind).select2({ dropdownAutoWidth: true, width: '100%' });
	});
	if (!settings['allow_clear'] && (!options || options.length < 1)) {
		result += makeAlert(settings['error_text'] || 'Option list not found!');
	}
	return result;
}

function makeAlert(text, ind, style) {
	text = text || 'Unknown problem!';
	let result = '<div class="col-xs-12 alert alert-danger"';
	if (ind) {
		result += ' id="' + ind + '"';
	}
	result += ' style="margin-top: 10px; ';
	if (style) {
		result += style;
	}
	result += '">' + text + '</div>'
	return result;
}



const PartEditHandlers = {};
Container.PartEditHandlers = PartEditHandlers;

PartEditHandlers['str'] = function (ind, part, value) {
	let result = '';
	result += `<input type="text" id="${ind}"`;
	let cur_val = null;
	if (typeof value === 'number' || typeof value === 'string') {
		cur_val = value.toString();
	}
	if (cur_val) {
		if (part.max_len) {
			cur_val = cur_val.slice(0, part.max_len);
		}
		result += ' value="' + escapeHtml(cur_val) + '"';
	}
	let cls = 'form-control edit-element-text';
	if (part.max_len) {
		result += ' maxlength="' + part.max_len + '"';
		result += ` onkeyup="PAF.textCounter('${ind}', ${part.max_len});"`;
		result += ` onfocus="PAF.textCounter('${ind}', ${part.max_len});"`;
		result += ' data-toggle="tooltip" title="Печатай!"';
		cls += ' tooltipped';
	}
	result += ' class="' + cls + '">';
	return result;
}
PartEditHandlers['select'] = function (ind, part, value) {
	// value, multiple, get_value, get_label, error_text, allow_clear
	const options = selectables[part.subtype];
	return makeSelect(ind, options, {
		value: value,
		multiple: false,
		allow_clear: part.allow_clear,
		empty_option: part.empty_option,
	});
}

Container.buildFormEdit = function (form, obj, prefix, is_creation) {
	prefix = prefix || '';
	let result = '';
	form.parts.forEach(function(part) {
		let hide = false;
		if (is_creation)
			hide = ifUndefined(part.hideCreate, false);
		else
			hide = ifUndefined(part.hideEdit, false);
		if (hide) return;
		if (!PartEditHandlers[part.type]) {
			console.error(`Missing PartEditHandlers for "${part.type}" type`);
			return;
		}
		const ind = prefix + part.code;
		const value = PartEditHandlers[part.type](ind, part, obj[part.code]);
		if (exists(value)) {
			result += '<div class="form-part">';
			result += `<b>${part.name}:</b> ${value}<br>`;
			result += makeAlert('', ind + '-alert', 'display: none;');
			result += '</div>';
		}
	});
	return result;
}

Container.updateEditor = function () {
	Container.toupdate.forEach(function(el){ el(); });
	Container.toupdate = [];
	$('[data-toggle="tooltip"]').tooltip();
}



const PartExtractHandlers = {};
Container.PartExtractHandlers = PartExtractHandlers;

PartExtractHandlers['int'] = function (ind, part) {
	return parseInt($('#' + ind).val());
}
PartExtractHandlers['str'] = function (ind, part) {
	return $('#' + ind).val();
}
PartExtractHandlers['select'] = function (ind, part) {
	let result = $('#' + ind).val();
	if (result === SELECT_NULL)
		result = null;
	return result;
}
PartExtractHandlers['const'] = function (ind, part) {
	return part.value;
}

Container.extractForm = function(form, prefix, is_creation) {
	let result = {};
	prefix = prefix || '';
	form.parts.forEach(function(part) {
		let hide = false;
		if (is_creation)
			hide = ifUndefined(part.hideCreate, false);
		else
			hide = ifUndefined(part.hideEdit, false);
		if (hide) return;
		if (!PartExtractHandlers[part.type]) {
			console.error(`Missing PartExtractHandlers for "${part.type}" type`);
			return;
		}
		const ind = prefix + part.code;
		result[part.code] = PartExtractHandlers[part.type](ind, part);
	});
	return result;
}



const PartValidateHandlers = {};
Container.PartValidateHandlers = PartValidateHandlers;
const SelectablesValidateHandlers = {};
Container.SelectablesValidateHandlers = SelectablesValidateHandlers;

PartValidateHandlers['select'] = function (part, value) {
	if (!exists(value) && !part.allow_clear)
		return 'Value not selected!';	
	if (SelectablesValidateHandlers[part.subtype]) {
		return SelectablesValidateHandlers[part.subtype](part, value);
	}
}
PartValidateHandlers['slug'] = function (part, value) {
	if (! /^[-a-zA-Z0-9]+$/.test(value)) {
		return 'Bad address characters!';
	}
}

Container.validateForm = function(form, prefix, is_creation) {
	let values = Container.extractForm(form, prefix, is_creation);
	let fine = true;
	prefix = prefix || '';
	form.parts.forEach(function(part) {
		let hide = false;
		if (is_creation)
			hide = ifUndefined(part.hideCreate, false);
		else
			hide = ifUndefined(part.hideEdit, false);
		if (hide) return;
		if (!PartValidateHandlers[part.type]) {
			console.error(`Missing PartValidateHandlers for "${part.type}" type`);
			return;
		}
		const ind = prefix + part.code;
		const value = values[part.code];
		const comment = PartValidateHandlers[part.type](part, value);
		const $alert = $('#' + ind + '-alert');
		if (exists(comment)) {
			fine = false;
			$alert.html(comment);
			$alert.show(500);
		} else {
			$alert.hide(500);
		}
	});
	if (fine) {
		return values;
	} else {
		return null;
	}
}

Container.addCustomType = function (type, obj) {
	if (exists(obj.view)) {
		// function (part, value)
		PartViewHandlers[type] = obj.view;
	}
	if (exists(obj.edit)) {
		// function (ind, part, value)
		PartEditHandlers[type] = obj.edit;
	}
	if (exists(obj.extract)) {
		// function (ind, part)
		PartExtractHandlers[type] = obj.extract;
	}
	if (exists(obj.validate)) {
		// function (part, value)
		PartValidateHandlers[type] = obj.validate;
	}
}
Container.addCustomSelectable = function (subtype, obj) {
	if (exists(obj.view)) {
		// function (found, value)
		SelectablesViewHandlers[subtype] = obj.view;
	}
	if (exists(obj.validate)) {
		// function (part, value)
		SelectablesValidateHandlers[subtype] = obj.validate;
	}
}

// TODO: int, bool, date

return Container;
}(jQuery);