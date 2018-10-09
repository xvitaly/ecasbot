%global appname ecasbot

Name: python-%{appname}
Version: 0
Release: 1%{?dist}
Summary: EC AntiSpam bot

License: GPLv3+
URL: https://github.com/xvitaly/%{appname}
Source0: %{url}/archive/v%{version}.tar.gz#/%{appname}-%{version}.tar.gz
BuildArch: noarch

BuildRequires: systemd
BuildRequires: python3-devel
BuildRequires: python3dist(pytelegrambotapi)
BuildRequires: python3dist(requests)
BuildRequires: python3dist(wheel)
BuildRequires: python3dist(six)
BuildRequires: python3dist(emoji)

%description
EC AntiSpam bot for Telegram messenger will block all multimedia
messages and links from new users, block chinese bots and users
who added them in supergroups.

%package -n python3-%{appname}
Summary: EC AntiSpam bot
Requires: python3dist(pytelegrambotapi)
Requires: python3dist(requests)
Requires: python3dist(six)
Requires: python3dist(emoji)
Requires(pre): shadow-utils
%{?systemd_requires}
%{?python_provide:%python_provide python3-%{appname}}

%description -n python3-%{appname}
EC AntiSpam bot for Telegram messenger will block all multimedia
messages and links from new users, block chinese bots and users
who added them in supergroups.

%prep
%autosetup -n %{appname}-%{version} -p1

%build
%py3_build

%install
%py3_install

mkdir -p %{buildroot}%{_sysconfdir}/%{appname}
install -p -m 0644 config/%{appname}.json %{buildroot}%{_sysconfdir}/%{appname}
install -p -m 0644 config/%{appname}-env.conf %{buildroot}%{_sysconfdir}/%{appname}

mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 config/%{appname}.service %{buildroot}%{_unitdir}

mkdir -p %{buildroot}%{_localstatedir}/log
install -d -m 0755 %{buildroot}%{_localstatedir}/log/%{name}

%check
%{__python3} setup.py test

%pre -n python3-%{appname}
getent group %{appname} >/dev/null || groupadd -r %{appname}
getent passwd %{appname} >/dev/null || \
useradd -r -g %{appname} -d /dev/null -s /sbin/nologin \
  -c "%{appname} service account" %{appname}
exit 0

%post -n python3-%{appname}
%systemd_post %{appname}.service

%preun -n python3-%{appname}
%systemd_preun %{appname}.service

%postun -n python3-%{appname}
%systemd_postun_with_restart %{appname}.service

%files -n python3-%{appname}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{appname}
%{python3_sitelib}/%{appname}-*.egg-info
%attr(-,%{appname},%{appname}) %config(noreplace) %{_sysconfdir}/%{appname}/*.json
%config(noreplace) %{_sysconfdir}/%{appname}/*.conf
%dir %attr(-,%{appname},%{appname}) %{_localstatedir}/log/%{name}
%ghost %{_localstatedir}/log/%{name}/*.log
%{_unitdir}/%{appname}.service

%changelog
* Tue Sep 11 2018 Vitaly Zaitsev <vitaly@easycoding.org> - 0-1
- Initial SPEC release.
