// React router behaves very weirdly with any URL containing a "%" (it
// automatically decodes them and there's nothing we can do about it). The
// work-around here is to char-encode every single character in base 36 (0-9,
// a-z), then join each code with a hyphen (e.g. "Hello" -> "2w-2t-30-30-33"),
// then use that as the url.

const base = 36;
const divider = '-';

function encodeChar(char) {
  return char.charCodeAt(0).toString(base);
}

function decodeChar(code) {
  return String.fromCharCode(parseInt(code, base))
}

export function encodeString(decodedString) {
  return [...decodedString].map((char) => encodeChar(char)).join(divider);
}

export function decodeString(encodedString) {
  return encodedString.split('-').map((code) => decodeChar(code)).join('');
}
