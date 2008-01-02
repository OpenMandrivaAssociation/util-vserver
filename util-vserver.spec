%define confdir		%_sysconfdir/vservers
%define confdefaultdir	%confdir/.defaults
%define pkglibdir	%_libdir/%name
%define __chattr	/usr/bin/chattr

%define with_docu	0
%define name		util-vserver
%define version		0.30.213
%define release		%mkrel 1

Summary:	Linux virtual server utilities
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:	 	System/Base	
URL:		http://savannah.nongnu.org/projects/util-vserver/
Source0:	http://savannah.nongnu.org/download/util-vserver/stable.pkg/%version/%name-%version.tar.bz2
Patch0:		util-vserver-0.30.212-mandriva.patch
Patch1:		vserver-urpmi-mandriva.patch
BuildRoot:	%_tmppath/%name-%version-%release-root
Requires:	init(util-vserver)
Requires:	%name-core = %version
Requires:	%name-lib  = %version
Requires:	%name-sysv  = %version
Requires:	diffutils mktemp sed
Provides:	vserver = %version
Obsoletes:	vserver < %version
BuildRequires:	mount vlan-utils gawk iproute2 iptables
BuildRequires:	gcc-c++ wget
BuildRequires:	e2fsprogs-devel libbeecrypt-devel
BuildRequires:	doxygen tetex-latex
BuildRequires:	libxslt-proc
BuildRequires:	rsync
BuildRequires:	dump
Requires(post):		%__chattr
Requires(pre):		%pkglibdir
Requires(postun):	%pkglibdir
%{!?_without_dietlibc:BuildRequires:	dietlibc >= 0:0.25}

%package lib
Summary:		Dynamic libraries for util-vserver
Group:			System/Libraries

%package core
Summary:		The core-utilities for util-vserver
Group:			System/Base
Requires:		util-linux

%package build
Summary:		Tools which can be used to build vservers
Group:			System/Base
Requires:		rpm apt wget binutils tar e2fsprogs
Requires:		%name = %version
Requires(pre):		%confdir
Requires(postun):	%confdir
Requires(post):		%name-core

%package sysv
Summary:		SysV-initscripts for vserver
Group:			System/Configuration/Other
Provides:		init(util-vserver)
Requires:		make diffutils
Requires:		initscripts
Requires:		%name = %version
Requires(post):		rpm-helper
Requires(preun):        rpm-helper
Requires(pre):		%_initrddir %pkglibdir
requires(postun):	%_initrddir %pkglibdir

%package legacy
Summary:		Legacy utilities for util-vserver
Group:			System/Base
Requires:		%name = %version
Requires(post):		rpm-helper
Requires(preun):	rpm-helper
Requires(pre):		%_initrddir %pkglibdir
requires(postun):	%_initrddir %pkglibdir

%package devel
Summary:		Header-files and libraries needed to develop vserver based applications
Group:			Development/C
Requires:		pkgconfig


%description
util-vserver provides the components and a framework to setup virtual
servers.  A virtual server runs inside a linux server. It is nevertheless
highly independent. As such, you can run various services with normal
configuration. The various vservers can't interact with each other and
can't interact with services in the main server.

This requires a special kernel supporting the new new_s_context and
set_ipv4root system call.

%description lib
util-vserver provides the components and a framework to setup virtual
servers.  A virtual server runs inside a linux server. It is nevertheless
highly independent. As such, you can run various services with normal
configuration. The various vservers can't interact with each other and
can't interact with services in the main server.

This package contains the shared libraries needed by all other
'util-vserver' subpackages.

%description core
util-vserver provides the components and a framework to setup virtual
servers.  A virtual server runs inside a linux server. It is nevertheless
highly independent. As such, you can run various services with normal
configuration. The various vservers can't interact with each other and
can't interact with services in the main server.

This package contains utilities which are required to communicate with
the Linux-Vserver enabled kernel.


%description build
util-vserver provides the components and a framework to setup virtual
servers.  A virtual server runs inside a linux server. It is nevertheless
highly independent. As such, you can run various services with normal
configuration. The various vservers can't interact with each other and
can't interact with services in the main server.

This package contains utilities which assist in building Vservers.

%description sysv
util-vserver provides the components and a framework to setup virtual
servers.  A virtual server runs inside a linux server. It is nevertheless
highly independent. As such, you can run various services with normal
configuration. The various vservers can't interact with each other and
can't interact with services in the main server.

This package contains the SysV initscripts which start and stop
VServers and related tools.


%description legacy
util-vserver provides the components and a framework to setup virtual
servers.  A virtual server runs inside a linux server. It is nevertheless
highly independent. As such, you can run various services with normal
configuration. The various vservers can't interact with each other and
can't interact with services in the main server.

This package contains the tools which are needed to work with VServers
having an old-style configuration.


%description devel
util-vserver provides the components and a framework to setup virtual
servers.  A virtual server runs inside a linux server. It is nevertheless
highly independent. As such, you can run various services with normal
configuration. The various vservers can't interact with each other and
can't interact with services in the main server.

