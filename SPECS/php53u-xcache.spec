%global php_extdir %(php-config --extension-dir 2>/dev/null || echo "undefined")
%global php_version %((echo 0; php-config --version 2>/dev/null) | tail -1)

%define real_name php-xcache
%define name php53u-xcache

Summary:       PHP accelerator, optimizer, encoder and dynamic content cacher
Name:          %{name}
Version:       3.0.1
Release:       1.ius%{?dist}
License:       BSD
Group:         Development/Languages
Vendor:        IUS Community Project
URL:           http://xcache.lighttpd.net/
Source0:       http://xcache.lighttpd.net/pub/Releases/%{version}/xcache-%{version}.tar.gz
Source1:       xcache.ini
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Conflicts:     php53u-eaccelerator php53u-pecl-apc
BuildRequires: php53u-devel >= 5.1.0

# to force use of autoconf and not autoconf26x
%if 0%{?rhel} >= 6
BuildRequires: autoconf
%else
BuildRequires: autoconf < 2.63
%endif

Provides:      php-eaccelerator = %{version}-%{release}
Requires:      php53u(zend-abi) = %{php_zend_api}
Requires:      php53u(api) = %{php_core_api}

%description
XCache is a fast, stable PHP opcode cacher that has been tested and is now
running on production servers under high load.

%prep
%setup -q -n xcache-%{version}
%{__rm} -f coverager/common-zh-simplified-gb2312.lang.php

%build
phpize
%configure --enable-xcache \
           --enable-xcache-constant \
           --enable-xcache-optimizer \
           --enable-xcache-coverager \
           --with-php-config=%{_bindir}/php-config
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install INSTALL_ROOT=$RPM_BUILD_ROOT

%{__install} -D -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/xcache.ini
sed -i -e 's|/EXT_DIR|%{php_extdir}|g' $RPM_BUILD_ROOT%{_sysconfdir}/php.d/xcache.ini

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%doc xcache.ini AUTHORS ChangeLog NEWS README THANKS COPYING
%doc htdocs
%config(noreplace) %{_sysconfdir}/php.d/xcache.ini
%{php_extdir}/xcache.so

%changelog
* Fri Jan 11 2013 Ben Harper <ben.harper@rackspace.com> - 3.0.1.-1.ius
- Latest sources from upstream

* Mon Nov 05 2012 Ben Harper <ben.harper@rackspace.com> -  3.0.0-1.ius
- Latest sources from upstream
- update xcache.ini to load module via extension as zend_extension is nsupported

* Thu Jul 19 2012 Dustin Offutt <dustin.offutt@rackspace.com> - 2.0.1-1.ius
- Latest sources from upstream

* Tue Apr 24 2012 Jeffrey Ness <jeffrey.ness@rackspace.com> - 2.0.0-1.ius
- Latest sources from upstream

* Fri Aug 19 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 1.3.2-2.ius
- Rebuilding

* Mon Jun 06 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 1.3.2-1.ius
- Latest sources from upstream

* Mon Jan 10 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 1.3.0-4.ius
- Porting from bugzilla #563510 to IUS
- Adding Provides tag

* Tue Feb 16 2010 Timon <timosha@gmail.com> - 1.3.0-4
- review notes

* Thu Feb 11 2010 Timon <timosha@gmail.com> - 1.3.0-3
- remove xcache.ini from spec
- remove RHEL lines
- add some configure features
- add doc files
- review fixes

* Wed Feb 10 2010 Timon <timosha@gmail.com> 1.3.0-1
- Updated source to 1.3.0
- First release for Fedora12


