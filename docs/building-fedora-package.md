# Build using mock
## Prepare build environment
### Step 1

Clone this repository with SPECs and patches to any directory:
```bash
git clone -b master https://github.com/xvitaly/ecasbot.git ecasbot
git checkout stable/1.x
```

### Step 2

Install mock, spectool and rpmbuild:
```bash
sudo dnf install rpm-build rpmdevtools
```

Add yourself to `mock` group (you must run this only for the first time after installing mock):
```bash
sudo usermod -a -G mock $(whoami)
```
You need to relogin to your system after doing this or run:
```bash
newgrp mock
```

### Step 3

Create RPM build base directories:
```bash
rpmdev-setuptree
```

## Download sources and patches

Download sources:
```bash
cd ecasbot
spectool -g -R config/ecasbot.spec
```

## Build package

### Step 1

Generate SRPM package for mock:
```bash
cd ecasbot
rpmbuild -bs config/ecasbot.spec
```

### Step 2

Start mock build sequence:
```bash
mock -r fedora-$(rpm -E %fedora)-$(uname -m) --rebuild ~/rpmbuild/SRPMS/ecasbot*.src.rpm
```

### Step 3

Wait for a while and then install result without debug subpackages:
```bash
sudo dnf install /var/lib/mock/*/result/*.rpm --exclude="*debug*"
```

## Cleanup

Remove temporary files:
```bash
mock -r fedora-$(rpm -E %fedora)-$(uname -m) --clean
```
