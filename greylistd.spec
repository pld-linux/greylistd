Summary:	Simple greylisting system for mail transport agents
Summary(pl.UTF-8):	Prosty system szarych list dla serwerów pocztowych
Name:		greylistd
Version:	0.8.3.4
Release:	1
License:	GPL v2
Group:		Daemons
Source0:	http://ftp.debian.org/debian/pool/main/g/greylistd/%{name}_%{version}.tar.gz
# Source0-md5:	20295c2722b56c84f2ea8846ca4a47ac
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://packages.debian.org/unstable/mail/greylistd
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	python
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This daemon provides a simple greylisting implementation for use with
Exim and other mail transport agents (MTAs).

%description -l pl.UTF-8
Ten demon udostępnia prostą implementację szarych list do
wykorzystania z Eximem i innymi serwerami pocztowymi (MTA).

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_sysconfdir}/{sysconfig,rc.d/init.d,%{name}},/var/run/%{name},/var/lib/%{name},%{_mandir}/man{1,8}}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install program/greylist $RPM_BUILD_ROOT%{_bindir}
install program/greylistd $RPM_BUILD_ROOT%{_sbindir}
install config/config $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/config
install doc/man1/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
install doc/man8/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service %{name} restart
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = 0 ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc doc/examples/*
%dir %attr(755,mail,mail) /var/run/%{name}
%dir %attr(755,mail,mail) /var/lib/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/config
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man?/*
