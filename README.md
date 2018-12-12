# passpwnedcheck Package

This is a simple wrapper for Pwned Passwords API. It uses k-anonymity to securely check if your password has been leaked without actually sending your password to  Pwned Passwords API.

## Install

You can install passpwnedcheck using pip, just run the following command in the command line

    C:\> pip install passpwnedcheck

## Usage

    from passpwnedcheck import PassChecker
    
    pass_checker = PassChecker()
    
    password = 'Password'
    is_leaked, count = pass_checker.is_password_compromised(password)
    
    if is_leaked:
        print('Your password has been leaked')
    else:
        print('Your password has not been leaked (yet)')

Alternatively, you can run pass_checker.py script from command line, make sure to install the package via pip first

    C:\> python pass_checker.py password
    Your password has been compromised xxxxxxx time(s)

## About k-anonymity

We utilize a mathematical property known as k-Anonymity and applying it to password hashes in the form of range queries. As such, the Pwned Passwords API service never gains enough information about a non-breached password hash to be able to breach it later.

Suppose a user enters the password test into a login form and the service they are logging into is programmed to validate whether their password is in a database of leaked password hashes. Firstly the client will generate a hash (in our example using SHA-1) of a94a8fe5ccb19ba61c4c0873d391e987982fbbd3. The client will then truncate the hash to a predetermined number of characters (for example, 5) resulting in a Hash Prefix of a94a8. This Hash Prefix is then used to query the remote database for all hashes starting with that prefix. The entire hash list is then downloaded and each downloaded hash is then compared to see if any match the locally generated hash. If so, the password is known to have been leaked.

Please see the following link for more information

https://blog.cloudflare.com/validating-leaked-passwords-with-k-anonymity/

## License

MIT License

https://opensource.org/licenses/MIT