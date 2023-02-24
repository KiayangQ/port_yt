import { jsx as _jsx, Fragment as _Fragment } from "react/jsx-runtime";
import { Translator } from '../../../../translator';
export var MyComponent = function (_a) {
    var dynamicCopy = _a.dynamicCopy, locale = _a.locale;
    var dynamicText = Translator.translate(dynamicCopy, locale);
    return (_jsx(_Fragment, { children: _jsx("div", { children: dynamicText }) }));
};
