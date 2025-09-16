%global debug_package %{nil}

Name:     xone
Version:  0.4.5
Release:  1%{?dist}
Epoch:    1
Summary:  Linux kernel driver for Xbox One and Xbox Series X|S accessories 
License:  GPLv2
#URL:      https://github.com/medusalix/xone
URL:      https://github.com/dlundqvist/xone
Source0:  %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:  modules-load-d-%{name}.conf

BuildRequires:  systemd-rpm-macros

Provides:       %{name}-kmod-common = %{epoch}:%{version}-%{release}
Requires:       %{name}-kmod >= %{epoch}:%{version}

Conflicts:      xow <= 0.5
Obsoletes:      xow <= 0.5

%description
xone is a Linux kernel driver for Xbox One and Xbox Series X|S accessories.
It serves as a modern replacement for xpad, aiming to be compatible with
Microsoft's Game Input Protocol (GIP).

%package kmod
Summary:  Kernel module (kmod) for %{name}
Requires: kernel-devel

%description kmod
kmod package for %{name}

%prep
%autosetup

%build
# Nothing to build

%install
install -D -m 0644 install/modprobe.conf %{buildroot}%{_modprobedir}/60-%{name}.conf
install -D -m 0644 %{SOURCE1} %{buildroot}%{_modulesloaddir}/%{name}.conf

%files
%license LICENSE
%{_modprobedir}/60-%{name}.conf
%{_modulesloaddir}/%{name}.conf

%changelog
* Tue Sep 16 2025 Jan200101 <sentrycraft123@gmail.com> - 1:0.4.5-1
- Update to 0.4.5

* Thu May 22 2025 Jan200101 <sentrycraft123@gmail.com> - 1:0.3.1-1
- rebuilt

* Sat Apr 19 2025 Jan200101 <sentrycraft123@gmail.com> - 1:0.3.0-9
- switch package to a maintained fork

* Sat Nov 30 2024 Jan200101 <sentrycraft123@gmail.com> - 1:0.3.0-8
- correct modules config

* Wed Nov 27 2024 Jan200101 <sentrycraft123@gmail.com> - 1:0.3.0-7
- split kernel module into separate package

* Fri Oct 18 2024 Jan200101 <sentrycraft123@gmail.com> - 1:0.3.0-6
- Normalize version to allow updates

* Fri Oct 18 2024 Jan200101 <sentrycraft123@gmail.com> - 0.3.0_29ec357-5
- Add kernel 6.12 patch

* Sun Jan 28 2024 Jan Drögehoff <sentrycraft123@gmail.com> - 0.3-4
- Force bump release

* Tue Jun 06 2023 Jan Drögehoff <sentrycraft123@gmail.com> - 0.3-3
- Fix Linux 6.3 compilation, add some patches

* Sun Nov 13 2022 Jan Drögehoff <sentrycraft123@gmail.com> - 0.3-2
- correct modules

* Thu Jun 23 2022 Jan Drögehoff <sentrycraft123@gmail.com> - 0.3-1
- Update to 0.3

* Sat Mar 19 2022 Jan Drögehoff <sentrycraft123@gmail.com> - 0.2-2
- Obsolete xow and require firmware

* Sun Feb 27 2022 Jan Drögehoff <sentrycraft123@gmail.com> - 0.2-1
- Update to 0.2

* Fri Jul 02 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.1-1
- Initial spec