This package contains header files and libraries which are needed to
develop VServer related applications.


%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .mdv


%build
rm -rf $RPM_BUILD_ROOT
%configure --with-initrddir=%_initrddir --enable-release \
          --localstatedir=%_var \
           %{?_without_dietlibc:--disable-dietlibc}

%__make %{?_smp_mflags} all
%__make %{?_smp_mflags} doc


%install
rm -rf $RPM_BUILD_ROOT
%__make DESTDIR="$RPM_BUILD_ROOT" install install-distribution

rm -f $RPM_BUILD_ROOT/%_libdir/*.la

contrib/make-manifest %name $RPM_BUILD_ROOT contrib/manifest.dat


%check || :
%__make check


%clean
rm -rf $RPM_BUILD_ROOT


%post
test -d /vservers      || mkdir -m0000 /vservers
test -d /vservers/.pkg || mkdir -m0755 /vservers/.pkg

f="%confdefaultdir/vdirbase";  test -L "$f" -o -e "$f" || ln -s /vservers                        "$f"
f="%confdefaultdir/run.rev";   test -L "$f" -o -e "$f" || ln -s %_var/run/vservers.rev "$f"
f="%confdefaultdir/cachebase"; test -L "$f" -o -e "$f" || ln -s %_var/cache/vservers   "$f"

%_sbindir/setattr --barrier /vservers /vservers/.pkg || :


%preun
test "$1" != 0 || rm -rf %_var/cache/vservers/* 2>/dev/null || :


%post   lib -p /sbin/ldconfig
%postun lib -p /sbin/ldconfig


%post sysv
%_post_service vservers-default
%_post_service vprocunhide



%preun sysv
%_preun_service vprocunhide
%_preun_service vservers-default


%postun sysv
test "$1" = 0  || service vprocunhide condrestart >/dev/null || :


%triggerin build -- fedora-release, centos-release
function copy()
{
    base=$1
    shift

    for i; do
	test -r "$i" || continue

	target=%confdir/.distributions/.common/pubkeys/$base-$(basename "$i")
	cp -a "$i" "$target"
    done
}
copy fedora /usr/share/doc/fedora-release-*/RPM-GPG-*
copy fedora /etc/pki/rpm-gpg/RPM-GPG-*
copy centos /usr/share/doc/centos-*/RPM-GPG-KEY-*


%post build
test -d /vservers/.hash || mkdir -m0700 /vservers/.hash

f="%confdefaultdir/apps/vunify/hash"; test -e "$f"/method -o -e "$f"/00 || \
	ln -s /vservers/.hash "$f"/00

%_sbindir/setattr --barrier /vservers/.hash || :


%preun build
test "$1" != 0 || rm -f %confdir/.distributions/.common/pubkeys/fedora-*


## Temporary workaround to remove old v_* files; it will conflict
## somehow with the -legacy package but can be fixed by reinstalling
## this package.
## TODO: remove me in the final .spec file
%define v_services	httpd named portmap sendmail smb sshd xinetd gated
%triggerun sysv -- util-vserver-sysv < 0.30.198
for i in %v_services; do
	%_preun_service v_$i || :
done


%post legacy
%_post_service rebootmgr
%_post_service vservers-legacy

for i in %v_services; do
	%_post_service v_$i
done


%preun legacy
for i in %v_services; do
	%_preun_service v_$i
done

%_preun_service rebootmgr
%_preun_service vservers-legacy

%postun legacy
test "$1" = 0  || service rebootmgr condrestart >/dev/null || :


%files -f %name-base.list
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS
%doc doc/*.html doc/*.css
/sbin/vshelper
%dir %confdir
%dir %confdefaultdir
%dir %confdefaultdir/apps
%dir %confdefaultdir/files
%dir %pkglibdir/defaults
%ghost %confdefaultdir/cachebase
%ghost %confdefaultdir/vdirbase
%ghost %confdefaultdir/run.rev

%dir %_var/cache/vservers
%dir %_var/run/vservers
%dir %_var/run/vservers.rev
%dir %_var/run/vshelper


%files lib -f %name-lib.list
%files sysv -f %name-sysv.list


%files core -f %name-core.list
%defattr(-,root,root,-)
%dir %pkglibdir


%files build -f %name-build.list
%defattr(-,root,root,-)
%doc contrib/yum*.patch
%dir %confdir/.distributions
%dir %confdir/.distributions/*
%dir %confdir/.distributions/*/apt
%dir %confdir/.distributions/.common
%dir %confdir/.distributions/.common/pubkeys
%dir %confdefaultdir/apps/vunify
%dir %confdefaultdir/apps/vunify/hash


%files legacy -f %name-legacy.list
%defattr(-,root,root,-)
%dir %pkglibdir/legacy
%config(noreplace) /etc/vservers.conf


%files devel -f %name-devel.list
%defattr(-,root,root,-)
%doc lib/apidoc/latex/refman.pdf
%doc lib/apidoc/html
