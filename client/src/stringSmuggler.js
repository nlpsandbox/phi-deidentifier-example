// React router behaves very weirdly with any URL containing a "%" (it
// automatically decodes them and there's nothing we can do about it). The
// work-around here is to char-encode every single character in base 36 (0-9,
// a-z), then join each code with a hyphen (e.g. "Hello" -> "2w-2t-30-30-33"),
// then use that as the url.

export function encodeString(decodedString) {
  let buff = new Buffer(decodedString);
  return buff.toString('base64');
}

export function decodeString(encodedString) {
  let buff = new Buffer(encodedString, 'base64');
  return buff.toString('utf-8');
}
