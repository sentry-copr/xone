%if 0%{?fedora}
%global buildforkernels akmod
%endif
%global debug_package %{nil}

%global commit 29ec3577e52a50f876440c81267f609575c5161e
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global prjname xone

Name:           %{prjname}-kmod
Summary:        Kernel module (kmod) for %{prjname}
Version:        0.3.0
Release:        7%{?dist}
Epoch:          1
License:        GPLv2+

URL:            https://github.com/medusalix/xone
#Source0:       %%{url}/archive/v%%{version}/%%{name}-%%{version}.tar.gz
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Patch:   https://patch-diff.githubusercontent.com/raw/medusalix/xone/pull/53.patch#/%{name}-%{version}-kernel-6.12.patch

BuildRequires:  gcc
BuildRequires:  elfutils-libelf-devel
BuildRequires:  kmodtool

Requires:       lpf-xone-firmware

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{prjname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
xone is a Linux kernel driver for Xbox One and Xbox Series X|S accessories.
It serves as a modern replacement for xpad, aiming to be compatible with
Microsoft's Game Input Protocol (GIP).

This package contains the kmod module for %{prjname}.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --kmodname %{prjname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c
(cd xone-%{commit}
%patch -P 0 -p1
)

for kernel_version  in %{?kernel_versions} ; do
  cp -a xone-%{commit} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done

%install
for kernel_version in %{?kernel_versions}; do
    mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -D -m 755 _kmod_build_${kernel_version%%___*}/*.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/*.ko
done
%{?akmod_install}


%changelog
* Wed Nov 27 2024 Jan200101 <sentrycraft123@gmail.com> - 1:0.3.0-7
- split kernel module into separate package

