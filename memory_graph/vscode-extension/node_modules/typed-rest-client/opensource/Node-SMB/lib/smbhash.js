var crypto = require('crypto');
var $ = require('./common');

/*
 * Generate the LM Hash
 */
function lmhashbuf(inputstr)
{
  /* ASCII --> uppercase */
  var x = inputstr.substring(0, 14).toUpperCase();
  var xl = Buffer.byteLength(x, 'ascii');

  /* null pad to 14 bytes */
  var y = new Buffer(14);
  y.write(x, 0, xl, 'ascii');
  y.fill(0, xl);

  /* insert odd parity bits in key */
  var halves = [
    $.oddpar($.expandkey(y.slice(0, 7))),
    $.oddpar($.expandkey(y.slice(7, 14)))
  ];

  /* DES encrypt magic number "KGS!@#$%" to two
   * 8-byte ciphertexts, (ECB, no padding)
   */
  var buf = new Buffer(16);
  var pos = 0;
  var cts = halves.forEach(function(z) {
    var des = crypto.createCipheriv('DES-ECB', z, '');
    var str = des.update('KGS!@#$%', 'binary', 'binary');
    buf.write(str, pos, pos + 8, 'binary');
    pos += 8;
  });

  /* concat the two ciphertexts to form 16byte value,
   * the LM hash */
  return buf;
}

function nthashbuf(str)
{
  /* take MD4 hash of UCS-2 encoded password */
  var ucs2 = new Buffer(str, 'ucs2');
  var md4 = crypto.createHash('md4');
  md4.update(ucs2);
  return new Buffer(md4.digest('binary'), 'binary');
}

function lmhash(is)
{
  return $.bintohex(lmhashbuf(is));
}

function nthash(is)
{
  return $.bintohex(nthashbuf(is));
}

module.exports.nthashbuf = nthashbuf;
module.exports.lmhashbuf = lmhashbuf;

module.exports.nthash = nthash;
module.exports.lmhash = lmhash;
