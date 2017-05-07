# Aliasfilter for Mail

## Introduction and Overview

This concept assumes a qmail environment as provided by [uberspace.de](https://uberspace.de) for example (additional information can be found at the [uberspace wiki solutions page](https://wiki.uberspace.de/cool) and [specifically here](https://wiki.uberspace.de/cool:qmail-aliasfilter)).


### Uberspace-specific
* Add a domain (e.g. `domain.com`) with namespace, e.g. `namespace`
* Add a qmail file, e.g. `.qmail-namespace-nospam-default`
  * This results in `nospam-*@domain.com` to be processed by the qmail file.
  * `nospam` is an example for a prefix. Suffixes are not possible.

Other options include
* No prefix
  * e.g. `.qmail-namespace-default`
  * This results in `*domain.com` to be processed. 
  * This is not recommended because spammers frequently use collected names as a user part of the address.
* No namespace (at uberspace, all domains will match)
  * e.g. `.qmail-nospam-default`
  * This results in `nospam-*@*` to be processed.


## Qmail File
e.g. `.qmail-namespace-nospam-default` (see above)

    |maildrop
    
Note that the mail will not be delivered if the maildrop command doesn't succeed.
 
## Mailfilter File
e.g. `.mailfilter`
Note: The file requires the rights set to 600, otherwise maildrop doesn't process the file.

    $ chmod 600 .mailfilter
    
Note: The file can be tested with the following command.

    $ echo | maildrop .mailfilter 
    
The mailfilter file.

    # .mailfilter file
    # https://github.com/n20s/mail-aliasfilter
    
    # Import additional environment variables that are provided by qmail to this context.
    # http://www.courier-mta.org/maildrop/maildropfilter.html
    
    # Provide a MAIL_ALIAS_CATCH from qmail's DEFAULT variable that contains the matching catch all part of the qmail default 
    # feature.
    # Note: Because DEFAULT is already used in maildrop, import qmail's DEFAULT variable fin a special way.
    SAVE_DEFAULT=$DEFAULT
    import DEFAULT
    MAIL_ALIAS_CATCH=$DEFAULT
    DEFAULT=$SAVE_DEFAULT
    
    # Provide qmail's SENDER variable that contains the sender's email address
    import SENDER
    
    # Provide qmails' DTLINE variable that contains a 'Delivered-To: receiver@mail.com' string with the final receiver address.
    import DTLINE
    
    # The xfilter command passes the whole email to the script and replaces it with the result from the script.
    xfilter "$HOME/aliasfilter.py"
 
    # Result handling
    # Note: The script ends with the first 'to' statement, use 'cc' for multiple options.

    # Option 1 - Delivery to a local user
    # Note: This will add an email header entry for the user which is appreciated for better traceability.
    #       At uberspace, this could simply be the main user name, which can have its own forward by putting the 
    #       forward address to the .qmail main file (see other chapter).
    # TODO: change 'username' to the actual username.
    to "!username"
    
    # Deactivated option
    # # Option 2 - Direct forward
    # # Note: This might not be a proper result, because the local mail server and the receiving address might not be
    # #       transparent to the final receiver, depending on the headers the sending mail server added. 
    # #       For example some mail servers do not add a "for"-part containing the address.
    # # Note: Change 'user@mail.com' to the actual forwarding address.
    # to "!user@mail.com"
    
    # Deactivated option
    # # Option 3 - Delivery to the maildir. 
    # # Note: In case the mails should be forwarded, this should be avoided because the mail take up local space.
    # # Note: Change 'Maildir' to the actual mail directory.
    # MAILDIR="$HOME/Maildir"
    # to "$MAILDIR"
    
## aliasfilter.py

The `aliasfilter.py` needs to be executable, e.g. 700.

    $ chmod 700 aliasfilter.py
    
Note: The file can be tested with the following command. The `testmail` file is a text file containing headers and body as described in [RFC 2822](https://tools.ietf.org/html/rfc2822).

    $ .aliasfilter.py < testmail
    

