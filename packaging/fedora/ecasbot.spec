# SPDX-FileCopyrightText: 2017-2022 EasyCoding Team
#
# SPDX-License-Identifier: GPL-3.0-or-later

%global pypi_name ecasbot

%global _description %{expand:
EC AntiSpam bot for the Telegram messenger will automatically detect
and block multimedia messages, links from the newly joined users,
some common spam bots and users who added them to super-groups.}

Name: %{pypi_name}
Version: 1.7.1
Release: 1%{?dist}

License: GPLv3+
Summary: EC AntiSpam bot for the Telegram messenger
URL: https://github.com/xvitaly/%{pypi_name}
Source0: %{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz
Source1: %{pypi_name}.sysusers
BuildArch: noarch

BuildRequires: doxygen
BuildRequires: pandoc
BuildRequires: python3-devel
BuildRequires: systemd
BuildRequires: systemd-rpm-macros

%{?systemd_requires}

%description %_description

%package doc
Summary: Documentation for the %{name}
Requires: %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description doc
This package provides auto-generated by Doxygen documentation for
the %{name} package.

%prep
%autosetup -p1
sed -e 's@"logtofile": "",@"logtofile": "%{_localstatedir}/log/%{pypi_name}/%{pypi_name}.log",@g' -i packaging/assets/%{pypi_name}.json

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel
doxygen
pandoc packaging/assets/manpage.md -s -t man > packaging/assets/%{pypi_name}.1

%install
%pyproject_install
%pyproject_save_files %{pypi_name}
install -D -d -m 0755 %{buildroot}%{_localstatedir}/log/%{pypi_name}/
install -D -p -m 0644 packaging/assets/%{pypi_name}.json %{buildroot}%{_sysconfdir}/%{pypi_name}/%{pypi_name}.json
install -D -p -m 0644 packaging/assets/%{pypi_name}-env.conf %{buildroot}%{_sysconfdir}/%{pypi_name}/%{pypi_name}-env.conf
install -D -p -m 0644 packaging/assets/%{pypi_name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{pypi_name}
install -D -p -m 0644 packaging/assets/%{pypi_name}.service %{buildroot}%{_unitdir}/%{pypi_name}.service
install -D -p -m 0644 packaging/assets/%{pypi_name}.1 %{buildroot}%{_mandir}/man1/%{pypi_name}.1
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{pypi_name}.conf

%pre
%sysusers_create_compat %{SOURCE1}

%post
%systemd_post %{pypi_name}.service

%preun
%systemd_preun %{pypi_name}.service

%postun
%systemd_postun_with_restart %{pypi_name}.service

%files -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/%{pypi_name}
%dir %{_sysconfdir}/%{pypi_name}
%attr(-,%{pypi_name},root) %config(noreplace) %{_sysconfdir}/%{pypi_name}/*.json
%config(noreplace) %{_sysconfdir}/%{pypi_name}/*.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{pypi_name}
%attr(-,%{pypi_name},root) %dir %{_localstatedir}/log/%{pypi_name}
%ghost %{_localstatedir}/log/%{pypi_name}/*.log*
%{_unitdir}/%{pypi_name}.service
%{_sysusersdir}/%{pypi_name}.conf
%{_mandir}/man1/%{pypi_name}.1*

%files doc
%doc docs/html/*

%changelog
* Tue Nov 22 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 1.7.1-1
- Updated to version 1.7.1.
