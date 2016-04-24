# gqrx-powermate

Control GQRX with a Griffin Powermate. 

Built with the powermate python framework - https://github.com/bethebunny/powermate

##powermate
A small python framework for scripting interactions with the Griffin Powermate.
- Python 2 and 3
- Any number of powermates
- Can have more than one script interact with the same powermate

##setup
In order to read and write to the Powermate event files on linux, you will need
to do the following (ymmv, but this should work on most modern distros).

```shellsession
$ sudo groupadd input
$ sudo usermod -a -G input "$USER"
$ echo 'KERNEL=="event*", NAME="input/%k", MODE="660", GROUP="input"' | sudo tee -a /etc/udev/rules.d/99-input.rules
```

After a reboot your scripts should be able to read/write to the device.

