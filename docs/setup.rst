.. _setup:

Initial Setup
=============

Before we can build a Twilio application, there are some steps you'll need to
complete. This setup shouldn't take more than five minutes.

Install a Text Editor
---------------------

Now that you've signed, up, we need to make sure you can edit the workshop
code. **If you already have a text-editor or IDE of choice, skip this section**.

- Windows - Download and install `Notepad++`_
- OS X - Download and install `Text Wrangler`_
- Linux - Install gedit via your package manager

.. _Text Wrangler: http://www.barebones.com/products/textwrangler/
.. _Notepad++: http://notepad-plus-plus.org/

Install Python
--------------

Open up a terminal or command prompt window and type the following

.. code-block:: bash

   $ python --version

If the output contains either Python 2.6.x or Python 2.7.x, your Python
installation is ready to go. Some of you may have Python 3.x installed. Sadly,
the twilio-python_ helper library only works with Python 2.6 or Python 2.7.

Find and download the installation for your operating system.

- `Python 2.7.3 Windows Installer <http://www.python.org/ftp/python/2.7.3/python-2.7.3.msi>`_
- `Python 2.7.3 Windows X86-64 Installer <http://www.python.org/ftp/python/2.7.3/python-2.7.3.amd64.msi>`_
- `Python 2.7.3 OS X Installer <http://www.python.org/ftp/python/2.7.3/python-2.7.3-macosx10.6.dmg>`_
- `Python 2.7.3 compressed source tarball <http://www.python.org/ftp/python/2.7.3/Python-2.7.3.tgz>`_

More downloads are available on the `Python downloads <http://www.python.org/download/>`_ page.

Once you are finished, opening up Terminal (OS X) or Powershell (Windows) and
verify the output is now the same

.. code-block:: bash

   $ python --version
   Python 2.7.3

Download Workshop Materials
---------------------------

Download the workshop materials as a zipfile_. You can also clone this
repository if you have git installed.

.. code-block:: bash

   $ git clone https://github.com/twilio/calworkshop.git

To verify that everything is working correctly, run ``check.py`` and make sure
the output matches below

.. code-block:: bash

   $ cd calworkshop
   $ python check.py
   :)

.. _zipfile: https://github.com/twilio/calworkshop/zipball/master
.. _twilio-python: https://github.com/twilio/twilio-python

Create a Twilio Account
-----------------------

First, `sign up`_ for a free Twilio account. You won't need a credit card, but
you will need a phone number to prove you aren't a robot. Once you've signed
up, you'll have your own Twilio phone number. We'll use this number for the
rest of the workshop.

.. _sign up: https://www.twilio.com/try-twilio

After you've created your account and verified your phone number, you should
end up at a screen that looks like this.

.. image:: _static/testdrive.png

This is your first chance to test out what Twilio can do. Send yourself a text
message and receive a call. Congratulations, you've used Twilio for the first
time!

However, how would you do this from your own code? I'm glad you asked.


