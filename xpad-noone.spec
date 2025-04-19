%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

%global commit 2f26ea44da28474d6f1680bbbb97afc37736a8fe

Name:     xpad-noone
Version:  1
Release:  4%{?dist}
Summary:  xpad drivers without support for Xbox Controllers
License:  GPLv2
URL:      https://github.com/Jan200101/xpad-noone
Source0:  %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kmodtool
BuildRequires:  systemd-rpm-macros

Requires:       bash

Provides:       %{name}-kmod-common = %{version}-%{release}
Requires:       %{name}-kmod >= %{version}

Conflicts:      xow <= 0.5
Obsoletes:      xow <= 0.5

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
xpad drivers without support for Xbox Controllers
Intended to be used with xone

%package kmod
Summary:  Kernel module (kmod) for %{name}
Requires: kernel-devel

%description kmod
kmod package for %{name}

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -c %{name}-%{commit}

for kernel_version  in %{?kernel_versions} ; do
  cp -a %{name}-%{commit} _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done

%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 _kmod_build_${kernel_version%%___*}/%{name}.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/%{name}.ko
done
%{?akmod_install}

%files
%doc %{name}-%{commit}/README.md 
%license %{name}-%{commit}/LICENSE

%changelog
* Sat Apr 19 2025 Jan200101 <sentrycraft123@gmail.com> - 1-4
- pull updates from upstream

* Tue Jul 23 2024 Jan200101 <sentrycraft123@gmail.com> - 1-3
- Initial build

