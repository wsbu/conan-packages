WSBU Conan Packages
===================

Here lies a suite of Conan recipes for third-party libraries used by the
WSBU team.

Instructions
------------

Packages are uploaded to the Red Lion Conan server. It is located at http://ci.redlion.net:9300 and can be added to your
repository listing with `conan remote add -r <name> http://ci.redlion.net:9300`.

Setting a package to always be built with specific options can be done by creating a file named `options.json` in the
package directory. The file should contain a single JSON object with key-value pairs for each additional argument
(`--option`) that should be passed to Conan. For instance, a file such as

```json
{
  "foo": true,
  "bar": "wtf"
}
```

would add `--option foo=True --option bar=wtf` to the command line. Note that the `true` in JSON is automatically
converted to the proper case for Conan (Python) to understand correctly.
