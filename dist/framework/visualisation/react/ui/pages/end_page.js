import { jsx as _jsx, Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import { Footer } from './templates/footer';
import { Sidebar } from './templates/sidebar';
import LogoSvg from '../../../../../assets/images/logo.svg';
import { Page } from './templates/page';
import TextBundle from '../../../../text_bundle';
import { Translator } from '../../../../translator';
import { BodyLarge, Title1 } from '../elements/text';
export var EndPage = function (props) {
    var _a = prepareCopy(props), title = _a.title, text = _a.text, text1 = _a.text1;
    var footer = _jsx(Footer, {});
    var sidebar = _jsx(Sidebar, { logo: LogoSvg });
    var body = (_jsxs(_Fragment, { children: [_jsx(Title1, { text: title }), _jsx(BodyLarge, { text: text }), _jsx(BodyLarge, { text: text1 })] }));
    return (_jsx(Page, { body: body, sidebar: sidebar, footer: footer }));
};
function prepareCopy(_a) {
    var locale = _a.locale;
    return {
        title: Translator.translate(title, locale),
        text: Translator.translate(text, locale),
        text1: Translator.translate(text1, locale)
    };
}
var title = new TextBundle()
    .add('en', 'Thank you')
    .add('nl', 'Bedankt');
function generateRandomString(length, num) {
    var result = '';
    var numberChars = '0123456789';
    var letterChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    var characters = num === 1 ? numberChars : letterChars;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}
// Generate a random string of 5 numbers and 5 letters
var numbers = generateRandomString(5, 1);
var letters = generateRandomString(5, 2);
// Combine the 'abcde' prefix with the random numbers and letters
var randomStringen = "Your return code is don0223".concat(numbers).concat(letters);
var randomStringnl = "Uw retourcode is don0223".concat(numbers).concat(letters, " ");
var text = new TextBundle()
    .add('en', randomStringen)
    .add('nl', randomStringnl);
var text1 = new TextBundle()
    .add('en', '\nPlease copy and paste your return code to the survey page. After you finish this, the data donation is complete and you can close this page.')
    .add('nl', '\nGelieve uw terugkeercode te kopiëren en te plakken op de enquêtepagina. Nadat je hiermee klaar bent, is de gegevensdonatie voltooid en kun je deze pagina sluiten.');
