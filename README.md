# passpwnedcheck Package

This is a simple wrapper for Pwned Passwords API. It uses k-anonymity to securely check if your password has been leaked without actually sending your password to Pwned Passwords API.

Also, please check my blog post below for more information.

[https://duongnt.com/leaked-password](https://duongnt.com/leaked-password)

## Install

You can install passpwnedcheck using pip, just run the following command in the command line.
```
C:\> pip install passpwnedcheck
```

## Usage

### Blocking call
```
from passpwnedcheck.pass_checker import PassChecker

pass_checker = PassChecker()

password = 'Password'
is_leaked, count = pass_checker.is_password_compromised(password)

if is_leaked:
    print(f'Your password has been leaked {count} times')
else:
    print('Your password has not been leaked (yet)')
```

Alternatively, you can run pass_checker.py script from the command line, make sure to install the package via pip first.
```
C:\> python pass_checker.py password
Your password has been compromised xxxxxxx time(s)
```

### Non-blocking call

```
from passpwnedcheck.pass_checker_async import PassCheckerAsync

# session = <Code to create an assyncio.session object>
pass_checker = PassCheckerAsync(session)

passwords = 'Password'
is_leaked, count = await pass_checker.is_password_compromised(password)

if is_leaked:
    print(f'Your password has been leaked {count} times')
else:
    print('Your password has not been leaked (yet)')
```

It's also possible to check multiple passwords at once. To reduce the load on Pwned Passwords API, we send requests in batches. The size of each batch is customizable, with 10 as the default.

```
# session = <Code to create an assyncio.session object>
pass_checker = PassCheckerAsync(session)

passwords = ['Password1', 'Password2', 'Password3', 'Password4']
results = await PassCheckerAsync.is_passwords_compromised(passwords)

print(results)
```

Results are stored in a dictionary, with each password as key.
```
{
  'Password1': xxxxxxx,
  'Password2': xxxxxxx,
  'Password3': xxxxxxx,
  'Password4': xxxxxxx
}
```

If you don't need to reuse the session then you can use the `SessionManager` helper class, which is included with this library. Just wrap the code above inside a `with` statement.
```
from passpwnedcheck.session_manager import SessionManager

async with SessionManager() as manager:
    pass_checker = PassCheckerAsync(manager.get_session())
    is_leaked, count = await pass_checker.is_password_compromised('Password')
```

You can also choose to increase/decrease the batch size when checking multiple passwords at once, but make sure that the number of concurrent requests is kept at a reasonable level.
```
passwords = ['Password1', 'Password2', 'Password3', 'Password4',...]

# Send requests to Pwned Passwords API in batch of five
results = await PassCheckerAsync.is_passwords_compromised(passwords=passwords, batch_size=5)
```

## About k-anonymity

We utilize a mathematical property known as [k-Anonymity](https://blog.cloudflare.com/validating-leaked-passwords-with-k-anonymity/) and apply it to password hashes in the form of range queries. As such, the Pwned Passwords API service never gains enough information about a non-breached password hash to be able to breach it later.

> Suppose a user enters the password test into a login form and the service they are logging into is programmed to validate whether their password is in a database of leaked password hashes. Firstly the client will generate a hash (in our example using SHA-1) of a94a8fe5ccb19ba61c4c0873d391e987982fbbd3. The client will then truncate the hash to a predetermined number of characters (for example, 5) resulting in a Hash Prefix of a94a8. This Hash Prefix is then used to query the remote database for all hashes starting with that prefix. The entire hash list is then downloaded and each downloaded hash is then compared to see if any match the locally generated hash. If so, the password is known to have been leaked.

## License

MIT License

https://opensource.org/licenses/MIT