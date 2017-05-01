#!/usr/bin/env python2.7

# aliasfilter.py
#
# Version 1.0
# https://github.com/n20s/mail-aliasfilter

import email
import sys
import os
import time

# Read email from stdin (xfilter)
msg = email.message_from_file(sys.stdin)

try:
        ### Collect environment
        
    	  default_alias = os.getenv('MAIL_ALIAS_CATCH')
        if not default_alias: default_alias = msg['X-qmail-default']

        sender_address = os.getenv('SENDER')
        if not sender_address: sender_address = '$SENDER_not_specified'

        delivered_to = os.getenv('DTLINE')

        ### Debug settings
        
        # sender_address = 'info@twitter.com'

        ### Process

        # sender_domain = 'twitter' <- 'info@mail.twitter.com'
        sender_host = str.split(sender_address, '@')[1]
        if str.find(sender_host, '.') == 0:
                sender_domain = sender_host
        else:
             	  # at least two parts
                sender_domain_parts = str.split(sender_host, '.')
                last_index = len(sender_domain_parts)-1
                sender_domain = sender_domain_parts[last_index-1]


        ### Verify tokens in default part of alias

        tokens = str.split(default_alias, '+')
        matches = 0
        for i, token in enumerate(tokens):
                token_parts = str.split(token, '-')
                token_domain = token_parts[len(token_parts)-1]

                if token_domain == sender_domain: matches = matches+1

        ### Apply results

        msg.add_header('X-Aliasfilter-Catch', default_alias)
        if matches == 0:
                msg.add_header('X-Aliasfilter-Result', 'failed; unexpected-sender-domain; %s' %sender_domain)
                # Note: subject modification won't be reflected in mail forward.
                # subject = msg['Subject']
                # msg['Subject'] = '[UNEXPECTED SENDER] %s' %subject
        else:
             	  msg.add_header('X-Aliasfilter-Result', 'ok')

        if delivered_to:
                delivered_to_parts = str.split(delivered_to, ': ')
                msg.add_header(delivered_to_parts[0], delivered_to_parts[1])
                
except Exception as err:
        # If an exception occurred, apply a specific result.
        # sys.stderr.writelines(err)
        
        msg.add_header('X-Aliasfilter-Result', 'script-execution-exception')

        try:
                homedir = os.getenv('HOME')
                logfile = open('%s/aliasfilter.log' %homedir, 'a')
                print >> logfile, '[%s] [Error] aliasfilter issue with email from \'%s\' default alias \'%s\'' %(time.asctime(), sender_address, default_alias)
                print >> logfile, err
                # print >> logfile, msg.as_string() # log mails only if appropriate content
                for a in os.environ:
                        print >> logfile, a, '=', os.getenv(a)
                logfile.close()
        except Exception as err2:
                # sys.stderr.writelines(err2)
                pass
finally:
        # In any case, return (modified) message to stdout (xfilter)
        sys.stdout.writelines(msg.as_string())
        sys.exit(0)

