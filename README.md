WSBU Conan Packages
===================

Here lies a suite of Conan recipes for third-party libraries used by the
WSBU team.

Instructions
------------

Packages are uploaded to the Red Lion Conan server. It is located at https://artifactory.redlion.net and can be 
added to your repository listing with 
`conan remote add <REMOTE> https://artifactory.redlion.net/artifactory/api/conan/conan-local`.

Setting a package to always be built with specific options can be done by creating a file named `options.json` in the
package directory. The file should contain a single JSON object with key-value pairs for each additional argument
(`--option`) that should be passed to Conan. For instance, a file such as

```json
[
  {
    "foo": true,
    "bar": "wtf"
  },
  {
    "foo": false,
    "bar": "wtf"
  }
]
```

would build two different versions of the project. On the first it would add `--option foo=True --option bar=wtf` to 
the command line and on the second it would add `--option foo=False --option bar=wtf`. Note that the `true` and 
`false`, in JSON are automatically converted to the proper case for Conan (Python) to understand correctly.
