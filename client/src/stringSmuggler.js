// React router behaves very weirdly with any URL containing a "%" (it
// automatically decodes them and there's nothing we can do about it). The
// work-around here is to percent-encode every single character, then remove the
// percent sign from each two-char chunk (e.g. "Hello" -> "%68%65%6c%6c%6f" ->
// "68656c6c6f"), then use that as the url.

function encodeChar(c) {
  return c.charCodeAt(0).toString(16);
}

export function encodeString(decodedString) {
  return [...decodedString].map((char) => encodeChar(char)).join('');
}

export function decodeString(encodedString) {
  return encodedString.match(/.{1,2}/g).map((chunk) => decodeURIComponent("%"+chunk)).join('');
}
